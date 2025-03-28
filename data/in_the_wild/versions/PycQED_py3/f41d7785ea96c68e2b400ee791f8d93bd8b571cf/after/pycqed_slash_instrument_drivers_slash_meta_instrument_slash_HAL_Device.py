"""
File:   HAL_Device.py (originally device_object_CCL.py)
Note:   see file "HAL.md"
Note:   a lot code was moved around within this file in December 2021. As a consequence, the author information provided
        by 'git blame' makes little sense. See GIT tag 'release_v0.3' for the original file.
"""

import numpy as np
import time
import logging
import adaptive
import networkx as nx
import datetime
import multiprocessing
from importlib import reload
from typing import List, Union, Optional
from deprecated import deprecated

from pycqed.instrument_drivers.meta_instrument.HAL.HAL_ShimMQ import HAL_ShimMQ

from pycqed.analysis import multiplexed_RO_analysis as mra
from pycqed.measurement import detector_functions as det
reload(det)

from pycqed.measurement import sweep_functions as swf
from pycqed.analysis import measurement_analysis as ma
from pycqed.analysis import tomography as tomo
from pycqed.analysis_v2 import measurement_analysis as ma2
import pycqed.analysis_v2.tomography_2q_v2 as tomo_v2

from pycqed.utilities import learner1D_minimizer as l1dm
from pycqed.utilities.general import check_keyboard_interrupt, print_exception

# Imported for type checks
#from pycqed.instrument_drivers.physical_instruments.QuTech_AWG_Module import QuTech_AWG_Module
from pycqed.measurement.measurement_control import MeasurementControl

from qcodes.instrument.parameter import ManualParameter, Parameter


log = logging.getLogger(__name__)

try:
    from pycqed.measurement.openql_experiments import single_qubit_oql as sqo
    import pycqed.measurement.openql_experiments.multi_qubit_oql as mqo
    from pycqed.measurement.openql_experiments import clifford_rb_oql as cl_oql
    from pycqed.measurement.openql_experiments import openql_helpers as oqh
    from pycqed.measurement import cz_cost_functions as czcf

    reload(sqo)
    reload(mqo)
    reload(cl_oql)
    reload(oqh)
    reload(czcf)
except ImportError:
    log.warning('Could not import OpenQL')
    mqo = None
    sqo = None
    cl_oql = None
    oqh = None
    czcf = None


class HAL_Device(HAL_ShimMQ):
    """
    Device object for systems controlled using the Distributed CC (CC).

    Former support for CCLight (CCL) and QuMa based CC (QCC) is deprecated.
    """

    def __init__(self, name, **kw):
        super().__init__(name, **kw)

        self.msmt_suffix = '_' + name

    ##########################################################################
    # public functions: measure
    ##########################################################################

    def measure_conditional_oscillation(
            self,
            q0: str,
            q1: str,
            q2: str = None,
            q3: str = None,
            flux_codeword="cz",
            flux_codeword_park=None,
            parked_qubit_seq=None,
            downsample_swp_points=1,  # x2 and x3 available
            prepare_for_timedomain=True,
            MC: Optional[MeasurementControl] = None,
            disable_cz: bool = False,
            disabled_cz_duration_ns: int = 60,
            cz_repetitions: int = 1,
            wait_time_before_flux_ns: int = 0,
            wait_time_after_flux_ns: int = 0,
            disable_parallel_single_q_gates: bool = False,
            label="",
            verbose=True,
            disable_metadata=False,
            extract_only=False,
    ):
        # USED_BY: inspire_dependency_graph.py,
        """
        Measures the "conventional cost function" for the CZ gate that
        is a conditional oscillation. In this experiment the conditional phase
        in the two-qubit Cphase gate is measured using Ramsey-lie sequence.
        Specifically qubit q0 is prepared in the superposition, while q1 is in 0 or 1 state.
        Next the flux pulse is applied. Finally pi/2 afterrotation around various axes
        is applied to q0, and q1 is flipped back (if neccessary) to 0 state.
        Plotting the probabilities of the zero state for each qubit as a function of
        the afterrotation axis angle, and comparing case of q1 in 0 or 1 state, enables to
        measure the conditional phase and estimale the leakage of the Cphase gate.

        Refs:
        Rol arXiv:1903.02492, Suppl. Sec. D

        Args:
            q0 (str):
                target qubit name (i.e. the qubit in the superposition state)

            q1 (str):
                control qubit name (i.e. the qubit remaining in 0 or 1 state)
            q2, q3 (str):
                names of optional extra qubit to either park or apply a CZ to.
            flux_codeword (str):
                the gate to be applied to the qubit pair q0, q1
            flux_codeword_park (str):
                optionally park qubits q2 (and q3) with either a 'park' pulse
                (single qubit operation on q2) or a 'cz' pulse on q2-q3.
                NB: depending on the CC configurations the parking can be
                implicit in the main `cz`
            prepare_for_timedomain (bool):
                should the insruments be reconfigured for time domain measurement
            disable_cz (bool):
                execute the experiment with no flux pulse applied
            disabled_cz_duration_ns (int):
                waiting time to emulate the flux pulse
            wait_time_after_flux_ns (int):
                additional waiting time (in ns) after the flux pulse, before
                the final afterrotations

        """
        if MC is None:
            MC = self.instr_MC.get_instr()
        assert q0 in self.qubits()
        assert q1 in self.qubits()
        q0idx = self.find_instrument(q0).cfg_qubit_nr()
        q1idx = self.find_instrument(q1).cfg_qubit_nr()
        list_qubits_used = [q0, q1]
        if q2 is None:
            q2idx = None
        else:
            q2idx = self.find_instrument(q2).cfg_qubit_nr()
            list_qubits_used.append(q2)
        if q3 is None:
            q3idx = None
        else:
            q3idx = self.find_instrument(q3).cfg_qubit_nr()
            list_qubits_used.append(q3)

        if prepare_for_timedomain:
            self.prepare_readout(qubits=list_qubits_used)
            self.prepare_fluxing(qubits=list_qubits_used)
            for q in list_qubits_used:  # only on the CZ qubits we add the ef pulses
                mw_lutman = self.find_instrument(q).instr_LutMan_MW.get_instr()
                lm = mw_lutman.LutMap()
                # FIXME: we hardcode the X on the ef transition to CW 31 here.
                lm[31] = {"name": "rX12", "theta": 180, "phi": 0, "type": "ef"}
                # load_phase_pulses will also upload other waveforms
                mw_lutman.load_phase_pulses_to_AWG_lookuptable()
                mw_lutman.load_waveforms_onto_AWG_lookuptable(
                    regenerate_waveforms=True)

        # These are hardcoded angles in the mw_lutman for the AWG8
        # only x2 and x3 downsample_swp_points available
        angles = np.arange(0, 341, 20 * downsample_swp_points)

        if parked_qubit_seq is None:
            parked_qubit_seq = "ramsey" if q2 is not None else "ground"

        p = mqo.conditional_oscillation_seq(
            q0idx,
            q1idx,
            q2idx,
            q3idx,
            platf_cfg=self.cfg_openql_platform_fn(),
            disable_cz=disable_cz,
            disabled_cz_duration=disabled_cz_duration_ns,
            angles=angles,
            wait_time_before_flux=wait_time_before_flux_ns,
            wait_time_after_flux=wait_time_after_flux_ns,
            flux_codeword=flux_codeword,
            flux_codeword_park=flux_codeword_park,
            cz_repetitions=cz_repetitions,
            parked_qubit_seq=parked_qubit_seq,
            disable_parallel_single_q_gates=disable_parallel_single_q_gates
        )

        s = swf.OpenQL_Sweep(
            openql_program=p,
            CCL=self.instr_CC.get_instr(),
            parameter_name="Phase",
            unit="deg",
        )
        MC.set_sweep_function(s)
        MC.set_sweep_points(p.sweep_points)
        # FIXME: unused now get_int_avg_det no longer has parameter 'qubits'
        # measured_qubits = [q0, q1]
        # if q2 is not None:
        #     measured_qubits.append(q2)
        # if q3 is not None:
        #     measured_qubits.append(q3)
        MC.set_detector_function(self.get_int_avg_det())
        MC.run(
            "conditional_oscillation_{}_{}_&_{}_{}_x{}_wb{}_wa{}{}{}".format(
                q0, q1, q2, q3, cz_repetitions,
                wait_time_before_flux_ns, wait_time_after_flux_ns,
                self.msmt_suffix, label,
            ),
            disable_snapshot_metadata=disable_metadata,
        )

        # [2020-06-24] parallel cz not supported (yet)
        # should be implemented by just running the analysis twice with
        # corresponding channels

        options_dict = {
            'ch_idx_osc': 0,
            'ch_idx_spec': 1
        }

        if q2 is not None:
            options_dict['ch_idx_park'] = 2

        a = ma2.Conditional_Oscillation_Analysis(
            options_dict=options_dict,
            extract_only=extract_only)

        return a


    def measure_conditional_oscillation_multi(
            self,
            pairs: list,
            parked_qbs: list,
            flux_codeword="cz",
            phase_offsets: list = None,
            parked_qubit_seq=None,
            downsample_swp_points=1,  # x2 and x3 available
            prepare_for_timedomain=True,
            MC: Optional[MeasurementControl] = None,
            disable_cz: bool = False,
            disabled_cz_duration_ns: int = 60,
            cz_repetitions: int = 1,
            wait_time_before_flux_ns: int = 0,
            wait_time_after_flux_ns: int = 0,
            disable_parallel_single_q_gates: bool = False,
            label="",
            verbose=True,
            disable_metadata=False,
            extract_only=False,
    ):
        """
        Measures the "conventional cost function" for the CZ gate that
        is a conditional oscillation. In this experiment the conditional phase
        in the two-qubit Cphase gate is measured using Ramsey-lie sequence.
        Specifically qubit q0 of each pair is prepared in the superposition, while q1 is in 0 or 1 state.
        Next the flux pulse is applied. Finally pi/2 afterrotation around various axes
        is applied to q0, and q1 is flipped back (if neccessary) to 0 state.
        Plotting the probabilities of the zero state for each qubit as a function of
        the afterrotation axis angle, and comparing case of q1 in 0 or 1 state, enables to
        measure the conditional phase and estimale the leakage of the Cphase gate.

        Refs:
        Rol arXiv:1903.02492, Suppl. Sec. D
        IARPA M6 for the flux-dance, not publicly available

        Args:
            pairs (lst(lst)):
                Contains all pairs with the order (q0,q1) where q0 in 'str' is the target and q1 in
                'str' is the control. This is based on qubits that are parked in the flux-dance.

            parked_qbs(lst):
                Contains a list of all qubits that are required to be parked.
                This is based on qubits that are parked in the flux-dance.

            flux_codeword (str):
                the gate to be applied to the qubit pair [q0, q1]

            flux_codeword_park (str):
                optionally park qubits. This is designed according to the flux-dance. if
                one has to measure a single pair, has to provide more qubits for parking.
                Problem here is parked qubits are hardcoded in cc config, thus one has to include the extra
                parked qubits in this file.
                (single qubit operation on q2) or a 'cz' pulse on q2-q3.
                NB: depending on the CC configurations the parking can be
                implicit in the main `cz`

            prepare_for_timedomain (bool):
                should the insruments be reconfigured for time domain measurement

            disable_cz (bool):
                execute the experiment with no flux pulse applied

            disabled_cz_duration_ns (int):
                waiting time to emulate the flux pulse

            wait_time_before_flux_ns (int):
                additional waiting time (in ns) before the flux pulse.

            wait_time_after_flux_ns (int):
                additional waiting time (in ns) after the flux pulse, before
                the final afterrotations

        """

        if self.ro_acq_weight_type() != 'optimal':
            # this occurs because the detector groups qubits per feedline.
            # If you do not pay attention, this will mess up the analysis of
            # this experiment.
            raise ValueError('Current conditional analysis is not working with {}'.format(self.ro_acq_weight_type()))

        if MC is None:
            MC = self.instr_MC.get_instr()

        Q_idxs_target = []
        Q_idxs_control = []
        Q_idxs_parked = []
        list_qubits_used = []
        ramsey_qubits = []

        for i, pair in enumerate(pairs):
            print('Pair (target,control) {} : ({},{})'.format(i + 1, pair[0], pair[1]))
            assert pair[0] in self.qubits()
            assert pair[1] in self.qubits()
            Q_idxs_target += [self.find_instrument(pair[0]).cfg_qubit_nr()]
            Q_idxs_control += [self.find_instrument(pair[1]).cfg_qubit_nr()]
            list_qubits_used += [pair[0], pair[1]]
            ramsey_qubits += [pair[0]]

        if parked_qbs is not None:
            Q_idxs_parked = [self.find_instrument(Q).cfg_qubit_nr() for Q in parked_qbs]

        if prepare_for_timedomain:
            self.prepare_readout(qubits=list_qubits_used)
            self.prepare_fluxing(qubits=list_qubits_used)

            for i, q in enumerate(np.concatenate([ramsey_qubits])):
                # only on the CZ qubits we add the ef pulses
                mw_lutman = self.find_instrument(q).instr_LutMan_MW.get_instr()

                lm = mw_lutman.LutMap()
                # FIXME: we hardcode the X on the ef transition to CW 31 here.
                lm[31] = {"name": "rX12", "theta": 180, "phi": 0, "type": "ef"}
                # load_phase_pulses will also upload other waveforms
                if phase_offsets == None:
                    mw_lutman.load_phase_pulses_to_AWG_lookuptable()
                else:
                    mw_lutman.load_phase_pulses_to_AWG_lookuptable(
                        phases=np.arange(0, 360, 20) + phase_offsets[i])
                mw_lutman.load_waveforms_onto_AWG_lookuptable(
                    regenerate_waveforms=True)

        # FIXME: These are hardcoded angles in the mw_lutman for the AWG8
        # only x2 and x3 downsample_swp_points available
        angles = np.arange(0, 341, 20 * downsample_swp_points)

        p = mqo.conditional_oscillation_seq_multi(
            Q_idxs_target,
            Q_idxs_control,
            Q_idxs_parked,
            platf_cfg=self.cfg_openql_platform_fn(),
            disable_cz=disable_cz,
            disabled_cz_duration=disabled_cz_duration_ns,
            angles=angles,
            wait_time_before_flux=wait_time_before_flux_ns,
            wait_time_after_flux=wait_time_after_flux_ns,
            flux_codeword=flux_codeword,
            cz_repetitions=cz_repetitions,
            parked_qubit_seq=parked_qubit_seq,
            disable_parallel_single_q_gates=disable_parallel_single_q_gates
        )

        s = swf.OpenQL_Sweep(
            openql_program=p,
            CCL=self.instr_CC.get_instr(),
            parameter_name="Phase",
            unit="deg",
        )
        MC.set_sweep_function(s)
        MC.set_sweep_points(p.sweep_points)
        d = self.get_int_avg_det()
        MC.set_detector_function(d)
        MC.run(
            "conditional_oscillation_{}_x{}_{}{}".format(
                list_qubits_used, cz_repetitions,
                self.msmt_suffix, label,
            ),
            disable_snapshot_metadata=disable_metadata,
        )

        if len(pairs) > 1:
            qb_ro_order = [qb for qb_dict in self._acq_ch_map.values() for qb in qb_dict.keys()]
        else:
            qb_ro_order = [pairs[0][0], pairs[0][1]]

        result_dict = {}
        for i, pair in enumerate(pairs):
            ch_osc = qb_ro_order.index(pair[0])
            ch_spec = qb_ro_order.index(pair[1])

            options_dict = {
                'ch_idx_osc': ch_osc,
                'ch_idx_spec': ch_spec
            }
            a = ma2.Conditional_Oscillation_Analysis(
                options_dict=options_dict,
                extract_only=extract_only)

            result_dict['pair_{}_delta_phi_a'.format(i + 1)] = \
                a.proc_data_dict['quantities_of_interest']['phi_cond'].n % 360

            result_dict['pair_{}_missing_frac_a'.format(i + 1)] = \
                a.proc_data_dict['quantities_of_interest']['missing_fraction'].n

            result_dict['pair_{}_offset_difference_a'.format(i + 1)] = \
                a.proc_data_dict['quantities_of_interest']['offs_diff'].n

            result_dict['pair_{}_phi_0_a'.format(i + 1)] = \
                (a.proc_data_dict['quantities_of_interest']['phi_0'].n + 180) % 360 - 180

            result_dict['pair_{}_phi_1_a'.format(i + 1)] = \
                (a.proc_data_dict['quantities_of_interest']['phi_1'].n + 180) % 360 - 180

        return result_dict


    def measure_parity_check_flux_dance(
            self,
            target_qubits: List[str],
            control_qubits: List[str],
            flux_dance_steps: List[int] = [1, 2, 3, 4],
            flux_codeword: str = 'flux-dance',
            refocusing: bool = False,
            ramsey_qubits: Union[List[str], bool] = None,
            parking_qubits: List[str] = None,
            nr_flux_dance_before_cal_points: int = None,
            phase_offsets: List[float] = None,
            control_cases_to_measure: List[str] = None,
            downsample_angle_points: int = 1,
            initialization_msmt: bool = False,
            wait_time_before_flux_ns: int = 0,
            wait_time_after_flux_ns: int = 0,
            analyze_parity_model: bool = False,
            plotting=True,
            prepare_for_timedomain=True,
            label_suffix="",
            disable_metadata=False,
            MC: Optional[MeasurementControl] = None,
    ):
        """
        Measures a parity check while playing codewords that are part
        of a flux dance (originally used for surface code).
        This experiment is similar to `measure_conditional_oscillation_multi()`,
        but plays composite flux codewords instead of only individual ones
        for the involved qubits.

        Specifically, a conditional oscillation is performed between the
        target qubit and each control qubit, where the target qubit is being ramsey'd
        and the control qubits are being prepared in every possible combination
        of 0 and 1 (for example, ['00','01','10','11']).
        These combinations can also be given explicitly in `control_cases_to_measure`,
        then only those control cases will be prepared. This option is still
        experimental and may not work as expected!

        Parkings have to be taken care of by the flux dance codewords,
        and lutmans of parking qubit have to be prepared externally before this measurement.

        The list of flux codewords to be played inbetween the two microwave
        pulses of the conditional oscillation is assembled from the
        `flux_codeword`, `flux_dance_steps` and `refocusing` arguments, and
        will contain as many codewords as there are steps given.

        By analyzing the phases of the oscillation for each prepared case,
        the quality of the parity check can be assessed.

        Args:
            target_qubits (List[str]):
                List of target qubit labels. These will be ramsey'd.

            control_qubits (List[str]):
                List of control qubit labels. These will be prepared in either 0 or 1.
                Has to be given in readout (feedline) order!
                Otherwise readout results will be scrambled.

            flux_dance_steps (List[int]):
                Numbers of flux dance codewords that should be played inbetween
                the MW pulses in the conditional oscillation. Has to match
                the definitons in the CC config file for the given `flux_codeword`.

            flux_codeword (str):
                The flux codeword to build flux dance list with. Will be combined
                with `flux_dance_steps` and `refocusing`.
                Codeword from this list will then be played inbetween the MW pulses
                in the conditional oscillation.
                Codewords have to be defined in CC config.

            refocusing (bool):
                If True, appends the 'refocus' flag to `flux_codeword`
                when assembling the flux codeword list, thereby turning on
                refocusing pulses on qubits that are not used during the flux dance steps.
                Corresponding refocusing codewords have to be defined in CC config.

            ramsey_qubits (Union[List[str], bool]):
                Apart from the target qubit, also additional qubits can be ramsey'd.
                This is done to mimic the real world scenario of the flux dance
                being executed as part of a QEC code.
                If given as list of labels, explicitly those qubits will be ramsey'd.
                If given as boolean, will turn on or off the automatic selection of
                all other ancillas of the same type as the target qubit.
                This is only implemented for surface-17 and may not match the desired behaviour.

            nr_flux_dance_before_cal_points (int):
                For investigation of the effect of fluxing on readout and for debugging purposes,
                The same flux dance as in the main experiment can be applied
                `nr_flux_dance_before_cal_points` times before the calibration points.

            phase_offsets: List[float] = None,
                Phase offsets to apply to all phase-gates of the conditional oscillation,
                given per target qubit.

            control_cases_to_measure (List[str]):
                Explicit list of control qubit preparation cases that should be measured.
                Experimental! May produce unexpected results.

            downsample_angle_points (int):
                Factor by which to reduce the number of points
                in the conditional oscillations.
                Restricted to 2 and 3, due to limitation in MW codewords.

            prepare_for_timedomain (bool):
                Whether the instruments should be prepared for time domain measurement.
                Includes preparation of readout, flux and MW pulses for the given qubits.
                This takes a significant amount of time and can be disabled if
                the instruments are already prepared, for example because the
                same measurement was executed right before.

            initialization_msmt (bool):
                Whether to initialize all qubits via measurement
                at the beginning of each experiment.

            wait_time_before_flux_ns (int):
                additional waiting time (in ns) before the flux dance.

            wait_time_after_flux_ns (int):
                additional waiting time (in ns) after the flux dance, before
                the final mw pulse

            label_suffix (str):
                String to be appended at the end of the measurement label.

            MC (`pycqed.measurement.MeasurementControl`):
                MeasurementControl object. Will be taken from instance parameter if None.

            disable_metadata (bool)
                Whether experiment metadata like intrument snapshots etc should
                be saved in the hdf5 file.

            plotting (bool):
                Whether the analysis should generate plots. Can save some time.

        Returns:
            Analysis result.
        """
        assert all([qb in self.qubits() for qb in control_qubits])
        assert all([qb in self.qubits() for qb in target_qubits])
        if MC is None:
            MC = self.instr_MC.get_instr()

        old_digitized = self.ro_acq_digitized()
        old_weight_type = self.ro_acq_weight_type()
        self.ro_acq_digitized(False)
        self.ro_acq_weight_type('optimal')

        # if `ramsey_qubits` and/or `flux_dance_steps` are given, they will be used literally.
        # otherwise, they will be set for the standard S17 experiment for the target qubit type
        # NOTE: this part is specific to surface-17!
        if 'X' in target_qubits[0]:
            if ramsey_qubits and type(ramsey_qubits) is bool:
                ramsey_qubits = [qb for qb in ['X1','X2','X3','X4'] if qb not in target_qubits]
            if not flux_dance_steps:
                flux_dance_steps = [1,2,3,4]
        elif 'Z' in target_qubits[0]:
            if ramsey_qubits and type(ramsey_qubits) is bool:
                ramsey_qubits = [qb for qb in ['Z1','Z2','Z3','Z4'] if qb not in target_qubits]
            if not flux_dance_steps:
                flux_dance_steps = [5,6,7,8]
        else:
            log.warning(f"Target qubit {target_qubits[0]} not X or Z!")

        # if ramsey_qubits is given as list of qubit names, 
        # only those will be used and converted to qubit numbers.
        # if ramsey_qubits is given as boolean,
        # all ancillas that are not part of the parity check will be ramseyd
        if ramsey_qubits:
            Q_idxs_ramsey = []
            for i,qb in enumerate(ramsey_qubits):
                assert qb in self.qubits()
                if qb in target_qubits:
                    log.warning(f"Ramsey qubit {qb} already given as ancilla qubit!")
                Q_idxs_ramsey += [self.find_instrument(qb).cfg_qubit_nr()]

        Q_idxs_target = [] 
        for i,target_qubit in enumerate(target_qubits):
            log.info(f"Parity {target_qubit} - {control_qubits}, flux dance steps {flux_dance_steps}")
            Q_idxs_target += [self.find_instrument(target_qubit).cfg_qubit_nr()]

        # filter control qubits based on control_cases_to_measure,
        # then the cases will be created based on the filtered control qubits
        Q_idxs_control = [] 
        if not control_cases_to_measure:
            # if cases are not given, measure all cases for all control qubits
            control_qubits_by_case = control_qubits   
            Q_idxs_control += [self.find_instrument(Q).cfg_qubit_nr() for Q in control_qubits_by_case]  
            cases = ['{:0{}b}'.format(i, len(Q_idxs_control)) for i in range(2**len(Q_idxs_control))]
        else:
            # if cases are given, prepare and measure only them
            # NOTE: this feature is not fully tested yet and may not work!
            # this part selects only the control qubits needed, avoid repetition
            control_qubits_by_case = []
            for case in control_cases_to_measure:
                control_qubits_by_case += [control_qubits[i] for i,c in enumerate(case) \
                                            if c == '1' and control_qubits[i] not in control_qubits_by_case]
                #control_qubits_by_case += [control_qubits[i] for i,c in enumerate(case) if c == '1']
              
            # sort selected control qubits according to readout (feedline) order
            # qb_ro_order = np.sum([ list(self._acq_ch_map[key].keys()) for key in self._acq_ch_map.keys()], dtype=object)
            # dqb_ro_order = np.array(qb_ro_order, dtype=str)[[qb[0] == 'D' for qb in qb_ro_order]]
            control_qubits_by_case = [x for x,_ in sorted(zip(control_qubits_by_case, control_qubits))]
            
            Q_idxs_control += [self.find_instrument(Q).cfg_qubit_nr() for Q in control_qubits_by_case]
            cases = control_cases_to_measure 

        # for separate preparation of parking qubits in 1, used to study parking
        if parking_qubits:
            Q_idxs_parking = []
            for i,qb in enumerate(parking_qubits):
                assert qb in self.qubits()
                if qb in target_qubits + control_qubits:
                    log.warning(f"Parking qubit {qb} already given as control or target qubit!")
                Q_idxs_parking += [self.find_instrument(qb).cfg_qubit_nr()]

        # prepare list of all used qubits
        all_qubits = target_qubits + control_qubits_by_case
        if parking_qubits:
            all_qubits += parking_qubits

        # MW preparation
        for qb in all_qubits:
            mw_lutman = self.find_instrument(qb).instr_LutMan_MW.get_instr()
            # check the lutman of the target, control and parking qubits for cw_27, 
            # which is needed for refocusing, case preparation, and preparation in 1 (respectively)
            # and prepare if necessary       
            xm180_dict = {"name": "rXm180", "theta": -180, "phi": 0, "type": "ge"}
            if mw_lutman.LutMap().get(27) != xm180_dict:
                log.warning(f"{mw_lutman.name} does not have refocusing pulse, overriding `cw_27` ...")
                mw_lutman.LutMap()[27] = xm180_dict
                mw_lutman.load_waveform_onto_AWG_lookuptable(27, regenerate_waveforms=True)

            # check if phase pulses already exist on target qubits to avoid unnecessary upload delay
            if qb in target_qubits:
                if not np.all([mw_lutman.LutMap()[i+9] == {"name": "rPhi90", "theta": 90, "phi": phase, "type": "ge"}
                                for i, phase in enumerate(np.arange(0,360,20)) ]) \
                        or phase_offsets:
                    # load_phase_pulses already uploads all other waveforms inside
                    mw_lutman.load_phase_pulses_to_AWG_lookuptable(
                        phases=np.arange(0,360,20)+phase_offsets[i] if phase_offsets else np.arange(0,360,20))

        if prepare_for_timedomain:
            # Take care of readout order (by feedline/UHF)
            if self.qubits_by_feedline():
                all_qubits = sorted(all_qubits, 
                                key=lambda x: [i for i, feedline in enumerate(self.qubits_by_feedline()) \
                                                if x in feedline])
                log.info(f"Sorted qubits for readout preparation: {all_qubits}")
            else:
                log.warning("Qubit order by feedline in `self.qubits_by_feedline()` parameter is not set, "
                            + "readout will be prepared in order of given qubits which can lead to errors!")
            
            self.prepare_for_timedomain(qubits=all_qubits)

        # These are hardcoded angles in the mw_lutman for the AWG8
        # only x2 and x3 downsample_swp_points available
        angles = np.arange(0, 341, 20*downsample_angle_points)

        # prepare flux codeword list according to given step numbers
        # will be programmed in order of the list, but scheduled in parallel (if possible)
        
        if refocusing:
            flux_cw_list = [flux_codeword + '_refocus' + f'_{step}' for step in flux_dance_steps]

        else:
            flux_cw_list = [flux_codeword + f'_{step}' for step in flux_dance_steps]
        p = mqo.parity_check_flux_dance(
            Q_idxs_target=Q_idxs_target,
            Q_idxs_control=Q_idxs_control,
            control_cases=cases,
            flux_cw_list=flux_cw_list,
            Q_idxs_ramsey=Q_idxs_ramsey if ramsey_qubits else None,
            Q_idxs_parking=Q_idxs_parking if parking_qubits else None,
            nr_flux_dance_before_cal_points=nr_flux_dance_before_cal_points,
            platf_cfg=self.cfg_openql_platform_fn(),
            angles=angles,
            initialization_msmt=initialization_msmt,
            wait_time_before_flux=wait_time_before_flux_ns,
            wait_time_after_flux=wait_time_after_flux_ns
            )

        s = swf.OpenQL_Sweep(
            openql_program=p,
            CCL=self.instr_CC.get_instr(),
            parameter_name="Cases",
            unit="a.u."
            )

        d = self.get_int_avg_det(qubits=target_qubits+control_qubits)

        MC.set_sweep_function(s)
        MC.set_sweep_points(p.sweep_points)
        MC.set_detector_function(d)

        label = f"Parity_check_flux_dance_{target_qubits}_{control_qubits_by_case}_{self.msmt_suffix}_{label_suffix}"
        MC.run(label, disable_snapshot_metadata=disable_metadata)
        self.ro_acq_digitized(old_digitized)
        self.ro_acq_weight_type(old_weight_type)

        a = ma2.Parity_Check_Analysis_OLD(
            label=label,
            ancilla_qubits=target_qubits,
            data_qubits=control_qubits_by_case,
            parking_qubits=parking_qubits,
            cases=cases,
            plotting=plotting
        )

        return a.result
        # a = ma2.Parity_Check_Analysis(
        #     label=label, 
        #     target_qubit=target_qubits[0],
        #     extract_only=not plotting,
        #     analyze_parity_model=analyze_parity_model
        #     )

        # result = a.proc_data_dict

        # if analyze_parity_model:
        #     model_errors = a.proc_data_dict['quantities_of_interest']['parity_model']['model_errors']
        #     model_terms = a.proc_data_dict['quantities_of_interest']['parity_model']['model_terms']
        #     # this return structure is necessary to use this as a detector function 
        #     # for higher level calibration routines
        #     result = {**result,
        #                 'model_errors': model_errors,
        #                 'model_terms': model_terms,
        #                 # must extract the nominal value here because MC/HDF5 cannot deal with ufloats in the data array
        #                 **{f'model_error_{term}': x.n for term, x in zip(model_terms, model_errors)}
        #                 }

        # return result


    def measure_parity_check_fidelity(
            self,
            target_qubits: List[str],
            control_qubits: List[str], # have to be given in readout (feedline) order
            flux_dance_steps: List[int] = [1,2,3,4],
            flux_codeword: str = 'flux_dance',
            ramsey_qubits: List[str] = None,
            refocusing: bool = False,
            phase_offsets: List[float] = None,
            cases_to_measure: List[str] = None,
            result_logging_mode: str = 'raw',
            prepare_for_timedomain: bool = True,
            initialization_msmt: bool = True,
            nr_shots_per_case: int = 2**14,
            shots_per_meas: int = 2**16,
            wait_time_before_flux_ns: int = 0,
            wait_time_after_flux_ns: int = 0,
            label_suffix: str = "",
            disable_metadata: bool = False,
            MC: Optional[MeasurementControl] = None,
    ):
        """
        Measures a parity check fidelity. In this experiment the conditional phase
        in the two-qubit Cphase gate is measured using Ramsey-lie sequence.
        Specifically qubit q0 of each pair is prepared in the superposition, while q1 is in 0 or 1 state.
        Next the flux pulse is applied. Finally pi/2 afterrotation around various axes
        is applied to q0, and q1 is flipped back (if neccessary) to 0 state.
        Plotting the probabilities of the zero state for each qubit as a function of
        the afterrotation axis angle, and comparing case of q1 in 0 or 1 state, enables to
        measure the conditional phase and estimale the leakage of the Cphase gate.

        Args:
            pairs (lst(lst)):
                Contains all pairs with the order (q0,q1) where q0 in 'str' is the target and q1 in
                'str' is the control. This is based on qubits that are parked in the flux-dance.

            prepare_for_timedomain (bool):
                should the insruments be reconfigured for time domain measurement

            disable_cz (bool):
                execute the experiment with no flux pulse applied

            disabled_cz_duration_ns (int):
                waiting time to emulate the flux pulse

            wait_time_before_flux_ns (int):
                additional waiting time (in ns) before the flux pulse.

            wait_time_after_flux_ns (int):
                additional waiting time (in ns) after the flux pulse, before
                the final afterrotations

        """

        assert all([qb in self.qubits() for qb in control_qubits])
        assert all([qb in self.qubits() for qb in target_qubits])
        if self.ro_acq_weight_type() != 'optimal':
            # this occurs because the detector groups qubits per feedline.
            # If you do not pay attention, this will mess up the analysis of
            # this experiment.
            raise ValueError('Current analysis is not working with {}'.format(self.ro_acq_weight_type()))
        if MC is None:
            MC = self.instr_MC.get_instr()

        cases = ['{:0{}b}'.format(i, len(control_qubits)) for i in range(2**len(control_qubits))]
        # prepare list of all used qubits
        all_qubits = target_qubits + control_qubits

        # MW preparation
        Q_idxs_control = []   
        for qb in control_qubits:
            Q_idxs_control += [self.find_instrument(qb).cfg_qubit_nr()]  
            mw_lutman = self.find_instrument(qb).instr_LutMan_MW.get_instr()
            # check the lutman of the target, control and parking qubits for cw_27, 
            # which is needed for refocusing, case preparation, and preparation in 1 (respectively)
            # and prepare if necessary       
            xm180_dict = {"name": "rXm180", "theta": -180, "phi": 0, "type": "ge"}
            if mw_lutman.LutMap().get(27) != xm180_dict:
                log.warning(f"{mw_lutman.name} does not have refocusing pulse, overriding `cw_27` ...")
                mw_lutman.LutMap()[27] = xm180_dict
                mw_lutman.load_waveform_onto_AWG_lookuptable(27, regenerate_waveforms=True)

        Q_idxs_target = [] 
        for i,ancilla in enumerate(target_qubits):
            log.info(f"Parity check fidelity {ancilla} - {control_qubits}")
            Q_idxs_target += [self.find_instrument(ancilla).cfg_qubit_nr()]
            mw_lutman = self.find_instrument(ancilla).instr_LutMan_MW.get_instr()
            # check if phase pulses already exist on target qubits to avoid unnecessary upload delay
            if not np.all([mw_lutman.LutMap()[i+9] == {"name": "rPhi90", "theta": 90, "phi": phase, "type": "ge"}
                            for i, phase in enumerate(np.arange(0,360,20)) ]) \
                    or phase_offsets:
                # load_phase_pulses already uploads all other waveforms inside
                mw_lutman.load_phase_pulses_to_AWG_lookuptable(
                    phases=np.arange(0,360,20)+phase_offsets[i] if phase_offsets else np.arange(0,360,20))

        if ramsey_qubits:
            Q_idxs_ramsey = []
            for i,qb in enumerate(ramsey_qubits):
                assert qb in self.qubits()
                if qb in target_qubits:
                    log.warning(f"Ramsey qubit {qb} already given as ancilla qubit!")
                Q_idxs_ramsey += [self.find_instrument(qb).cfg_qubit_nr()]

        if initialization_msmt:
            nr_shots = 2 * nr_shots_per_case * len(cases)
            label_suffix = '_'.join([label_suffix, "init-msmt"])
        else:
            nr_shots = nr_shots_per_case * len(cases)

        self.ro_acq_digitized(False)
        if prepare_for_timedomain:
            # Take care of readout order (by feedline/UHF)
            if self.qubits_by_feedline():
                all_qubits = sorted(all_qubits, 
                                key=lambda x: [i for i, feedline in enumerate(self.qubits_by_feedline()) \
                                                if x in feedline])
                log.info(f"Sorted qubits for readout preparation: {all_qubits}")
            else:
                log.warning("Qubit order by feedline in `self.qubits_by_feedline()` parameter is not set, "
                            + "readout will be prepared in order of given qubits which can lead to errors!")

            self.prepare_for_timedomain(qubits=target_qubits+control_qubits)

        # prepare flux codeword list according to given step numbers
        # will be programmed in order of the list, but scheduled in parallel (if possible)
        # flux_cw_list = [flux_codeword + f'_{step}' for step in flux_dance_steps]
        if refocusing:
            flux_cw_list = [flux_codeword + '_refocus' + f'_{step}' for step in flux_dance_steps]

        else:
            flux_cw_list = [flux_codeword + f'_{step}' for step in flux_dance_steps]

        p = mqo.parity_check_fidelity(
            Q_idxs_target=Q_idxs_target,
            Q_idxs_control=Q_idxs_control,
            control_cases=cases,
            flux_cw_list=flux_cw_list,
            Q_idxs_ramsey=Q_idxs_ramsey if ramsey_qubits else None,
            refocusing=refocusing,
            platf_cfg=self.cfg_openql_platform_fn(),
            initialization_msmt=initialization_msmt,
            wait_time_before_flux=wait_time_before_flux_ns,
            wait_time_after_flux=wait_time_after_flux_ns
            )

        s = swf.OpenQL_Sweep(openql_program=p, CCL=self.instr_CC.get_instr())

        d = self.get_int_logging_detector(
            qubits=target_qubits+control_qubits, 
            result_logging_mode=result_logging_mode
            )
        shots_per_meas = int(np.floor(np.min([shots_per_meas, nr_shots]) / len(cases)) 
                            * len(cases) )
        d.set_child_attr("nr_shots", shots_per_meas)

        MC.set_sweep_function(s)
        MC.set_sweep_points(np.arange(nr_shots))
        MC.set_detector_function(d)

        # disable live plotting and soft averages
        old_soft_avg = MC.soft_avg()
        old_live_plot_enabled = MC.live_plot_enabled()
        MC.soft_avg(1)
        MC.live_plot_enabled(False)

        label = f"Parity_check_fidelity_{target_qubits}_{control_qubits}_{self.msmt_suffix}_{label_suffix}"
        MC.run(label, disable_snapshot_metadata=disable_metadata)

        MC.soft_avg(old_soft_avg)
        MC.live_plot_enabled(old_live_plot_enabled)

        # a = ma2.Parity_Check_Fidelity_Analysis(label=label)
        # return a.result

    def measure_sandia_parity_benchmark(self,
                                        ancilla_qubit: str,
                                        data_qubits: list,
                                        prepare_for_timedomain:bool=True):
        ###################
        # setup qubit idxs
        ###################
        all_qubits = [ancilla_qubit]+data_qubits
        ancilla_idx = self.find_instrument(ancilla_qubit).cfg_qubit_nr()
        data_idxs = [ self.find_instrument(q).cfg_qubit_nr() for q in data_qubits ]
        ###########################################
        # RO preparation (assign res_combinations)
        ###########################################
        RO_lms = np.unique([self.find_instrument(q).instr_LutMan_RO() for q in all_qubits])
        qubit_RO_lm = { self.find_instrument(q).cfg_qubit_nr() : 
                      (self.find_instrument(q).name, 
                       self.find_instrument(q).instr_LutMan_RO()) for q in all_qubits }
        main_qubits = []
        exception_qubits = []
        res_combs = {}
        for lm in RO_lms:
            res_combs[lm] = []
            comb = []
            for idx in data_idxs+[ancilla_idx]:
                  if qubit_RO_lm[idx][1] == lm:
                        comb += [idx]
            res_combs[lm] += [comb]
            if qubit_RO_lm[ancilla_idx][1] == lm:
                  res_combs[lm] += [[ancilla_idx]]
                  main_qubits = [qubit_RO_lm[idx][0] for idx in comb]
            else:
                  exception_qubits += [qubit_RO_lm[idx][0] for idx in comb]
        # Time-domain preparation
        ordered_qubits = main_qubits+exception_qubits
        if prepare_for_timedomain:
            assert self.ro_acq_weight_type() == 'optimal'
            self.prepare_for_timedomain(ordered_qubits)
            for lm in RO_lms:
                ro_lm = self.find_instrument(lm)
                ro_lm.resonator_combinations(res_combs[lm])
                ro_lm.load_DIO_triggered_sequence_onto_UHFQC()
        ########################
        # SETUP MC and detector
        ########################
        uhfqc_max_avg = 2**17
        d = self.get_int_logging_detector(qubits=ordered_qubits, result_logging_mode='raw')
        for detector in d.detectors:
            detector.nr_shots = int(uhfqc_max_avg/5)*5
        p = mqo.Parity_Sandia_benchmark(qA=ancilla_idx,
                                        QDs=data_idxs,
                                        platf_cfg=self.cfg_openql_platform_fn())
        s = swf.OpenQL_Sweep(openql_program=p,
                             CCL=self.instr_CC.get_instr())
        MC = self.instr_MC.get_instr()
        MC.soft_avg(1)
        MC.live_plot_enabled(False)
        MC.set_sweep_function(s)
        MC.set_sweep_points(np.arange(int(uhfqc_max_avg/5)*5))
        MC.set_detector_function(d)
        MC.run(f"Sandia_parity_benchmark_{ancilla_qubit}_{data_qubits[0]}_{data_qubits[1]}_{data_qubits[2]}_{data_qubits[3]}")

        ma2.pba.Sandia_parity_benchmark(label='Sandia',
                                        ancilla_qubit=ancilla_qubit, 
                                        data_qubits=data_qubits,
                                        exception_qubits=exception_qubits)


    def measure_weight4_parity_tomography(
            self,
            ancilla_qubit: str,
            data_qubits: list,
            sim_measurement: bool,
            prepare_for_timedomain: bool=True,
            repetitions: int=10,
            label: str=''
            ):
        assert self.ro_acq_digitized() == False
        ###################
        # setup qubit idxs
        ###################
        all_qubits = [ancilla_qubit]+data_qubits
        ancilla_idx = self.find_instrument(ancilla_qubit).cfg_qubit_nr()
        data_idxs = [ self.find_instrument(q).cfg_qubit_nr() for q in data_qubits ]
        ###########################################
        # RO preparation (assign res_combinations)
        ###########################################
        RO_lms = np.unique([self.find_instrument(q).instr_LutMan_RO() for q in all_qubits])
        qubit_RO_lm = { self.find_instrument(q).cfg_qubit_nr() : 
                      (self.find_instrument(q).name, 
                       self.find_instrument(q).instr_LutMan_RO()) for q in all_qubits }
        main_qubits = []
        exception_qubits = []
        res_combs = {}
        for lm in RO_lms:
            res_combs[lm] = []
            comb1= []
            comb2= []
            # ancilla + data qubits resonators
            for idx in [ancilla_idx]+data_idxs:
                  if qubit_RO_lm[idx][1] == lm:
                        comb1+= [idx]
                        comb2+= [idx]
            res_combs[lm] += [comb1]
            if qubit_RO_lm[ancilla_idx][1] == lm:
                  res_combs[lm] += [[ancilla_idx]]
                  comb2.remove(ancilla_idx)
                  res_combs[lm] += [comb2]
                  main_qubits = [qubit_RO_lm[idx][0] for idx in comb1]
            else:
                  exception_qubits += [qubit_RO_lm[idx][0] for idx in comb1]
        # Time-domain preparation
        ordered_qubits = main_qubits+exception_qubits
        if prepare_for_timedomain:
            assert self.ro_acq_weight_type() == 'optimal'
            self.prepare_for_timedomain(ordered_qubits)
            for lm in RO_lms:
                ro_lm = self.find_instrument(lm)
                ro_lm.resonator_combinations(res_combs[lm])
                ro_lm.load_DIO_triggered_sequence_onto_UHFQC()
        
        p = mqo.Weight_4_parity_tomography(
            Q_anc=ancilla_idx,
            Q_D1=data_idxs[0],
            Q_D2=data_idxs[1],
            Q_D3=data_idxs[2],
            Q_D4=data_idxs[3],
            simultaneous_measurement=sim_measurement,
            platf_cfg=self.cfg_openql_platform_fn())

        uhfqc_max_avg = 2**17
        if sim_measurement:
            readouts_per_round = 81+2**5
        else:
            readouts_per_round = 81*2+2**5
        d = self.get_int_logging_detector(qubits=all_qubits, result_logging_mode='raw')
        d.detectors[0].nr_shots = int(uhfqc_max_avg/readouts_per_round) * readouts_per_round
        d.detectors[1].nr_shots = int(uhfqc_max_avg/readouts_per_round) * readouts_per_round
        s = swf.OpenQL_Sweep(openql_program=p,
                     CCL=self.instr_CC.get_instr())
        MC = self.instr_MC.get_instr()
        MC.soft_avg(1)
        MC.live_plot_enabled(False)
        MC.set_sweep_function(s)
        MC.set_sweep_points(np.arange(int(uhfqc_max_avg/readouts_per_round) 
                                        * readouts_per_round * repetitions))
        MC.set_detector_function(d)
        MC.run(f'Weight_4_parity_tomography_{ancilla_qubit}_{data_qubits}_sim-msmt-{sim_measurement}_{label}')
        # Warning analysis requires that the detector function is ordered
        # as: [anc_qubit, data_qubit[0],[1],[2],[3]]
        ma2.pba.Weight_4_parity_tomography(sim_measurement=sim_measurement)


    def measure_phase_corrections(
            self,
            pairs: List[List[str]],
            flux_codeword: str = "cz",
            measure_switched_target: bool = True,
            update: bool = True,
            prepare_for_timedomain = True,
            label: str = "_ph-corr",
            ):
        """
        FIXME: not fully tested yet
        """
        assert all(pair in self.qubit_edges() or pair[::-1] in self.qubit_edges()
                     for pair in pairs)

        a = self.measure_conditional_oscillation_multi(
            pairs=pairs,
            flux_codeword=flux_codeword,
            prepare_for_timedomain=prepare_for_timedomain,
            label=label
            )
        phase_updates = dict.fromkeys([pair[0] for pair in pairs])
        for i,pair in enumerate(pairs):
            phase_updates[pair[0]] = a[f"pair_{i}_phi_0_a"]
        
        if measure_switched_target:
            a = self.measure_conditional_oscillation(
                pairs=[pair[::-1] for pair in pairs],
                flux_codeword=flux_codeword,
                prepare_for_timedomain=prepare_for_timedomain,
                label=label
                )
            for i,pair in enumerate(pairs):
                phase_updates[pair[1]] = a[f"pair_{i}_phi_0_a"]

        if update:
            # find gate direction to update corresponding lutman parameter
            if measure_switched_target:
                all_pairs = pairs + [pair[::-1] for pair in pairs]
            else:
                all_pairs = pairs

            for i,pair in enumerate(all_pairs):
                if self.qubit_edges().get('-'.join(pair), False):
                    gate = self.qubit_edges()['-'.join(pair)]
                elif self.qubit_edges().get('-'.join(pair[::-1]), False):
                    gate = self.qubit_edges()['-'.join(pair[::-1])]
                else:
                    raise ValueError(f"Gate direction for pair {pair} not found in list of qubit edges!")

                mw_lutman = self.find_instrument(pair[0]).instr_LutMan_MW.get_instr()
                mw_lutman.parameters[f"vcz_virtual_q_ph_corr_{gate}"](phase_updates[pair[0]])

        return phase_updates


    def measure_two_qubit_tomo_bell(
            self,
            qubits: list,
            bell_state=0,
            wait_after_flux=None,
            analyze=True,
            close_fig=True,
            prepare_for_timedomain=True,
            MC: Optional[MeasurementControl] = None,
            label="",
            shots_logging: bool = False,
            shots_per_meas=2 ** 16,
            flux_codeword="cz"
    ):
        """
        Prepares and performs a tomography of the one of the bell states, indicated
        by its index.

        Args:
            bell_state (int):
                index of prepared bell state
                0 -> |Phi_m>=|00>-|11>
                1 -> |Phi_p>=|00>+|11>
                2 -> |Psi_m>=|01>-|10>
                3 -> |Psi_p>=|01>+|10>

            qubits (list):
                list of names of the target qubits

            wait_after_flux (float):
                wait time (in seconds) after the flux pulse and
                after-rotation before tomographic rotations
            shots_logging (bool):
                if False uses correlation mode to acquire shots for tomography.
                if True uses single shot mode to acquire shots.
        """
        q0 = qubits[0]
        q1 = qubits[1]

        if prepare_for_timedomain:
            self.prepare_for_timedomain(qubits=[q0, q1])
        if MC is None:
            MC = self.instr_MC.get_instr()

        assert q0 in self.qubits()
        assert q1 in self.qubits()

        q0idx = self.find_instrument(q0).cfg_qubit_nr()
        q1idx = self.find_instrument(q1).cfg_qubit_nr()

        p = mqo.two_qubit_tomo_bell(
            bell_state,
            q0idx,
            q1idx,
            wait_after_flux=wait_after_flux,
            platf_cfg=self.cfg_openql_platform_fn(),
            flux_codeword=flux_codeword
        )

        s = swf.OpenQL_Sweep(openql_program=p, CCL=self.instr_CC.get_instr())
        MC.set_sweep_function(s)
        # 36 tomo rotations + 7*4 calibration points
        cases = np.arange(36 + 7 * 4)
        if not shots_logging:
            d = self.get_correlation_detector([q0, q1])
            MC.set_sweep_points(cases)
            MC.set_detector_function(d)
            MC.run("TwoQubitBellTomo_{}_{}{}".format(q0, q1, self.msmt_suffix) + label)
            if analyze:
                a = tomo.Tomo_Multiplexed(
                    label="Tomo",
                    MLE=True,
                    target_bell=bell_state,
                    single_shots=False,
                    q0_label=q0,
                    q1_label=q1,

                )
                return a

        else:
            nr_cases = len(cases)
            d = self.get_int_logging_detector(qubits)
            nr_shots = self.ro_acq_averages() * nr_cases
            shots_per_meas = int(
                np.floor(np.min([shots_per_meas, nr_shots]) / nr_cases) * nr_cases
            )
            d.set_child_attr("nr_shots", shots_per_meas)

            MC.set_sweep_points(np.tile(cases, self.ro_acq_averages()))
            MC.set_detector_function(d)
            MC.run(
                "TwoQubitBellTomo_{}_{}{}".format(q0, q1, self.msmt_suffix) + label,
                bins=cases,
            )


    def measure_two_qubit_allxy(
            self,
            q0: str,
            q1: str,
            sequence_type="sequential",
            replace_q1_pulses_with: str = None,
            repetitions: int = 2,
            analyze: bool = True,
            close_fig: bool = True,
            detector: str = "correl",
            prepare_for_timedomain: bool = True,
            MC=None
    ):
        """
        Perform AllXY measurement simultaneously of two qubits (c.f. measure_allxy
        method of the Qubit class). Order in which the mw pulses are executed
        can be varied.

        For detailed description of the (single qubit) AllXY measurement
        and symptomes of different errors see PhD thesis
        by Matthed Reed (2013, Schoelkopf lab), pp. 124.
        https://rsl.yale.edu/sites/default/files/files/RSL_Theses/reed.pdf

        Args:
            q0 (str):
                first quibit to perform allxy measurement on

            q1 (str):
                second quibit to perform allxy measurement on

            replace_q1_pulses_with (str):
                replaces all gates for q1 with the specified gate
                main use case: replace with "i" or "rx180" for crosstalks
                assessments

            sequence_type (str) : Describes the timing/order of the pulses.
                options are: sequential | interleaved | simultaneous | sandwiched
                           q0|q0|q1|q1   q0|q1|q0|q1     q01|q01       q1|q0|q0|q1
                describes the order of the AllXY pulses
        """
        if prepare_for_timedomain:
            self.prepare_for_timedomain(qubits=[q0, q1])
        if MC is None:
            MC = self.instr_MC.get_instr()

        assert q0 in self.qubits()
        assert q1 in self.qubits()

        q0idx = self.find_instrument(q0).cfg_qubit_nr()
        q1idx = self.find_instrument(q1).cfg_qubit_nr()

        p = mqo.two_qubit_AllXY(
            q0idx,
            q1idx,
            platf_cfg=self.cfg_openql_platform_fn(),
            sequence_type=sequence_type,
            replace_q1_pulses_with=replace_q1_pulses_with,
            repetitions=repetitions,
        )

        s = swf.OpenQL_Sweep(openql_program=p, CCL=self.instr_CC.get_instr())
        if detector == "correl":
            d = self.get_correlation_detector([q0, q1])
        elif detector == "int_avg":
            d = self.get_int_avg_det()
        MC.set_sweep_function(s)
        MC.set_sweep_points(np.arange(21 * repetitions))
        MC.set_detector_function(d)
        MC.run("TwoQubitAllXY_{}_{}_{}_q1_repl={}{}".format(
            q0, q1, sequence_type, replace_q1_pulses_with,
            self.msmt_suffix))
        if analyze:
            a = ma.MeasurementAnalysis(close_main_fig=close_fig)
            a = ma2.Basic1DAnalysis()
        return a


    def measure_two_qubit_allXY_crosstalk(
            self, q0: str,
            q1: str,
            q1_replace_cases: list = [
                None, "i", "rx180", "rx180", "rx180"
            ],
            sequence_type_cases: list = [
                'sequential', 'sequential', 'sequential', 'simultaneous', 'sandwiched'
            ],
            repetitions: int = 1,
            **kw
    ):
        timestamps = []
        legend_labels = []

        for seq_type, q1_replace in zip(sequence_type_cases, q1_replace_cases):
            a = self.measure_two_qubit_allxy(
                q0=q0,
                q1=q1,
                replace_q1_pulses_with=q1_replace,
                sequence_type=seq_type,
                repetitions=repetitions,
                **kw)
            timestamps.append(a.timestamps[0])
            legend_labels.append("{}, {} replace: {}".format(seq_type, q1, q1_replace))

        a_full = ma2.Basic1DAnalysis(
            t_start=timestamps[0],
            t_stop=timestamps[-1],
            legend_labels=legend_labels,
            hide_pnts=True)

        # This one is to compare only the specific sequences we are after
        a_seq = ma2.Basic1DAnalysis(
            t_start=timestamps[-3],
            t_stop=timestamps[-1],
            legend_labels=legend_labels,
            hide_pnts=True)

        return a_full, a_seq


    def measure_residual_ZZ_coupling(
            self,
            q0: str,
            q_spectators: list,
            spectator_state="0",
            times=np.linspace(0, 10e-6, 26),
            analyze: bool = True,
            close_fig: bool = True,
            prepare_for_timedomain: bool = True,
            MC: Optional[MeasurementControl] = None,
            CC=None
    ):

        assert q0 in self.qubits()
        for q_s in q_spectators:
            assert q_s in self.qubits()

        all_qubits = [q0] + q_spectators
        if prepare_for_timedomain:
            self.prepare_for_timedomain(qubits=all_qubits, prepare_for_readout=False)
            self.prepare_readout(qubits=[q0])
        if MC is None:
            MC = self.instr_MC.get_instr()

        q0idx = self.find_instrument(q0).cfg_qubit_nr()
        q_spec_idx_list = [
            self.find_instrument(q_s).cfg_qubit_nr() for q_s in q_spectators
        ]

        dt = times[1] - times[0]
        cal_points = dt/2 * np.arange(1,5) + times[-1]
        times_with_cal_points = np.append(times, cal_points)

        p = mqo.residual_coupling_sequence(
            times_with_cal_points,
            q0idx,
            q_spec_idx_list,
            spectator_state,
            self.cfg_openql_platform_fn(),
        )

        s = swf.OpenQL_Sweep(openql_program=p, CCL=self.instr_CC.get_instr())
        d = self.get_int_avg_det(qubits=[q0])
        MC.set_sweep_function(s)
        MC.set_sweep_points(times_with_cal_points)
        MC.set_detector_function(d)
        MC.run('Residual_ZZ_{}_{}_{}{}'.format(q0, q_spectators, spectator_state, self.msmt_suffix),
               exp_metadata={'target_qubit': q0,
                             'spectator_qubits': str(q_spectators),
                             'spectator_state': spectator_state})

        if analyze:
            a = ma.MeasurementAnalysis(close_main_fig=close_fig)
        return a


    def measure_state_tomography(
            self, qubits=['D2', 'X'],
            MC: Optional[MeasurementControl] = None,
            bell_state: float = None,
            product_state: float = None,
            wait_after_flux: float = None,
            prepare_for_timedomain: bool = False,
            live_plot=False,
            nr_shots_per_case=2 ** 14,
            shots_per_meas=2 ** 16,
            disable_snapshot_metadata: bool = False,
            label='State_Tomography_',
            flux_codeword="cz"
    ):
        if MC is None:
            MC = self.instr_MC.get_instr()
        if prepare_for_timedomain:
            self.prepare_for_timedomain(qubits)

        qubit_idxs = [self.find_instrument(qn).cfg_qubit_nr()
                      for qn in qubits]
        p = mqo.two_qubit_state_tomography(
            qubit_idxs,
            bell_state=bell_state,
            product_state=product_state,
            wait_after_flux=wait_after_flux,
            platf_cfg=self.cfg_openql_platform_fn(),
            flux_codeword=flux_codeword
        )

        # Special argument added to program
        combinations = p.combinations  # FIXME, see comment in mqo.two_qubit_state_tomography

        s = swf.OpenQL_Sweep(openql_program=p, CCL=self.instr_CC.get_instr())
        d = self.get_int_logging_detector(qubits)
        nr_cases = len(combinations)
        nr_shots = nr_shots_per_case * nr_cases
        shots_per_meas = int(np.floor(np.min([shots_per_meas, nr_shots]) / nr_cases) * nr_cases)

        # Ensures shots per measurement is a multiple of the number of cases
        shots_per_meas -= shots_per_meas % nr_cases

        d.set_child_attr('nr_shots', shots_per_meas)

        MC.live_plot_enabled(live_plot)  # FIXME: changes state

        MC.set_sweep_function(s)
        MC.set_sweep_points(np.tile(np.arange(nr_cases), nr_shots_per_case))
        MC.set_detector_function(d)
        MC.run('{}'.format(label),
               exp_metadata={'combinations': combinations},
               disable_snapshot_metadata=disable_snapshot_metadata)

        # mra.Multiplexed_Readout_Analysis(extract_combinations=True, options_dict={'skip_cross_fidelity': True})
        tomo_v2.Full_State_Tomography_2Q(label=label,
                                         qubit_ro_channels=qubits,  # channels we will want to use for tomo
                                         correl_ro_channels=[qubits],  # correlations we will want for the tomo
                                         tomo_qubits_idx=qubits)


    def measure_ssro_multi_qubit(
            self,
            qubits: list,
            nr_shots_per_case: int = 2 ** 13,  # 8192
            prepare_for_timedomain: bool = True,
            result_logging_mode='raw',
            initialize: bool = False,
            analyze=True,
            shots_per_meas: int = 2 ** 16,
            label='Mux_SSRO',
            MC=None):
        """
        Perform a simultaneous ssro experiment on multiple qubits.
        Args:
            qubits (list of str)
                list of qubit names
            nr_shots_per_case (int):
                total number of measurements for each case under consideration
                    e.g., n*|00> , n*|01>, n*|10> , n*|11> for two qubits

            shots_per_meas (int):
                number of single shot measurements per single
                acquisition with UHFQC

        """
        log.info("{}.measure_ssro_multi_qubit for qubits{}".format(self.name, qubits))

        # # off and on, not including post selection init measurements yet
        # nr_cases = 2**len(qubits)  # e.g., 00, 01 ,10 and 11 in the case of 2q
        # nr_shots = nr_shots_per_case*nr_cases

        # off and on, not including post selection init measurements yet
        nr_cases = 2 ** len(qubits)  # e.g., 00, 01 ,10 and 11 in the case of 2q

        if initialize:
            nr_shots = 2 * nr_shots_per_case * nr_cases
        else:
            nr_shots = nr_shots_per_case * nr_cases

        self.ro_acq_digitized(False)

        if prepare_for_timedomain:
            self.prepare_for_timedomain(qubits, bypass_flux=True)
        if MC is None:
            MC = self.instr_MC.get_instr()

        qubit_idxs = [self.find_instrument(qn).cfg_qubit_nr() for qn in qubits]
        p = mqo.multi_qubit_off_on(
            qubit_idxs,
            initialize=initialize,
            second_excited_state=False,
            platf_cfg=self.cfg_openql_platform_fn(),
        )

        s = swf.OpenQL_Sweep(openql_program=p, CCL=self.instr_CC.get_instr())

        # right is LSQ
        d = self.get_int_logging_detector(
            qubits, result_logging_mode=result_logging_mode
        )

        # This assumes qubit names do not contain spaces
        det_qubits = [v.split()[-1] for v in d.value_names]
        if (qubits != det_qubits) and (self.ro_acq_weight_type() == 'optimal'):
            # this occurs because the detector groups qubits per feedline.
            # If you do not pay attention, this will mess up the analysis of
            # this experiment.
            raise ValueError('Detector qubits do not match order specified.{} vs {}'.format(qubits, det_qubits))

        shots_per_meas = int(
            np.floor(np.min([shots_per_meas, nr_shots]) / nr_cases) * nr_cases
        )

        d.set_child_attr("nr_shots", shots_per_meas)

        # save and change parameters
        old_soft_avg = MC.soft_avg()
        old_live_plot_enabled = MC.live_plot_enabled()
        MC.soft_avg(1)
        MC.live_plot_enabled(False)

        MC.set_sweep_function(s)
        MC.set_sweep_points(np.arange(nr_shots))
        MC.set_detector_function(d)
        MC.run("{}_{}_{}".format(label, qubits, self.msmt_suffix))

        # restore parameters
        MC.soft_avg(old_soft_avg)
        MC.live_plot_enabled(old_live_plot_enabled)

        if analyze:
            if initialize:
                thresholds = [self.find_instrument(qubit).ro_acq_threshold() for qubit in qubits]
                a = ma2.Multiplexed_Readout_Analysis(
                    label=label,
                    nr_qubits=len(qubits),
                    post_selection=True,
                    post_selec_thresholds=thresholds)
                for qubit in qubits:
                    for key in a.proc_data_dict['quantities_of_interest'].keys():
                        if f' {qubit}' in str(key):
                            self.find_instrument(qubit).F_ssro(a.proc_data_dict['quantities_of_interest'][key]['Post_F_a'])
                            self.find_instrument(qubit).F_init(1-a.proc_data_dict['quantities_of_interest'][key]['Post_residual_excitation'])
            else:
                a = ma2.Multiplexed_Readout_Analysis(
                    label=label,
                    nr_qubits=len(qubits))
            # Set thresholds
            for i, qubit in enumerate(qubits):
                label = a.Channels[i]
                threshold = a.qoi[label]['threshold_raw']
                self.find_instrument(qubit).ro_acq_threshold(threshold)
        return True


    def measure_ssro_single_qubit(
            self,
            qubits: list,
            q_target: str,
            nr_shots: int = 2 ** 13,  # 8192
            prepare_for_timedomain: bool = True,
            second_excited_state: bool = False,
            result_logging_mode='raw',
            initialize: bool = False,
            analyze=True,
            shots_per_meas: int = 2 ** 16,
            nr_flux_dance: int = None,
            wait_time: float = None,
            label='Mux_SSRO',
            MC=None):
        # FIXME: lots of similarity with measure_ssro_multi_qubit
        '''
        Performs MUX single shot readout experiments of all possible
        combinations of prepared states of <qubits>. Outputs analysis
        of a single qubit <q_target>. This function is meant to
        assess a particular qubit readout in the multiplexed context.

        Args:
            qubits: List of qubits adressed in the mux readout.

            q_target: Qubit targeted in the analysis.

            nr_shots: number of shots for each prepared state of
            q_target. That is the experiment will include
            <nr_shots> shots of the qubit prepared in the ground state
            and <nr_shots> shots of the qubit prepared in the excited
            state. The remaining qubits will be prepared such that the
            experiment goes through all 2**n possible combinations of
            computational states.

            initialize: Include measurement post-selection by
            initialization.
        '''

        log.info('{}.measure_ssro_multi_qubit for qubits{}'.format(self.name, qubits))

        # off and on, not including post selection init measurements yet
        nr_cases = 2 ** len(qubits)  # e.g., 00, 01 ,10 and 11 in the case of 2q
        if second_excited_state:
            nr_cases = 3 ** len(qubits)

        if initialize == True:
            nr_shots = 4 * nr_shots
        else:
            nr_shots = 2 * nr_shots

        if prepare_for_timedomain:
            self.prepare_for_timedomain(qubits)
        if MC is None:
            MC = self.instr_MC.get_instr()

        qubit_idxs = [self.find_instrument(qn).cfg_qubit_nr()
                      for qn in qubits]

        p = mqo.multi_qubit_off_on(
            qubit_idxs,
            initialize=initialize,
            nr_flux_dance=nr_flux_dance,
            wait_time=wait_time,
            second_excited_state=second_excited_state,
            platf_cfg=self.cfg_openql_platform_fn()
        )

        s = swf.OpenQL_Sweep(openql_program=p, CCL=self.instr_CC.get_instr())

        # right is LSQ
        d = self.get_int_logging_detector(qubits, result_logging_mode=result_logging_mode)

        # This assumes qubit names do not contain spaces
        det_qubits = [v.split()[-1] for v in d.value_names]
        if (qubits != det_qubits) and (self.ro_acq_weight_type() == 'optimal'):
            # this occurs because the detector groups qubits per feedline.
            # If you do not pay attention, this will mess up the analysis of
            # this experiment.
            raise ValueError('Detector qubits do not match order specified.{} vs {}'.format(qubits, det_qubits))

        shots_per_meas = int(np.floor(
            np.min([shots_per_meas, nr_shots]) / nr_cases) * nr_cases)

        d.set_child_attr('nr_shots', shots_per_meas)

        # save and change parameters
        old_soft_avg = MC.soft_avg()
        old_live_plot_enabled = MC.live_plot_enabled()
        MC.soft_avg(1)
        MC.live_plot_enabled(False)

        MC.set_sweep_function(s)
        MC.set_sweep_points(np.arange(nr_shots))
        MC.set_detector_function(d)
        MC.run('{}_{}_{}'.format(label, q_target, self.msmt_suffix))

        # restore parameters
        MC.soft_avg(old_soft_avg)
        MC.live_plot_enabled(old_live_plot_enabled)

        if analyze:
            if initialize == True:
                thresholds = [self.find_instrument(qubit).ro_acq_threshold() \
                              for qubit in qubits]
                a = ma2.Multiplexed_Readout_Analysis(label=label,
                                                     nr_qubits=len(qubits),
                                                     q_target=q_target,
                                                     post_selection=True,
                                                     post_selec_thresholds=thresholds)
                # Print fraction of discarded shots
                # Dict = a.proc_data_dict['Post_selected_shots']
                # key = next(iter(Dict))
                # fraction=0
                # for comb in Dict[key].keys():
                #    fraction += len(Dict[key][comb])/(2**12 * 4)
                # print('Fraction of discarded results was {:.2f}'.format(1-fraction))
            else:
                a = ma2.Multiplexed_Readout_Analysis(label=label,
                                                     nr_qubits=len(qubits),
                                                     q_target=q_target)
            q_ch = [ch for ch in a.Channels if q_target in ch.decode()][0]
            # Set thresholds
            for i, qubit in enumerate(qubits):
                label = a.raw_data_dict['value_names'][i]
                threshold = a.qoi[label]['threshold_raw']
                self.find_instrument(qubit).ro_acq_threshold(threshold)
            return a.qoi[q_ch]


    def measure_transients(
            self,
            qubits: list,
            q_target: str,
            cases: list = ['off', 'on'],
            MC: Optional[MeasurementControl] = None,
            prepare_for_timedomain: bool = True,
            analyze: bool = True
    ):
        '''
        Documentation.
        '''
        if q_target not in qubits:
            raise ValueError("q_target must be included in qubits.")
        # Ensure all qubits use same acquisition instrument
        instruments = [self.find_instrument(q).instr_acquisition() for q in qubits]
        if instruments[1:] != instruments[:-1]:
            raise ValueError("All qubits must have common acquisition instrument")

        qubits_nr = [self.find_instrument(q).cfg_qubit_nr() for q in qubits]
        q_target_nr = self.find_instrument(q_target).cfg_qubit_nr()

        if MC is None:
            MC = self.instr_MC.get_instr()
        if prepare_for_timedomain:
            self.prepare_for_timedomain(qubits)

        p = mqo.targeted_off_on(
            qubits=qubits_nr,
            q_target=q_target_nr,
            pulse_comb='on',
            platf_cfg=self.cfg_openql_platform_fn()
        )

        analysis = [None for case in cases]
        for i, pulse_comb in enumerate(cases):
            if 'off' in pulse_comb.lower():
                self.find_instrument(q_target).instr_LO_mw.get_instr().off()
            elif 'on' in pulse_comb.lower():
                self.find_instrument(q_target).instr_LO_mw.get_instr().on()
            else:
                raise ValueError("pulse_comb {} not understood: Only 'on' and 'off' allowed.".format(pulse_comb))

            s = swf.OpenQL_Sweep(
                openql_program=p,
                parameter_name='Transient time',
                unit='s',
                CCL=self.instr_CC.get_instr()
            )

            if 'UHFQC' in instruments[0]:
                sampling_rate = 1.8e9
            else:
                raise NotImplementedError()
            nr_samples = self.ro_acq_integration_length() * sampling_rate

            d = det.UHFQC_input_average_detector(
                UHFQC=self.find_instrument(instruments[0]),
                AWG=self.instr_CC.get_instr(),
                nr_averages=self.ro_acq_averages(),
                nr_samples=int(nr_samples))

            MC.set_sweep_function(s)
            MC.set_sweep_points(np.arange(nr_samples) / sampling_rate)
            MC.set_detector_function(d)
            MC.run('Mux_transients_{}_{}_{}'.format(q_target, pulse_comb, self.msmt_suffix))

            if analyze:
                analysis[i] = ma2.Multiplexed_Transient_Analysis(
                    q_target='{}_{}'.format(q_target, pulse_comb))
        return analysis


    def measure_msmt_induced_dephasing(
            self,
            meas_qubit: str, 
            target_qubits: list,
            measurement_time_ns: int,
            echo_times: list = None,
            echo_phases: list = None,
            prepare_for_timedomain: bool=True):

        assert self.ro_acq_digitized() == False
        assert self.ro_acq_weight_type() == 'optimal'
        ###################
        # setup qubit idxs
        ###################
        all_qubits = [meas_qubit]+target_qubits
        meas_qubit_idx = self.find_instrument(meas_qubit).cfg_qubit_nr()
        target_idxs = [ self.find_instrument(q).cfg_qubit_nr() for q in target_qubits ]
        ###########################################
        # RO preparation (assign res_combinations)
        ###########################################
        RO_lms = np.unique([self.find_instrument(q).instr_LutMan_RO() for q in all_qubits])
        qubit_RO_lm = { self.find_instrument(q).cfg_qubit_nr() : 
                      (self.find_instrument(q).name, 
                       self.find_instrument(q).instr_LutMan_RO()) for q in all_qubits }
        main_qubits = []
        exception_qubits = []
        res_combs = {}
        for lm in RO_lms:
            res_combs[lm] = []
            comb1= []
            comb2= []
            # meas_qubit + target qubits resonators
            for idx in [meas_qubit_idx]+target_idxs:
                  if qubit_RO_lm[idx][1] == lm:
                        comb1+= [idx]
                        comb2+= [idx]
            res_combs[lm] += [comb1]
            if qubit_RO_lm[meas_qubit_idx][1] == lm:
                  res_combs[lm] += [[meas_qubit_idx]]
                  comb2.remove(meas_qubit_idx)
                  res_combs[lm] += [comb2]
                  main_qubits = [qubit_RO_lm[idx][0] for idx in comb1]
            else:
                  exception_qubits += [qubit_RO_lm[idx][0] for idx in comb1]
        # Time-domain preparation
        ordered_qubits = main_qubits+exception_qubits
        if prepare_for_timedomain:
            self.prepare_for_timedomain(ordered_qubits, bypass_flux=True)
            for lm in RO_lms:
                ro_lm = self.find_instrument(lm)
                ro_lm.resonator_combinations(res_combs[lm])
                ro_lm.load_DIO_triggered_sequence_onto_UHFQC()
            if echo_times != None:
                assert echo_phases != None
                for i, q in enumerate(target_qubits):
                    mw_lm = self.find_instrument(f'MW_lutman_{q}')
                    print(mw_lm.name)    
                    mw_lm.LutMap()[30] = {'name': 'rEcho', 'theta': 180, 
                                          'phi': echo_phases[i], 'type': 'ge'}
                    mw_lm.load_phase_pulses_to_AWG_lookuptable()

        if exception_qubits != []:
            exception_idxs = [self.find_instrument(q).cfg_qubit_nr()
                             for q in exception_qubits]
        else:
            exception_idxs = None

        p = mqo.Msmt_induced_dephasing_ramsey(
            q_rams = target_idxs,
            q_meas = meas_qubit_idx,
            echo_times = echo_times,
            meas_time = measurement_time_ns,
            exception_qubits=exception_idxs,
            platf_cfg=self.cfg_openql_platform_fn())

        d = self.get_int_avg_det(qubits=ordered_qubits)
        s = swf.OpenQL_Sweep(openql_program=p,
                             CCL=self.instr_CC.get_instr())
        MC = self.instr_MC.get_instr()
        MC.soft_avg(1)
        MC.live_plot_enabled(True)
        MC.set_sweep_function(s)
        sw_pts = np.concatenate((np.repeat(np.arange(0, 360, 20), 6), 
                                 np.array([360, 361, 362, 364])))
        MC.set_sweep_points(sw_pts)
        MC.set_detector_function(d)
        MC.run(f'Msmt_induced_dephasing_{meas_qubit}_{target_qubits}')

        a = ma2.mra.measurement_dephasing_analysis(
                meas_time=measurement_time_ns*1e-9,
                exception_qubits=exception_qubits)


    def measure_chevron(
        self,
        q0: str,
        q_spec: str,
        q_parks=None,
        amps=np.arange(0, 1, 0.05),
        lengths=np.arange(5e-9, 51e-9, 5e-9),
        adaptive_sampling=False,
        adaptive_sampling_pts=None,
        adaptive_pars: dict = None,
        prepare_for_timedomain=True,
        MC: Optional[MeasurementControl] = None,
        freq_tone=6e9,
        pow_tone=-10,
        spec_tone=False,
        target_qubit_sequence: str = "ramsey",
        waveform_name="square",
        recover_q_spec: bool = False,
    ):
        """
        Measure a chevron patter of esulting from swapping of the excitations
        of the two qubits. Qubit q0 is prepared in 1 state and flux-pulsed
        close to the interaction zone using (usually) a rectangular pulse.
        Meanwhile q1 is prepared in 0, 1 or superposition state. If it is in 0
    state flipping between 01-10 can be observed. It if is in 1 state flipping
        between 11-20 as well as 11-02 show up. In superpostion everything is visible.

        Args:
            q0 (str):
                flux-pulsed qubit (prepared in 1 state at the beginning)
            q_spec (str):
                stationary qubit (in 0, 1 or superposition)
            q_parks (list):
                qubits to move out of the interaction zone by applying a
                square flux pulse. Note that this is optional. Not specifying
                this means no extra pulses are applied.
                Note that this qubit is not read out.

            amps (array):
                amplitudes of the applied flux pulse controlled via the amplitude
                of the correspnding AWG channel

            lengths (array):
                durations of the applied flux pulses

            adaptive_sampling (bool):
                indicates whether to adaptivelly probe
                values of ampitude and duration, with points more dense where
                the data has more fine features

            adaptive_sampling_pts (int):
                number of points to measur in the adaptive_sampling mode

            prepare_for_timedomain (bool):
                should all instruments be reconfigured to
                time domain measurements

            target_qubit_sequence (str {"ground", "extited", "ramsey"}):
                specifies whether the spectator qubit should be
                prepared in the 0 state ('ground'), 1 state ('extited') or
                in superposition ('ramsey')

            spec_tone (bool):
                uses the spectroscopy source (in CW mode) of the qubit to produce
                a fake chevron.

            freq_tone (float):
                When spec_tone = True, controls the frequency of the spec source

            pow_tone (float):
                When spec_tone = True, controls the power of the spec source

            recover_q_spec (bool):
                applies the first gate of qspec at the end as well if `True`

        Circuit:
            q0    -x180-flux-x180-RO-
            qspec --x90-----(x90)-RO- (target_qubit_sequence='ramsey')

            q0    -x180-flux-x180-RO-
            qspec -x180----(x180)-RO- (target_qubit_sequence='excited')

            q0    -x180-flux-x180-RO-
            qspec ----------------RO- (target_qubit_sequence='ground')
        """

        if MC is None:
            MC = self.instr_MC.get_instr()

        assert q0 in self.qubits()
        assert q_spec in self.qubits()

        q0idx = self.find_instrument(q0).cfg_qubit_nr()
        q_specidx = self.find_instrument(q_spec).cfg_qubit_nr()
        if q_parks is not None:
            q_park_idxs = [self.find_instrument(q_park).cfg_qubit_nr() for q_park in q_parks]
            for q_park in q_parks:
                q_park_idx = self.find_instrument(q_park).cfg_qubit_nr()
                fl_lutman_park = self.find_instrument(q_park).instr_LutMan_Flux.get_instr()
                if fl_lutman_park.park_amp() < 0.1:
                    # This can cause weird behaviour if not paid attention to.
                    log.warning("Square amp for park pulse < 0.1")
                if fl_lutman_park.park_length() < np.max(lengths):
                    log.warning("Square length shorter than max Chevron length")
        else:
            q_park_idxs = None

        fl_lutman = self.find_instrument(q0).instr_LutMan_Flux.get_instr()
        fl_lutman_spec = self.find_instrument(q_spec).instr_LutMan_Flux.get_instr()

        if waveform_name == "square":
            length_par = fl_lutman.sq_length
            flux_cw = 6
        elif "cz" in waveform_name:
            length_par = fl_lutman.cz_length
            flux_cw = fl_lutman._get_cw_from_wf_name(waveform_name)
        else:
            raise ValueError("Waveform shape not understood")

        if prepare_for_timedomain:
            self.prepare_for_timedomain(qubits=[q0, q_spec])

        if 1:
            amp_par = self.hal_get_flux_amp_parameter(q0)
        else:
            # FIXME: HW dependency
            awg = fl_lutman.AWG.get_instr()
            using_QWG = isinstance(awg, QuTech_AWG_Module)
            if using_QWG:
                awg_ch = fl_lutman.cfg_awg_channel()
                amp_par = awg.parameters["ch{}_amp".format(awg_ch)]
            else:
                awg_ch = (
                    fl_lutman.cfg_awg_channel() - 1
                )  # -1 is to account for starting at 1
                ch_pair = awg_ch % 2
                awg_nr = awg_ch // 2

                amp_par = awg.parameters[
                    "awgs_{}_outputs_{}_amplitude".format(awg_nr, ch_pair)
                ]

        sw = swf.FLsweep(fl_lutman, length_par, waveform_name=waveform_name)

        p = mqo.Chevron(
            q0idx,
            q_specidx,
            q_park_idxs,
            buffer_time=0,
            buffer_time2=0,
            flux_cw=flux_cw,
            platf_cfg=self.cfg_openql_platform_fn(),
            target_qubit_sequence=target_qubit_sequence,
            cc=self.instr_CC.get_instr().name,
            recover_q_spec=recover_q_spec
        )
        self.instr_CC.get_instr().eqasm_program(p.filename)
        self.instr_CC.get_instr().start()

        d = self.get_correlation_detector(
            qubits=[q0, q_spec],
            single_int_avg=True,
            seg_per_point=1,
            always_prepare=True,
        )

        MC.set_sweep_function(amp_par)
        MC.set_sweep_function_2D(sw)
        MC.set_detector_function(d)

        label = "Chevron {} {} {}".format(q0, q_spec, target_qubit_sequence)

        if not adaptive_sampling:
            MC.set_sweep_points(amps)
            MC.set_sweep_points_2D(lengths)
            MC.run(label, mode="2D")

            ma.TwoD_Analysis()
        else:
            if adaptive_pars is None:
                adaptive_pars = {
                    "adaptive_function": adaptive.Learner2D,
                    "goal": lambda l: l.npoints > adaptive_sampling_pts,
                    "bounds": (amps, lengths),
                }
            MC.set_adaptive_function_parameters(adaptive_pars)
            MC.run(label + " adaptive", mode="adaptive")

            ma2.Basic2DInterpolatedAnalysis()


    def measure_chevron_1D_bias_sweeps(
        self,
        q0: str,
        q_spec: str,
        q_parks,
        amps=np.arange(0, 1, 0.05),
        prepare_for_timedomain=True,
        MC: Optional[MeasurementControl] = None,
        freq_tone=6e9,
        pow_tone=-10,
        spec_tone=False,
        target_qubit_sequence: str = "excited",
        waveform_name="square",
        sq_duration=None,
        adaptive_sampling=False,
        adaptive_num_pts_max=None,
        adaptive_sample_for_alignment=True,
        max_pnts_beyond_threshold=10,
        adaptive_num_pnts_uniform=0,
        minimizer_threshold=0.5,
        par_idx=1,
        peak_is_inverted=True,
        mv_bias_by=[-150e-6, 150e-6],
        flux_buffer_time=40e-9,  # use multiples of 20 ns
    ):
        """
        Measure a chevron pattern resulting from swapping of the excitations
        of the two qubits. Qubit q0 is prepared in 1 state and flux-pulsed
        close to the interaction zone using (usually) a rectangular pulse.
        Meanwhile q1 is prepared in 0, 1 or superposition state. If it is in 0
        state flipping between 10-01 can be observed. It if is in 1 state flipping
        between 11-20 as well as 11-02 show up. In superposition everything is visible.

        Args:
            q0 (str):
                flux-pulsed qubit (prepared in 1 state at the beginning)

            q_spec (str):
                stationary qubit (in 0, 1 or superposition)

            q_park (str):
                qubit to move out of the interaction zone by applying a
                square flux pulse. Note that this is optional. Not specifying
                this means no extra pulses are applied.
                Note that this qubit is not read out.

            amps (array):
                amplitudes of the applied flux pulse controlled via the amplitude
                of the corresponding AWG channel

            lengths (array):
                durations of the applied flux pulses

            adaptive_sampling (bool):
                indicates whether to adaptively probe
                values of amplitude and duration, with points more dense where
                the data has more fine features

            adaptive_num_pts_max (int):
                number of points to measure in the adaptive_sampling mode

            adaptive_num_pnts_uniform (bool):
                number of points to measure uniformly before giving control to
                adaptive sampler. Only relevant for `adaptive_sample_for_alignment`

            prepare_for_timedomain (bool):
                should all instruments be reconfigured to
                time domain measurements

            target_qubit_sequence (str {"ground", "excited", "ramsey"}):
                specifies whether the spectator qubit should be
                prepared in the 0 state ('ground'), 1 state ('excited') or
                in superposition ('ramsey')

            flux_buffer_time (float):
                buffer time added before and after the flux pulse

        Circuit:
            q0    -x180-flux-x180-RO-
            qspec --x90-----------RO- (target_qubit_sequence='ramsey')

            q0    -x180-flux-x180-RO-
            qspec -x180-----------RO- (target_qubit_sequence='excited')

            q0    -x180-flux-x180-RO-
            qspec ----------------RO- (target_qubit_sequence='ground')
        """
        if MC is None:
            MC = self.instr_MC.get_instr()

        assert q0 in self.qubits()
        assert q_spec in self.qubits()

        q0idx = self.find_instrument(q0).cfg_qubit_nr()
        q_specidx = self.find_instrument(q_spec).cfg_qubit_nr()
        if q_parks is not None:
            q_park_idxs = [self.find_instrument(q_park).cfg_qubit_nr() for q_park in q_parks]
            for q_park in q_parks:
                q_park_idx = self.find_instrument(q_park).cfg_qubit_nr()
                fl_lutman_park = self.find_instrument(q_park).instr_LutMan_Flux.get_instr()
                if fl_lutman_park.park_amp() < 0.1:
                    # This can cause weird behaviour if not paid attention to.
                    log.warning("Square amp for park pulse < 0.1")
        else:
            q_park_idxs = None

        fl_lutman = self.find_instrument(q0).instr_LutMan_Flux.get_instr()

        if waveform_name == "square":
            length_par = fl_lutman.sq_length
            flux_cw = 6  # FIXME: Hard-coded for now [2020-04-28]
            if sq_duration is None:
                raise ValueError("Square pulse duration must be specified.")
        else:
            raise ValueError("Waveform name not recognized.")

        if 1:
            amp_par = self.hal_get_flux_amp_parameter(q0)
        else:
            # FIXME: HW dependency
            awg = fl_lutman.AWG.get_instr()
            using_QWG = isinstance(awg, QuTech_AWG_Module)
            if using_QWG:
                awg_ch = fl_lutman.cfg_awg_channel()
                amp_par = awg.parameters["ch{}_amp".format(awg_ch)]
            else:
                # -1 is to account for starting at 1
                awg_ch = fl_lutman.cfg_awg_channel() - 1
                ch_pair = awg_ch % 2
                awg_nr = awg_ch // 2

                amp_par = awg.parameters[
                    "awgs_{}_outputs_{}_amplitude".format(awg_nr, ch_pair)
                ]

        p = mqo.Chevron(
            q0idx,
            q_specidx,
            q_park_idxs,
            buffer_time=flux_buffer_time,
            buffer_time2=length_par() + flux_buffer_time,
            flux_cw=flux_cw,
            platf_cfg=self.cfg_openql_platform_fn(),
            target_qubit_sequence=target_qubit_sequence,
            cc=self.instr_CC.get_instr().name,
        )
        self.instr_CC.get_instr().eqasm_program(p.filename)

        qubits = [q0, q_spec]

        d = self.get_int_avg_det()

        # if we want to add a spec tone
        # NB: not tested [2020-04-27]
        if spec_tone:
            spec_source = self.find_instrument(q0).instr_spec_source.get_instr()
            spec_source.pulsemod_state(False)
            spec_source.power(pow_tone)
            spec_source.frequency(freq_tone)
            spec_source.on()

        MC.set_sweep_function(amp_par)
        MC.set_detector_function(d)

        old_sq_duration = length_par()
        # Assumes the waveforms will be generated below in the prepare_for_timedomain
        length_par(sq_duration)
        old_amp_par = amp_par()

        fluxcurrent_instr = self.find_instrument(q0).instr_FluxCtrl.get_instr()
        flux_bias_par_name = "FBL_" + q0
        flux_bias_par = fluxcurrent_instr[flux_bias_par_name]

        flux_bias_old_val = flux_bias_par()

        label = "Chevron {} {} [cut @ {:4g} ns]".format(q0, q_spec, length_par() / 1e-9)

        def restore_pars():
            length_par(old_sq_duration)
            amp_par(old_amp_par)
            flux_bias_par(flux_bias_old_val)

        # Keep below the length_par
        if prepare_for_timedomain:
            self.prepare_for_timedomain(qubits=[q0, q_spec])
        else:
            log.warning("The flux waveform is not being uploaded!")

        if not adaptive_sampling:
            # Just single 1D sweep
            MC.set_sweep_points(amps)
            MC.run(label, mode="1D")

            restore_pars()

            ma2.Basic1DAnalysis()
        elif adaptive_sample_for_alignment:
            # Adaptive sampling intended for the calibration of the flux bias
            # (centering the chevron, and the qubit at the sweetspot)
            goal = l1dm.mk_min_threshold_goal_func(
                max_pnts_beyond_threshold=max_pnts_beyond_threshold
            )
            minimize = peak_is_inverted
            loss = l1dm.mk_minimization_loss_func(
                # Just in case it is ever changed to maximize
                threshold=(-1) ** (minimize + 1) * minimizer_threshold,
                interval_weight=200.0
            )
            bounds = (np.min(amps), np.max(amps))
            # q0 is the one leaking in the first CZ interaction point
            # because |2> amplitude is generally unpredictable, we use the
            # population in qspec to ensure there will be a peak for the
            # adaptive sampler
            # par_idx = 1 # Moved to method's arguments
            adaptive_pars_pos = {
                "adaptive_function": l1dm.Learner1D_Minimizer,
                "goal": lambda l: goal(l) or l.npoints > adaptive_num_pts_max,
                "bounds": bounds,
                "loss_per_interval": loss,
                "minimize": minimize,
                # A few uniform points to make more likely to find the peak
                "X0": np.linspace(
                    np.min(bounds),
                    np.max(bounds),
                    adaptive_num_pnts_uniform + 2)[1:-1]
            }
            bounds_neg = np.flip(-np.array(bounds), 0)
            adaptive_pars_neg = {
                "adaptive_function": l1dm.Learner1D_Minimizer,
                "goal": lambda l: goal(l) or l.npoints > adaptive_num_pts_max,
                # NB: order of the bounds matters, mind negative numbers ordering
                "bounds": bounds_neg,
                "loss_per_interval": loss,
                "minimize": minimize,
                # A few uniform points to make more likely to find the peak
                "X0": np.linspace(
                    np.min(bounds_neg),
                    np.max(bounds_neg),
                    adaptive_num_pnts_uniform + 2)[1:-1]
            }

            MC.set_sweep_functions([amp_par, flux_bias_par])
            adaptive_pars = {
                "multi_adaptive_single_dset": True,
                "adaptive_pars_list": [adaptive_pars_pos, adaptive_pars_neg],
                "extra_dims_sweep_pnts": flux_bias_par() + np.array(mv_bias_by),
                "par_idx": par_idx,
            }

            MC.set_adaptive_function_parameters(adaptive_pars)
            MC.run(label, mode="adaptive")

            restore_pars()

            a = ma2.Chevron_Alignment_Analysis(
                label=label,
                sq_pulse_duration=length_par(),
                fit_threshold=minimizer_threshold,
                fit_from=d.value_names[par_idx],
                peak_is_inverted=minimize,
            )

            return a

        else:
            # Default single 1D adaptive sampling
            adaptive_pars = {
                "adaptive_function": adaptive.Learner1D,
                "goal": lambda l: l.npoints > adaptive_num_pts_max,
                "bounds": (np.min(amps), np.max(amps)),
            }
            MC.set_adaptive_function_parameters(adaptive_pars)
            MC.run(label, mode="adaptive")

            restore_pars()

            ma2.Basic1DAnalysis()


    def measure_cryoscope(
        self,
        qubits,
        times,
        MC: Optional[MeasurementControl] = None,
        nested_MC: Optional[MeasurementControl] = None,
        double_projections: bool = False,
        update_FIRs: bool=False,
        waveform_name: str = "square",
        max_delay=None,
        twoq_pair=[2, 0],
        init_buffer=0,
        prepare_for_timedomain: bool = True,
    ):
        """
        Performs a cryoscope experiment to measure the shape of a flux pulse.

        Args:
            qubits  (list):
                a list of two target qubits

            times   (array):
                array of measurment times

            label (str):
                used to label the experiment

            waveform_name (str {"square", "custom_wf"}) :
                defines the name of the waveform used in the
                cryoscope. Valid values are either "square" or "custom_wf"

            max_delay {float, "auto"} :
                determines the delay in the pulse sequence
                if set to "auto" this is automatically set to the largest
                pulse duration for the cryoscope.

            prepare_for_timedomain (bool):
                calls self.prepare_for_timedomain on start
        """
        if MC is None:
            MC = self.instr_MC.get_instr()
        if nested_MC is None:
            nested_MC = self.instr_nested_MC.get_instr()

        for q in qubits:
            assert q in self.qubits()
        
        Q_idxs = [self.find_instrument(q).cfg_qubit_nr() for q in qubits]

        if prepare_for_timedomain:
            self.prepare_for_timedomain(qubits=qubits)

        if max_delay is None:
            max_delay = 0 
        else:
            max_delay = np.max(times) + 40e-9

        Fl_lutmans = [self.find_instrument(q).instr_LutMan_Flux.get_instr() \
                      for q in qubits]

        if waveform_name == "square":
            Sw_functions = [swf.FLsweep(lutman, lutman.sq_length,
                            waveform_name="square") for lutman in Fl_lutmans]
            swfs = swf.multi_sweep_function(Sw_functions)
            flux_cw = "fl_cw_06"

        elif waveform_name == "custom_wf":
            Sw_functions = [swf.FLsweep(lutman, lutman.custom_wf_length, 
                            waveform_name="custom_wf") for lutman in Fl_lutmans]
            swfs = swf.multi_sweep_function(Sw_functions)
            flux_cw = "fl_cw_05"

        else:
            raise ValueError(
                'waveform_name "{}" should be either '
                '"square" or "custom_wf"'.format(waveform_name)
            )

        p = mqo.Cryoscope(
            qubit_idxs=Q_idxs,
            flux_cw=flux_cw,
            twoq_pair=twoq_pair,
            platf_cfg=self.cfg_openql_platform_fn(),
            cc=self.instr_CC.get_instr().name,
            double_projections=double_projections,
        )
        self.instr_CC.get_instr().eqasm_program(p.filename)
        self.instr_CC.get_instr().start()

        MC.set_sweep_function(swfs)
        MC.set_sweep_points(times)

        if double_projections:
            # Cryoscope v2
            values_per_point = 4
            values_per_point_suffex = ["cos", "sin", "mcos", "msin"]
        else:
            # Cryoscope v1
            values_per_point = 2
            values_per_point_suffex = ["cos", "sin"]

        d = self.get_int_avg_det(
            qubits=qubits,
            values_per_point=values_per_point,
            values_per_point_suffex=values_per_point_suffex,
            single_int_avg=True,
            always_prepare=True
        )
        MC.set_detector_function(d)
        label = 'Cryoscope_{}_amps'.format('_'.join(qubits))
        MC.run(label)
        # Run analysis
        a = ma2.cv2.multi_qubit_cryoscope_analysis(label='Cryoscope',
                                                   update_FIRs=update_FIRs)
        if update_FIRs:
            for qubit, fltr in a.proc_data_dict['conv_filters'].items():
                lin_dist_kern = self.find_instrument(f'lin_dist_kern_{qubit}')
                filter_dict = {'params': {'weights': fltr},
                               'model': 'FIR', 'real-time': True }
                lin_dist_kern.filter_model_04(filter_dict)

        return True


    def measure_cryoscope_vs_amp(
        self,
        q0: str,
        amps,
        flux_cw: str = 'fl_cw_06',
        duration: float = 100e-9,
        amp_parameter: str = "channel",
        MC: Optional[MeasurementControl] = None,
        twoq_pair=[2, 0],
        label="Cryoscope",
        max_delay: float = "auto",
        prepare_for_timedomain: bool = True,
    ):
        """
        Performs a cryoscope experiment to measure the shape of a flux pulse.


        Args:
            q0  (str)     :
                name of the target qubit

            amps   (array):
                array of square pulse amplitudes

            amps_paramater (str):
                The parameter through which the amplitude is changed either
                    {"channel",  "dac"}
                    channel : uses the AWG channel amplitude parameter
                    to rescale all waveforms
                    dac : uploads a new waveform with a different amlitude
                    for each data point.

            label (str):
                used to label the experiment

            waveform_name (str {"square", "custom_wf"}) :
                defines the name of the waveform used in the
                cryoscope. Valid values are either "square" or "custom_wf"

            max_delay {float, "auto"} :
                determines the delay in the pulse sequence
                if set to "auto" this is automatically set to the largest
                pulse duration for the cryoscope.

            prepare_for_timedomain (bool):
                calls self.prepare_for_timedomain on start
        """
        if MC is None:
            MC = self.instr_MC.get_instr()

        assert q0 in self.qubits()
        q0idx = self.find_instrument(q0).cfg_qubit_nr()

        fl_lutman = self.find_instrument(q0).instr_LutMan_Flux.get_instr()
        fl_lutman.sq_length(duration)

        if prepare_for_timedomain:
            self.prepare_for_timedomain(qubits=[q0])

        if max_delay == "auto":
            max_delay = duration + 40e-9

        if amp_parameter == "channel":
            sw = fl_lutman.cfg_awg_channel_amplitude
        elif amp_parameter == "dac":
            sw = swf.FLsweep(fl_lutman, fl_lutman.sq_amp, waveform_name="square")
        else:
            raise ValueError(
                'amp_parameter "{}" should be either '
                '"channel" or "dac"'.format(amp_parameter)
            )

        p = mqo.Cryoscope(
            q0idx,
            buffer_time1=0,
            buffer_time2=max_delay,
            twoq_pair=twoq_pair,
            flux_cw=flux_cw,
            platf_cfg=self.cfg_openql_platform_fn())
        self.instr_CC.get_instr().eqasm_program(p.filename)
        self.instr_CC.get_instr().start()

        MC.set_sweep_function(sw)
        MC.set_sweep_points(amps)
        d = self.get_int_avg_det(
            values_per_point=2,
            values_per_point_suffex=["cos", "sin"],
            single_int_avg=True,
            always_prepare=True,
        )
        MC.set_detector_function(d)
        MC.run(label)
        ma2.Basic1DAnalysis()


    def measure_timing_diagram(
            self,
            qubits: list,
            flux_latencies,
            microwave_latencies,
            MC: Optional[MeasurementControl] = None,
            pulse_length=40e-9,
            flux_cw='fl_cw_06',
            prepare_for_timedomain: bool = True
    ):
        """
        Measure the ramsey-like sequence with the 40 ns flux pulses played between
        the two pi/2. While playing this sequence the delay of flux and microwave pulses
        is varied (relative to the readout pulse), looking for configuration in which
        the pulses arrive at the sample in the desired order.

        After measuting the pattern use ma2.Timing_Cal_Flux_Fine with manually
        chosen parameters to match the drawn line to the measured patern.

        Args:
            qubits  (str)     :
                list of the target qubits
            flux_latencies   (array):
                array of flux latencies to set (in seconds)
            microwave_latencies (array):
                array of microwave latencies to set (in seconds)

            label (str):
                used to label the experiment

            prepare_for_timedomain (bool):
                calls self.prepare_for_timedomain on start
        """
        if MC is None:
            MC = self.instr_MC.get_instr()
        if prepare_for_timedomain:
            self.prepare_for_timedomain(qubits)

        for q in qubits:
            assert q in self.qubits()

        Q_idxs = [self.find_instrument(q).cfg_qubit_nr() for q in qubits]

        Fl_lutmans = [self.find_instrument(q).instr_LutMan_Flux.get_instr() \
                      for q in qubits]
        for lutman in Fl_lutmans:
            lutman.sq_length(pulse_length)

        p = mqo.FluxTimingCalibration(
            qubit_idxs=Q_idxs,
            platf_cfg=self.cfg_openql_platform_fn(),
            flux_cw=flux_cw,
            cal_points=False
        )
        self.instr_CC.get_instr().eqasm_program(p.filename)

        d = self.get_int_avg_det(single_int_avg=True)
        MC.set_detector_function(d)

        s = swf.tim_flux_latency_sweep(self)
        s2 = swf.tim_mw_latency_sweep(self)
        MC.set_sweep_functions([s, s2])
        # MC.set_sweep_functions(s2)

        # MC.set_sweep_points(microwave_latencies)
        MC.set_sweep_points(flux_latencies)
        MC.set_sweep_points_2D(microwave_latencies)
        label = 'Timing_diag_{}'.format('_'.join(qubits))
        MC.run_2D(label)

        # This is the analysis that should be run but with custom delays
        ma2.Timing_Cal_Flux_Fine(
            ch_idx=0,
            close_figs=False,
            ro_latency=-100e-9,
            flux_latency=0,
            flux_pulse_duration=10e-9,
            mw_pulse_separation=80e-9
        )


    def measure_two_qubit_randomized_benchmarking(
        self,
        qubits,
        nr_cliffords=np.array(
            [1.0, 2.0, 3.0, 4.0, 5.0, 6.0, 7.0, 9.0, 12.0, 15.0, 20.0, 25.0, 30.0, 50.0]
        ),
        nr_seeds=100,
        interleaving_cliffords=[None],
        label="TwoQubit_RB_{}seeds_recompile={}_icl{}_{}_{}_{}",
        recompile: bool = "as needed",
        cal_points=True,
        flux_codeword="cz",
        flux_allocated_duration_ns: int = None,
        sim_cz_qubits: list = None,
        compile_only: bool = False,
        pool=None,  # a multiprocessing.Pool()
        rb_tasks=None,  # used after called with `compile_only=True`
        MC=None
    ):
        """
        Measures two qubit randomized benchmarking, including
        the leakage estimate.

        [2020-07-04 Victor] this method was updated to allow for parallel
        compilation using all the cores of the measurement computer

        Refs:
        Knill PRA 77, 012307 (2008)
        Wood PRA 97, 032306 (2018)

        Args:
            qubits (list):
                pair of the qubit names on which to perform RB

            nr_cliffords (array):
                lengths of the clifford sequences to perform

            nr_seeds (int):
                number of different clifford sequences of each length

            interleaving_cliffords (list):
                list of integers (or None) which specifies which cliffords
                to interleave the sequence with (for interleaved RB)
                For indices of Clifford group elements go to
                two_qubit_clifford_group.py

            label (str):
                string for formatting the measurement name

            recompile (bool, str {'as needed'}):
                indicate whether to regenerate the sequences of clifford gates.
                By default it checks whether the needed sequences were already
                generated since the most recent change of OpenQL file
                specified in self.cfg_openql_platform_fn

            cal_points (bool):
                should calibration point (qubits in 0 and 1 states)
                be included in the measurement

            flux_codeword (str):
                flux codeword corresponding to the Cphase gate

            sim_cz_qubits (list):
                A list of qubit names on which a simultaneous cz
                instruction must be applied. This is for characterizing
                CZ gates that are intended to be performed in parallel
                with other CZ gates.

            flux_allocated_duration_ns (list):
                Duration in ns of the flux pulse used when interleaved gate is
                [100_000], i.e. idle identity

            compile_only (bool):
                Compile only the RB sequences without measuring, intended for
                parallelizing iRB sequences compilation with measurements

            pool (multiprocessing.Pool):
                Only relevant for `compilation_only=True`
                Pool to which the compilation tasks will be assigned

            rb_tasks (list):
                Only relevant when running `compilation_only=True` previously,
                saving the rb_tasks, waiting for them to finish then running
                this method again and providing the `rb_tasks`.
                See the interleaved RB for use case.
        """
        if MC is None:
            MC = self.instr_MC.get_instr()

        # Settings that have to be preserved, change is required for
        # 2-state readout and postprocessing
        old_weight_type = self.ro_acq_weight_type()
        old_digitized = self.ro_acq_digitized()
        old_avg = self.ro_acq_averages()
        self.ro_acq_weight_type("optimal IQ")
        self.ro_acq_digitized(False)

        self.prepare_for_timedomain(qubits=qubits)
        MC.soft_avg(1)  # FIXME: changes state
        # The detector needs to be defined before setting back parameters
        d = self.get_int_logging_detector(qubits=qubits)
        # set back the settings
        self.ro_acq_weight_type(old_weight_type)
        self.ro_acq_digitized(old_digitized)

        for q in qubits:
            q_instr = self.find_instrument(q)
            mw_lutman = q_instr.instr_LutMan_MW.get_instr()
            mw_lutman.load_ef_rabi_pulses_to_AWG_lookuptable()

        MC.soft_avg(1)

        qubit_idxs = [self.find_instrument(q).cfg_qubit_nr() for q in qubits]
        if sim_cz_qubits is not None:
            sim_cz_qubits_idxs = [
                self.find_instrument(q).cfg_qubit_nr() for q in sim_cz_qubits
            ]
        else:
            sim_cz_qubits_idxs = None

        net_cliffords = [0, 3 * 24 + 3]  # see two_qubit_clifford_group::common_cliffords

        def send_rb_tasks(pool_):
            tasks_inputs = []
            for i in range(nr_seeds):
                task_dict = dict(
                    qubits=qubit_idxs,
                    nr_cliffords=nr_cliffords,
                    nr_seeds=1,
                    flux_codeword=flux_codeword,
                    flux_allocated_duration_ns=flux_allocated_duration_ns,
                    platf_cfg=self.cfg_openql_platform_fn(),
                    program_name="TwoQ_RB_int_cl_s{}_ncl{}_icl{}_{}_{}".format(
                        int(i),
                        list(map(int, nr_cliffords)),
                        interleaving_cliffords,
                        qubits[0],
                        qubits[1],
                    ),
                    interleaving_cliffords=interleaving_cliffords,
                    cal_points=cal_points,
                    net_cliffords=net_cliffords,  # measures with and without inverting
                    f_state_cal_pts=True,
                    recompile=recompile,
                    sim_cz_qubits=sim_cz_qubits_idxs,
                )
                tasks_inputs.append(task_dict)

            rb_tasks = pool_.map_async(cl_oql.parallel_friendly_rb, tasks_inputs)

            return rb_tasks

        if compile_only:
            assert pool is not None  # FIXME: add proper message
            rb_tasks = send_rb_tasks(pool)
            return rb_tasks

        if rb_tasks is None:
            # Using `with ...:` makes sure the other processes will be terminated
            # avoid starting too mane processes,
            # nr_processes = None will start as many as the PC can handle
            nr_processes = None if recompile else 1
            with multiprocessing.Pool(
                nr_processes,
                maxtasksperchild=cl_oql.maxtasksperchild  # avoid RAM issues
            ) as pool:
                rb_tasks = send_rb_tasks(pool)
                cl_oql.wait_for_rb_tasks(rb_tasks)

        programs_filenames = rb_tasks.get()

        # to include calibration points
        if cal_points:
            sweep_points = np.append(
                np.repeat(nr_cliffords, 2),
                [nr_cliffords[-1] + 0.5] * 2
                + [nr_cliffords[-1] + 1.5] * 2
                + [nr_cliffords[-1] + 2.5] * 3,
            )
        else:
            sweep_points = np.repeat(nr_cliffords, 2)

        counter_param = ManualParameter("name_ctr", initial_value=0)
        prepare_function_kwargs = {
            "counter_param": counter_param,
            "programs_filenames": programs_filenames,
            "CC": self.instr_CC.get_instr(),
        }

        # Using the first detector of the multi-detector as this is
        # in charge of controlling the CC (see self.get_int_logging_detector)
        d.set_prepare_function(
            oqh.load_range_of_oql_programs_from_filenames,
            prepare_function_kwargs, detectors="first"
        )
        # d.nr_averages = 128

        reps_per_seed = 4094 // len(sweep_points)
        nr_shots = reps_per_seed * len(sweep_points)
        d.set_child_attr("nr_shots", nr_shots)

        s = swf.None_Sweep(parameter_name="Number of Cliffords", unit="#")

        MC.set_sweep_function(s)
        MC.set_sweep_points(np.tile(sweep_points, reps_per_seed * nr_seeds))

        MC.set_detector_function(d)
        label = label.format(
            nr_seeds,
            recompile,
            interleaving_cliffords,
            qubits[0],
            qubits[1],
            flux_codeword)
        MC.run(label, exp_metadata={"bins": sweep_points})
        # N.B. if interleaving cliffords are used, this won't work
        ma2.RandomizedBenchmarking_TwoQubit_Analysis(label=label)

    # FIXME: Under testing by Jorge
    # def measure_two_qubit_randomized_benchmarking(
    #     self,
    #     qubits,
    #     nr_cliffords=np.array(
    #         [1.0, 2.0, 3.0, 4.0, 5.0, 6.0, 7.0, 9.0, 12.0, 15.0, 20.0, 25.0, 30.0, 50.0]
    #     ),
    #     nr_seeds=100,
    #     interleaving_cliffords=[None],
    #     label="TwoQubit_RB_{}seeds_recompile={}_icl{}_{}_{}_{}",
    #     recompile: bool = "as needed",
    #     cal_points=True,
    #     flux_codeword="cz",
    #     flux_allocated_duration_ns: int = None,
    #     sim_cz_qubits: list = None,
    #     sim_single_qubits: list = None,
    #     compile_only: bool = False,
    #     pool=None,  # a multiprocessing.Pool()
    #     rb_tasks=None,  # used after called with `compile_only=True`
    #     MC=None
    # ):
    #     """
    #     Measures two qubit randomized benchmarking, including
    #     the leakage estimate.

    #     [2020-07-04 Victor] this method was updated to allow for parallel
    #     compilation using all the cores of the measurement computer

    #     Refs:
    #     Knill PRA 77, 012307 (2008)
    #     Wood PRA 97, 032306 (2018)

    #     Args:
    #         qubits (list):
    #             pair of the qubit names on which to perform RB

    #         nr_cliffords (array):
    #             lengths of the clifford sequences to perform

    #         nr_seeds (int):
    #             number of different clifford sequences of each length

    #         interleaving_cliffords (list):
    #             list of integers (or None) which specifies which cliffords
    #             to interleave the sequence with (for interleaved RB)
    #             For indices of Clifford group elements go to
    #             two_qubit_clifford_group.py

    #         label (str):
    #             string for formatting the measurement name

    #         recompile (bool, str {'as needed'}):
    #             indicate whether to regenerate the sequences of clifford gates.
    #             By default it checks whether the needed sequences were already
    #             generated since the most recent change of OpenQL file
    #             specified in self.cfg_openql_platform_fn

    #         cal_points (bool):
    #             should calibration point (qubits in 0 and 1 states)
    #             be included in the measurement

    #         flux_codeword (str):
    #             flux codeword corresponding to the Cphase gate
    #         sim_cz_qubits (list):
    #             A list of qubit names on which a simultaneous cz
    #             instruction must be applied. This is for characterizing
    #             CZ gates that are intended to be performed in parallel
    #             with other CZ gates.
    #         flux_allocated_duration_ns (list):
    #             Duration in ns of the flux pulse used when interleaved gate is
    #             [100_000], i.e. idle identity
    #         compilation_only (bool):
    #             Compile only the RB sequences without measuring, intended for
    #             parallelizing iRB sequences compilation with measurements
    #         pool (multiprocessing.Pool):
    #             Only relevant for `compilation_only=True`
    #             Pool to which the compilation tasks will be assigned
    #         rb_tasks (list):
    #             Only relevant when running `compilation_only=True` previously,
    #             saving the rb_tasks, waiting for them to finish then running
    #             this method again and providing the `rb_tasks`.
    #             See the interleaved RB for use case.
    #     """
    #     if MC is None:
    #         MC = self.instr_MC.get_instr()

    #     # Settings that have to be preserved, change is required for
    #     # 2-state readout and postprocessing
    #     old_weight_type = self.ro_acq_weight_type()
    #     old_digitized = self.ro_acq_digitized()
    #     old_avg = self.ro_acq_averages()
    #     self.ro_acq_weight_type("optimal IQ")
    #     self.ro_acq_digitized(False)

    #     self.prepare_for_timedomain(qubits=qubits)
    #     MC.soft_avg(1)
    #     # The detector needs to be defined before setting back parameters
    #     d = self.get_int_logging_detector(qubits=qubits)
    #     # set back the settings
    #     self.ro_acq_weight_type(old_weight_type)
    #     self.ro_acq_digitized(old_digitized)

    #     for q in qubits:
    #         q_instr = self.find_instrument(q)
    #         mw_lutman = q_instr.instr_LutMan_MW.get_instr()
    #         mw_lutman.load_ef_rabi_pulses_to_AWG_lookuptable()
    #     if sim_single_qubits:
    #         for q in sim_single_qubits:
    #             q_instr = self.find_instrument(q)
    #             mw_lutman = q_instr.instr_LutMan_MW.get_instr()
    #             mw_lutman.set_default_lutmap()
    #             mw_lutman.load_waveforms_onto_AWG_lookuptable()


    #     MC.soft_avg(1)

    #     qubit_idxs = [self.find_instrument(q).cfg_qubit_nr() for q in qubits]
    #     if sim_cz_qubits is not None:
    #         sim_cz_qubits_idxs = [
    #             self.find_instrument(q).cfg_qubit_nr() for q in sim_cz_qubits
    #         ]
    #     else:
    #         sim_cz_qubits_idxs = None

    #     if sim_single_qubits is not None:
    #         sim_single_qubits_idxs = [
    #             self.find_instrument(q).cfg_qubit_nr() for q in sim_single_qubits
    #         ]
    #     else:
    #         sim_single_qubits_idxs = None

    #     net_cliffords = [0, 3 * 24 + 3]

    #     programs = []
        
    #     print('Generating {} RB programs'.format(nr_seeds))
    #     t0 = time.time()
    #     for i in range(nr_seeds):
    #         check_keyboard_interrupt()
    #         # p = cl_oql.randomized_benchmarking(
    #         #     qubits=qubit_idxs,
    #         #     nr_cliffords=nr_cliffords,
    #         #     nr_seeds=1,
    #         #     flux_codeword=flux_codeword,
    #         #     flux_allocated_duration_ns=flux_allocated_duration_ns,
    #         #     platf_cfg=self.cfg_openql_platform_fn(),
    #         #     program_name="TwoQ_RB_int_cl_s{}_ncl{}_icl{}_{}_{}".format(
    #         #         int(i),
    #         #         list(map(int, nr_cliffords)),
    #         #         interleaving_cliffords,
    #         #         qubits[0],
    #         #         qubits[1],
    #         #         ),
    #         #     interleaving_cliffords=interleaving_cliffords,
    #         #     cal_points=cal_points,
    #         #     net_cliffords=net_cliffords,  # measures with and without inverting
    #         #     f_state_cal_pts=True,
    #         #     recompile=recompile,
    #         #     sim_cz_qubits=sim_cz_qubits_idxs,
    #         #     )
    #         p = cl_oql.two_qubit_randomized_benchmarking(
    #             two_qubit_pair= qubit_idxs,
    #             single_qubits=sim_single_qubits_idxs,
    #             nr_cliffords=nr_cliffords,
    #             nr_seeds= 1,
    #             flux_codeword=flux_codeword,
    #             flux_allocated_duration_ns=flux_allocated_duration_ns,
    #             platf_cfg=self.cfg_openql_platform_fn(),
    #             program_name="TwoQ_RB_int_cl_s{}_ncl{}_icl{}_{}_{}".format(
    #                 int(i),
    #                 list(map(int, nr_cliffords)),
    #                 interleaving_cliffords,
    #                 qubits[0],
    #                 qubits[1],
    #                 ),
    #             interleaving_cliffords=interleaving_cliffords,
    #             cal_points=cal_points,
    #             two_qubit_net_cliffords=net_cliffords,
    #             single_qubit_net_cliffords=net_cliffords,
    #             f_state_cal_pts=True,
    #             recompile=recompile
    #             )
    #         print(f'compiled_program {i+1}')
    #         programs.append(p)


    #     # to include calibration points
    #     if cal_points:
    #         sweep_points = np.append(
    #             np.repeat(nr_cliffords, 2),
    #             [nr_cliffords[-1] + 0.5] * 2
    #             + [nr_cliffords[-1] + 1.5] * 2
    #             + [nr_cliffords[-1] + 2.5] * 3,
    #         )
    #     else:
    #         sweep_points = np.repeat(nr_cliffords, 2)

    #     counter_param = ManualParameter("name_ctr", initial_value=0)
    #     prepare_function_kwargs = {
    #         "counter_param": counter_param,
    #         "programs": programs,
    #         "CC": self.instr_CC.get_instr(),
    #     }

    #     # Using the first detector of the multi-detector as this is
    #     # in charge of controlling the CC (see self.get_int_logging_detector)
    #     d.set_prepare_function(
    #         oqh.load_range_of_oql_programs,
    #         prepare_function_kwargs, detectors="first"
    #     )
    #     # d.nr_averages = 128

    #     reps_per_seed = 4094 // len(sweep_points)
    #     nr_shots = reps_per_seed * len(sweep_points)
    #     d.set_child_attr("nr_shots", nr_shots)

    #     s = swf.None_Sweep(parameter_name="Number of Cliffords", unit="#")

    #     MC.set_sweep_function(s)
    #     MC.set_sweep_points(np.tile(sweep_points, reps_per_seed * nr_seeds))

    #     MC.set_detector_function(d)
    #     label = label.format(
    #         nr_seeds,
    #         recompile,
    #         interleaving_cliffords,
    #         qubits[0],
    #         qubits[1],
    #         flux_codeword)
    #     if sim_single_qubits:
    #         label += f'_sim_{sim_single_qubits}'
    #     MC.run(label, exp_metadata={"bins": sweep_points})
    #     # N.B. if interleaving cliffords are used, this won't work
    #     ma2.RandomizedBenchmarking_TwoQubit_Analysis(label=label)

    def measure_interleaved_randomized_benchmarking_statistics(
            self,
            RB_type: str = "CZ",
            nr_iRB_runs: int = 30,
            **iRB_kw
        ):
        """
        This is an optimized way of measuring statistics of the iRB
        Main advantage: it recompiles the RB sequences for the next run in the
        loop while measuring the current run. This ensures that measurements
        are as close to back-to-back as possible and saves a significant
        amount of idle time on the experimental setup
        """
        if not iRB_kw["recompile"]:
            log.warning(
                "iRB statistics are intended to be measured while " +
                "recompiling the RB sequences!"
            )

        if RB_type == "CZ":
            measurement_func = self.measure_two_qubit_interleaved_randomized_benchmarking
        elif RB_type == "CZ_parked_qubit":
            measurement_func = self.measure_single_qubit_interleaved_randomized_benchmarking_parking
        else:
            raise ValueError(
                "RB type `{}` not recognized!".format(RB_type)
            )

        rounds_success = np.zeros(nr_iRB_runs)
        t0 = time.time()
        # `maxtasksperchild` avoid RAM issues
        with multiprocessing.Pool(maxtasksperchild=cl_oql.maxtasksperchild) as pool:
            rb_tasks_start = None
            last_run = nr_iRB_runs - 1
            for i in range(nr_iRB_runs):
                iRB_kw["rb_tasks_start"] = rb_tasks_start
                iRB_kw["pool"] = pool
                iRB_kw["start_next_round_compilation"] = (i < last_run)
                round_successful = False
                try:
                    rb_tasks_start = measurement_func(
                        **iRB_kw
                    )
                    round_successful = True
                except Exception:
                    print_exception()
                finally:
                    rounds_success[i] = 1 if round_successful else 0
        t1 = time.time()
        good_rounds = int(np.sum(rounds_success))
        print("Performed {}/{} successful iRB measurements in {:>7.1f} s ({:>7.1f} min.).".format(
            good_rounds, nr_iRB_runs, t1 - t0, (t1 - t0) / 60
        ))
        if good_rounds < nr_iRB_runs:
            log.error("Not all iRB measurements were successful!")


    def measure_two_qubit_interleaved_randomized_benchmarking(
            self,
            qubits: list,
            nr_cliffords=np.array(
                [1., 3., 5., 7., 9., 11., 15., 20., 25., 30., 40., 50., 70., 90., 120.]
            ),
            nr_seeds=100,
            recompile: bool = "as needed",
            flux_codeword="cz",
            flux_allocated_duration_ns: int = None,
            sim_cz_qubits: list = None,
            measure_idle_flux: bool = True,
            rb_tasks_start: list = None,
            pool=None,
            cardinal: dict = None,
            start_next_round_compilation: bool = False,
            maxtasksperchild=None,
            MC = None,
        ):
        # USED_BY: inspire_dependency_graph.py,
        """
        Perform two qubit interleaved randomized benchmarking with an
        interleaved CZ gate, and optionally an interleaved idle identity with
        the duration of the CZ.

        If recompile is `True` or `as needed` it will parallelize RB sequence
        compilation with measurement (beside the parallelization of the RB
        sequences which will always happen in parallel).
        """
        if MC is None:
            MC = self.instr_MC.get_instr()

        def run_parallel_iRB(
                recompile, pool, rb_tasks_start: list = None,
                start_next_round_compilation: bool = False
            ):
            """
            We define the full parallel iRB procedure here as function such
            that we can control the flow of the parallel RB sequences
            compilations from the outside of this method, and allow for
            chaining RB compilations for sequential measurements intended for
            taking statistics of the RB performance
            """
            rb_tasks_next = None

            # 1. Start (non-blocking) compilation for [None]
            # We make it non-blocking such that the non-blocking feature
            # is used for the interleaved cases
            if rb_tasks_start is None:
                rb_tasks_start = self.measure_two_qubit_randomized_benchmarking(
                    qubits=qubits,
                    MC=MC,
                    nr_cliffords=nr_cliffords,
                    interleaving_cliffords=[None],
                    recompile=recompile,
                    flux_codeword=flux_codeword,
                    nr_seeds=nr_seeds,
                    sim_cz_qubits=sim_cz_qubits,
                    # FIXME: Under testing by Jorge
                    # sim_single_qubits=sim_single_qubits,
                    compile_only=True,
                    pool=pool
                )

            # 2. Wait for [None] compilation to finish
            cl_oql.wait_for_rb_tasks(rb_tasks_start)

            # 3. Start (non-blocking) compilation for [104368]
            rb_tasks_CZ = self.measure_two_qubit_randomized_benchmarking(
                qubits=qubits,
                MC=MC,
                nr_cliffords=nr_cliffords,
                interleaving_cliffords=[104368],
                recompile=recompile,
                flux_codeword=flux_codeword,
                nr_seeds=nr_seeds,
                sim_cz_qubits=sim_cz_qubits,
                # FIXME: Under testing by Jorge
                # sim_single_qubits=sim_single_qubits,
                compile_only=True,
                pool=pool
            )

            # 4. Start the measurement and run the analysis for [None]
            self.measure_two_qubit_randomized_benchmarking(
                qubits=qubits,
                MC=MC,
                nr_cliffords=nr_cliffords,
                interleaving_cliffords=[None],
                recompile=False,  # This of course needs to be False
                flux_codeword=flux_codeword,
                nr_seeds=nr_seeds,
                sim_cz_qubits=sim_cz_qubits,
                # FIXME: Under testing by Jorge
                # sim_single_qubits=sim_single_qubits,
                rb_tasks=rb_tasks_start,
            )

            # 5. Wait for [104368] compilation to finish
            cl_oql.wait_for_rb_tasks(rb_tasks_CZ)

            # 6. Start (non-blocking) compilation for [100_000]
            if measure_idle_flux:
                rb_tasks_I = self.measure_two_qubit_randomized_benchmarking(
                    qubits=qubits,
                    MC=MC,
                    nr_cliffords=nr_cliffords,
                    interleaving_cliffords=[100_000],
                    recompile=recompile,
                    flux_codeword=flux_codeword,
                    flux_allocated_duration_ns=flux_allocated_duration_ns,
                    nr_seeds=nr_seeds,
                    sim_cz_qubits=sim_cz_qubits,
                    # FIXME: Under testing by Jorge
                    # sim_single_qubits=sim_single_qubits,
                    compile_only=True,
                    pool=pool,
                )
            elif start_next_round_compilation:
                # Optionally send to the `pool` the tasks of RB compilation to be
                # used on the next round of calling the iRB method
                rb_tasks_next = self.measure_two_qubit_randomized_benchmarking(
                    qubits=qubits,
                    MC=MC,
                    nr_cliffords=nr_cliffords,
                    interleaving_cliffords=[None],
                    recompile=recompile,
                    flux_codeword=flux_codeword,
                    nr_seeds=nr_seeds,
                    sim_cz_qubits=sim_cz_qubits,
                    # FIXME: Under testing by Jorge
                    # sim_single_qubits=sim_single_qubits,
                    compile_only=True,
                    pool=pool
                )
            # 7. Start the measurement and run the analysis for [104368]
            self.measure_two_qubit_randomized_benchmarking(
                qubits=qubits,
                MC=MC,
                nr_cliffords=nr_cliffords,
                interleaving_cliffords=[104368],
                recompile=False,
                flux_codeword=flux_codeword,
                nr_seeds=nr_seeds,
                sim_cz_qubits=sim_cz_qubits,
                # FIXME: Under testing by Jorge
                # sim_single_qubits=sim_single_qubits,
                rb_tasks=rb_tasks_CZ,
            )
            ma2.InterleavedRandomizedBenchmarkingAnalysis(
                label_base="icl[None]",
                label_int="icl[104368]"
            )

            if measure_idle_flux:
                # 8. Wait for [100_000] compilation to finish
                cl_oql.wait_for_rb_tasks(rb_tasks_I)

                # 8.a. Optionally send to the `pool` the tasks of RB compilation to be
                # used on the next round of calling the iRB method
                if start_next_round_compilation:
                    rb_tasks_next = self.measure_two_qubit_randomized_benchmarking(
                        qubits=qubits,
                        MC=MC,
                        nr_cliffords=nr_cliffords,
                        interleaving_cliffords=[None],
                        recompile=recompile,
                        flux_codeword=flux_codeword,
                        nr_seeds=nr_seeds,
                        sim_cz_qubits=sim_cz_qubits,
                        # FIXME: Under testing by Jorge
                        # sim_single_qubits=sim_single_qubits,
                        compile_only=True,
                        pool=pool
                    )

                # 9. Start the measurement and run the analysis for [100_000]
                self.measure_two_qubit_randomized_benchmarking(
                    qubits=qubits,
                    MC=MC,
                    nr_cliffords=nr_cliffords,
                    interleaving_cliffords=[100_000],
                    recompile=False,
                    flux_codeword=flux_codeword,
                    flux_allocated_duration_ns=flux_allocated_duration_ns,
                    nr_seeds=nr_seeds,
                    sim_cz_qubits=sim_cz_qubits,
                    # FIXME: Under testing by Jorge
                    # sim_single_qubits=sim_single_qubits,
                    rb_tasks=rb_tasks_I
                )
                ma2.InterleavedRandomizedBenchmarkingAnalysis(
                    label_base="icl[None]",
                    label_int="icl[104368]",
                    label_int_idle="icl[100000]"
                )

            return rb_tasks_next

        if recompile or recompile == "as needed":
            # This is an optimization that compiles the interleaved RB
            # sequences for the next measurement while measuring the previous
            # one
            if pool is None:
                # Using `with ...:` makes sure the other processes will be terminated
                # `maxtasksperchild` avoid RAM issues
                if not maxtasksperchild:
                    maxtasksperchild = cl_oql.maxtasksperchild
                with multiprocessing.Pool(maxtasksperchild=maxtasksperchild) as pool:
                    run_parallel_iRB(recompile=recompile,
                                    pool=pool,
                                    rb_tasks_start=rb_tasks_start)
            else:
                # In this case the `pool` to execute the RB compilation tasks
                # is provided, `rb_tasks_start` is expected to be as well
                rb_tasks_next = run_parallel_iRB(
                    recompile=recompile,
                    pool=pool,
                    rb_tasks_start=rb_tasks_start,
                    start_next_round_compilation=start_next_round_compilation)
                return rb_tasks_next
        else:
            # recompile=False no need to parallelize compilation with measurement
            # Perform two-qubit RB (no interleaved gate)
            self.measure_two_qubit_randomized_benchmarking(
                qubits=qubits,
                MC=MC,
                nr_cliffords=nr_cliffords,
                interleaving_cliffords=[None],
                recompile=recompile,
                flux_codeword=flux_codeword,
                nr_seeds=nr_seeds,
                sim_cz_qubits=sim_cz_qubits,
                # FIXME: Under testing by Jorge
                # sim_single_qubits=sim_single_qubits,
            )

            # Perform two-qubit RB with CZ interleaved
            self.measure_two_qubit_randomized_benchmarking(
                qubits=qubits,
                MC=MC,
                nr_cliffords=nr_cliffords,
                interleaving_cliffords=[104368],
                recompile=recompile,
                flux_codeword=flux_codeword,
                nr_seeds=nr_seeds,
                sim_cz_qubits=sim_cz_qubits,
                # FIXME: Under testing by Jorge
                # sim_single_qubits=sim_single_qubits,
            )

            a = ma2.InterleavedRandomizedBenchmarkingAnalysis(
                label_base="icl[None]",
                label_int="icl[104368]",
            )
            if cardinal:
                opposite_cardinal = {'NW':'SE', 'NE':'SW', 'SW':'NE', 'SE':'NW'}
                self.find_instrument(qubits[0]).parameters[f'F_2QRB_{cardinal}'].set(1-a.proc_data_dict['quantities_of_interest']['eps_CZ_simple'].n)
                self.find_instrument(qubits[1]).parameters[f'F_2QRB_{opposite_cardinal[cardinal]}'].set(1-a.proc_data_dict['quantities_of_interest']['eps_CZ_simple'].n)

            if measure_idle_flux:
                # Perform two-qubit iRB with idle identity of same duration as CZ
                self.measure_two_qubit_randomized_benchmarking(
                    qubits=qubits,
                    MC=MC,
                    nr_cliffords=nr_cliffords,
                    interleaving_cliffords=[100_000],
                    recompile=recompile,
                    flux_codeword=flux_codeword,
                    flux_allocated_duration_ns=flux_allocated_duration_ns,
                    nr_seeds=nr_seeds,
                    sim_cz_qubits=sim_cz_qubits,
                    # FIXME: Under testing by Jorge
                    # sim_single_qubits=sim_single_qubits,
                )
                ma2.InterleavedRandomizedBenchmarkingAnalysis(
                    label_base="icl[None]",
                    label_int="icl[104368]",
                    label_int_idle="icl[100000]"

                )
        return True


    def measure_two_qubit_purity_benchmarking(
            self,
            qubits,
            MC,
            nr_cliffords=np.array(
                [1.0, 2.0, 3.0, 4.0, 5.0, 6.0, 7.0, 9.0, 12.0, 15.0, 20.0, 25.0]
            ),
            nr_seeds=100,
            interleaving_cliffords=[None],
            label="TwoQubit_purityB_{}seeds_{}_{}",
            recompile: bool = "as needed",
            cal_points: bool = True,
            flux_codeword: str = "cz",
        ):
        """
        Measures two qubit purity (aka unitarity) benchmarking.
        It is a modified RB routine which measures the length of
        the Bloch vector at the end of the sequence of cliffords
        to verify the putity of the final state. In this way it is
        not sensitive to systematic errors in the gates allowing
        to estimate whether the RB gate fidelity is limited by
        incoherent errors or inaccurate tuning.

        Refs:
        Joel Wallman, New J. Phys. 17, 113020 (2015)

        Args:
            qubits (list):
                pair of the qubit names on which to perform RB

            nr_cliffords (array):
                lengths of the clifford sequences to perform

            nr_seeds (int):
                number of different clifford sequences of each length

            interleaving_cliffords (list):
                list of integers (or None) which specifies which cliffords
                to interleave the sequence with (for interleaved RB)
                For indices of Clifford group elements go to
                two_qubit_clifford_group.py

            label (str):
                string for formatting the measurement name

            recompile (bool, str {'as needed'}):
                indicate whether to regenerate the sequences of clifford gates.
                By default it checks whether the needed sequences were already
                generated since the most recent change of OpenQL file
                specified in self.cfg_openql_platform_fn

            cal_points (bool):
                should calibration point (qubits in 0 and 1 states)
                be included in the measurement
        """

        # Settings that have to be preserved, change is required for
        # 2-state readout and postprocessing
        old_weight_type = self.ro_acq_weight_type()
        old_digitized = self.ro_acq_digitized()
        # [2020-07-02] 'optimal IQ' mode is the standard now,
        self.ro_acq_weight_type("optimal IQ")
        self.ro_acq_digitized(False)

        self.prepare_for_timedomain(qubits=qubits)

        # Need to be created before setting back the ro mode
        d = self.get_int_logging_detector(qubits=qubits)

        MC.soft_avg(1)
        # set back the settings
        self.ro_acq_weight_type(old_weight_type)
        self.ro_acq_digitized(old_digitized)

        for q in qubits:
            q_instr = self.find_instrument(q)
            mw_lutman = q_instr.instr_LutMan_MW.get_instr()
            mw_lutman.load_ef_rabi_pulses_to_AWG_lookuptable()

        MC.soft_avg(1)

        programs = []
        t0 = time.time()
        print("Generating {} PB programs".format(nr_seeds))
        qubit_idxs = [self.find_instrument(q).cfg_qubit_nr() for q in qubits]
        for i in range(nr_seeds):
            # check for keyboard interrupt q because generating can be slow
            check_keyboard_interrupt()
            sweep_points = np.concatenate([nr_cliffords, [nr_cliffords[-1] + 0.5] * 4])

            p = cl_oql.randomized_benchmarking(
                qubits=qubit_idxs,
                nr_cliffords=nr_cliffords,
                nr_seeds=1,
                platf_cfg=self.cfg_openql_platform_fn(),
                program_name="TwoQ_PB_int_cl{}_s{}_ncl{}_{}_{}_double".format(
                    i,
                    list(map(int, nr_cliffords)),
                    interleaving_cliffords,
                    qubits[0],
                    qubits[1],
                ),
                interleaving_cliffords=interleaving_cliffords,
                cal_points=cal_points,
                net_cliffords=[
                    0 * 24 + 0,
                    0 * 24 + 21,
                    0 * 24 + 16,
                    21 * 24 + 0,
                    21 * 24 + 21,
                    21 * 24 + 16,
                    16 * 24 + 0,
                    16 * 24 + 21,
                    16 * 24 + 16,
                    3 * 24 + 3,
                ],
                # ZZ, XZ, YZ,
                # ZX, XX, YX
                # ZY, XY, YY
                # (-Z)(-Z) (for f state calibration)
                f_state_cal_pts=True,
                recompile=recompile,
                flux_codeword=flux_codeword,
            )
            p.sweep_points = sweep_points
            programs.append(p)
            print(
                "Generated {} PB programs in {:>7.1f}s".format(i + 1, time.time() - t0),
                end="\r",
            )
        print(
            "Succesfully generated {} PB programs in {:>7.1f}s".format(
                nr_seeds, time.time() - t0
            )
        )

        # to include calibration points
        if cal_points:
            sweep_points = np.append(
                np.repeat(nr_cliffords, 10),
                [nr_cliffords[-1] + 0.5] * 2
                + [nr_cliffords[-1] + 1.5] * 2
                + [nr_cliffords[-1] + 2.5] * 3,
            )
        else:
            sweep_points = np.repeat(nr_cliffords, 10)

        counter_param = ManualParameter("name_ctr", initial_value=0)
        prepare_function_kwargs = {
            "counter_param": counter_param,
            "programs": programs,
            "CC": self.instr_CC.get_instr(),
        }

        # Using the first detector of the multi-detector as this is
        # in charge of controlling the CC (see self.get_int_logging_detector)
        d.set_prepare_function(
            oqh.load_range_of_oql_programs, prepare_function_kwargs,
            detectors="first"
        )
        # d.nr_averages = 128

        reps_per_seed = 4094 // len(sweep_points)
        nr_shots = reps_per_seed * len(sweep_points)
        d.set_child_attr("nr_shots", nr_shots)

        s = swf.None_Sweep(parameter_name="Number of Cliffords", unit="#")

        MC.set_sweep_function(s)
        MC.set_sweep_points(np.tile(sweep_points, reps_per_seed * nr_seeds))

        MC.set_detector_function(d)
        MC.run(
            label.format(nr_seeds, qubits[0], qubits[1]),
            exp_metadata={"bins": sweep_points},
        )
        # N.B. if measurement was interrupted this wont work
        ma2.UnitarityBenchmarking_TwoQubit_Analysis(nseeds=nr_seeds)


    def measure_two_qubit_character_benchmarking(
        self,
        qubits,
        MC,
        nr_cliffords=np.array(
            [
                1.0,
                2.0,
                3.0,
                5.0,
                6.0,
                7.0,
                9.0,
                12.0,
                15.0,
                19.0,
                25.0,
                31.0,
                39.0,
                49,
                62,
                79,
            ]
        ),
        nr_seeds=100,
        interleaving_cliffords=[None, -4368],
        label="TwoQubit_CharBench_{}seeds_icl{}_{}_{}",
        flux_codeword="fl_cw_01",
        recompile: bool = "as needed",
        ch_idxs=np.array([1, 2]),
    ):
        # Refs:
        # Helsen arXiv:1806.02048v1
        # Xue PRX 9, 021011 (2019)

        # Settings that have to be preserved, change is required for
        # 2-state readout and postprocessing
        old_weight_type = self.ro_acq_weight_type()
        old_digitized = self.ro_acq_digitized()
        self.ro_acq_weight_type("SSB")
        self.ro_acq_digitized(False)

        self.prepare_for_timedomain(qubits=qubits)

        MC.soft_avg(1)
        # set back the settings
        d = self.get_int_logging_detector(qubits=qubits)
        self.ro_acq_weight_type(old_weight_type)
        self.ro_acq_digitized(old_digitized)

        for q in qubits:
            q_instr = self.find_instrument(q)
            mw_lutman = q_instr.instr_LutMan_MW.get_instr()
            mw_lutman.load_ef_rabi_pulses_to_AWG_lookuptable()

        MC.soft_avg(1)

        programs = []
        t0 = time.time()
        print("Generating {} Character benchmarking programs".format(nr_seeds))
        qubit_idxs = [self.find_instrument(q).cfg_qubit_nr() for q in qubits]
        for i in range(nr_seeds):
            # check for keyboard interrupt q because generating can be slow
            check_keyboard_interrupt()
            sweep_points = np.concatenate(
                [
                    np.repeat(nr_cliffords, 4 * len(interleaving_cliffords)),
                    nr_cliffords[-1] + np.arange(7) * 0.05 + 0.5,
                ]
            )  # cal pts

            p = cl_oql.character_benchmarking(
                qubits=qubit_idxs,
                nr_cliffords=nr_cliffords,
                nr_seeds=1,
                program_name="Char_RB_s{}_ncl{}_icl{}_{}_{}".format(
                    i,
                    list(map(int, nr_cliffords)),
                    interleaving_cliffords,
                    qubits[0],
                    qubits[1],
                ),
                flux_codeword=flux_codeword,
                platf_cfg=self.cfg_openql_platform_fn(),
                interleaving_cliffords=interleaving_cliffords,
                recompile=recompile,
            )

            p.sweep_points = sweep_points
            programs.append(p)
            print(
                "Generated {} Character benchmarking programs in {:>7.1f}s".format(
                    i + 1, time.time() - t0
                ),
                end="\r",
            )
        print(
            "Succesfully generated {} Character benchmarking programs in {:>7.1f}s".format(
                nr_seeds, time.time() - t0
            )
        )

        counter_param = ManualParameter("name_ctr", initial_value=0)
        prepare_function_kwargs = {
            "counter_param": counter_param,
            "programs": programs,
            "CC": self.instr_CC.get_instr(),
        }

        # Using the first detector of the multi-detector as this is
        # in charge of controlling the CC (see self.get_int_logging_detector)
        d.set_prepare_function(
            oqh.load_range_of_oql_programs, prepare_function_kwargs, detectors="first"
        )
        # d.nr_averages = 128

        reps_per_seed = 4094 // len(sweep_points)
        nr_shots = reps_per_seed * len(sweep_points)
        d.set_child_attr("nr_shots", nr_shots)

        s = swf.None_Sweep(parameter_name="Number of Cliffords", unit="#")

        MC.set_sweep_function(s)
        MC.set_sweep_points(np.tile(sweep_points, reps_per_seed * nr_seeds))

        MC.set_detector_function(d)
        MC.run(
            label.format(nr_seeds, interleaving_cliffords, qubits[0], qubits[1]),
            exp_metadata={"bins": sweep_points},
        )
        # N.B. if measurement was interrupted this wont work
        ma2.CharacterBenchmarking_TwoQubit_Analysis(ch_idxs=ch_idxs)


    def measure_two_qubit_simultaneous_randomized_benchmarking(
            self,
            qubits,
            MC: Optional[MeasurementControl] = None,
            nr_cliffords=2 ** np.arange(11),
            nr_seeds=100,
            interleaving_cliffords=[None],
            label="TwoQubit_sim_RB_{}seeds_recompile={}_{}_{}",
            recompile: bool = "as needed",
            cal_points: bool = True,
            ro_acq_weight_type: str = "optimal IQ",
            compile_only: bool = False,
            pool=None,  # a multiprocessing.Pool()
            rb_tasks=None  # used after called with `compile_only=True`
        ):
        """
        Performs simultaneous single qubit RB on two qubits.
        The data of this experiment should be compared to the results of single
        qubit RB to reveal differences due to crosstalk and residual coupling

        Args:
            qubits (list):
                pair of the qubit names on which to perform RB

            nr_cliffords (array):
                lengths of the clifford sequences to perform

            nr_seeds (int):
                number of different clifford sequences of each length

            interleaving_cliffords (list):
                list of integers (or None) which specifies which cliffords
                to interleave the sequence with (for interleaved RB)
                For indices of Clifford group elements go to
                two_qubit_clifford_group.py

            label (str):
                string for formatting the measurement name

            recompile (bool, str {'as needed'}):
                indicate whether to regenerate the sequences of clifford gates.
                By default it checks whether the needed sequences were already
                generated since the most recent change of OpenQL file
                specified in self.cfg_openql_platform_fn

            cal_points (bool):
                should calibration point (qubits in 0, 1 and 2 states)
                be included in the measurement
        """

        # Settings that have to be preserved, change is required for
        # 2-state readout and postprocessing
        old_weight_type = self.ro_acq_weight_type()
        old_digitized = self.ro_acq_digitized()
        self.ro_acq_weight_type(ro_acq_weight_type)
        self.ro_acq_digitized(False)

        self.prepare_for_timedomain(qubits=qubits)
        if MC is None:
            MC = self.instr_MC.get_instr()
        MC.soft_avg(1)

        # The detector needs to be defined before setting back parameters
        d = self.get_int_logging_detector(qubits=qubits)
        # set back the settings
        self.ro_acq_weight_type(old_weight_type)
        self.ro_acq_digitized(old_digitized)

        for q in qubits:
            q_instr = self.find_instrument(q)
            mw_lutman = q_instr.instr_LutMan_MW.get_instr()
            mw_lutman.load_ef_rabi_pulses_to_AWG_lookuptable()

        MC.soft_avg(1)

        def send_rb_tasks(pool_):
            tasks_inputs = []
            for i in range(nr_seeds):
                task_dict = dict(
                    qubits=[self.find_instrument(q).cfg_qubit_nr() for q in qubits],
                    nr_cliffords=nr_cliffords,
                    nr_seeds=1,
                    platf_cfg=self.cfg_openql_platform_fn(),
                    program_name="TwoQ_Sim_RB_int_cl{}_s{}_ncl{}_{}_{}_double".format(
                        i,
                        list(map(int, nr_cliffords)),
                        interleaving_cliffords,
                        qubits[0],
                        qubits[1],
                    ),
                    interleaving_cliffords=interleaving_cliffords,
                    simultaneous_single_qubit_RB=True,
                    cal_points=cal_points,
                    net_cliffords=[0, 3],  # measures with and without inverting
                    f_state_cal_pts=True,
                    recompile=recompile,
                )
                tasks_inputs.append(task_dict)
            # pool.starmap_async can be used for positional arguments
            # but we are using a wrapper
            rb_tasks = pool_.map_async(cl_oql.parallel_friendly_rb, tasks_inputs)

            return rb_tasks

        if compile_only:
            assert pool is not None
            rb_tasks = send_rb_tasks(pool)
            return rb_tasks

        if rb_tasks is None:
            # Using `with ...:` makes sure the other processes will be terminated
            # avoid starting too mane processes,
            # nr_processes = None will start as many as the PC can handle
            nr_processes = None if recompile else 1
            with multiprocessing.Pool(
                nr_processes,
                maxtasksperchild=cl_oql.maxtasksperchild  # avoid RAM issues
            ) as pool:
                rb_tasks = send_rb_tasks(pool)
                cl_oql.wait_for_rb_tasks(rb_tasks)

        programs_filenames = rb_tasks.get()

        # to include calibration points
        if cal_points:
            sweep_points = np.append(
                np.repeat(nr_cliffords, 2),
                [nr_cliffords[-1] + 0.5] * 2
                + [nr_cliffords[-1] + 1.5] * 2
                + [nr_cliffords[-1] + 2.5] * 3,
            )
        else:
            sweep_points = np.repeat(nr_cliffords, 2)

        counter_param = ManualParameter("name_ctr", initial_value=0)
        prepare_function_kwargs = {
            "counter_param": counter_param,
            "programs_filenames": programs_filenames,
            "CC": self.instr_CC.get_instr(),
        }

        # Using the first detector of the multi-detector as this is
        # in charge of controlling the CC (see self.get_int_logging_detector)
        d.set_prepare_function(
            oqh.load_range_of_oql_programs_from_filenames,
            prepare_function_kwargs, detectors="first"
        )
        # d.nr_averages = 128

        reps_per_seed = 4094 // len(sweep_points)
        d.set_child_attr("nr_shots", reps_per_seed * len(sweep_points))

        s = swf.None_Sweep(parameter_name="Number of Cliffords", unit="#")

        MC.set_sweep_function(s)
        MC.set_sweep_points(np.tile(sweep_points, reps_per_seed * nr_seeds))

        MC.set_detector_function(d)
        label = label.format(nr_seeds, recompile, qubits[0], qubits[1])
        MC.run(label, exp_metadata={"bins": sweep_points})

        # N.B. if interleaving cliffords are used, this won't work
        # [2020-07-11 Victor] not sure if NB still holds

        cal_2Q = ["00", "01", "10", "11", "02", "20", "22"]

        rates_I_quad_ch_idx = 0
        cal_1Q = [state[rates_I_quad_ch_idx // 2] for state in cal_2Q]
        a_q0 = ma2.RandomizedBenchmarking_SingleQubit_Analysis(
            label=label,
            rates_I_quad_ch_idx=rates_I_quad_ch_idx,
            cal_pnts_in_dset=cal_1Q
        )
        rates_I_quad_ch_idx = 2
        cal_1Q = [state[rates_I_quad_ch_idx // 2] for state in cal_2Q]
        a_q1 = ma2.RandomizedBenchmarking_SingleQubit_Analysis(
            label=label,
            rates_I_quad_ch_idx=rates_I_quad_ch_idx,
            cal_pnts_in_dset=cal_1Q
        )

        return a_q0, a_q1


    def measure_multi_qubit_simultaneous_randomized_benchmarking(
            self,
            qubits,
            MC: Optional[MeasurementControl] = None,
            nr_cliffords=2 ** np.arange(11),
            nr_seeds=100,
            recompile: bool = "as needed",
            cal_points: bool = True,
            ro_acq_weight_type: str = "optimal IQ",
            compile_only: bool = False,
            pool=None,  # a multiprocessing.Pool()
            rb_tasks=None,  # used after called with `compile_only=True
            label_name=None,
            prepare_for_timedomain=True
        ):
        """
        Performs simultaneous single qubit RB on multiple qubits.
        The data of this experiment should be compared to the results of single
        qubit RB to reveal differences due to crosstalk and residual coupling

        Args:
            qubits (list):
                list of the qubit names on which to perform RB

            nr_cliffords (array):
                lengths of the clifford sequences to perform

            nr_seeds (int):
                number of different clifford sequences of each length

            recompile (bool, str {'as needed'}):
                indicate whether to regenerate the sequences of clifford gates.
                By default it checks whether the needed sequences were already
                generated since the most recent change of OpenQL file
                specified in self.cfg_openql_platform_fn

            cal_points (bool):
                should calibration point (qubits in 0, 1 and 2 states)
                be included in the measurement
        """

        # Settings that have to be preserved, change is required for
        # 2-state readout and postprocessing
        old_weight_type = self.ro_acq_weight_type()
        old_digitized = self.ro_acq_digitized()
        self.ro_acq_weight_type(ro_acq_weight_type)
        self.ro_acq_digitized(False)

        if prepare_for_timedomain:
            self.prepare_for_timedomain(qubits=qubits, bypass_flux=True)
        if MC is None:
            MC = self.instr_MC.get_instr()
        MC.soft_avg(1)

        # The detector needs to be defined before setting back parameters
        d = self.get_int_logging_detector(qubits=qubits)
        # set back the settings
        self.ro_acq_weight_type(old_weight_type)
        self.ro_acq_digitized(old_digitized)

        for q in qubits:
            q_instr = self.find_instrument(q)
            mw_lutman = q_instr.instr_LutMan_MW.get_instr()
            mw_lutman.load_ef_rabi_pulses_to_AWG_lookuptable()

        MC.soft_avg(1)

        def send_rb_tasks(pool_):
            tasks_inputs = []
            for i in range(nr_seeds):
                task_dict = dict(
                    qubits=[self.find_instrument(q).cfg_qubit_nr() for q in qubits],
                    nr_cliffords=nr_cliffords,
                    nr_seeds=1,
                    platf_cfg=self.cfg_openql_platform_fn(),
                    program_name="MultiQ_RB_s{}_ncl{}_{}".format(
                        i,
                        list(map(int, nr_cliffords)),
                        '_'.join(qubits)
                    ),
                    interleaving_cliffords=[None],
                    simultaneous_single_qubit_RB=True,
                    cal_points=cal_points,
                    net_cliffords=[0, 3],  # measures with and without inverting
                    f_state_cal_pts=True,
                    recompile=recompile,
                )
                tasks_inputs.append(task_dict)
            # pool.starmap_async can be used for positional arguments
            # but we are using a wrapper
            rb_tasks = pool_.map_async(cl_oql.parallel_friendly_rb, tasks_inputs)
            return rb_tasks

        if compile_only:
            assert pool is not None
            rb_tasks = send_rb_tasks(pool)
            return rb_tasks

        if rb_tasks is None:
            # Using `with ...:` makes sure the other processes will be terminated
            # avoid starting too mane processes,
            # nr_processes = None will start as many as the PC can handle
            nr_processes = None if recompile else 1
            with multiprocessing.Pool(
                nr_processes,
                maxtasksperchild=cl_oql.maxtasksperchild  # avoid RAM issues
            ) as pool:
                rb_tasks = send_rb_tasks(pool)
                cl_oql.wait_for_rb_tasks(rb_tasks)

        programs_filenames = rb_tasks.get()

        # to include calibration points
        if cal_points:
            sweep_points = np.append(
                np.repeat(nr_cliffords, 2),
                [nr_cliffords[-1] + 0.5]
                + [nr_cliffords[-1] + 1.5]
                + [nr_cliffords[-1] + 2.5],
            )
        else:
            sweep_points = np.repeat(nr_cliffords, 2)

        counter_param = ManualParameter("name_ctr", initial_value=0)
        prepare_function_kwargs = {
            "counter_param": counter_param,
            "programs_filenames": programs_filenames,
            "CC": self.instr_CC.get_instr(),
        }

        # Using the first detector of the multi-detector as this is
        # in charge of controlling the CC (see self.get_int_logging_detector)
        d.set_prepare_function(
            oqh.load_range_of_oql_programs_from_filenames,
            prepare_function_kwargs, detectors="first"
        )
        # d.nr_averages = 128

        reps_per_seed = 4094 // len(sweep_points)
        d.set_child_attr("nr_shots", reps_per_seed * len(sweep_points))

        s = swf.None_Sweep(parameter_name="Number of Cliffords", unit="#")

        MC.set_sweep_function(s)
        MC.set_sweep_points(np.tile(sweep_points, reps_per_seed * nr_seeds))

        MC.set_detector_function(d)

        label="Multi_Qubit_sim_RB_{}seeds_recompile={}_".format(nr_seeds, recompile)
        if label_name is None:
            label += '_'.join(qubits)
        else:
            label += label_name
        MC.run(label, exp_metadata={"bins": sweep_points})

        cal_2Q = ["0"*len(qubits), "1"*len(qubits), "2"*len(qubits)]
        Analysis = []
        for i in range(len(qubits)):
            rates_I_quad_ch_idx = 2*i
            cal_1Q = [state[rates_I_quad_ch_idx // 2] for state in cal_2Q]
            a = ma2.RandomizedBenchmarking_SingleQubit_Analysis(
                label=label,
                rates_I_quad_ch_idx=rates_I_quad_ch_idx,
                cal_pnts_in_dset=cal_1Q
            )
            Analysis.append(a)

        return Analysis


    def measure_multi_rabi(
            self,
            qubits: list = None,
            prepare_for_timedomain=True,
            MC: Optional[MeasurementControl] = None,
            amps=np.linspace(0, 1, 31),
            calibrate=True
    ):
        if qubits is None:
            qubits = self.qubits()
        if prepare_for_timedomain:
            self.prepare_for_timedomain(qubits=qubits)

        qubits_idx = []
        for q in qubits:
            qub = self.find_instrument(q)
            qubits_idx.append(qub.cfg_qubit_nr())

        p = mqo.multi_qubit_rabi(qubits_idx=qubits_idx, platf_cfg=self.cfg_openql_platform_fn())

        self.instr_CC.get_instr().eqasm_program(p.filename)

        s = swf.mw_lutman_amp_sweep(qubits=qubits, device=self)

        d = self.get_int_avg_det(single_int_avg=True)

        if MC is None:
            MC = self.instr_MC.get_instr()

        MC.set_sweep_function(s)
        MC.set_sweep_points(amps)
        MC.set_detector_function(d)
        label = 'Multi_qubit_rabi_' + '_'.join(qubits)
        MC.run(name=label)
        a = ma2.Multi_Rabi_Analysis(qubits=qubits, label=label)
        if calibrate:
            b = a.proc_data_dict
            for q in qubits:
                pi_amp = b['quantities_of_interest'][q]['pi_amp']
                qub = self.find_instrument(q)
                qub.mw_channel_amp(pi_amp)
        return True


    def measure_multi_ramsey(
            self,
            qubits: list = None,
            times=None,
            GBT=True,
            artificial_periods: float = None,
            label=None,
            MC: Optional[MeasurementControl] = None,
            prepare_for_timedomain=True,
            update_T2=True,
            update_frequency=False
    ):
        if MC is None:
            MC = self.instr_MC.get_instr()

        if qubits is None:
            qubits = self.qubits()

        if prepare_for_timedomain:
            self.prepare_for_timedomain(qubits=qubits, bypass_flux=True)

        if artificial_periods is None:
            artificial_periods = 5

        if times is None:
            t = True
            times = []
        else:
            t = False

        qubits_idx = []
        for i, q in enumerate(qubits):
            qub = self.find_instrument(q)
            qubits_idx.append(qub.cfg_qubit_nr())
            stepsize = max((4 * qub.T2_star() / 61) // (abs(qub.cfg_cycle_time()))
                           * abs(qub.cfg_cycle_time()), 40e-9)
            if t is True:
                set_time = np.arange(0, stepsize * 64, stepsize)
                times.append(set_time)

            artificial_detuning = artificial_periods / times[i][-1]
            freq_qubit = qub.freq_qubit()
            mw_mod = qub.mw_freq_mod.get()
            freq_det = freq_qubit - mw_mod + artificial_detuning
            qub.instr_LO_mw.get_instr().set('frequency', freq_det)

        points = len(times[0])

        p = mqo.multi_qubit_ramsey(times=times, qubits_idx=qubits_idx,
                                   platf_cfg=self.cfg_openql_platform_fn())

        s = swf.OpenQL_Sweep(openql_program=p, CCL=self.instr_CC.get_instr())
        MC.set_sweep_function(s)
        MC.set_sweep_points(np.arange(points))
        d = self.get_int_avg_det()
        MC.set_detector_function(d)
        if label is None:
            label = 'Multi_Ramsey_' + '_'.join(qubits)
        MC.run(label)

        a = ma2.Multi_Ramsey_Analysis(qubits=qubits, times=times, artificial_detuning=artificial_detuning, label=label)
        qoi = a.proc_data_dict['quantities_of_interest']
        for q in qubits:
            qub = self.find_instrument(q)
            if update_T2:
                T2_star = qoi[q]['tau']
                qub.T2_star(T2_star)
            if update_frequency:
                new_freq = qoi[q]['freq_new']
                qub.freq_qubit(new_freq)
        if GBT:
            return True
        else:
            return a


    def measure_multi_AllXY(
            self,
            qubits: list = None,
            MC: Optional[MeasurementControl] = None,
            double_points=True,
            termination_opt=0.08
    ):
        # USED_BY: device_dependency_graphs_v2.py,

        if qubits is None:
            qubits = self.qubits()
        if MC is None:
            MC = self.instr_MC.get_instr()

        self.ro_acq_weight_type('optimal')
        self.prepare_for_timedomain(qubits=qubits, bypass_flux=True)

        qubits_idx = []
        for q in qubits:
            q_ob = self.find_instrument(q)
            q_nr = q_ob.cfg_qubit_nr()
            qubits_idx.append(q_nr)

        p = mqo.multi_qubit_AllXY(
            qubits_idx=qubits_idx,
            platf_cfg=self.cfg_openql_platform_fn(),
            double_points=double_points
        )

        s = swf.OpenQL_Sweep(openql_program=p, CCL=self.instr_CC.get_instr())
        MC.set_sweep_function(s)
        MC.set_sweep_points(np.arange(42))
        d = self.get_int_avg_det()
        MC.set_detector_function(d)
        MC.run('Multi_AllXY_'+'_'.join(qubits))

        a = ma2.Multi_AllXY_Analysis(qubits = qubits)

        dev = 0
        for Q in qubits:
            dev += a.proc_data_dict['deviation_{}'.format(Q)]
            if dev > len(qubits)*termination_opt:
                return False
            else:
                return True


    def measure_multi_T1(
            self,
            qubits: list = None,
            times=None,
            MC: Optional[MeasurementControl] = None,
            prepare_for_timedomain=True,
            analyze=True,
            update=True):

        if MC is None:
            MC = self.instr_MC.get_instr()

        if qubits is None:
            qubits = self.qubits()

        if prepare_for_timedomain:
            self.prepare_for_timedomain(qubits=qubits)

        qubits_idx = []
        set_times = []
        for q in qubits:
            qub = self.find_instrument(q)
            qubits_idx.append(qub.cfg_qubit_nr())
            stepsize = max((4 * qub.T1() / 31) // (abs(qub.cfg_cycle_time()))
                           * abs(qub.cfg_cycle_time()), 40e-9)
            set_time = np.arange(0, stepsize * 34, stepsize)
            set_times.append(set_time)

        if times is None:
            times = set_times

        points = len(times[0])

        p = mqo.multi_qubit_T1(
            times=times,
            qubits_idx=qubits_idx,
            platf_cfg=self.cfg_openql_platform_fn()
        )

        s = swf.OpenQL_Sweep(openql_program=p, CCL=self.instr_CC.get_instr())
        MC.set_sweep_function(s)
        MC.set_sweep_points(np.arange(points))
        d = self.get_int_avg_det()
        MC.set_detector_function(d)
        label = 'Multi_T1_' + '_'.join(qubits)
        MC.run(label)

        if analyze:
            a = ma2.Multi_T1_Analysis(qubits=qubits, times=times)
        if update:
            for q in qubits:
                qub = self.find_instrument(q)
                T1 = a.proc_data_dict['quantities_of_interest'][q]['tau']
                qub.T1(T1)

        return a


    def measure_multi_Echo(
            self,
            qubits: list = None,
            times=None,
            MC: Optional[MeasurementControl] = None,
            prepare_for_timedomain=True,
            analyze=True,
            update=True
    ):
        if MC is None:
            MC = self.instr_MC.get_instr()

        if qubits is None:
            qubits = self.qubits()

        if prepare_for_timedomain:
            self.prepare_for_timedomain(qubits=qubits)

        qubits_idx = []
        set_times = []
        for q in qubits:
            qub = self.find_instrument(q)
            qubits_idx.append(qub.cfg_qubit_nr())
            stepsize = max((2 * qub.T2_echo() / 61) // (abs(qub.cfg_cycle_time()))
                           * abs(qub.cfg_cycle_time()), 20e-9)
            set_time = np.arange(0, stepsize * 64, stepsize)
            set_times.append(set_time)

        if times is None:
            times = set_times

        points = len(times[0])

        p = mqo.multi_qubit_Echo(
            times=times,
            qubits_idx=qubits_idx,
            platf_cfg=self.cfg_openql_platform_fn())

        s = swf.OpenQL_Sweep(openql_program=p, CCL=self.instr_CC.get_instr())
        MC.set_sweep_function(s)
        MC.set_sweep_points(np.arange(points))
        d = self.get_int_avg_det()
        MC.set_detector_function(d)
        label = 'Multi_Echo_' + '_'.join(qubits)
        MC.run(label)

        if analyze:
            a = ma2.Multi_Echo_Analysis(label=label, qubits=qubits, times=times)
        if update:
            qoi = a.proc_data_dict['quantities_of_interest']
            for q in qubits:
                qub = self.find_instrument(q)
                T2_echo = qoi[q]['tau']
                qub.T2_echo(T2_echo)

        return True


    def measure_multi_flipping(
            self,
            qubits: list = None,
            number_of_flips: int = None,
            equator=True,
            ax='x',
            angle='180',
            MC: Optional[MeasurementControl] = None,
            prepare_for_timedomain=True,
            update=False,
            scale_factor_based_on_line: bool = False
    ):
        # allow flipping only with pi/2 or pi, and x or y pulses
        assert angle in ['90', '180']
        assert ax.lower() in ['x', 'y']

        if MC is None:
            MC = self.instr_MC.get_instr()

        if qubits is None:
            qubits = self.qubits()

        if prepare_for_timedomain:
            self.prepare_for_timedomain(qubits=qubits, bypass_flux=True)

        if number_of_flips is None:
            number_of_flips = 30
        nf = np.arange(0, (number_of_flips + 4) * 2, 2)

        qubits_idx = []
        for q in qubits:
            qub = self.find_instrument(q)
            qubits_idx.append(qub.cfg_qubit_nr())

        p = mqo.multi_qubit_flipping(
            number_of_flips=nf,
            qubits_idx=qubits_idx,
            platf_cfg=self.cfg_openql_platform_fn(),
            equator=equator,
            ax=ax,
            angle=angle
        )

        s = swf.OpenQL_Sweep(openql_program=p, unit='#', CCL=self.instr_CC.get_instr())
        MC.set_sweep_function(s)
        MC.set_sweep_points(nf)
        d = self.get_int_avg_det()
        MC.set_detector_function(d)
        label = 'Multi_flipping_' + '_'.join(qubits)
        MC.run(label)

        a = ma2.Multi_Flipping_Analysis(qubits=qubits, label=label)

        if update:
            for q in qubits:
                # Same as in single-qubit flipping:
                # Choose scale factor based on simple goodness-of-fit comparison,
                # unless it is forced by `scale_factor_based_on_line`
                # This method gives priority to the line fit:
                # the cos fit will only be chosen if its chi^2 relative to the
                # chi^2 of the line fit is at least 10% smaller
                # cos_chisqr = a.proc_data_dict['quantities_of_interest'][q]['cos_fit'].chisqr
                # line_chisqr = a.proc_data_dict['quantities_of_interest'][q]['line_fit'].chisqr

                # if scale_factor_based_on_line:
                #     scale_factor = a.proc_data_dict['quantities_of_interest'][q]['line_fit']['sf']
                # elif (line_chisqr - cos_chisqr)/line_chisqr > 0.1:
                #     scale_factor = a.proc_data_dict['quantities_of_interest'][q]['cos_fit']['sf']
                # else:
                #     scale_factor = a.proc_data_dict['quantities_of_interest'][q]['line_fit']['sf']

                if scale_factor_based_on_line:
                    scale_factor = a.proc_data_dict['quantities_of_interest'][q]['line_fit']['sf']
                else:
                    # choose scale factor preferred by analysis (currently based on BIC measure)
                    scale_factor = a.proc_data_dict['{}_scale_factor'.format(q)]

                if abs(scale_factor - 1) < 1e-3:
                    print(f'Qubit {q}: Pulse amplitude accurate within 0.1%. Amplitude not updated.')
                    return a

                qb = self.find_instrument(q)
                if angle == '180':
                    if qb.cfg_with_vsm():
                        amp_old = qb.mw_vsm_G_amp()
                        qb.mw_vsm_G_amp(scale_factor * amp_old)
                    else:
                        amp_old = qb.mw_channel_amp()
                        qb.mw_channel_amp(scale_factor * amp_old)
                elif angle == '90':
                    amp_old = qb.mw_amp90_scale()
                    qb.mw_amp90_scale(scale_factor * amp_old)

                print('Qubit {}: Pulse amplitude for {}-{} pulse changed from {:.3f} to {:.3f}'.format(
                    q, ax, angle, amp_old, scale_factor * amp_old))


    def measure_multi_motzoi(
            self,
            qubits: list = None,
            prepare_for_timedomain=True,
            MC: Optional[MeasurementControl] = None,
            amps=None,
            calibrate=True
    ):
        if qubits is None:
            qubits = self.qubits()
        if prepare_for_timedomain:
            self.prepare_for_timedomain(qubits=qubits)
        if amps is None:
            amps = np.linspace(-0.3, 0.3, 31)
        if MC is None:
            MC = self.instr_MC.get_instr()

        qubits_idx = []
        for q in qubits:
            qub = self.find_instrument(q)
            qubits_idx.append(qub.cfg_qubit_nr())

        p = mqo.multi_qubit_motzoi(qubits_idx=qubits_idx, platf_cfg=self.cfg_openql_platform_fn())

        self.instr_CC.get_instr().eqasm_program(p.filename)

        s = swf.motzoi_lutman_amp_sweep(qubits=qubits, device=self)
        d = self.get_int_avg_det(single_int_avg=True,
                                 values_per_point=2,
                                 values_per_point_suffex=['yX', 'xY'],
                                 always_prepare=True)
        MC.set_sweep_function(s)
        MC.set_sweep_points(amps)
        MC.set_detector_function(d)
        label = 'Multi_Motzoi_' + '_'.join(qubits)
        MC.run(name=label)

        a = ma2.Multi_Motzoi_Analysis(qubits=qubits, label=label)
        if calibrate:
            for q in qubits:
                qub = self.find_instrument(q)
                opt_motzoi = a.proc_data_dict['{}_intersect'.format(q)][0]
                qub.mw_motzoi(opt_motzoi)
            return True


    # FIXME commented out
    # def measure_ramsey_tomo(self,
    #                         qubit_ramsey: list,
    #                         qubit_control: list,
    #                         excited_spectators: list = [],
    #                         nr_shots_per_case: int = 2**10,
    #                         MC=None):
    #     '''
    #     Doc string

    #     '''

    #     qubitR = self.find_instrument(qubit_ramsey)
    #     qubitR_idx = qubitR.cfg_qubit_nr()
    #     if type(qubit_control) == list:
    #         qubitC = [self.find_instrument(q) for q in qubit_control]
    #         qubitC_idx = [q.cfg_qubit_nr() for q in qubitC]
    #     else:
    #         qubitC = self.find_instrument(qubit_control)
    #         qubitC_idx = qubitC.cfg_qubit_nr()

    #     # Get indices for spectator qubits
    #     qubitS = [self.find_instrument(q) for q in excited_spectators]
    #     qubitS_indcs = [q.cfg_qubit_nr() for q in qubitS]

    #     # Assert we have IQ readout
    #     assert self.ro_acq_weight_type() == 'optimal IQ', 'device not in "optimal IQ" mode'
    #     assert self.ro_acq_digitized() == False, 'RO should not be digitized'

    #     mw_lutman = qubitR.instr_LutMan_MW.get_instr()
    #     mw_lutman.load_ef_rabi_pulses_to_AWG_lookuptable()
    #     self.prepare_for_timedomain(qubits=[qubit_ramsey, qubit_control, *excited_spectators])

    #     p = mqo.Ramsey_tomo(qR= qubitR_idx,
    #                         qC= qubitC_idx,
    #                         exc_specs= qubitS_indcs,
    #                         platf_cfg=self.cfg_openql_platform_fn())

    #     s = swf.OpenQL_Sweep(openql_program=p,
    #                          CCL=self.instr_CC.get_instr())

    #     # d = self.get_int_log_det(qubits=[qubit_ramsey, qubit_control])
    #     d = self.get_int_logging_detector([qubit_ramsey, qubit_control],
    #                                       result_logging_mode='raw')
    #     d.detectors[0].nr_shots = 4096
    #     try:
    #         d.detectors[1].nr_shots = 4096
    #     except:
    #         pass

    #     nr_shots = int(16*256*2**4)
    #     if MC is None:
    #         MC = self.instr_MC.get_instr()
    #     MC.set_sweep_function(s)
    #     MC.set_sweep_points(np.arange(nr_shots))
    #     MC.set_detector_function(d)
    #     MC.run('Ramsey_tomo_R_{}_C_{}_S_{}'.format(qubit_ramsey, qubit_control, excited_spectators))
    #     # Analysis
    #     ma2.tqg.Two_qubit_gate_tomo_Analysis(label='Ramsey')


    def measure_ramsey_tomo(
            self,
            qubit_ramsey: list,
            qubit_control: list,
            excited_spectators: list = [],
            nr_shots_per_case: int = 2 ** 10,
            flux_codeword: str = 'cz',
            prepare_for_timedomain: bool = True,
            MC: Optional[MeasurementControl] = None
    ):
        '''
        Doc string

        '''

        qubitR = [self.find_instrument(qr) for qr in qubit_ramsey]
        qubitR_idxs = [qr.cfg_qubit_nr() for qr in qubitR]

        qubitC = [self.find_instrument(qc) for qc in qubit_control]
        qubitC_idxs = [qc.cfg_qubit_nr() for qc in qubitC]

        # Get indices for spectator qubits
        qubitS = [self.find_instrument(q) for q in excited_spectators]
        qubitS_idxs = [q.cfg_qubit_nr() for q in qubitS]

        # Assert we have IQ readout
        assert self.ro_acq_weight_type() == 'optimal IQ', 'device not in "optimal IQ" mode'
        assert self.ro_acq_digitized() == False, 'RO should not be digitized'

        for qr in qubitR:
            mw_lutman = qr.instr_LutMan_MW.get_instr()
            mw_lutman.load_ef_rabi_pulses_to_AWG_lookuptable()
        if prepare_for_timedomain:
            self.prepare_for_timedomain(qubits=[*excited_spectators], prepare_for_readout=False)
            self.prepare_for_timedomain(qubits=[*qubit_ramsey, *qubit_control])

        p = mqo.Ramsey_tomo(
            qR=qubitR_idxs,
            qC=qubitC_idxs,
            exc_specs=qubitS_idxs,
            flux_codeword=flux_codeword,
            platf_cfg=self.cfg_openql_platform_fn()
        )

        s = swf.OpenQL_Sweep(openql_program=p, CCL=self.instr_CC.get_instr())

        # d = self.get_int_log_det(qubits=[qubit_ramsey, qubit_control])
        d = self.get_int_logging_detector(
            qubits=[*qubit_ramsey, *qubit_control],
            result_logging_mode='raw'
        )
        d.detectors[0].nr_shots = 4096
        try:
            d.detectors[1].nr_shots = 4096
        except:
            pass
        try:
            d.detectors[2].nr_shots = 4096
        except:
            pass

        nr_shots = int(16 * 256 * 2 ** 4)
        if MC is None:
            MC = self.instr_MC.get_instr()
        MC.set_sweep_function(s)
        MC.set_sweep_points(np.arange(nr_shots))
        MC.set_detector_function(d)
        MC.run('Ramsey_tomo_R_{}_C_{}_S_{}'.format(qubit_ramsey, qubit_control, excited_spectators))

        # Analysis
        a = ma2.tqg.Two_qubit_gate_tomo_Analysis(label='Ramsey', n_pairs=len(qubit_ramsey))

        return a.qoi

    ##########################################################################
    # public functions: calibrate
    ##########################################################################

    def calibrate_optimal_weights_mux(
            self,
            qubits: list,
            q_target: str,
            update=True,
            verify=True,
            averages=2 ** 15,
            return_analysis=True
    ):
        # USED_BY: inspire_dependency_graph.py,
        """
        Measures the multiplexed readout transients of <qubits> for <q_target>
        in ground and excited state. After that, it calculates optimal
        integration weights that are used to weigh measuremet traces to maximize
        the SNR.

        Args:
            qubits (list):
                List of strings specifying qubits included in the multiplexed
                readout signal.

            q_target (str):
                ()

            verify (bool):
                indicates whether to run measure_ssro at the end of the routine
                to find the new SNR and readout fidelities with optimized weights

            update (bool):
                specifies whether to update the weights in the qubit object
        """
        if q_target not in qubits:
            raise ValueError("q_target must be included in qubits.")

        # Ensure that enough averages are used to get accurate weights
        old_avg = self.ro_acq_averages()
        self.ro_acq_averages(averages)

        Q_target = self.find_instrument(q_target)
        # Transient analysis
        A = self.measure_transients(
            qubits=qubits,
            q_target=q_target,
            cases=['on', 'off']
        )

        # resore parameters
        self.ro_acq_averages(old_avg)

        # Optimal weights
        B = ma2.Multiplexed_Weights_Analysis(
            q_target=q_target,
            IF=Q_target.ro_freq_mod(),
            pulse_duration=Q_target.ro_pulse_length(),
            A_ground=A[1],
            A_excited=A[0]
        )

        if update:
            Q_target.ro_acq_weight_func_I(B.qoi['W_I'])
            Q_target.ro_acq_weight_func_Q(B.qoi['W_Q'])
            Q_target.ro_acq_weight_type('optimal')

            if verify:
                Q_target._prep_ro_integration_weights()
                Q_target._prep_ro_instantiate_detectors()
                ssro_dict= self.measure_ssro_single_qubit(
                    qubits=qubits,
                    q_target=q_target
                )
            if return_analysis:
                return ssro_dict
            else:
                return True


    def calibrate_mux_ro(
        self,
        qubits,
        calibrate_optimal_weights=True,
        calibrate_threshold=True,
        # option should be here but is currently not implemented:
        # update_threshold: bool=True,
        mux_ro_label="Mux_SSRO",
        update_cross_talk_matrix: bool = False,
    ) -> bool:
        """
        Calibrates multiplexed Readout.

        Multiplexed readout is calibrated by
            - iterating over all qubits and calibrating optimal weights.
                This steps involves measuring the transients
                Measuring single qubit SSRO to determine the threshold and
                updating it.
            - Measuring multi qubit SSRO using the optimal weights.

        N.B. Currently only works for 2 qubits
        """

        q0 = self.find_instrument(qubits[0])
        q1 = self.find_instrument(qubits[1])

        q0idx = q0.cfg_qubit_nr()
        q1idx = q1.cfg_qubit_nr()

        UHFQC = q0.instr_acquisition.get_instr()
        self.ro_acq_weight_type("optimal")
        log.info("Setting ro acq weight type to Optimal")
        self.prepare_for_timedomain(qubits)

        if calibrate_optimal_weights:
            # Important that this happens before calibrating the weights
            # 10 is the number of channels in the UHFQC
            for i in range(9):
                UHFQC.set("qas_0_trans_offset_weightfunction_{}".format(i), 0)

            # This resets the crosstalk correction matrix
            UHFQC.upload_crosstalk_matrix(np.eye(10))

            for q_name in qubits:
                q = self.find_instrument(q_name)
                # The optimal weights are calibrated for each individual qubit
                # verify = True -> measure SSRO aftewards to determin the
                # acquisition threshold.
                if calibrate_optimal_weights:
                    q.calibrate_optimal_weights(analyze=True, verify=False, update=True)
                if calibrate_optimal_weights and not calibrate_threshold:
                    log.warning("Updated acq weights but not updating threshold")
                if calibrate_threshold:
                    q.measure_ssro(update=True, nr_shots_per_case=2 ** 13)

        self.measure_ssro_multi_qubit(
            qubits, label=mux_ro_label, result_logging_mode="lin_trans"
        )

        # if len (qubits)> 2:
        #     raise NotImplementedError

        # res_dict = mra.two_qubit_ssro_fidelity(
        #     label='{}_{}'.format(q0.name, q1.name),
        #     qubit_labels=[q0.name, q1.name])
        # V_offset_cor = res_dict['V_offset_cor']

        # N.B. no crosstalk parameters are assigned
        # # weights 0 and 1 are the correct indices because I set the numbering
        # # at the start of this calibration script.
        # UHFQC.qas_trans_offset_weightfunction_0(V_offset_cor[0])
        # UHFQC.qas_trans_offset_weightfunction_1(V_offset_cor[1])

        # # Does not work because axes are not normalized
        # matrix_normalized = res_dict['mu_matrix_inv']
        # matrix_rescaled = matrix_normalized/abs(matrix_normalized).max()
        # UHFQC.upload_transformation_matrix(matrix_rescaled)

        # a = self.check_mux_RO(update=update, update_threshold=update_threshold)
        return True


    def calibrate_cz_single_q_phase(
        self,
        q_osc: str,
        q_spec: str,
        amps,
        q2=None,
        q3=None,
        waveform="cz_NE",
        flux_codeword_park=None,
        update: bool = True,
        prepare_for_timedomain: bool = True,
        MC: Optional[MeasurementControl] = None,
    ):
        """
        Calibrate single qubit phase corrections of CZ pulse.

        Parameters
        ----------
        q_osc : str
            Name of the "oscillating" qubit. The phase correction of this
            qubit will be calibrated.
        q_spec: str
            Name of the "spectator" qubit. This qubit is used as the control.
        amps: array_like
            Amplitudes of the phase correction to measure.
        waveform: str
            Name of the waveform used on the "oscillating" qubit. This waveform
            will be reuploaded for each datapoint. Common names are "cz_z" and
            "idle_z"

        Returns
        -------
        succes: bool
            True if calibration succeeded, False if it failed.

        procedure works by performing a conditional oscillation experiment at
        a phase of 90 degrees. If the phase correction is correct, the "off" and
        "on" curves (control qubit in 0 and 1) should interesect. The
        analysis looks for the intersect.
        """

        if prepare_for_timedomain:
            self.prepare_for_timedomain(qubits=[q_osc, q_spec])
        if MC is None:
            MC = self.instr_MC.get_instr()

        which_gate = waveform[-2:]
        flux_codeword = waveform[:-3]

        q0idx = self.find_instrument(q_osc).cfg_qubit_nr()
        q1idx = self.find_instrument(q_spec).cfg_qubit_nr()
        if q2 is not None:
            q2idx = self.find_instrument(q2).cfg_qubit_nr()
            q3idx = self.find_instrument(q3).cfg_qubit_nr()
        else:
            q2idx = None
            q3idx = None
        fl_lutman_q0 = self.find_instrument(q_osc).instr_LutMan_Flux.get_instr()

        phase_par = fl_lutman_q0.parameters["cz_phase_corr_amp_{}".format(which_gate)]

        p = mqo.conditional_oscillation_seq(
            q0idx,
            q1idx,
            q2idx,
            q3idx,
            flux_codeword=flux_codeword,
            flux_codeword_park=flux_codeword_park,
            platf_cfg=self.cfg_openql_platform_fn(),
#            CZ_disabled=False,
            add_cal_points=False,
            angles=[90],
        )

        CC = self.instr_CC.get_instr()
        CC.eqasm_program(p.filename)
        CC.start()

        s = swf.FLsweep(fl_lutman_q0, phase_par, waveform)
        d = self.get_correlation_detector(
            qubits=[q_osc, q_spec], single_int_avg=True, seg_per_point=2
        )
        d.detector_control = "hard"

        MC.set_sweep_function(s)
        MC.set_sweep_points(np.repeat(amps, 2))
        MC.set_detector_function(d)
        MC.run("{}_CZphase".format(q_osc))

        # The correlation detector has q_osc on channel 0
        a = ma2.Intersect_Analysis(options_dict={"ch_idx_A": 0, "ch_idx_B": 0})

        phase_corr_amp = a.get_intersect()[0]
        if phase_corr_amp > np.max(amps) or phase_corr_amp < np.min(amps):
            print("Calibration failed, intersect outside of initial range")
            return False
        else:
            if update:
                phase_par(phase_corr_amp)
            return True


    def calibrate_phases(
            self,
            phase_offset_park: float = 0.003,
            skip_reverse: bool = False,
            phase_offset_sq: float = 0.05,
            do_park_cal: bool = True,
            do_sq_cal: bool = True,
            operation_pairs: list = [(['QNW', 'QC'], 'SE'), (['QNE', 'QC'], 'SW'),
                                     (['QC', 'QSW', 'QSE'], 'SW'), (['QC', 'QSE', 'QSW'], 'SE')]
    ):
        # USED_BY: inspire_dependency_graph.py,

        # First, fix parking phases
        # Set 'qubits': [q0.name, q1.name, q2.name] and 'parked_qubit_seq': 'ramsey'
        if do_park_cal:
            for operation_tuple in operation_pairs:
                pair, gate = operation_tuple
                if len(pair) != 3: continue

                check = self.measure_conditional_oscillation(q0=pair[0], q1=pair[1], q2=pair[2], parked_qubit_seq='ramsey')
                cur_val = check.proc_data_dict['quantities_of_interest']['park_phase_off'].nominal_value
                if abs(cur_val) < 3 or abs(360-cur_val) < 3:
                    continue

                q0 = self.find_instrument(pair[0]) # ramsey qubit (we make this be the fluxed one)
                q1 = self.find_instrument(pair[1]) # control qubit
                q2 = self.find_instrument(pair[2]) # parked qubit

                # cf.counter_param(0)
                flux_lm = q0.instr_LutMan_Flux.get_instr() # flux_lm of fluxed_qubit
                nested_mc = q0.instr_nested_MC.get_instr() # device object has no nested MC object, get from qubit object
                mc = self.instr_MC.get_instr()

                parked_seq = 'ramsey'
                conv_cost_det = det.Function_Detector( get_function=czcf.conventional_CZ_cost_func,
                        msmt_kw={'device': self, 'FL_LutMan_QR': flux_lm,
                            'MC': mc, 'waveform_name': 'cz_{}'.format(gate),
                            'qubits': [q0.name, q1.name, q2.name],
                            'parked_qubit_seq': parked_seq},
                        value_names=['Cost function value',
                            'Conditional phase', 'offset difference', 'missing fraction',
                            'Q0 phase', 'Park Phase OFF', 'Park Phase ON'],
                        result_keys=['cost_function_val',
                            'delta_phi', 'offset_difference', 'missing_fraction',
                            'single_qubit_phase_0', 'park_phase_off', 'park_phase_on'],
                        value_units=['a.u.', 'deg', '%', '%', 'deg', 'deg', 'deg'])

                park_flux_lm = q2.instr_LutMan_Flux.get_instr() # flux_lm of fluxed_qubit

                # 1D Scan of phase corrections after flux pulse
                value_min = park_flux_lm.park_amp() - phase_offset_park
                value_max = park_flux_lm.park_amp() + phase_offset_park
                sw = swf.joint_HDAWG_lutman_parameters(name='park_amp',
                                                    parameter_1=park_flux_lm.park_amp,
                                                    parameter_2=park_flux_lm.park_amp_minus,
                                                    AWG=park_flux_lm.AWG.get_instr(),
                                                    lutman=park_flux_lm)

                nested_mc.set_sweep_function(sw)
                nested_mc.set_sweep_points(np.linspace(value_min, value_max, 10))
                label = '1D_park_phase_corr_{}_{}_{}'.format(q0.name,q1.name,q2.name)
                nested_mc.set_detector_function(conv_cost_det)
                result = nested_mc.run(label)

                # Use ch_to_analyze as 5 for parking phase
                a_obj = ma2.Crossing_Analysis(label=label, ch_idx='Park Phase OFF', target_crossing=0)
                crossed_value = a_obj.proc_data_dict['root']
                park_flux_lm.park_amp(crossed_value)
                park_flux_lm.park_amp_minus(-crossed_value)

        # Then, fix single-qubit phases
        # Set 'qubits': [q0.name, q1.name] and 'parked_qubit_seq': 'ground'
        if do_sq_cal:
            for operation_tuple in operation_pairs:
                # For each qubit pair, calibrate both individually (requires inversion of arguments)
                for reverse in [False, True]:
                    if reverse and skip_reverse:
                        continue
                    pair, gate = operation_tuple
                    parked_seq = 'ground'

                    if reverse:
                        check = self.measure_conditional_oscillation(q0=pair[1], q1=pair[0])
                    else:
                        check = self.measure_conditional_oscillation(q0=pair[0], q1=pair[1])
                    cur_val = check.proc_data_dict['quantities_of_interest']['phi_0'].nominal_value
                    if abs(cur_val) < 3 or abs(360-cur_val) < 3:
                        continue

                    if reverse:
                        q0 = self.find_instrument(pair[1]) # ramsey qubit (we make this be the fluxed one)
                        q1 = self.find_instrument(pair[0]) # control qubit
                        if gate=='NE': gate='SW'
                        elif gate=='NW': gate = 'SE'
                        elif gate=='SW': gate = 'NE'
                        elif gate=='SE': gate = 'NW'
                    else:
                        q0 = self.find_instrument(pair[0]) # ramsey qubit (we make this be the fluxed one)
                        q1 = self.find_instrument(pair[1]) # control qubit
                        gate = gate

                    q2 = None
                    # cf.counter_param(0)
                    flux_lm = q0.instr_LutMan_Flux.get_instr() # flux_lm of fluxed_qubit
                    nested_mc = q0.instr_nested_MC.get_instr() # device object has no nested MC object, get from qubit object
                    mc = self.instr_MC.get_instr()

                    conv_cost_det = det.Function_Detector( get_function=czcf.conventional_CZ_cost_func,
                                    msmt_kw={'device': self, 'FL_LutMan_QR': flux_lm,
                                        'MC': mc,'waveform_name': 'cz_{}'.format(gate),
                                        'qubits': [q0.name, q1.name], 'parked_qubit_seq': parked_seq},
                                    value_names=['Cost function value',
                                        'Conditional phase', 'offset difference', 'missing fraction',
                                        'Q0 phase', 'Park Phase OFF', 'Park Phase ON'],
                                    result_keys=['cost_function_val',
                                        'delta_phi', 'offset_difference', 'missing_fraction',
                                        'single_qubit_phase_0', 'park_phase_off', 'park_phase_on'],
                                    value_units=['a.u.', 'deg', '%', '%', 'deg', 'deg', 'deg'])

                    # 1D Scan of phase corrections after flux pulse
                    #value_min = flux_lm.cz_phase_corr_amp_SW()-phase_offset
                    value_min = getattr(flux_lm, 'cz_phase_corr_amp_' + gate )()-phase_offset_sq
                    #value_max = flux_lm.cz_phase_corr_amp_SW()+phase_offset
                    value_max = getattr(flux_lm, 'cz_phase_corr_amp_' + gate )()+phase_offset_sq

                    label = 'CZ_1D_sweep_phase_corr_{}'.format(gate)
                    nested_mc.set_sweep_function(getattr(flux_lm, 'cz_phase_corr_amp_' + gate ))
                    nested_mc.set_sweep_points(np.linspace(value_min, value_max, 10))
                    nested_mc.set_detector_function(conv_cost_det)
                    result = nested_mc.run(label)

                    # Use ch_to_analyze as 4 for single qubit phases ('Q0 phase')
                    a_obj = ma2.Crossing_Analysis(label=label,
                                                ch_idx='Q0 phase',
                                                target_crossing=0)
                    crossed_value = a_obj.proc_data_dict['root']
                    getattr(flux_lm, 'cz_phase_corr_amp_' + gate )(crossed_value)
        return True


    def calibrate_cz_thetas(
            self,
            phase_offset: float = 1,
            operation_pairs: list = [(['QNW', 'QC'], 'SE'), (['QNE', 'QC'], 'SW'),
                                     (['QC', 'QSW', 'QSE'], 'SW'), (['QC', 'QSE', 'QSW'], 'SE')]
    ):
        # USED_BY: inspire_dependency_graph.py,

        # Set 'qubits': [q0.name, q1.name] and 'parked_qubit_seq': 'ground'
        for operation_tuple in operation_pairs:
            pair, gate = operation_tuple
            parked_seq = 'ground'

            check = self.measure_conditional_oscillation(q0=pair[0], q1=pair[1])
            if abs(180-check.proc_data_dict['quantities_of_interest']['phi_cond'].nominal_value)<2:
                continue

            q0 = self.find_instrument(pair[0]) # ramsey qubit (we make this be the fluxed one)
            q1 = self.find_instrument(pair[1]) # control qubit
            q2 = None
            gate = gate

            # cf.counter_param(0)
            flux_lm = q0.instr_LutMan_Flux.get_instr() # flux_lm of fluxed_qubit
            nested_mc = q0.instr_nested_MC.get_instr() # device object has no nested MC object, get from qubit object
            mc = self.instr_MC.get_instr()

            conv_cost_det = det.Function_Detector( get_function=czcf.conventional_CZ_cost_func,
                            msmt_kw={'device': self, 'FL_LutMan_QR': flux_lm,
                                'MC': mc,'waveform_name': 'cz_{}'.format(gate),
                                'qubits': [q0.name, q1.name], 'parked_qubit_seq': parked_seq},
                            value_names=['Cost function value',
                                'Conditional phase', 'offset difference', 'missing fraction',
                                'Q0 phase', 'Park Phase OFF', 'Park Phase ON'],
                            result_keys=['cost_function_val',
                                'delta_phi', 'offset_difference', 'missing_fraction',
                                'single_qubit_phase_0', 'park_phase_off', 'park_phase_on'],
                            value_units=['a.u.', 'deg', '%', '%', 'deg', 'deg', 'deg'])

            # 1D Scan of phase corrections after flux pulse
            value_min = getattr(flux_lm, 'cz_theta_f_' + gate )()-phase_offset
            #value_max = flux_lm.cz_phase_corr_amp_SW()+phase_offset
            value_max = getattr(flux_lm, 'cz_theta_f_' + gate )()+phase_offset

            label = 'CZ_1D_sweep_theta_{}'.format(gate)
            nested_mc.set_sweep_function(getattr(flux_lm, 'cz_theta_f_' + gate ))
            nested_mc.set_sweep_points(np.linspace(value_min, value_max, 10))
            nested_mc.set_detector_function(conv_cost_det)
            result = nested_mc.run(label)

            # Use ch_to_analyze as 4 for single qubit phases ('Q0 phase')
            a_obj = ma2.Crossing_Analysis(label=label,
                                          ch_idx='Conditional phase',
                                          target_crossing=180)
            crossed_value = a_obj.proc_data_dict['root']
            getattr(flux_lm, 'cz_theta_f_' + gate )(crossed_value)

        return True


    def calibrate_multi_frequency_fine(
            self,
            qubits: list = None,
            times=None,
            artificial_periods: float = None,
            MC: Optional[MeasurementControl] = None,
            prepare_for_timedomain=True,
            update_T2=False,
            update_frequency=True,
            stepsize: float = None,
            termination_opt=0,
            steps=[1, 1, 3, 10, 30, 100, 300, 1000]
    ):
        if qubits is None:
            qubits = self.qubits()
        if artificial_periods is None:
            artificial_periods = 2.5
        if stepsize is None:
            stepsize = 20e-9
        for n in steps:
            times = []
            for q in qubits:
                qub = self.find_instrument(q)
                time = np.arange(0, 50 * n * stepsize, n * stepsize)
                times.append(time)

            label = 'Multi_Ramsey_{}_pulse_sep_'.format(n) + '_'.join(qubits)

            a = self.measure_multi_ramsey(
                qubits=qubits,
                times=times,
                MC=MC,
                GBT=False,
                artificial_periods=artificial_periods,
                label=label,
                prepare_for_timedomain=prepare_for_timedomain,
                update_frequency=False,
                update_T2=update_T2
            )
            for q in qubits:
                qub = self.find_instrument(q)
                freq = a.proc_data_dict['quantities_of_interest'][q]['freq_new']
                T2 = a.proc_data_dict['quantities_of_interest'][q]['tau']
                fit_error = a.proc_data_dict['{}_fit_res'.format(q)].chisqr

                if (times[0][-1] < 2. * T2) and (update_frequency is True):
                    # If the last step is > T2* then the next will be for sure
                    qub.freq_qubit(freq)

            T2_max = max(a.proc_data_dict['quantities_of_interest'][q]['tau'] for q in qubits)
            if times[0][-1] > 2. * T2_max:
                # If the last step is > T2* then the next will be for sure

                print('Breaking of measurement because of T2*')
                break

        return True

    ########################################################
    # other methods
    ########################################################

    def create_dep_graph(self):
        dags = []
        for qi in self.qubits():
            q_obj = self.find_instrument(qi)
            if hasattr(q_obj, "_dag"):
                dag = q_obj._dag
            else:
                dag = q_obj.create_dep_graph()
            dags.append(dag)

        dag = nx.compose_all(dags)

        dag.add_node(self.name + " multiplexed readout")
        dag.add_node(self.name + " resonator frequencies coarse")
        dag.add_node("AWG8 MW-staircase")
        dag.add_node("AWG8 Flux-staircase")

        # Timing of channels can be done independent of the qubits
        # it is on a per frequency per feedline basis so not qubit specific
        dag.add_node(self.name + " mw-ro timing")
        dag.add_edge(self.name + " mw-ro timing", "AWG8 MW-staircase")

        dag.add_node(self.name + " mw-vsm timing")
        dag.add_edge(self.name + " mw-vsm timing", self.name + " mw-ro timing")

        for edge_L, edge_R in self.qubit_edges():
            dag.add_node("Chevron {}-{}".format(edge_L, edge_R))
            dag.add_node("CZ {}-{}".format(edge_L, edge_R))

            dag.add_edge(
                "CZ {}-{}".format(edge_L, edge_R),
                "Chevron {}-{}".format(edge_L, edge_R),
            )
            dag.add_edge(
                "CZ {}-{}".format(edge_L, edge_R), "{} cryo dist. corr.".format(edge_L)
            )
            dag.add_edge(
                "CZ {}-{}".format(edge_L, edge_R), "{} cryo dist. corr.".format(edge_R)
            )

            dag.add_edge(
                "Chevron {}-{}".format(edge_L, edge_R),
                "{} single qubit gates fine".format(edge_L),
            )
            dag.add_edge(
                "Chevron {}-{}".format(edge_L, edge_R),
                "{} single qubit gates fine".format(edge_R),
            )
            dag.add_edge("Chevron {}-{}".format(edge_L, edge_R), "AWG8 Flux-staircase")
            dag.add_edge(
                "Chevron {}-{}".format(edge_L, edge_R),
                self.name + " multiplexed readout",
            )

            dag.add_node("{}-{} mw-flux timing".format(edge_L, edge_R))

            dag.add_edge(
                edge_L + " cryo dist. corr.",
                "{}-{} mw-flux timing".format(edge_L, edge_R),
            )
            dag.add_edge(
                edge_R + " cryo dist. corr.",
                "{}-{} mw-flux timing".format(edge_L, edge_R),
            )

            dag.add_edge(
                "Chevron {}-{}".format(edge_L, edge_R),
                "{}-{} mw-flux timing".format(edge_L, edge_R),
            )
            dag.add_edge(
                "{}-{} mw-flux timing".format(edge_L, edge_R), "AWG8 Flux-staircase"
            )

            dag.add_edge(
                "{}-{} mw-flux timing".format(edge_L, edge_R),
                self.name + " mw-ro timing",
            )

        for qubit in self.qubits():
            dag.add_edge(qubit + " ro pulse-acq window timing", "AWG8 MW-staircase")

            dag.add_edge(qubit + " room temp. dist. corr.", "AWG8 Flux-staircase")
            dag.add_edge(self.name + " multiplexed readout", qubit + " optimal weights")

            dag.add_edge(
                qubit + " resonator frequency",
                self.name + " resonator frequencies coarse",
            )
            dag.add_edge(qubit + " pulse amplitude coarse", "AWG8 MW-staircase")

        for qi in self.qubits():
            q_obj = self.find_instrument(qi)
            # ensures all references are to the main dag
            q_obj._dag = dag

        self._dag = dag
        return dag

    def calibrate_parity_model_phases(
            self,
            parity_check: List[List[str]],
            B_sweep_range_frac: float = 0.2,
            B_sweep_n_points: int = 2,
            refocusing: bool = False,
            ramsey_qubits: List[str] = None,
            flux_codeword: str = 'repetition-code',
            flux_dance_steps: List[int] = [1,2],
            update: bool = True,
            prepare_for_timedomain: bool = True,
            plot_each_msmt: bool = False,
            MC = None
        ) -> dict:
        """
        Measures parity check as part of a flux dance for `B_sweep_points` different
        SNZ B values for each gate defined in `parity_check`.
        Runs parity check model optimization analysis, which fits 
        a linear dependence of the parity check model phase error given 
        the measured error of each B value, to determine the B value required 
        to achieve an error of zero.

        Args:
            parity_check: 
                List of qubits and gate directions which define the flux_lutmans to be used.
                Parking qubits are not used for this routine, and can be replaced with an empty list.
                Assumed format: [ [[ancilla_qubit]], [[data_qubit]], [[gate_direction]], [[parking_qubits]] ]
                Example:        [   [['Z4']]*4, \
                                    [['D9'],['D6'],['D8'],['D5']], \
                                    [['NE'],['NW'],['NW'],['NE']], \
                                    [['D8'],['X2','Z2'],['D8'],['X3','X2']] ]
        Returns:
            optimal B values per gate of `parity_check`
        """
        if MC is None:
            MC = self.instr_MC.get_instr()

        # here we need to measure all data qubits, since we are intereseted in the model phases
        # of all qubits and not just the one we sweeep
        control_qubits_all = np.asarray(parity_check[1]).flatten().tolist()
        results = OrderedDict().fromkeys(control_qubits_all)

        for target_qubit, control_qubit, gate_direction, _ in list(zip(*parity_check)):

            # if the pair has a high frequency qubit, we need to select its lutman instead of the ancilla's
            if control_qubit[0] in ['D4','D5','D6']:
                flux_lm = self.find_instrument(f"flux_lm_{control_qubit[0]}")
            else:
                flux_lm = self.find_instrument(f"flux_lm_{target_qubit[0]}")
        
            old_B = flux_lm.parameters[f"vcz_amp_fine_{gate_direction[0]}"]()
            sweep_points = a_tools.get_values_around(old_B, range_frac=B_sweep_range_frac, num_points=B_sweep_n_points)

            log.info(f"Parity check B sweep: {target_qubit} - {control_qubit} - {gate_direction}")
            log.info(f"Control qubits in sweep order: {control_qubits_all}")
            log.info(f"Ramsey qubits: {ramsey_qubits}")
            log.info(f"Flux codeword: {flux_codeword}, flux dance steps: {flux_dance_steps}")
            log.info(f"B sweep: {flux_lm.name}-{gate_direction}, around {old_B}, values: {sweep_points}")

            old_digitized = self.ro_acq_digitized()
            old_weight_type = self.ro_acq_weight_type()
            self.ro_acq_digitized(False)
            self.ro_acq_weight_type('optimal')
            
            all_qubits = target_qubit + control_qubits_all
            if prepare_for_timedomain:
                # Take care of readout order (by feedline/UHF)
                if self.qubits_by_feedline():
                    all_qubits = sorted(all_qubits, 
                                    key=lambda x: [i for i, feedline in enumerate(self.qubits_by_feedline()) \
                                                    if x in feedline])
                    log.info(f"Sorted qubits for readout preparation: {all_qubits}")
                else:
                    log.warning("Qubit order by feedline in `self.qubits_by_feedline()` parameter is not set, "
                                + "readout will be prepared in order of given qubits which can lead to errors!")

                self.prepare_for_timedomain(qubits=all_qubits)

            # generate model terms to use for labels
            controls_qubits_sorted = [qb for qb in all_qubits if qb != target_qubit[0]]
            control_combinations = [elem for k in range(1, len(controls_qubits_sorted)+1) 
                                            for elem in itt.combinations(controls_qubits_sorted, k)]
            model_terms = [target_qubit[0]]
            model_terms += [ target_qubit[0] + ',' + qbs 
                            for qbs in [','.join(comb) for comb in control_combinations] ]

            d = det.Function_Detector(
                get_function=self.measure_parity_check_flux_dance,
                msmt_kw={'target_qubits': target_qubit,
                        'control_qubits': controls_qubits_sorted,
                        'ramsey_qubits': ramsey_qubits,
                        'flux_dance_steps': flux_dance_steps,
                        'flux_codeword': flux_codeword,
                        'refocusing': False,
                        'prepare_for_timedomain': False,
                        'plotting': plot_each_msmt,
                        'MC': self.instr_nested_MC.get_instr()
                        },
                value_names=[f'model_error_{term}' for term in model_terms],
                result_keys=[f'model_error_{term}' for term in model_terms],
                value_units=['deg'] * len(model_terms)
                )

            s = swf.FLsweep(
                lm=flux_lm, 
                par=flux_lm.parameters[f"vcz_amp_fine_{gate_direction[0]}"],
                waveform_name=f"cz_{gate_direction[0]}",
                upload_waveforms_always=True
                )

            MC.set_detector_function(d)
            MC.set_sweep_function(s)
            MC.set_sweep_points(sweep_points)
            label = f"Parity_model_optimization_{target_qubit}-{control_qubit}-{gate_direction}_Bpoints-{B_sweep_n_points}_Brange-{B_sweep_range_frac}"

            try:
                MC.run(label,
                    exp_metadata={
                        'target_qubit': target_qubit,
                        'control_qubits': controls_qubits_sorted,
                        'sweep_qubit': control_qubit,
                        'sweep_points': sweep_points,
                        'old_B_value': [old_B],
                        'model_terms': model_terms,
                    })
            except Exception as e:
                log.warning("\nMeasurement interrupted! Resetting old B value.\n")
                flux_lm.parameters[f"vcz_amp_fine_{gate_direction[0]}"](old_B)
                print(repr(e))
                print(e.__traceback__)
                log.error(logging.traceback.format_exc())
            
            # reset B!
            flux_lm.parameters[f"vcz_amp_fine_{gate_direction[0]}"](old_B)

            a = ma2.Parity_Model_Optimization_Analysis(label=label)
            new_B = a.proc_data_dict['quantities_of_interest']['optimal_B_value']
            rel_B_change = a.proc_data_dict['quantities_of_interest']['relative_B_change']

            if update:
                if 0 <= new_B <= 1:
                    log.info(f"Changing B of {flux_lm.name} for direction {gate_direction[0]} from {old_B} to {new_B.n}.")
                    log.info(f"Relative change in B is {rel_B_change} %.")
                    flux_lm.parameters[f"vcz_amp_fine_{gate_direction[0]}"](new_B.n)
                else:
                    log.warning(f"Optimal B value {new_B} outside of range (0,1)! Value left unchanged.")

            results[control_qubit[0]] = {'a': a, 'new_B': new_B, 'rel_B_change': rel_B_change}

        self.ro_acq_digitized(old_digitized)
        self.ro_acq_weight_type(old_weight_type)

        return results


    def calibrate_snz_fine_landscape(
            self,
            pair: List[str],
            gate_direction: str,
            ramsey_qubits: Union[bool, List[str]] = False,
            parked_qubits: List[str]=None,
            horizontal_calibration: bool = False,
            flux_codeword: str = 'flux-dance',
            flux_dance_steps: List[int] = [1],
            adaptive_sampling_pts: int = 60,
            adaptive_A_bounds: Tuple[float] = (0.97, 1.03),
            adaptive_volume_weight: float = 20,
            adaptive_target_cost: float = 0.01,
            measure_result: bool = True,
            update: bool = True,
            prepare_for_timedomain: bool = True,
            MC = None,
        ) -> dict:
        """
        Calibrates A and B parameters of SNZ gate(s) between pair(s) given in `pair`
        by sampling the cost function landscaping adaptively.
        Works in two modes:
            horizontal_calibration == False:
                Vertical calibration mode, individual SNZ gate will be optimized.
                `flux_codeword` can be a composite codeword for a flux dance step.
                Supports parallel optimization of gate in a flux dance step.
            horizontal_calibration == True:
                Horizontal calibration mode, parity check will be optimized while whole flux dance
                specified by `flux_codeword` and `flux_dance_steps` is played.
        
        Args:

        Raises:
            ValueError: If amount of gates specified by `pair` and `gate_directions`
                does not match what is expected given the mode (`horizontal_calibration`).

        Returns:
            Optimal point (A,B) of SNZ between `pair`
        """
        if type(pair) != list or type(pair[0]) != str:
            raise ValueError(f"`pair` always must be given as simple list of target and control qubit names!")
        if MC is None:
            MC = self.instr_MC.get_instr()

        old_digitized = self.ro_acq_digitized()
        old_weight_type = self.ro_acq_weight_type()
        self.ro_acq_digitized(False)
        self.ro_acq_weight_type('optimal')

        # reset cost function counter to keep track of a new optimization run
        cf.counter_param(0)
        if horizontal_calibration:
            self.prepare_for_timedomain(qubits=pair)
            cost_det = det.Function_Detector(
                get_function=cf.parity_check_cost_function,
                msmt_kw={'device': self,
                        'MC': self.instr_nested_MC.get_instr(),
                        'target_qubits': [pair[0]],
                        'control_qubits': [pair[1]],
                        'ramsey_qubits': ramsey_qubits,
                        'flux_codeword': flux_codeword,
                        'flux_dance_steps': flux_dance_steps,
                        'phase_weight_factor': 0.5,
                        'include_missing_frac_cost': True,
                        'prepare_for_timedomain': False,
                        'disable_metadata': True,
                        'plotting': False,
                        'analyze_parity_model': False},
                value_names=['cost_function_val', 'phi_diff', f'missing_frac_{pair[1]}'],
                result_keys=['cost_function_val', 'phi_diff', f'missing_frac_{pair[1]}'],
                value_units=['a.u.', 'deg', '%']
                )
        else:
            self.prepare_for_timedomain(qubits=np.asarray(pair).flatten().tolist())
            cost_det = det.Function_Detector(
                get_function=cf.conventional_CZ_cost_func2,
                msmt_kw={'device': self,
                       'MC': self.instr_nested_MC.get_instr(),
                       'pairs': [pair],
                       'parked_qbs': parked_qubits,
                       'flux_codeword': flux_codeword + '_' + str(flux_dance_steps[0]),
                       'parked_qubit_seq': 'ground',
                       'include_single_qubit_phase_in_cost': False,
                       'target_single_qubit_phase': 360,
                       'include_leakage_in_cost': True,
                       'target_phase': 180,
                       'cond_phase_weight_factor': 0.5,
                       'prepare_for_timedomain': False,
                       'extract_only': True,
                       'disable_metadata': True},
                       # TODO adapt for nested lists
                value_names=[f'cost_function_val_{pair}', 
                            f'delta_phi_{pair}', 
                            f'missing_fraction_{pair}'],
                result_keys=[f'cost_function_val_{pair}',
                            f'delta_phi_{pair}',
                            f'missing_fraction_{pair}'],
                value_units=['a.u.', 'deg', '%']
                )


        # if the pair has a high frequency data qubit, we need to select its lutman
        # NOTE: here we assume no pairs between two data qubits are possible (S17 architecture)
        # qb = [qb for qb in pair if 'D' in qb]
        # if qb and qb[0] in ['D4','D5','D6']:
        if pair[0] in ['D4','D5','D6']:
            flux_lm = self.find_instrument(f"flux_lm_{pair[0]}")
        else:
            flux_lm = self.find_instrument(f"flux_lm_{pair[1]}")

        # TODO: bypass waveform upload in sweep functions to save time by avoiding 
        #       repeated upload of the same parameters.
        #       Waveforms can be updated and uploaded only in the detector function
        #       which should be enough since the detector function is called by the MC 
        #       only after new sweep function values are set.
        #       But somehow this was not working during an initial test.
        sweep_function_1 = swf.FLsweep(lm=flux_lm, 
                                        par=flux_lm.parameters[f"vcz_amp_sq_{gate_direction}"],
                                        waveform_name=f"cz_{gate_direction}",
                                        # bypass_waveform_upload=True,
                                        upload_waveforms_always=True) 
        sweep_function_2 = swf.FLsweep(lm=flux_lm, 
                                        par=flux_lm.parameters[f"vcz_amp_fine_{gate_direction}"],
                                        waveform_name=f"cz_{gate_direction}",
                                        # bypass_waveform_upload=True,
                                        upload_waveforms_always=True)

        log.info(f"SNZ fine landscape adaptive optimization: {pair}, {flux_lm}, {gate_direction}")
        log.info(f"Flux codeword: {flux_codeword}, flux dance steps: {flux_dance_steps}")

        if adaptive_target_cost is not None:
            # target cost value can be computed by: 
            # target_cost = cf.parity_check_cost(
            #     phase_diff=185, 
            #     phase_weight=0.5, 
            #     missing_fraction=0.02)
            # convergence threshold strangely has to be given in loss function, not here
            goal = lndm.mk_min_threshold_goal_func(max_pnts_beyond_threshold=2) 
        else:
            goal = lndm.mk_minimization_goal_func()
        
        loss = lndm.mk_minimization_loss_func(
            max_no_improve_in_local=6,
            converge_below=adaptive_target_cost,
            volume_weight=adaptive_volume_weight
            )

        fine_B_amp_bounds = (0.0,  1.0)
        num_init_points = 10
        X0 = np.array([np.ones(num_init_points),
                        np.linspace(*fine_B_amp_bounds[::-1], num_init_points+2)[1:-1]
                        ]).T

        adaptive_pars = {'adaptive_function': lndm.LearnerND_Minimizer,
                        'goal': lambda l: goal(l) or l.npoints >= adaptive_sampling_pts,
                        'bounds': [np.array(adaptive_A_bounds), np.array(fine_B_amp_bounds)],
                        'loss_per_simplex': loss,
                        'minimize': True,
                        'X0': X0
                        }

        MC.cfg_clipping_mode(True)
        MC.set_detector_function(cost_det)
        MC.set_sweep_functions([sweep_function_1, sweep_function_2])
        MC.set_adaptive_function_parameters(adaptive_pars)
        label = f'SNZ_fine_landscape_{pair}_horizontal-{horizontal_calibration}_{flux_codeword}'

        # save initial gate parameters to restore in case of failure
        old_A = flux_lm.parameters[f'vcz_amp_sq_{gate_direction}']()
        old_B = flux_lm.parameters[f'vcz_amp_fine_{gate_direction}']()

        try:
            result = MC.run(label, mode='adaptive')
            log.info(f"Optimization result: {result['opt_res']}")
            log.info(f"A = {flux_lm.parameters[f'vcz_amp_sq_{gate_direction}']()},"
                    f"B = {flux_lm.parameters[f'vcz_amp_fine_{gate_direction}']()}")
            
            if update:
                if horizontal_calibration:
                    # Heatmap analysis currently doesn't work for msmt format of horizontal calibration
                    # apply optimal parameters:
                    flux_lm.parameters[f"vcz_amp_sq_{gate_direction}"](result['opt_res']['xopt'][0])
                    flux_lm.parameters[f"vcz_amp_fine_{gate_direction}"](result['opt_res']['xopt'][1])
                else:
                    a = ma2.Conditional_Oscillation_Heatmap_Analysis(
                        label=label,
                        for_multi_CZ=True,
                        pair={'pair_name': pair, 'sweep_ratio': [1,1], 'pair_num': 0},
                        close_figs=True,
                        extract_only=False,
                        plt_orig_pnts=True,
                        plt_contour_L1=False,
                        plt_contour_phase=True,
                        plt_optimal_values=True,
                        plt_optimal_values_max=1,
                        find_local_optimals=True,
                        plt_clusters=False,
                        cluster_from_interp=False,
                        clims={"Cost func": [0, 300],
                                "missing fraction": [0, 30],
                                "offset difference": [0, 30]},
                        target_cond_phase=180,
                        phase_thr=20,
                        L1_thr=10,
                        clustering_thr=0.1,
                        gen_optima_hulls=True,
                        hull_L1_thr=5,
                        hull_phase_thr=20,
                        plt_optimal_hulls=True,
                        save_cond_phase_contours=[180])
                    # apply optimal params from point with smallest missing fraction:
                    opt_point = np.argmin([x['missing fraction'] for x in a.proc_data_dict['optimal_measured_values']])
                    flux_lm.parameters[f'vcz_amp_sq_{gate_direction}'](a.proc_data_dict['optimal_pars_values'][opt_point]['relative_sq_amp'])
                    flux_lm.parameters[f'vcz_amp_fine_{gate_direction}'](a.proc_data_dict['optimal_pars_values'][opt_point]['fine_amp'])

                log.info(f"Gate parameters updated to:"
                        f"A = {flux_lm.parameters[f'vcz_amp_sq_{gate_direction}']()},"
                        f"B = {flux_lm.parameters[f'vcz_amp_fine_{gate_direction}']()}.")
                flux_lm.load_waveforms_onto_AWG_lookuptable(regenerate_waveforms=True)

            if measure_result:
                # measure optimized parity check for reference
                self.measure_parity_check_flux_dance(
                    target_qubits=[pair[0]],
                    control_qubits=[pair[1]],
                    ramsey_qubits=ramsey_qubits, 
                    flux_dance_steps=flux_dance_steps,
                    flux_codeword=flux_codeword,
                    prepare_for_timedomain=True,
                    plotting=True,
                    analyze_parity_model=False
                    )

            return result

        except Exception as e:
            log.warning(f"Measurement for {pair} interrupted! Resetting old values.")
            flux_lm.parameters[f'vcz_amp_sq_{gate_direction}'](old_A)
            flux_lm.parameters[f'vcz_amp_fine_{gate_direction}'](old_B)
            print(repr(e))
            print(e.__traceback__)
            log.error(logging.traceback.format_exc())

    def measure_vcz_A_B_landscape(
        self, 
        Q0,
        Q1,
        A_ranges,
        A_points: int,
        B_amps: list,
        Q_parks: list = None,
        flux_codeword: str = 'cz'):
        """
        Perform 2D sweep of amplitude and wave parameter while measuring 
        conditional phase and missing fraction via the "conditional 
        oscillation" experiment.

        Q0 : High frequency qubit(s). Can be given as single qubit or list.
        Q1 : Low frequency qubit(s). Can be given as single qubit or list.
        T_mids : list of vcz "T_mid" values to sweep.
        A_ranges : list of tuples containing ranges of amplitude sweep.
        A_points : Number of points to sweep for amplitude range.
        Q_parks : list of qubits parked during operation.
        """
        if isinstance(Q0, str):
            Q0 = [Q0]
        if isinstance(Q1, str):
            Q1 = [Q1]
        assert len(Q0) == len(Q1)

        MC = self.instr_MC.get_instr()
        nested_MC = self.instr_nested_MC.get_instr()
        # get gate directions
        directions = [get_gate_directions(q0, q1) for q0, q1 in zip(Q0, Q1)]
        
        # Time-domain preparation
        # Prepare for time domain
        self.prepare_for_timedomain(
            qubits=np.array([[Q0[i],Q1[i]] for i in range(len(Q0))]).flatten(),
            bypass_flux=True)
        Flux_lm_0 = [self.find_instrument(q0).instr_LutMan_Flux.get_instr() for q0 in Q0]
        Flux_lm_1 = [self.find_instrument(q1).instr_LutMan_Flux.get_instr() for q1 in Q1]
        Flux_lms_park = [self.find_instrument(q).instr_LutMan_Flux.get_instr() for q in Q_parks]
        for i, lm in enumerate(Flux_lm_0):
            print(f'Setting {Q0[i]} vcz_amp_sq_{directions[i][0]} to 1')
            print(f'Setting {Q0[i]} vcz_amp_dac_at_11_02_{directions[i][0]} to 0.5')
            lm.set(f'vcz_amp_sq_{directions[i][0]}', 1)
            lm.set(f'vcz_amp_dac_at_11_02_{directions[i][0]}', .5)
        for i, lm in enumerate(Flux_lm_1):
            print(f'Setting {Q1[i]} vcz_amp_dac_at_11_02_{directions[i][1]} to 0')
            lm.set(f'vcz_amp_dac_at_11_02_{directions[i][1]}',  0)

        # Wrapper function for conditional oscillation detector function.
        def wrapper(Q0, Q1,
                    prepare_for_timedomain,
                    downsample_swp_points,
                    extract_only,
                    disable_metadata):
            a = self.measure_conditional_oscillation_multi(
                    pairs=[[Q0[i], Q1[i]] for i in range(len(Q0))], 
                    parked_qbs=Q_parks,
                    flux_codeword=flux_codeword,
                    prepare_for_timedomain=prepare_for_timedomain,
                    downsample_swp_points=downsample_swp_points,
                    extract_only=extract_only,
                    disable_metadata=disable_metadata,
                    verbose=False)
            cp = { f'phi_cond_{i+1}' : a[f'pair_{i+1}_delta_phi_a']\
                  for i in range(len(Q0)) }
            mf = { f'missing_fraction_{i+1}' : a[f'pair_{i+1}_missing_frac_a']\
                  for i in range(len(Q0)) }
            return { **cp, **mf} 
            
        d = det.Function_Detector(
            wrapper,
            msmt_kw={'Q0' : Q0, 'Q1' : Q1,
                     'prepare_for_timedomain' : False,
                     'downsample_swp_points': 3,
                     'extract_only': True,
                     'disable_metadata': True},
            result_keys=list(np.array([[f'phi_cond_{i+1}', f'missing_fraction_{i+1}']\
                                   for i in range(len(Q0))]).flatten()),
            value_names=list(np.array([[f'conditional_phase_{i+1}', f'missing_fraction_{i+1}']\
                                   for i in range(len(Q0))]).flatten()),
            value_units=list(np.array([['deg', '%']\
                                   for i in range(len(Q0))]).flatten()))
        nested_MC.set_detector_function(d)

        swf1 = swf.multi_sweep_function_ranges(
            sweep_functions=[Flux_lm_0[i].cfg_awg_channel_amplitude
                             for i in range(len(Q0))],
            sweep_ranges= A_ranges,
            n_points=A_points)
        swfs = [swf.FLsweep(lm = lm,
                            par = lm.parameters[f'vcz_amp_fine_{directions[i][0]}'],
                            waveform_name = f'cz_{directions[i][0]}')
                for i, lm in enumerate(Flux_lm_0) ]
        swf2 = swf.multi_sweep_function(sweep_functions=swfs)
        nested_MC.set_sweep_function(swf1)
        nested_MC.set_sweep_points(np.arange(A_points))
        nested_MC.set_sweep_function_2D(swf2)
        nested_MC.set_sweep_points_2D(B_amps)

        MC.live_plot_enabled(False)
        nested_MC.run(f'VCZ_Amp_vs_B_{Q0}_{Q1}_{Q_parks}',
                      mode='2D')
        MC.live_plot_enabled(True)


    def measure_vcz_A_tmid_landscape(
        self, 
        Q0,
        Q1,
        T_mids,
        A_ranges,
        A_points: int,
        Q_parks: list = None,
        Tp : float = None,
        flux_codeword: str = 'cz'):
        """
        Perform 2D sweep of amplitude and wave parameter while measuring 
        conditional phase and missing fraction via the "conditional 
        oscillation" experiment.

        Q0 : High frequency qubit(s). Can be given as single qubit or list.
        Q1 : Low frequency qubit(s). Can be given as single qubit or list.
        T_mids : list of vcz "T_mid" values to sweep.
        A_ranges : list of tuples containing ranges of amplitude sweep.
        A_points : Number of points to sweep for amplitude range.
        Q_parks : list of qubits parked during operation.
        """
        if isinstance(Q0, str):
            Q0 = [Q0]
        if isinstance(Q1, str):
            Q1 = [Q1]
        assert len(Q0) == len(Q1)

        MC = self.instr_MC.get_instr()
        nested_MC = self.instr_nested_MC.get_instr()
        # get gate directions
        directions = [get_gate_directions(q0, q1) for q0, q1 in zip(Q0, Q1)]
        # Prepare for time domain
        self.prepare_for_timedomain(
            qubits=np.array([[Q0[i],Q1[i]] for i in range(len(Q0))]).flatten(),
            bypass_flux=True)
        Flux_lm_0 = [self.find_instrument(q0).instr_LutMan_Flux.get_instr() for q0 in Q0]
        Flux_lm_1 = [self.find_instrument(q1).instr_LutMan_Flux.get_instr() for q1 in Q1]
        Flux_lms_park = [self.find_instrument(q).instr_LutMan_Flux.get_instr() for q in Q_parks]
        for i, lm in enumerate(Flux_lm_0):
            print(f'Setting {Q0[i]} vcz_amp_sq_{directions[i][0]} to 1')
            print(f'Setting {Q0[i]} vcz_amp_fine_{directions[i][0]} to 0.5')
            print(f'Setting {Q0[i]} vcz_amp_dac_at_11_02_{directions[i][0]} to 0.5')
            lm.set(f'vcz_amp_sq_{directions[i][0]}', 1)
            lm.set(f'vcz_amp_fine_{directions[i][0]}', .5)
            lm.set(f'vcz_amp_dac_at_11_02_{directions[i][0]}', .5)
        for i, lm in enumerate(Flux_lm_1):
            print(f'Setting {Q1[i]} vcz_amp_dac_at_11_02_{directions[i][1]} to 0')
            lm.set(f'vcz_amp_dac_at_11_02_{directions[i][1]}',  0)
        # Look for Tp values
        if Tp:
            if isinstance(Tp, str):
                Tp = [Tp]
        else:
            Tp = [lm.get(f'vcz_time_single_sq_{directions[0]}')*2 for lm in Flux_lm_0]
        assert len(Q0) == len(Tp)

        # Wrapper function for conditional oscillation detector function.
        def wrapper(Q0, Q1,
                    prepare_for_timedomain,
                    downsample_swp_points,
                    extract_only,
                    disable_metadata):
            a = self.measure_conditional_oscillation_multi(
                    pairs=[[Q0[i], Q1[i]] for i in range(len(Q0))], 
                    parked_qbs=Q_parks,
                    flux_codeword=flux_codeword,
                    prepare_for_timedomain=prepare_for_timedomain,
                    downsample_swp_points=downsample_swp_points,
                    extract_only=extract_only,
                    disable_metadata=disable_metadata,
                    verbose=False)
            cp = { f'phi_cond_{i+1}' : a[f'pair_{i+1}_delta_phi_a']\
                  for i in range(len(Q0)) }
            mf = { f'missing_fraction_{i+1}' : a[f'pair_{i+1}_missing_frac_a']\
                  for i in range(len(Q0)) }
            return { **cp, **mf} 

        d = det.Function_Detector(
            wrapper,
            msmt_kw={'Q0' : Q0, 'Q1' : Q1,
                     'prepare_for_timedomain' : False,
                     'downsample_swp_points': 3,
                     'extract_only': True,
                     'disable_metadata': True},
            result_keys=list(np.array([[f'phi_cond_{i+1}', f'missing_fraction_{i+1}']\
                                   for i in range(len(Q0))]).flatten()),
            value_names=list(np.array([[f'conditional_phase_{i+1}', f'missing_fraction_{i+1}']\
                                   for i in range(len(Q0))]).flatten()),
            value_units=list(np.array([['deg', '%']\
                                   for i in range(len(Q0))]).flatten()))
        nested_MC.set_detector_function(d)

        swf1 = swf.multi_sweep_function_ranges(
            sweep_functions=[Flux_lm_0[i].cfg_awg_channel_amplitude\
                             for i in range(len(Q0))],
            sweep_ranges= A_ranges,
            n_points=A_points)
        swf2 = swf.flux_t_middle_sweep(
            fl_lm_tm =  list(np.array([[Flux_lm_0[i], Flux_lm_1[i] ]\
                             for i in range(len(Q0))]).flatten()), 
            fl_lm_park = Flux_lms_park,
            which_gate = list(np.array(directions).flatten()),
            t_pulse = Tp)
        nested_MC.set_sweep_function(swf1)
        nested_MC.set_sweep_points(np.arange(A_points))
        nested_MC.set_sweep_function_2D(swf2)
        nested_MC.set_sweep_points_2D(T_mids)

        MC.live_plot_enabled(False)
        nested_MC.run(f'VCZ_Amp_vs_Tmid_{Q0}_{Q1}_{Q_parks}',
                      mode='2D')
        MC.live_plot_enabled(True)


def get_gate_directions(q0, q1,
                        map_qubits=None):
    """
    Helper function to determine two-qubit gate directions.
    q0 and q1 should be given as high-freq and low-freq qubit, respectively.
    Default map is surface-17, however other maps are supported.
    """
    if map_qubits == None:
        # Surface-17 layout
        map_qubits = {'Z3' : [-2,-1],
                      'D9' : [ 0, 2],
                      'X4' : [-1, 2],
                      'D8' : [-1, 1],
                      'Z4' : [ 0, 1],
                      'D6' : [ 1, 1],
                      'D7' : [-2, 0],
                      'X3' : [-1, 0],
                      'D5' : [ 0, 0],
                      'X2' : [ 1, 0],
                      'D3' : [ 2, 0],
                      'D4' : [-1,-1],
                      'Z1' : [ 0,-1],
                      'D2' : [ 1,-1],
                      'X1' : [ 1,-2],
                      'Z2' : [ 2, 1],
                      'D1' : [ 0,-2]
                     }
    V0 = np.array(map_qubits[q0])
    V1 = np.array(map_qubits[q1])
    diff = V1-V0
    dist = np.sqrt(np.sum((diff)**2))
    if dist > 1:
        raise ValueError('Qubits are not nearest neighbors')
    if diff[0] == 0.:
        if diff[1] > 0:
            return ('NE', 'SW')
        else:
            return ('SW', 'NE')
    elif diff[1] == 0.:
        if diff[0] > 0:
            return ('SE', 'NW')
        else:
            return ('NW', 'SE')
