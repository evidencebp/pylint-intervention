from itertools import product
import logging
import os

import numpy as np
import pandas as pd

from edisgo.io import timeseries_import
from edisgo.flex_opt import q_control
from edisgo.tools.tools import (
    assign_voltage_level_to_component,
    drop_duplicated_columns,
    get_weather_cells_intersecting_with_grid_district,
)

logger = logging.getLogger("edisgo")


class TimeSeries:
    """
    Holds component-specific active and reactive power time series.

    All time series are fixed time series that in case of flexibilities result after
    application of a heuristic or optimisation. They can be used for power flow
    calculations.

    Also holds any raw time series data that was used to generate component-specific
    time series in attribute `time_series_raw`. See
    :class:`~.network.timeseries.TimeSeriesRaw` for more information.

    Other Parameters
    -----------------
    timeindex : :pandas:`pandas.DatetimeIndex<DatetimeIndex>`, optional
        Can be used to define a time range for which to obtain the provided
        time series and run power flow analysis. Default: None.

    Attributes
    -----------
    time_series_raw : :class:`~.network.timeseries.TimeSeriesRaw`
        Raw time series. See :class:`~.network.timeseries.TimeSeriesRaw` for  more
        information.

    """

    def __init__(self, **kwargs):

        self._timeindex = kwargs.get("timeindex", pd.DatetimeIndex([]))
        self.time_series_raw = TimeSeriesRaw()

    @property
    def timeindex(self):
        """
        Time index all time-dependent attributes are indexed by.

        Is used as default time steps in e.g. power flow analysis.

        Parameters
        -----------
        ind : :pandas:`pandas.DatetimeIndex<DatetimeIndex>`
            Time index all time-dependent attributes are indexed by.

        Returns
        -------
        :pandas:`pandas.DatetimeIndex<DatetimeIndex>`
            Time index all time-dependent attributes are indexed by.

        """
        return self._timeindex

    @timeindex.setter
    def timeindex(self, ind):
        if len(self._timeindex) > 0:
            # check if new time index is subset of existing time index
            if not ind.isin(self._timeindex).all():
                logger.warning(
                    "Not all time steps of new time index lie within existing "
                    "time index. This may cause problems later on."
                )
        self._timeindex = ind

    @property
    def generators_active_power(self):
        """
        Active power time series of generators in MW.

        Parameters
        ----------
        df : :pandas:`pandas.DataFrame<DataFrame>`
            Active power time series of all generators in topology in MW. Index of the
            dataframe is a time index and column names are names of generators.

        Returns
        -------
        :pandas:`pandas.DataFrame<DataFrame>`
            Active power time series of all generators in topology in MW for time steps
            given in :py:attr:`~timeindex`. For more information on the dataframe see
            input parameter `df`.

        """
        try:
            return self._generators_active_power.loc[self.timeindex, :]
        except:
            return pd.DataFrame(index=self.timeindex)

    @generators_active_power.setter
    def generators_active_power(self, df):
        self._generators_active_power = df

    @property
    def generators_reactive_power(self):
        """
        Reactive power time series of generators in MVA.

        Parameters
        ----------
        df : :pandas:`pandas.DataFrame<DataFrame>`
            Reactive power time series of all generators in topology in MVA. Index of
            the dataframe is a time index and column names are names of generators.

        Returns
        -------
        :pandas:`pandas.DataFrame<DataFrame>`
            Reactive power time series of all generators in topology in MVA for time
            steps given in :py:attr:`~timeindex`. For more information on the dataframe
            see input parameter `df`.

        """
        try:
            return self._generators_reactive_power.loc[self.timeindex, :]
        except:
            return pd.DataFrame(index=self.timeindex)

    @generators_reactive_power.setter
    def generators_reactive_power(self, df):
        self._generators_reactive_power = df

    @property
    def loads_active_power(self):
        """
        Active power time series of loads in MW.

        Parameters
        ----------
        df : :pandas:`pandas.DataFrame<DataFrame>`
            Active power time series of all loads in topology in MW. Index of the
            dataframe is a time index and column names are names of loads.

        Returns
        -------
        :pandas:`pandas.DataFrame<DataFrame>`
            Active power time series of all loads in topology in MW for time steps
            given in :py:attr:`~timeindex`. For more information on the dataframe see
            input parameter `df`.

        """
        try:
            return self._loads_active_power.loc[self.timeindex, :]
        except:
            return pd.DataFrame(index=self.timeindex)

    @loads_active_power.setter
    def loads_active_power(self, df):
        self._loads_active_power = df

    @property
    def loads_reactive_power(self):
        """
        Reactive power time series of loads in MVA.

        Parameters
        ----------
        df : :pandas:`pandas.DataFrame<DataFrame>`
            Reactive power time series of all loads in topology in MVA. Index of
            the dataframe is a time index and column names are names of loads.

        Returns
        -------
        :pandas:`pandas.DataFrame<DataFrame>`
            Reactive power time series of all loads in topology in MVA for time
            steps given in :py:attr:`~timeindex`. For more information on the dataframe
            see input parameter `df`.

        """
        try:
            return self._loads_reactive_power.loc[self.timeindex, :]
        except:
            return pd.DataFrame(index=self.timeindex)

    @loads_reactive_power.setter
    def loads_reactive_power(self, df):
        self._loads_reactive_power = df

    @property
    def storage_units_active_power(self):
        """
        Active power time series of storage units in MW.

        Parameters
        ----------
        df : :pandas:`pandas.DataFrame<DataFrame>`
            Active power time series of all storage units in topology in MW. Index of
            the dataframe is a time index and column names are names of storage units.

        Returns
        -------
        :pandas:`pandas.DataFrame<DataFrame>`
            Active power time series of all storage units in topology in MW for time
            steps given in :py:attr:`~timeindex`. For more information on the dataframe
            see input parameter `df`.

        """
        try:
            return self._storage_units_active_power.loc[self.timeindex, :]
        except:
            return pd.DataFrame(index=self.timeindex)

    @storage_units_active_power.setter
    def storage_units_active_power(self, df):
        self._storage_units_active_power = df

    @property
    def storage_units_reactive_power(self):
        """
        Reactive power time series of storage units in MVA.

        Parameters
        ----------
        df : :pandas:`pandas.DataFrame<DataFrame>`
            Reactive power time series of all storage units in topology in MVA. Index of
            the dataframe is a time index and column names are names of storage units.

        Returns
        -------
        :pandas:`pandas.DataFrame<DataFrame>`
            Reactive power time series of all storage units in topology in MVA for time
            steps given in :py:attr:`~timeindex`. For more information on the dataframe
            see input parameter `df`.

        """
        try:
            return self._storage_units_reactive_power.loc[self.timeindex, :]
        except:
            return pd.DataFrame(index=self.timeindex)

    @storage_units_reactive_power.setter
    def storage_units_reactive_power(self, df):
        self._storage_units_reactive_power = df

    def reset(self):
        """
        Resets all time series.

        Active and reactive power time series of all loads, generators and storage units
        are deleted, as well as everything stored in :py:attr:`~time_series_raw`.

        """
        self.generators_active_power = None
        self.loads_active_power = None
        self.storage_units_active_power = None
        self.time_series_raw = TimeSeriesRaw()

    def set_active_power_manual(self, edisgo_object, ts_generators=None, ts_loads=None,
                                ts_storage_units=None):
        """
        Sets given component active power time series.

        If time series for a component were already set before, they are overwritten.

        Parameters
        ----------
        edisgo_object : :class:`~.EDisGo`
        ts_generators : :pandas:`pandas.DataFrame<DataFrame>`
            Active power time series in MW of generators. Index of the data frame is
            a datetime index. Columns contain generators names of generators to set
            time series for.
        ts_loads : :pandas:`pandas.DataFrame<DataFrame>`
            Active power time series in MW of loads. Index of the data frame is
            a datetime index. Columns contain load names of loads to set
            time series for.
        ts_storage_units : :pandas:`pandas.DataFrame<DataFrame>`
            Active power time series in MW of storage units. Index of the data frame is
            a datetime index. Columns contain storage unit names of storage units to set
            time series for.

        """
        self._set_manual(edisgo_object, "active", ts_generators=ts_generators,
                         ts_loads=ts_loads, ts_storage_units=ts_storage_units)

    def set_reactive_power_manual(self, edisgo_object, ts_generators=None,
                                  ts_loads=None, ts_storage_units=None):
        """
        Sets given component reactive power time series.

        If time series for a component were already set before, they are overwritten.

        Parameters
        ----------
        edisgo_object : :class:`~.EDisGo`
        ts_generators : :pandas:`pandas.DataFrame<DataFrame>`
            Reactive power time series in MVA of generators. Index of the data frame is
            a datetime index. Columns contain generators names of generators to set
            time series for.
        ts_loads : :pandas:`pandas.DataFrame<DataFrame>`
            Reactive power time series in MVA of loads. Index of the data frame is
            a datetime index. Columns contain load names of loads to set
            time series for.
        ts_storage_units : :pandas:`pandas.DataFrame<DataFrame>`
            Reactive power time series in MVA of storage units. Index of the data frame
            is a datetime index. Columns contain storage unit names of storage units to
            set time series for.

        """
        self._set_manual(edisgo_object, "reactive", ts_generators=ts_generators,
                         ts_loads=ts_loads, ts_storage_units=ts_storage_units)

    def _set_manual(self, edisgo_object, mode, ts_generators=None, ts_loads=None,
                    ts_storage_units=None):
        """
        Sets given component time series.

        If time series for a component were already set before, they are overwritten.

        Parameters
        ----------
        edisgo_object : :class:`~.EDisGo`
        mode : str
            Defines whether to set active or reactive power time series. Possible
            options are "active" and "reactive".
        ts_generators : :pandas:`pandas.DataFrame<DataFrame>`
            Active or reactive power time series in MW or MVA of generators.
            Index of the data frame is a datetime index. Columns contain generator
            names of generators to set time series for.
        ts_loads : :pandas:`pandas.DataFrame<DataFrame>`
            Active or reactive power time series in MW or MVA of loads.
            Index of the data frame is a datetime index. Columns contain load names of
            loads to set time series for.
        ts_storage_units : :pandas:`pandas.DataFrame<DataFrame>`
            Active or reactive power time series in MW or MVA of storage units.
            Index of the data frame is a datetime index. Columns contain storage unit
            names of storage units to set time series for.

        """
        if ts_generators is not None:
            # check if all generators time series are provided for exist in the network
            # and only set time series for those that do
            comps_in_network = _check_if_components_exist(
                edisgo_object, ts_generators.columns, "generators")
            ts_generators = ts_generators.loc[:, comps_in_network]

            # drop generators time series from self.generators_(re)active_power that may
            # already exist for some of the given generators
            df_name = "generators_{}_power".format(mode)
            _drop_component_time_series(
                obj=self, df_name=df_name,
                comp_names=ts_generators.columns
            )
            # set (re)active power
            _add_component_time_series(obj=self, df_name=df_name,
                                       ts_new=ts_generators)

        if ts_loads is not None:
            # check if all loads time series are provided for exist in the network
            # and only set time series for those that do
            comps_in_network = _check_if_components_exist(
                edisgo_object, ts_loads.columns, "loads")
            ts_loads = ts_loads.loc[:, comps_in_network]

            # drop load time series from self.loads_(re)active_power that may
            # already exist for some of the given loads
            df_name = "loads_{}_power".format(mode)
            _drop_component_time_series(
                obj=self, df_name=df_name, comp_names=ts_loads.columns
            )
            # set (re)active power
            _add_component_time_series(obj=self, df_name=df_name,
                                       ts_new=ts_loads)

        if ts_storage_units is not None:
            # check if all storage units time series are provided for exist in the
            # network and only set time series for those that do
            comps_in_network = _check_if_components_exist(
                edisgo_object, ts_storage_units.columns, "storage_units")
            ts_storage_units = ts_storage_units.loc[:, comps_in_network]

            # drop storage unit time series from self.storage_units_(re)active_power
            # that may already exist for some of the given storage units
            df_name = "storage_units_{}_power".format(mode)
            _drop_component_time_series(
                obj=self, df_name=df_name,
                comp_names=ts_storage_units.columns
            )
            # set (re)active power
            _add_component_time_series(obj=self, df_name=df_name,
                                       ts_new=ts_storage_units)

    def set_worst_case(self, edisgo_object, cases):
        """
        Sets demand and feed-in of all loads, generators and storage units for the
        specified worst cases.

        Possible worst cases are 'load_case' (heavy load flow case) and 'feed-in_case'
        (reverse power flow case). Each case is set up once for dimensioning of the MV
        grid ('load_case_mv'/'feed-in_case_mv') and once for the dimensioning of the LV
        grid ('load_case_lv'/'feed-in_case_lv'), as different simultaneity factors are
        assumed for the different voltage levels.

        Assumed simultaneity factors specified in the config section
        `worst_case_scale_factor` are used to generate active power demand or feed-in.
        For the reactive power behavior fixed cosphi is assumed and the power factors
        specified in the config section `reactive_power_factor` are used.

        Component specific information is given below:

        * Generators

            Worst case feed-in time series are distinguished by technology (PV, wind
            and all other) and whether it is a load or feed-in case.
            In case of generator worst case time series it is not distinguished by
            whether it is used to analyse the MV or LV. However, both options are
            generated as it is distinguished in the case of loads.
            Worst case scaling factors for generators are specified in
            the config section `worst_case_scale_factor` through the parameters:
            'feed-in_case_feed-in_pv', 'feed-in_case_feed-in_wind',
            'feed-in_case_feed-in_other',
            'load_case_feed-in_pv', load_case_feed-in_wind', and
            'load_case_feed-in_other'.

            For reactive power a fixed cosphi is assumed. A different reactive power
            factor is used for generators in the MV and generators in the LV.
            The reactive power factors for generators are specified in
            the config section `reactive_power_factor` through the parameters:
            'mv_gen' and 'lv_gen'.

        * Conventional loads

            Worst case load time series are distinguished by whether it
            is a load or feed-in case and whether it used to analyse the MV or LV.
            Worst case scaling factors for conventional loads are specified in
            the config section `worst_case_scale_factor` through the parameters:
            'mv_feed-in_case_load', 'lv_feed-in_case_load', 'mv_load_case_load', and
            'lv_load_case_load'.

            For reactive power a fixed cosphi is assumed. A different reactive power
            factor is used for loads in the MV and loads in the LV.
            The reactive power factors for conventional loads are specified in
            the config section `reactive_power_factor` through the parameters:
            'mv_load' and 'lv_load'.

        * Charging points

            Worst case demand time series are distinguished by use case (home charging,
            work charging, public (slow) charging and HPC), by whether it is a load or
            feed-in case and by whether it used to analyse the MV or LV.
            Worst case scaling factors for charging points are specified in
            the config section `worst_case_scale_factor` through the parameters:
            'mv_feed-in_case_cp_home', 'mv_feed-in_case_cp_work',
            'mv_feed-in_case_cp_public', and 'mv_feed-in_case_cp_hpc',
            'lv_feed-in_case_cp_home', 'lv_feed-in_case_cp_work',
            'lv_feed-in_case_cp_public', and 'lv_feed-in_case_cp_hpc',
            'mv_load-in_case_cp_home', 'mv_load-in_case_cp_work',
            'mv_load-in_case_cp_public', and 'mv_load-in_case_cp_hpc',
            'lv_load-in_case_cp_home', 'lv_load-in_case_cp_work',
            'lv_load-in_case_cp_public', and 'lv_load-in_case_cp_hpc'.

            For reactive power a fixed cosphi is assumed. A different reactive power
            factor is used for charging points in the MV and charging points in the LV.
            The reactive power factors for charging points are specified in
            the config section `reactive_power_factor` through the parameters:
            'mv_cp' and 'lv_cp'.

        * Heat pumps

            Worst case demand time series are distinguished by whether it is a load or
            feed-in case and by whether it used to analyse the MV or LV.
            Worst case scaling factors for heat pumps are specified in
            the config section `worst_case_scale_factor` through the parameters:
            'mv_feed-in_case_hp', 'lv_feed-in_case_hp', 'mv_load_case_hp', and
            'lv_load_case_hp'.

            For reactive power a fixed cosphi is assumed. A different reactive power
            factor is used for heat pumps in the MV and heat pumps in the LV.
            The reactive power factors for heat pumps are specified in
            the config section `reactive_power_factor` through the parameters:
            'mv_hp' and 'lv_hp'.

        * Storage units

            Worst case feed-in time series are distinguished by whether it is a load or
            feed-in case.
            In case of storage units worst case time series it is not distinguished by
            whether it is used to analyse the MV or LV. However, both options are
            generated as it is distinguished in the case of loads.
            Worst case scaling factors for storage units are specified in
            the config section `worst_case_scale_factor` through the parameters:
            'feed-in_case_storage' and 'load_case_storage'.

            For reactive power a fixed cosphi is assumed. A different reactive power
            factor is used for storage units in the MV and storage units in the LV.
            The reactive power factors for storage units are specified in
            the config section `reactive_power_factor` through the parameters:
            'mv_storage' and 'lv_storage'.

        Parameters
        ----------
        edisgo_object : :class:`~.EDisGo`
        cases : list(str)
            List with worst-cases to generate time series for. Can be
            'feed-in_case', 'load_case' or both.

        Notes
        -----
        Loads for which type information is not set are handled as conventional loads.

        """
        # reset all time series
        self.reset()

        #ToDo: Check if index needs to be time index
        # self.timeindex = pd.date_range(
        #     "1/1/1970", periods=len(modes), freq="H"
        # )
        self.timeindex = ["_".join(case) for case in product(cases, ["mv", "lv"])]

        if not edisgo_object.topology.generators_df.empty:
            # assign voltage level for reactive power
            df = assign_voltage_level_to_component(
                edisgo_object.topology.generators_df, edisgo_object.topology.buses_df)
            self.generators_active_power, self.generators_reactive_power = (
                self._worst_case_generators(
                    cases, df, edisgo_object.config)
            )
        if not edisgo_object.topology.loads_df.empty:
            # assign voltage level for reactive power
            df = assign_voltage_level_to_component(
                edisgo_object.topology.loads_df, edisgo_object.topology.buses_df)
            # conventional loads
            df_tmp = df[df.type == "conventional_load"]
            if not df_tmp.empty:
                self.loads_active_power, self.loads_reactive_power = (
                    self._worst_case_conventional_load(
                        cases, df_tmp, edisgo_object.config)
                )
            # charging points
            df_tmp = df[df.type == "charging_point"]
            if not df_tmp.empty:
                p_tmp, q_tmp = self._worst_case_charging_points(
                    cases, df_tmp, edisgo_object.config)
                self.loads_active_power = pd.concat(
                    [self.loads_active_power, p_tmp],
                    axis=1
                )
                self.loads_reactive_power = pd.concat(
                    [self.loads_reactive_power, q_tmp],
                    axis=1
                )
            # heat pumps
            df_tmp = df[df.type == "heat_pump"]
            if not df_tmp.empty:
                p_tmp, q_tmp = self._worst_case_heat_pumps(
                    cases, df_tmp, edisgo_object.config)
                self.loads_active_power = pd.concat(
                    [self.loads_active_power, p_tmp],
                    axis=1
                )
                self.loads_reactive_power = pd.concat(
                    [self.loads_reactive_power, q_tmp],
                    axis=1
                )
            # check if there are loads without time series remaining and if so, handle
            # them as conventional loads
            loads_without_ts = list(
                set(df.index) - set(self.loads_active_power.columns))
            if len(loads_without_ts) > 0:
                logging.warning(
                    "There are loads where information on type of load is missing. "
                    "Handled types are 'conventional_load', 'charging_point', and "
                    "'heat_pump'. Loads with missing type information are handled as "
                    "conventional loads. If this is not the wanted behavior, please "
                    "set type information. This concerns the following "
                    "loads: {}.".format(loads_without_ts)
                )
                p_tmp, q_tmp = (
                    self._worst_case_conventional_load(
                        cases, df.loc[loads_without_ts, :], edisgo_object.config)
                )
                self.loads_active_power = pd.concat(
                    [self.loads_active_power, p_tmp],
                    axis=1
                )
                self.loads_reactive_power = pd.concat(
                    [self.loads_reactive_power, q_tmp],
                    axis=1
                )
        if not edisgo_object.topology.storage_units_df.empty:
            # assign voltage level for reactive power
            df = assign_voltage_level_to_component(
                edisgo_object.topology.storage_units_df,
                edisgo_object.topology.buses_df)
            self.storage_units_active_power, self.storage_units_reactive_power = (
                self._worst_case_storage_units(
                    cases, df, edisgo_object.config)
            )

    def _worst_case_generators(self, cases, df, configs):
        """
        Get feed-in of generators for worst case analyses.

        See :py:attr:`~set_worst_case` for further information.

        Parameters
        ----------
        cases : list(str)
            List with worst-cases to generate time series for. Can be
            'feed-in_case', 'load_case' or both.
        df : :pandas:`pandas.DataFrame<DataFrame>`
            Dataframe with information on generators in the format of
            :attr:`~.network.topology.Topology.generators_df` with additional column
            "voltage_level".
        configs : :class:`~.tools.config.Config`
            Configuration data with assumed simultaneity factors and reactive power
            behavior.

        Returns
        -------
        (:pandas:`pandas.DataFrame<DataFrame>`, :pandas:`pandas.DataFrame<DataFrame>`)
            Active and reactive power (in MW and MVA, respectively) in each case for
            each generator. The index of the dataframe contains the case and the columns
            are the generator names.

        """
        # check that all generators have information on nominal power, technology type,
        # and voltage level they are in
        df = df.loc[:, ["p_nom", "voltage_level", "type"]]
        check = df.isnull().any(axis=1)
        if check.any():
            raise AttributeError(
                "The following generators have missing information on "
                "nominal power, technology type or voltage level: {}.".format(
                    check[check].index.values)
            )

        # active power
        # get worst case configurations
        worst_case_scale_factors = configs["worst_case_scale_factor"]
        # get power scaling factors for different technologies, voltage levels and
        # feed-in/load case
        types = ["pv", "wind", "other"]
        power_scaling = pd.DataFrame(columns=types)
        for t in types:
            for case in cases:
                power_scaling.at["{}_{}".format(case, "mv"), t] = (
                    worst_case_scale_factors[
                        "{}_feed-in_{}".format(case, t)]
                )
                power_scaling.at["{}_{}".format(case, "lv"), t] = power_scaling.at[
                    "{}_{}".format(case, "mv"), t]
        # calculate active power of generators
        active_power = pd.concat(
            [power_scaling.pv.to_frame("p_nom").dot(
                df[df.type == "solar"].loc[:, ["p_nom"]].T),
             power_scaling.wind.to_frame("p_nom").dot(
                 df[df.type == "wind"].loc[:, ["p_nom"]].T),
                power_scaling.other.to_frame("p_nom").dot(
                    df[~df.type.isin(["solar", "wind"])].loc[:, ["p_nom"]].T)
             ], axis=1
        )

        # reactive power
        # get worst case configurations for each load
        q_sign, power_factor = _reactive_power_factor_and_mode_default(
            df, "generators", configs)
        # write reactive power configuration to TimeSeriesRaw
        self.time_series_raw.q_control = pd.concat([
            self.time_series_raw.q_control,
            pd.DataFrame(
                index=df.index,
                data={"type": "fixed_cosphi",
                      "q_sign": q_sign,
                      "power_factor": power_factor
                      }
            )]
        )
        # calculate reactive power of generators
        reactive_power = q_control.fixed_cosphi(
            active_power, q_sign, power_factor)
        return active_power, reactive_power

    def _worst_case_conventional_load(self, cases, df, configs):
        """
        Get demand of conventional loads for worst case analyses.

        See :py:attr:`~set_worst_case` for further information.

        Parameters
        ----------
        cases : list(str)
            List with worst-cases to generate time series for. Can be
            'feed-in_case', 'load_case' or both.
        df : :pandas:`pandas.DataFrame<DataFrame>`
            Dataframe with information on conventional loads in the format of
            :attr:`~.network.topology.Topology.loads_df` with additional column
            "voltage_level".
        configs : :class:`~.tools.config.Config`
            Configuration data with assumed simultaneity factors and reactive power
            behavior.

        Returns
        -------
        (:pandas:`pandas.DataFrame<DataFrame>`, :pandas:`pandas.DataFrame<DataFrame>`)
            Active and reactive power (in MW and MVA, respectively) in each case for
            each load. The index of the dataframe contains the case and the columns
            are the load names.

        """
        # check that all loads have information on nominal power (grid connection power)
        # and voltage level they are in
        df = df.loc[:, ["p_nom", "voltage_level"]]
        check = df.isnull().any(axis=1)
        if check.any():
            raise AttributeError(
                "The following loads have missing information on "
                "grid connection power or voltage level: {}.".format(
                    check[check].index.values)
            )

        # active power
        # get worst case configurations
        worst_case_scale_factors = configs["worst_case_scale_factor"]
        # get power scaling factors for different voltage levels and feed-in/load case
        power_scaling = pd.Series()
        for case in cases:
            for voltage_level in ["mv", "lv"]:
                power_scaling.at["{}_{}".format(case, voltage_level)] = (
                    worst_case_scale_factors[
                        "{}_{}_load".format(voltage_level, case)]
                )
        # calculate active power of loads
        active_power = power_scaling.to_frame("p_nom").dot(
            df.loc[:, ["p_nom"]].T)

        # reactive power
        # get worst case configurations for each load
        q_sign, power_factor = _reactive_power_factor_and_mode_default(
            df, "loads", configs)
        # write reactive power configuration to TimeSeriesRaw
        self.time_series_raw.q_control = pd.concat([
            self.time_series_raw.q_control,
            pd.DataFrame(
                index=df.index,
                data={"type": "fixed_cosphi",
                      "q_sign": q_sign,
                      "power_factor": power_factor
                      }
            )]
        )
        # calculate reactive power of loads
        reactive_power = q_control.fixed_cosphi(
            active_power, q_sign, power_factor)
        return active_power, reactive_power

    def _worst_case_charging_points(self, cases, df, configs):
        """
        Get demand of charging points for worst case analyses.

        See :py:attr:`~set_worst_case` for further information.

        Parameters
        ----------
        cases : list(str)
            List with worst-cases to generate time series for. Can be
            'feed-in_case', 'load_case' or both.
        df : :pandas:`pandas.DataFrame<DataFrame>`
            Dataframe with information on charging points in the format of
            :attr:`~.network.topology.Topology.loads_df` with additional column
            "voltage_level".
        configs : :class:`~.tools.config.Config`
            Configuration data with assumed simultaneity factors and reactive power
            behavior.

        Returns
        -------
        (:pandas:`pandas.DataFrame<DataFrame>`, :pandas:`pandas.DataFrame<DataFrame>`)
            Active and reactive power (in MW and MVA, respectively) in each case for
            each charging point. The index of the dataframe contains the case and the
            columns are the charging point names.

        """
        # check that all charging points have information on nominal power,
        # sector (use case), and voltage level they are in
        df = df.loc[:, ["p_nom", "voltage_level", "sector"]]
        check = df.isnull().any(axis=1)
        if check.any():
            raise AttributeError(
                "The following charging points have missing information on "
                "nominal power, use case or voltage level: {}.".format(
                    check[check].index.values)
            )
        # check that there is no invalid sector (only "home", "work", "public", and
        # "hpc" allowed)
        use_cases = ["home", "work", "public", "hpc"]
        sectors = df.sector.unique()
        diff = list(set(sectors) - set(use_cases))
        if len(diff) > 0:
            raise AttributeError(
                "The following charging points have a use case no worst case "
                "simultaneity factor is defined for: {}.".format(
                    df[df.sector.isin(diff)].index.values)
            )

        # active power
        # get worst case configurations
        worst_case_scale_factors = configs["worst_case_scale_factor"]
        # get power scaling factors for different use cases, voltage levels and
        # feed-in/load case
        power_scaling = pd.DataFrame(columns=sectors)
        for s in sectors:
            for case in cases:
                for voltage_level in ["mv", "lv"]:
                    power_scaling.at["{}_{}".format(case, voltage_level), s] = (
                        worst_case_scale_factors[
                            "{}_{}_cp_{}".format(voltage_level, case, s)]
                    )
        # calculate active power of charging points
        active_power = pd.concat(
            [power_scaling.loc[:, s].to_frame("p_nom").dot(
                 df[df.sector == s].loc[:, ["p_nom"]].T) for s in sectors
             ], axis=1
        )

        # reactive power
        # get worst case configurations for each charging point
        q_sign, power_factor = _reactive_power_factor_and_mode_default(
            df, "charging_points", configs)
        # write reactive power configuration to TimeSeriesRaw
        self.time_series_raw.q_control = pd.concat([
            self.time_series_raw.q_control,
            pd.DataFrame(
                index=df.index,
                data={"type": "fixed_cosphi",
                      "q_sign": q_sign,
                      "power_factor": power_factor
                      }
            )]
        )
        # calculate reactive power of charging points
        reactive_power = q_control.fixed_cosphi(
            active_power, q_sign, power_factor)
        return active_power, reactive_power

    def _worst_case_heat_pumps(self, cases, df, configs):
        """
        Get demand of heat pumps for worst case analyses.

        See :py:attr:`~set_worst_case` for further information.

        Parameters
        ----------
        cases : list(str)
            List with worst-cases to generate time series for. Can be
            'feed-in_case', 'load_case' or both.
        df : :pandas:`pandas.DataFrame<DataFrame>`
            Dataframe with information on heat pumps in the format of
            :attr:`~.network.topology.Topology.loads_df` with additional column
            "voltage_level".
        configs : :class:`~.tools.config.Config`
            Configuration data with assumed simultaneity factors and reactive power
            behavior.

        Returns
        -------
        (:pandas:`pandas.DataFrame<DataFrame>`, :pandas:`pandas.DataFrame<DataFrame>`)
            Active and reactive power (in MW and MVA, respectively) in each case for
            each heat pump. The index of the dataframe contains the case and the columns
            are the heat pump names.

        """
        # check that all heat pumps have information on nominal power, and voltage level
        # they are in
        df = df.loc[:, ["p_nom", "voltage_level"]]
        check = df.isnull().any(axis=1)
        if check.any():
            raise AttributeError(
                "The following heat pumps have missing information on "
                "nominal power or voltage level: {}.".format(
                    check[check].index.values)
            )

        # active power
        # get worst case configurations
        worst_case_scale_factors = configs["worst_case_scale_factor"]
        # get power scaling factors for different voltage levels and feed-in/load case
        power_scaling = pd.Series()
        for case in cases:
            for voltage_level in ["mv", "lv"]:
                power_scaling.at["{}_{}".format(case, voltage_level)] = (
                    worst_case_scale_factors[
                        "{}_{}_hp".format(voltage_level, case)]
                )
        # calculate active power of heat pumps
        active_power = power_scaling.to_frame("p_nom").dot(df.loc[:, ["p_nom"]].T)

        # reactive power
        # get worst case configurations for each heat pump
        q_sign, power_factor = _reactive_power_factor_and_mode_default(
            df, "heat_pumps", configs)
        # write reactive power configuration to TimeSeriesRaw
        self.time_series_raw.q_control = pd.concat([
            self.time_series_raw.q_control,
            pd.DataFrame(
                index=df.index,
                data={"type": "fixed_cosphi",
                      "q_sign": q_sign,
                      "power_factor": power_factor
                      }
            )]
        )
        # calculate reactive power of heat pumps
        reactive_power = q_control.fixed_cosphi(
            active_power, q_sign, power_factor)
        return active_power, reactive_power

    def _worst_case_storage_units(self, cases, df, configs):
        """
        Get charging and discharging of storage units for worst case analyses.

        See :py:attr:`~set_worst_case` for further information.

        Parameters
        ----------
        cases : list(str)
            List with worst-cases to generate time series for. Can be
            'feed-in_case', 'load_case' or both.
        df : :pandas:`pandas.DataFrame<DataFrame>`
            Dataframe with information on generators in the format of
            :attr:`~.network.topology.Topology.generators_df` with additional column
            "voltage_level".
        configs : :class:`~.tools.config.Config`
            Configuration data with assumed simultaneity factors and reactive power
            behavior.

        Returns
        -------
        (:pandas:`pandas.DataFrame<DataFrame>`, :pandas:`pandas.DataFrame<DataFrame>`)
            Active and reactive power (in MW and MVA, respectively) in each case for
            each storage. The index of the dataframe contains the case and the columns
            are the storage names.

        """
        # check that all storage units have information on nominal power
        # and voltage level they are in
        df = df.loc[:, ["p_nom", "voltage_level"]]
        check = df.isnull().any(axis=1)
        if check.any():
            raise AttributeError(
                "The following storage units have missing information on "
                "nominal power or voltage level: {}.".format(
                    check[check].index.values)
            )

        # active power
        # get worst case configurations
        worst_case_scale_factors = configs["worst_case_scale_factor"]
        # get power scaling factors for different voltage levels and feed-in/load case
        power_scaling = pd.Series()
        for case in cases:
            power_scaling.at["{}_{}".format(case, "mv")] = (
                worst_case_scale_factors[
                    "{}_storage".format(case)]
            )
            power_scaling.at["{}_{}".format(case, "lv")] = power_scaling.at[
                "{}_{}".format(case, "mv")]
        # calculate active power of loads
        active_power = power_scaling.to_frame("p_nom").dot(
            df.loc[:, ["p_nom"]].T)

        # reactive power
        # get worst case configurations for each load
        q_sign, power_factor = _reactive_power_factor_and_mode_default(
            df, "storage_units", configs)
        # write reactive power configuration to TimeSeriesRaw
        self.time_series_raw.q_control = pd.concat([
            self.time_series_raw.q_control,
            pd.DataFrame(
                index=df.index,
                data={"type": "fixed_cosphi",
                      "q_sign": q_sign,
                      "power_factor": power_factor
                      }
            )]
        )
        # calculate reactive power of loads
        reactive_power = q_control.fixed_cosphi(
            active_power, q_sign, power_factor)
        return active_power, reactive_power

    def predefined_conventional_load_by_sector(
            self, edisgo_object, ts_loads, load_names=None):
        """
        Set active power demand time series for conventional loads by sector.

        Parameters
        ----------
        edisgo_object : :class:`~.EDisGo`
        ts_loads : str or :pandas:`pandas.DataFrame<DataFrame>`
            Possible options are:

            * 'demandlib'

                Time series for the year specified :py:attr:`~timeindex` are
                generated using standard electric load profiles from the oemof
                `demandlib <https://github.com/oemof/demandlib/>`_.
                The demandlib provides sector-specific time series for the sectors
                'residential', 'retail', 'industrial', and 'agricultural'.

            * :pandas:`pandas.DataFrame<DataFrame>`

                DataFrame with load time series per sector normalized to an annual
                consumption of 1. Index needs to
                be a :pandas:`pandas.DatetimeIndex<DatetimeIndex>`.
                Columns contain the sector as string.
                In the current grid existing load types can be retrieved from column
                `sector` in :attr:`~.network.topology.Topology.loads_df`. In ding0 grid
                the differentiated sectors are 'residential', 'retail', 'industrial',
                and 'agricultural'.
        load_names : list(str)
            If None, all loads of sectors for which sector-specific time series are
            provided are used. In case the demandlib is used, all loads of sectors
            'residential', 'retail', 'industrial', and 'agricultural' are used.

        """
        # in case time series from demandlib are used, retrieve demandlib time series
        if isinstance(ts_loads, str) and ts_loads == "demandlib":
            ts_loads = \
                timeseries_import.load_time_series_demandlib(
                    edisgo_object.config,
                    year=self.timeindex[0].year
                )
        elif not isinstance(ts_loads, pd.DataFrame):
            raise ValueError(
                "'ts_loads' must either be a pandas DataFrame or 'demandlib'.")

        # write to TimeSeriesRaw
        self.time_series_raw.conventional_loads_active_power_by_sector = ts_loads

        # set load_names if None
        if load_names is None:
            sectors = ts_loads.columns.unique()
            load_names = edisgo_object.topology.loads_df[
                edisgo_object.topology.loads_df.sector.isin(sectors)].index
        load_names = _check_if_components_exist(edisgo_object, load_names, "loads")
        loads_df = edisgo_object.topology.loads_df.loc[load_names, :]

        # drop existing time series
        _drop_component_time_series(
            obj=self, df_name="loads_active_power",
            comp_names=load_names
        )

        # scale time series by annual consumption
        self.loads_active_power = pd.concat(
            [
                self.loads_active_power,
                loads_df.apply(
                    lambda x: ts_loads[x.sector] * x.annual_consumption,
                    axis=1,
                ).T,
            ],
            axis=1,
        )

    @property
    def residual_load(self):
        """
        Returns residual load in network.

        Residual load for each time step is calculated from total load
        minus total generation minus storage active power (discharge is
        positive).
        A positive residual load represents a load case while a negative
        residual load here represents a feed-in case.
        Grid losses are not considered.

        Returns
        -------
        :pandas:`pandas.Series<Series>`
            Series with residual load in MW.

        """
        return (
                self.loads_active_power.sum(axis=1) -
                self.generators_active_power.sum(axis=1) -
                self.storage_units_active_power.sum(axis=1)
        )

    @property
    def timesteps_load_feedin_case(self):
        """
        Contains residual load and information on feed-in and load case.

        Residual load is calculated from total (load - generation) in the
        network. Grid losses are not considered.

        Feed-in and load case are identified based on the
        generation, load and storage time series and defined as follows:

        1. Load case: positive (load - generation - storage) at HV/MV
           substation
        2. Feed-in case: negative (load - generation - storage) at HV/MV
           substation

        Returns
        -------
        :pandas:`pandas.Series<Series>`

            Series with information on whether time step is handled as load
            case ('load_case') or feed-in case ('feed-in_case') for each time
            step in :py:attr:`~timeindex`.

        """

        return self.residual_load.apply(
            lambda _: "feed-in_case" if _ < 0.0 else "load_case"
        )

    @property
    def _attributes(self):
        return [
            "loads_active_power", "loads_reactive_power",
            "generators_active_power", "generators_reactive_power",
            "storage_units_active_power", "storage_units_reactive_power"
        ]

    def reduce_memory(self, attr_to_reduce=None, to_type="float32",
                      time_series_raw=True, **kwargs):
        """
        Reduces size of dataframes to save memory.

        See :attr:`EDisGo.reduce_memory` for more information.

        Parameters
        -----------
        attr_to_reduce : list(str), optional
            List of attributes to reduce size for. Per default, all active
            and reactive power time series of generators, loads, and storage units
            are reduced.
        to_type : str, optional
            Data type to convert time series data to. This is a tradeoff
            between precision and memory. Default: "float32".
        time_series_raw : bool, optional
            If True raw time series data in :py:attr:`~time_series_raw` is reduced
            as well. Default: True.

        Other Parameters
        ------------------
        attr_to_reduce_raw : list(str), optional
            List of attributes in :class:`~.network.timeseries.TimeSeriesRaw` to reduce
            size for. See :attr:`~.network.timeseries.TimeSeriesRaw.reduce_memory`
            for default.

        """
        if attr_to_reduce is None:
            attr_to_reduce = self._attributes
        for attr in attr_to_reduce:
            setattr(
                self,
                attr,
                getattr(self, attr).apply(lambda _: _.astype(to_type)),
            )
        if time_series_raw:
            self.time_series_raw.reduce_memory(
                kwargs.get("attr_to_reduce_raw", None),
                to_type=to_type
            )

    def to_csv(self, directory, reduce_memory=False, time_series_raw=False, **kwargs):
        """
        Saves component time series to csv.

        Saves the following time series to csv files with the same file name
        (if the time series dataframe is not empty):

        * loads_active_power and loads_reactive_power
        * generators_active_power and generators_reactive_power
        * storage_units_active_power and  storage_units_reactive_power

        If parameter `time_series_raw` is set to True, raw time series data is saved
        to csv as well. See :attr:`~.network.timeseries.TimeSeriesRaw.to_csv`
        for more information.

        Parameters
        ----------
        directory : str
            Directory to save time series in.
        reduce_memory : bool, optional
            If True, size of dataframes is reduced using
            :attr:`~.network.timeseries.TimeSeries.reduce_memory`.
            Optional parameters of
            :attr:`~.network.timeseries.TimeSeries.reduce_memory`
            can be passed as kwargs to this function. Default: False.
        time_series_raw : bool, optional
            If True raw time series data in :py:attr:`~time_series_raw` is saved to csv
            as well. Per default all raw time series data is then stored in a
            subdirectory of the specified `directory` called "time_series_raw". Further,
            if `reduce_memory` is set to True, raw time series data is reduced as well.
            To change this default behavior please call
            :attr:`~.network.timeseries.TimeSeriesRaw.to_csv` separately.
            Default: False.

        Other Parameters
        ------------------
        kwargs :
            Kwargs may contain arguments of
            :attr:`~.network.timeseries.TimeSeries.reduce_memory`.

        """
        if reduce_memory is True:
            self.reduce_memory(**kwargs)

        os.makedirs(directory, exist_ok=True)

        for attr in self._attributes:
            if not getattr(self, attr).empty:
                getattr(self, attr).to_csv(
                    os.path.join(directory, "{}.csv".format(attr))
                )

        if time_series_raw:
            self.time_series_raw.to_csv(
                directory=os.path.join(directory, "time_series_raw"),
                reduce_memory=reduce_memory
            )

    def from_csv(self, directory, time_series_raw=False, **kwargs):
        """
        Restores time series from csv files.

        See :func:`~to_csv` for more information on which time series can be saved and
        thus restored.

        Parameters
        ----------
        directory : str
            Directory time series are saved in.
        time_series_raw : bool, optional
            If True raw time series data is as well read in (see
            :attr:`~.network.timeseries.TimeSeriesRaw.from_csv` for further
            information). Directory data is restored from can be specified through
            kwargs.
            Default: False.

        Other Parameters
        ------------------
        directory_raw : str, optional
            Directory to read raw time series data from. Per default this is a
            subdirectory of the specified `directory` called "time_series_raw".

        """
        timeindex = None
        for attr in self._attributes:
            path = os.path.join(directory, "{}.csv".format(attr))
            if os.path.exists(path):
                setattr(
                    self,
                    attr,
                    pd.read_csv(path, index_col=0, parse_dates=True),
                )
                if timeindex is None:
                    timeindex = getattr(self, "_{}".format(attr)).index
        if timeindex is None:
            timeindex = pd.DatetimeIndex([])
        self._timeindex = timeindex

        if time_series_raw:
            self.time_series_raw.from_csv(
                directory=kwargs.get(
                    "directory_raw", os.path.join(directory, "time_series_raw"))
            )


class TimeSeriesRaw:
    """
    Holds raw time series data, e.g. sector-specific demand and standing times of EV.

    Normalised time series are e.g. sector-specific demand time series or
    technology-specific feed-in time series. Time series needed for
    flexibilities are e.g. heat time series or curtailment time series.

    Attributes
    ------------
    q_control : :pandas:`pandas.DataFrame<DataFrame>`
        Dataframe with information on applied reactive power control or in case of
        conventional loads assumed reactive power behavior. Index of the dataframe are
        the component names as in index of
        :attr:`~.network.topology.Topology.generators_df`,
        :attr:`~.network.topology.Topology.loads_df`, and
        :attr:`~.network.topology.Topology.storage_units_df`. Columns are
        "type" with the type of Q-control applied (can be "fixed_cosphi", "cosphi(P)",
        or "Q(V)"),
        "power_factor" with the (maximum) power factor,
        "q_sign" giving the sign of the reactive power (only applicable to
        "fixed_cosphi"),
        "parametrisation" with the parametrisation of the
        respective Q-control (only applicable to "cosphi(P)" and "Q(V)").
    conventional_loads_active_power_by_sector : :pandas:`pandas.DataFrame<DataFrame>`
        DataFrame with load time series of each type of conventional load
        normalized to an annual consumption of 1. Index needs to
        be a :pandas:`pandas.DatetimeIndex<DatetimeIndex>`.
        Columns represent load type. In ding0 grids the
        differentiated sectors are 'residential', 'retail', 'industrial', and
        'agricultural'.
    curtailment_target : :pandas:`pandas.DataFrame<dataframe>`
        DataFrame with generator- or technology-specific curtailment target in MW.
        In the case of generator-specific curtailment targets columns
        of the DataFrame hold the generator name.
        In the case of technology-specific curtailment targets columns
        hold the technology type.
        If curtailment targets are provided by generator type and weather cell ID,
        columns are a :pandas:`pandas.MultiIndex<multiindex>`
        with the first level containing the technology type and the second
        level the weather cell ID.
        Index of the DataFrame is a time index.

    Notes
    -----
    Can also hold the following attributes when specific mode of
    :meth:`get_component_timeseries` is called: mode, generation_fluctuating,
    generation_dispatchable, generation_reactive_power, load,
    load_reactive_power. See description of meth:`get_component_timeseries` for
    format of these.

    """

    def __init__(self):
        self.q_control = pd.DataFrame(
            columns=["type", "q_sign", "power_factor", "parametrisation"])
        self.conventional_loads_active_power_by_sector = None

    @property
    def _attributes(self):
        return [
            "q_control",
            "conventional_loads_active_power_by_sector"
        ]

    def reduce_memory(self, attr_to_reduce=None, to_type="float32"):
        """
        Reduces size of dataframes to save memory.

        See :attr:`EDisGo.reduce_memory` for more information.

        Parameters
        -----------
        attr_to_reduce : list(str), optional
            List of attributes to reduce size for. Attributes need to be
            dataframes containing only time series. Per default, all active
            and reactive power time series of generators, loads, storage units
            and charging points are reduced.
        to_type : str, optional
            Data type to convert time series data to. This is a tradeoff
            between precision and memory. Default: "float32".

        """
        if attr_to_reduce is None:
            attr_to_reduce = self._attributes
        # remove attributes that do not contain only floats
        if "q_control" in attr_to_reduce:
            attr_to_reduce.remove("q_control")
        for attr in attr_to_reduce:
            if hasattr(self, attr):
                setattr(
                    self,
                    attr,
                    getattr(self, attr).apply(
                        lambda _: _.astype(to_type)
                    )
                )

    def to_csv(self, directory, reduce_memory=False, **kwargs):
        """
        Saves time series to csv.

        Saves all attributes that are set to csv files with the same file name.
        See class definition for possible attributes.

        Parameters
        ----------
        directory: str
            Directory to save time series in.
        reduce_memory : bool, optional
            If True, size of dataframes is reduced using
            :attr:`~.network.timeseries.TimeSeriesRaw.reduce_memory`. Optional
            parameters of
            :attr:`~.network.timeseries.TimeSeriesRaw.reduce_memory`
            can be passed as kwargs to this function. Default: False.

        Other Parameters
        ------------------
        kwargs :
            Kwargs may contain optional arguments of
            :attr:`~.network.timeseries.TimeSeriesRaw.reduce_memory`.

        """
        if reduce_memory is True:
            self.reduce_memory(**kwargs)

        os.makedirs(directory, exist_ok=True)

        for attr in self._attributes:
            if hasattr(self, attr) and not getattr(self, attr).empty:
                getattr(self, attr).to_csv(
                    os.path.join(directory, "{}.csv".format(attr))
                )

    def from_csv(self, directory):
        """
        Restores time series from csv files.

        See :func:`~to_csv` for more information on which time series are
        saved.

        Parameters
        ----------
        directory : str
            Directory time series are saved in.

        """
        timeindex = None
        for attr in self._attributes:
            path = os.path.join(directory, "{}.csv".format(attr))
            if os.path.exists(path):
                setattr(
                    self,
                    attr,
                    pd.read_csv(path, index_col=0, parse_dates=True),
                )
                if timeindex is None:
                    timeindex = getattr(self, "_{}".format(attr)).index
        if timeindex is None:
            timeindex = pd.DatetimeIndex([])
        self._timeindex = timeindex


def _drop_component_time_series(obj, df_name, comp_names):
    """
    Drop component time series.

    Parameters
    ----------
    obj : obj
        Object with attr `df_name` to remove columns from. Can e.g. be
        :class:`~.network.timeseries.TimeSeries`.
    df_name : str
        Name of attribute of given object holding the dataframe to remove columns from.
        Can e.g. be "generators_active_power" if time series should be removed from
        :attr:`~.network.timeseries.TimeSeries.generators_active_power`.
    comp_names: str or list(str)
        Names of components to drop.

    """
    if isinstance(comp_names, str):
        comp_names = [comp_names]
    # drop existing time series of component
    setattr(
        obj,
        df_name,
        getattr(obj, df_name).drop(
            getattr(obj, df_name).columns[
                getattr(
                    obj, df_name
                ).columns.isin(comp_names)
            ],
            axis=1,
        ),
    )


def _add_component_time_series(obj, df_name, ts_new):
    """
    Add component time series.

    Parameters
    ----------
    obj : obj
        Object with attr `df_name` to add columns to. Can e.g. be
        :class:`~.network.timeseries.TimeSeries`.
    df_name : str
        Name of attribute of given object holding the dataframe to add columns to.
        Can e.g. be "generators_active_power" if time series should be added to
        :attr:`~.network.timeseries.TimeSeries.generators_active_power`.
    ts_new : :pandas:`pandas.DataFrame<DataFrame>`
        Dataframe with new time series to add to existing time series dataframe.

    """
    setattr(
        obj,
        df_name,
        pd.concat(
            [
                getattr(obj, df_name),
                ts_new
            ],
            axis=1,
        ),
    )


def _check_if_components_exist(edisgo_object, component_names, component_type):
    """
    Checks if all provided components exist in the network.

    Raises warning if there any provided components that are not in the network.

    Parameters
    ----------
    edisgo_object : :class:`~.EDisGo`
    component_names : list(str)
        Names of components for which time series are added.
    component_type : str
        The component type for which time series are added.
        Possible options are 'generators', 'storage_units', 'loads'.

    Returns
    --------
    set(str)
        Returns a set of all provided components that are in the network.

    """
    comps_in_network = getattr(
        edisgo_object.topology, "{}_df".format(component_type)).index
    comps_not_in_network = list(
        set(component_names) - set(comps_in_network))
    if len(comps_not_in_network) > 0:
        logging.warning(
            "Some of the provided {} are not in the network. "
            "This concerns the following components: {}.".format(
                component_type, comps_not_in_network)
        )
        provided_comps_in_network = set(component_names) - set(comps_not_in_network)
        return provided_comps_in_network
    return component_names


def _reactive_power_factor_and_mode_default(comp_df, component_type, configs):
    """
    Gets default values for sign of reactive power and power factor for each component.

    Parameters
    -----------
    comp_df : :pandas:`pandas.DataFrame<DataFrame>`
        Dataframe with component names (in the index) of all components
        reactive power factor and mode needs to be set. Only required column is
        column 'voltage_level', giving the voltage level the component is in (the
        voltage level can be set using the function
        :func:`~.tools.tools.assign_voltage_level_to_component`).
        All components must have the same `component_type`.
    component_type : str
        The component type determines the reactive power factor and mode used.
        Possible options are 'generators', 'storage_units', 'loads', 'charging_points',
        and 'heat_pumps'.
    configs : :class:`~.tools.config.Config`
        eDisGo configuration data.

    Returns
    --------
    (:pandas:`pandas.Series<Series>`, :pandas:`pandas.Series<Series>`)
        Series with sign of reactive power (positive or negative) and series with
        reactive power factor are returned.

    """
    # get default configurations
    reactive_power_mode = configs["reactive_power_mode"]
    reactive_power_factor = configs["reactive_power_factor"]

    # write series with sign of reactive power and power factor for each component
    q_sign = pd.Series(index=comp_df.index)
    power_factor = pd.Series(index=comp_df.index)
    if component_type == "generators":
        get_q_sign = q_control.get_q_sign_generator
        comp = "gen"
    elif component_type == "storage_units":
        get_q_sign = q_control.get_q_sign_generator
        comp = "storage"
    elif component_type == "loads":
        get_q_sign = q_control.get_q_sign_load
        comp = "load"
    elif component_type == "charging_points":
        get_q_sign = q_control.get_q_sign_load
        comp = "cp"
    elif component_type == "heat_pumps":
        get_q_sign = q_control.get_q_sign_load
        comp = "hp"
    else:
        raise ValueError(
            "Given 'component_type' is not valid. Valid options are "
            "'generators','storage_units', 'loads', 'charging_points', and "
            "'heat_pumps'.")
    for voltage_level in comp_df.voltage_level.unique():
        cols = comp_df.index[comp_df.voltage_level == voltage_level]
        if len(cols) > 0:
            q_sign[cols] = get_q_sign(
                reactive_power_mode[
                    "{}_{}".format(voltage_level, comp)
                ]
            )
            power_factor[cols] = reactive_power_factor[
                "{}_{}".format(voltage_level, comp)
            ]
    return q_sign, power_factor
