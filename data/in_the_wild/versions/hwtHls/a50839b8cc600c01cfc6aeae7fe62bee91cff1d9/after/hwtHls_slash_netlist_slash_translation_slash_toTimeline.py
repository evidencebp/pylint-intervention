from pathlib import Path
from typing import Dict, List, Optional, Union

from plotly import graph_objs as go
from plotly.graph_objs import Figure
import plotly.offline

from hwt.hdl.types.bitsVal import BitsVal
from hwt.pyUtils.uniqList import UniqList
from hwt.synthesizer.interface import Interface
from hwt.synthesizer.interfaceLevel.unitImplHelpers import getSignalName
from hwtHls.netlist.nodes.const import HlsNetNodeConst
from hwtHls.netlist.nodes.io import HlsNetNodeWrite, HlsNetNodeRead, HlsNetNodeExplicitSync, \
    HOrderingVoidT
from hwtHls.netlist.nodes.node import HlsNetNode
from hwtHls.netlist.nodes.ops import HlsNetNodeOperator
from hwtHls.netlist.transformation.hlsNetlistPass import HlsNetlistPass
from hwtHls.netlist.nodes.backwardEdge import HlsNetNodeWriteBackwardEdge
from hwtHls.netlist.nodes.aggregatedBitwiseOps import HlsNetNodeBitwiseOps


class TimelineRow():
    """
    A container of data for row in timeline graph.
    """

    def __init__(self, label:str, group: int, start:float, finish:float, color:str):
        self.label = label
        self.group = group
        self.start = start
        self.finish = finish
        self.deps: UniqList[TimelineRow, float] = UniqList()
        self.backward_deps: UniqList[TimelineRow, float] = UniqList()
        self.color = color


class HwtHlsNetlistToTimeline():
    """
    Generate a timeline (Gantt) diagram of how operations in circuit are scheduled in time.
    
    :ivar time_scale: Specified how to format time numbers in output.
    """

    def __init__(self, normalizedClkPeriod: int, resolution: float, expandCompositeNodes=True):
        self.obj_to_row: Dict[HlsNetNode, dict] = {}
        self.rows: List[dict] = []
        self.time_scale = resolution / 1e-9  # to ns
        self.clkPeriod = self.time_scale * normalizedClkPeriod
        self.min_duration = 0.05 * normalizedClkPeriod * self.time_scale  # minimum width of boexes representing operations
        self.expandCompositeNodes = expandCompositeNodes

    def translateNodeToRow(self, obj: HlsNetNode, row_i: int, io_group_ids: Dict[Interface, int]):
        obj_group_id = row_i
        if obj.scheduledIn:
            start = min(obj.scheduledIn)
        else:
            start = max(obj.scheduledOut)

        if obj.scheduledOut:
            finish = max(obj.scheduledOut)
        else:
            finish = start

        start *= self.time_scale
        finish *= self.time_scale

        assert start <= finish, (start, finish, obj)
        duration = finish - start
        if duration < self.min_duration:
            to_add = self.min_duration - duration
            start -= to_add / 2
            finish += to_add / 2

        color = "purple"
        if isinstance(obj, HlsNetNodeOperator):
            label = f"{obj.operator.id:s} {obj._id:d}"

        elif isinstance(obj, HlsNetNodeWrite):
            label = f"{getSignalName(obj.dst)}.write()  {obj._id:d}"
            if isinstance(obj, HlsNetNodeWriteBackwardEdge):
                obj_group_id = io_group_ids.setdefault(obj.associated_read.src, obj_group_id)
            color = "green"

        elif isinstance(obj, HlsNetNodeRead):
            label = f"{getSignalName(obj.src)}.read()  {obj._id:d}"
            obj_group_id = io_group_ids.setdefault(obj.src, obj_group_id)
            color = "green"

        elif isinstance(obj, HlsNetNodeConst):
            val = obj.val
            if isinstance(val, BitsVal):
                if val._is_full_valid():
                    label = "0x%x" % int(val)
                else:
                    label = repr(val)
            else:
                label = repr(val)
            color = "plum"

        elif isinstance(obj, HlsNetNodeExplicitSync):
            label = f"{obj.__class__.__name__:s}  {obj._id:d}"

        else:
            label = repr(obj)

        row = TimelineRow(label, obj_group_id, start, finish, color)
        self.rows.append(row)
        self.obj_to_row[obj] = (row, row_i)

    def construct(self, nodes: List[HlsNetNode]):
        rows = self.rows
        obj_to_row = self.obj_to_row
        io_group_ids: Dict[Interface, int] = {}
        offset = 0
        nodesFlat = []
        compositeNodes = set()
        for row_i, obj in enumerate(nodes):
            if self.expandCompositeNodes and isinstance(obj, HlsNetNodeBitwiseOps):
                compositeNodes.add(obj)
                for subNode in obj._subNodes.nodes:
                    self.translateNodeToRow(subNode, offset + row_i, io_group_ids)
                    nodesFlat.append(subNode)
                    offset += 1
            else:
                self.translateNodeToRow(obj, offset + row_i, io_group_ids)
                nodesFlat.append(obj)
        
        for row_i, (row, obj) in enumerate(zip(rows, nodesFlat)):
            obj: HlsNetNode
            for t, dep in zip(obj.scheduledIn, obj.dependsOn):
                if dep.obj in compositeNodes:
                    dep = dep.obj._subNodes.outputs[dep.out_i]
                depObj = dep.obj
                depOutI = dep.out_i
                print()
                row.deps.append((
                    obj_to_row[depObj][1], # src
                    depObj.scheduledOut[depOutI] * self.time_scale, # start
                    t * self.time_scale, # finish
                    dep._dtype) # type
                )
            for bdep_obj in obj.debug_iter_shadow_connection_dst():
                bdep = obj_to_row[bdep_obj][0]
                bdep.backward_deps.append(row_i)

    def _draw_clock_boundaries(self, fig: Figure):
        clkPeriod = self.clkPeriod
        last_time = max(r.finish for r in self.rows) + clkPeriod
        i = 0.0
        row_cnt = len(self.rows)
        while i < last_time:
            fig.add_shape(
                x0=i, y0=0,
                x1=i, y1=row_cnt,
                line=dict(color="gray", dash='dash', width=2)
            )
            i += clkPeriod

    def _draw_arrow(self, x0:float, y0:float, x1:float, y1:float, color: str, shapesToAdd: List[dict], annotationsToAdd: List[dict]):
        # assert x1 >= x0
        jobs_delta = x1 - x0
        if jobs_delta > 0 and y0 == y1:
            p = f"M {x0} {y0} L {x1} {y1}"
        else:
            if jobs_delta > 0:
                middleX = x0 + jobs_delta / 2
                p = f"M {x0} {y0} C {middleX} {y0}, {middleX} {y1}, {x1} {y1}"
            else:
                # x0 is on right, x1 on left
                p = f"M {x0} {y0} C {x0 + 4*self.min_duration} {y0}, {x1-4*self.min_duration} {y1}, {x1} {y1}"
        # fig.add_shape(
        shapesToAdd.append(dict(
            type="path",
            path=p,
            line_color=color,
        ))

        # # draw an arrow
        # fig.add_annotation(
        annotationsToAdd.append(dict(
            x=x1, y=y1,
            xref="x", yref="y",
            showarrow=True,
            ax=-10,
            ay=0,
            arrowwidth=2,
            arrowcolor=color,
            arrowhead=2,
        ))

    def _draw_arrow_between_jobs(self, shapesToAdd: List[dict], annotationsToAdd: List[dict]):
        # # draw an arrow from the end of the first job to the start of the second job
        # # retrieve tick text and tick vals
        # job_yaxis_mapping = dict(zip(fig.layout.yaxis.ticktext, fig.layout.yaxis.tickvals))
        for second_job in self.rows:
            second_job: TimelineRow
            endX = second_job.start
            endY = second_job.group

            for start_i, start_t, finish_t, dtype in second_job.deps:
                first_job = self.rows[start_i]
                startX = first_job.finish
                startX = start_t
                # assert start_t >= first_job.start and start_t <= first_job.finish, (start_t, first_job.start, first_job.finish)
                startY = first_job.group
                # assert finish_t >= second_job.start and finish_t <= second_job.finish, (finish_t, (second_job.start, second_job.finish))
                self._draw_arrow(startX, startY, finish_t, endY, "green" if dtype is HOrderingVoidT else "blue", shapesToAdd, annotationsToAdd)

            for start_i in second_job.backward_deps:
                first_job = self.rows[start_i]
                startX = first_job.finish
                startY = first_job.group
                self._draw_arrow(startX, startY, endX, endY, "gray", shapesToAdd, annotationsToAdd)

    def _generate_fig(self):
        # df = self.df
        # df['delta'] = df['finish'] - df['start']

        # https://plotly.com/python/bar-charts/
        rows_by_color = {}
        for row in self.rows:
            c = row.color
            _rows = rows_by_color.get(c, None)
            if _rows is None:
                _rows = rows_by_color[c] = []
            _rows.append(row)

        bars = []
        for color, rows in sorted(rows_by_color.items(), key=lambda x: x[0]):
            rows: List[TimelineRow]
            b = go.Bar(x=[r.finish - r.start for r in rows],
                       base=[r.start for r in rows],
                       y=[r.group for r in rows],
                       width=[1 for _ in rows],
                       marker_color=color,
                       orientation='h',
                       customdata=[r.label for r in rows],
                       showlegend=False,
                       texttemplate="%{customdata}",
                       textangle=0,
                       textposition="inside",
                       insidetextanchor="middle",
                       hovertemplate="<br>".join([
                           "(%{base}, %{x}):",
                           " %{customdata}",
                       ]))
            bars.append(b)
        fig = Figure(bars, go.Layout(barmode='overlay'))

        fig.update_yaxes(title="Operations", autorange="reversed", visible=True, showticklabels=False)  # otherwise tasks are listed from the bottom up
        fig.update_xaxes(title="Time[ns]")
        shapesToAdd: List[dict] = []
        annotationsToAdd: List[dict] = []
        self._draw_arrow_between_jobs(shapesToAdd, annotationsToAdd)
        if annotationsToAdd or shapesToAdd:
            fig.layout.update({
                "annotations": annotationsToAdd,
                "shapes": shapesToAdd,
            })
        self._draw_clock_boundaries(fig)
        return fig

    def show(self):
        fig = self._generate_fig()
        plotly.offline.iplot(fig, config={"scrollZoom":True})

    def save_html(self, filename: Union[str, Path], auto_open):
        fig = self._generate_fig()
        if isinstance(filename, Path):
            filename = filename.as_posix()

        plotly.offline.plot(fig, filename=filename, auto_open=auto_open, config={"scrollZoom":True})


class HlsNetlistPassShowTimeline(HlsNetlistPass):

    def __init__(self, filename:Optional[str]=None, auto_open=False, expandCompositeNodes=False):
        self.filename = filename
        self.auto_open = auto_open
        self.expandCompositeNodes = expandCompositeNodes

    def apply(self, hls: "HlsStreamProc", to_hw: "SsaSegmentToHwPipeline"):
        if not to_hw.is_scheduled:
            to_hw.schedulerRun()

        to_timeline = HwtHlsNetlistToTimeline(to_hw.hls.normalizedClkPeriod,
                                              to_hw.hls.scheduler.resolution,
                                              expandCompositeNodes=self.expandCompositeNodes)
        to_timeline.construct(to_hw.hls.inputs + to_hw.hls.nodes + to_hw.hls.outputs)
        if self.filename is not None:
            to_timeline.save_html(self.filename, self.auto_open)
        else:
            assert self.auto_open, "Must be True because we can not show figure without opening it"
            to_timeline.show()


if __name__ == "__main__":
    to_timeline = HwtHlsNetlistToTimeline()
    to_timeline.show()
