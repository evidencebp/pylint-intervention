from datetime import datetime, timedelta
from typing import TYPE_CHECKING, Any
import weakref

import numpy as np

from pandas._libs import index as libindex
from pandas._libs.tslibs import NaT, frequencies as libfrequencies, resolution
from pandas._libs.tslibs.parsing import parse_time_string
from pandas._libs.tslibs.period import Period
from pandas.util._decorators import Appender, cache_readonly

from pandas.core.dtypes.common import (
    ensure_platform_int,
    is_bool_dtype,
    is_datetime64_any_dtype,
    is_dtype_equal,
    is_float,
    is_integer,
    is_integer_dtype,
    is_list_like,
    is_object_dtype,
    is_scalar,
    pandas_dtype,
)

from pandas.core.arrays.period import (
    PeriodArray,
    period_array,
    raise_on_incompatible,
    validate_dtype_freq,
)
import pandas.core.common as com
import pandas.core.indexes.base as ibase
from pandas.core.indexes.base import (
    InvalidIndexError,
    _index_shared_docs,
    ensure_index,
    maybe_extract_name,
)
from pandas.core.indexes.datetimelike import DatetimeIndexOpsMixin
from pandas.core.indexes.datetimes import DatetimeIndex, Index
from pandas.core.indexes.extension import inherit_names
from pandas.core.indexes.numeric import Int64Index
from pandas.core.ops import get_op_result_name
from pandas.core.tools.datetimes import DateParseError

from pandas.tseries import frequencies
from pandas.tseries.offsets import DateOffset, Tick

_index_doc_kwargs = dict(ibase._index_doc_kwargs)
_index_doc_kwargs.update(dict(target_klass="PeriodIndex or list of Periods"))

if TYPE_CHECKING:
    from pandas import Series

# --- Period index sketch


def _new_PeriodIndex(cls, **d):
    # GH13277 for unpickling
    values = d.pop("data")
    if values.dtype == "int64":
        freq = d.pop("freq", None)
        values = PeriodArray(values, freq=freq)
        return cls._simple_new(values, **d)
    else:
        return cls(values, **d)


@inherit_names(
    ["strftime", "to_timestamp", "asfreq", "start_time", "end_time"]
    + PeriodArray._field_ops,
    PeriodArray,
    wrap=True,
)
@inherit_names(["is_leap_year", "freq", "_format_native_types"], PeriodArray)
class PeriodIndex(DatetimeIndexOpsMixin, Int64Index):
    """
    Immutable ndarray holding ordinal values indicating regular periods in time.

    Index keys are boxed to Period objects which carries the metadata (eg,
    frequency information).

    Parameters
    ----------
    data : array-like (1d int np.ndarray or PeriodArray), optional
        Optional period-like data to construct index with.
    copy : bool
        Make a copy of input ndarray.
    freq : str or period object, optional
        One of pandas period strings or corresponding objects
    year : int, array, or Series, default None
    month : int, array, or Series, default None
    quarter : int, array, or Series, default None
    day : int, array, or Series, default None
    hour : int, array, or Series, default None
    minute : int, array, or Series, default None
    second : int, array, or Series, default None
    tz : object, default None
        Timezone for converting datetime64 data to Periods.
    dtype : str or PeriodDtype, default None

    Attributes
    ----------
    day
    dayofweek
    dayofyear
    days_in_month
    daysinmonth
    end_time
    freq
    freqstr
    hour
    is_leap_year
    minute
    month
    quarter
    qyear
    second
    start_time
    week
    weekday
    weekofyear
    year

    Methods
    -------
    asfreq
    strftime
    to_timestamp

    See Also
    --------
    Index : The base pandas Index type.
    Period : Represents a period of time.
    DatetimeIndex : Index with datetime64 data.
    TimedeltaIndex : Index of timedelta64 data.
    period_range : Create a fixed-frequency PeriodIndex.

    Examples
    --------
    >>> idx = pd.PeriodIndex(year=year_arr, quarter=q_arr)
    """

    _typ = "periodindex"
    _attributes = ["name", "freq"]

    # define my properties & methods for delegation
    _is_numeric_dtype = False
    _infer_as_myclass = True

    _data: PeriodArray

    _engine_type = libindex.PeriodEngine
    _supports_partial_string_indexing = True

    # ------------------------------------------------------------------------
    # Index Constructors

    def __new__(
        cls,
        data=None,
        ordinal=None,
        freq=None,
        tz=None,
        dtype=None,
        copy=False,
        name=None,
        **fields,
    ):

        valid_field_set = {
            "year",
            "month",
            "day",
            "quarter",
            "hour",
            "minute",
            "second",
        }

        if not set(fields).issubset(valid_field_set):
            argument = list(set(fields) - valid_field_set)[0]
            raise TypeError(f"__new__() got an unexpected keyword argument {argument}")

        name = maybe_extract_name(name, data, cls)

        if data is None and ordinal is None:
            # range-based.
            data, freq2 = PeriodArray._generate_range(None, None, None, freq, fields)
            # PeriodArray._generate range does validation that fields is
            # empty when really using the range-based constructor.
            freq = freq2

            data = PeriodArray(data, freq=freq)
        else:
            freq = validate_dtype_freq(dtype, freq)

            # PeriodIndex allow PeriodIndex(period_index, freq=different)
            # Let's not encourage that kind of behavior in PeriodArray.

            if freq and isinstance(data, cls) and data.freq != freq:
                # TODO: We can do some of these with no-copy / coercion?
                # e.g. D -> 2D seems to be OK
                data = data.asfreq(freq)

            if data is None and ordinal is not None:
                # we strangely ignore `ordinal` if data is passed.
                ordinal = np.asarray(ordinal, dtype=np.int64)
                data = PeriodArray(ordinal, freq)
            else:
                # don't pass copy here, since we copy later.
                data = period_array(data=data, freq=freq)

        if copy:
            data = data.copy()

        return cls._simple_new(data, name=name)

    @classmethod
    def _simple_new(cls, values, name=None, freq=None, **kwargs):
        """
        Create a new PeriodIndex.

        Parameters
        ----------
        values : PeriodArray
            Values that can be converted to a PeriodArray without inference
            or coercion.
        """
        assert isinstance(values, PeriodArray), type(values)
        assert freq is None or freq == values.freq, (freq, values.freq)

        result = object.__new__(cls)
        result._data = values
        # For groupby perf. See note in indexes/base about _index_data
        result._index_data = values._data
        result.name = name
        result._reset_identity()
        return result

    # ------------------------------------------------------------------------
    # Data

    @property
    def values(self):
        return np.asarray(self)

    @property
    def _has_complex_internals(self):
        # used to avoid libreduction code paths, which raise or require conversion
        return True

    def _shallow_copy(self, values=None, **kwargs):
        # TODO: simplify, figure out type of values
        if values is None:
            values = self._data

        if isinstance(values, type(self)):
            values = values._data

        if not isinstance(values, PeriodArray):
            if isinstance(values, np.ndarray) and values.dtype == "i8":
                values = PeriodArray(values, freq=self.freq)
            else:
                # GH#30713 this should never be reached
                raise TypeError(type(values), getattr(values, "dtype", None))

        # We don't allow changing `freq` in _shallow_copy.
        validate_dtype_freq(self.dtype, kwargs.get("freq"))
        attributes = self._get_attributes_dict()

        attributes.update(kwargs)
        if not len(values) and "dtype" not in kwargs:
            attributes["dtype"] = self.dtype
        return self._simple_new(values, **attributes)

    def _shallow_copy_with_infer(self, values=None, **kwargs):
        """ we always want to return a PeriodIndex """
        return self._shallow_copy(values=values, **kwargs)

    def _maybe_convert_timedelta(self, other):
        """
        Convert timedelta-like input to an integer multiple of self.freq

        Parameters
        ----------
        other : timedelta, np.timedelta64, DateOffset, int, np.ndarray

        Returns
        -------
        converted : int, np.ndarray[int64]

        Raises
        ------
        IncompatibleFrequency : if the input cannot be written as a multiple
            of self.freq.  Note IncompatibleFrequency subclasses ValueError.
        """
        if isinstance(other, (timedelta, np.timedelta64, Tick, np.ndarray)):
            offset = frequencies.to_offset(self.freq.rule_code)
            if isinstance(offset, Tick):
                # _check_timedeltalike_freq_compat will raise if incompatible
                delta = self._data._check_timedeltalike_freq_compat(other)
                return delta
        elif isinstance(other, DateOffset):
            freqstr = other.rule_code
            base = libfrequencies.get_base_alias(freqstr)
            if base == self.freq.rule_code:
                return other.n

            raise raise_on_incompatible(self, other)
        elif is_integer(other):
            # integer is passed to .shift via
            # _add_datetimelike_methods basically
            # but ufunc may pass integer to _add_delta
            return other

        # raise when input doesn't have freq
        raise raise_on_incompatible(self, None)

    # ------------------------------------------------------------------------
    # Rendering Methods

    def _mpl_repr(self):
        # how to represent ourselves to matplotlib
        return self.astype(object).values

    @property
    def _formatter_func(self):
        return self.array._formatter(boxed=False)

    # ------------------------------------------------------------------------
    # Indexing

    @cache_readonly
    def _engine(self):
        # To avoid a reference cycle, pass a weakref of self to _engine_type.
        period = weakref.ref(self)
        return self._engine_type(period, len(self))

    @Appender(Index.__contains__.__doc__)
    def __contains__(self, key: Any) -> bool:
        if isinstance(key, Period):
            if key.freq != self.freq:
                return False
            else:
                return key.ordinal in self._engine
        else:
            hash(key)
            try:
                self.get_loc(key)
                return True
            except KeyError:
                return False

    @cache_readonly
    def _int64index(self) -> Int64Index:
        return Int64Index._simple_new(self.asi8, name=self.name)

    # ------------------------------------------------------------------------
    # Index Methods

    def __array__(self, dtype=None) -> np.ndarray:
        if is_integer_dtype(dtype):
            return self.asi8
        else:
            return self.astype(object).values

    def __array_wrap__(self, result, context=None):
        """
        Gets called after a ufunc. Needs additional handling as
        PeriodIndex stores internal data as int dtype

        Replace this to __numpy_ufunc__ in future version
        """
        if isinstance(context, tuple) and len(context) > 0:
            func = context[0]
            if func is np.add:
                pass
            elif func is np.subtract:
                name = self.name
                left = context[1][0]
                right = context[1][1]
                if isinstance(left, PeriodIndex) and isinstance(right, PeriodIndex):
                    name = left.name if left.name == right.name else None
                    return Index(result, name=name)
                elif isinstance(left, Period) or isinstance(right, Period):
                    return Index(result, name=name)
            elif isinstance(func, np.ufunc):
                if "M->M" not in func.types:
                    msg = f"ufunc '{func.__name__}' not supported for the PeriodIndex"
                    # This should be TypeError, but TypeError cannot be raised
                    # from here because numpy catches.
                    raise ValueError(msg)

        if is_bool_dtype(result):
            return result
        # the result is object dtype array of Period
        # cannot pass _simple_new as it is
        return type(self)(result, freq=self.freq, name=self.name)

    def asof_locs(self, where, mask):
        """
        where : array of timestamps
        mask : array of booleans where data is not NA

        """
        where_idx = where
        if isinstance(where_idx, DatetimeIndex):
            where_idx = PeriodIndex(where_idx.values, freq=self.freq)

        locs = self._ndarray_values[mask].searchsorted(
            where_idx._ndarray_values, side="right"
        )

        locs = np.where(locs > 0, locs - 1, 0)
        result = np.arange(len(self))[mask].take(locs)

        first = mask.argmax()
        result[
            (locs == 0) & (where_idx._ndarray_values < self._ndarray_values[first])
        ] = -1

        return result

    @Appender(Index.astype.__doc__)
    def astype(self, dtype, copy=True, how="start"):
        dtype = pandas_dtype(dtype)

        if is_datetime64_any_dtype(dtype):
            # 'how' is index-specific, isn't part of the EA interface.
            tz = getattr(dtype, "tz", None)
            return self.to_timestamp(how=how).tz_localize(tz)

        # TODO: should probably raise on `how` here, so we don't ignore it.
        return super().astype(dtype, copy=copy)

    @property
    def is_full(self) -> bool:
        """
        Returns True if this PeriodIndex is range-like in that all Periods
        between start and end are present, in order.
        """
        if len(self) == 0:
            return True
        if not self.is_monotonic:
            raise ValueError("Index is not monotonic")
        values = self.asi8
        return ((values[1:] - values[:-1]) < 2).all()

    @property
    def inferred_type(self) -> str:
        # b/c data is represented as ints make sure we can't have ambiguous
        # indexing
        return "period"

    def get_value(self, series: "Series", key):
        """
        Fast lookup of value from 1-dimensional ndarray. Only use this if you
        know what you're doing
        """
        if is_integer(key):
            loc = key
        else:
            loc = self.get_loc(key)
        return self._get_values_for_loc(series, loc)

    @Appender(_index_shared_docs["get_indexer"] % _index_doc_kwargs)
    def get_indexer(self, target, method=None, limit=None, tolerance=None):
        target = ensure_index(target)

        if isinstance(target, PeriodIndex):
            if target.freq != self.freq:
                # No matches
                no_matches = -1 * np.ones(self.shape, dtype=np.intp)
                return no_matches

            target = target.asi8
            self_index = self._int64index
        else:
            self_index = self

        if tolerance is not None:
            tolerance = self._convert_tolerance(tolerance, target)
        return Index.get_indexer(self_index, target, method, limit, tolerance)

    @Appender(_index_shared_docs["get_indexer_non_unique"] % _index_doc_kwargs)
    def get_indexer_non_unique(self, target):
        target = ensure_index(target)

        if isinstance(target, PeriodIndex):
            if target.freq != self.freq:
                no_matches = -1 * np.ones(self.shape, dtype=np.intp)
                return no_matches, no_matches

            target = target.asi8

        indexer, missing = self._int64index.get_indexer_non_unique(target)
        return ensure_platform_int(indexer), missing

    def get_loc(self, key, method=None, tolerance=None):
        """
        Get integer location for requested label.

        Parameters
        ----------
        key : Period, NaT, str, or datetime
            String or datetime key must be parseable as Period.

        Returns
        -------
        loc : int or ndarray[int64]

        Raises
        ------
        KeyError
            Key is not present in the index.
        TypeError
            If key is listlike or otherwise not hashable.
        """

        if not is_scalar(key):
            raise InvalidIndexError(key)

        if isinstance(key, str):

            try:
                loc = self._get_string_slice(key)
                return loc
            except (TypeError, ValueError):
                pass

            try:
                asdt, reso = parse_time_string(key, self.freq)
            except DateParseError:
                # A string with invalid format
                raise KeyError(f"Cannot interpret '{key}' as period")

            grp = resolution.Resolution.get_freq_group(reso)
            freqn = resolution.get_freq_group(self.freq)

            # _get_string_slice will handle cases where grp < freqn
            assert grp >= freqn

            if grp == freqn:
                key = Period(asdt, freq=self.freq)
                loc = self.get_loc(key, method=method, tolerance=tolerance)
                return loc
            elif method is None:
                raise KeyError(key)
            else:
                key = asdt

        elif is_integer(key):
            # Period constructor will cast to string, which we dont want
            raise KeyError(key)

        try:
            key = Period(key, freq=self.freq)
        except ValueError:
            # we cannot construct the Period
            # as we have an invalid type
            if is_list_like(key):
                raise TypeError(f"'{key}' is an invalid key")
            raise KeyError(key)

        ordinal = key.ordinal if key is not NaT else key.value
        try:
            return self._engine.get_loc(ordinal)
        except KeyError:

            try:
                if tolerance is not None:
                    tolerance = self._convert_tolerance(tolerance, np.asarray(key))
                return self._int64index.get_loc(ordinal, method, tolerance)

            except KeyError:
                raise KeyError(key)

    def _maybe_cast_slice_bound(self, label, side: str, kind: str):
        """
        If label is a string or a datetime, cast it to Period.ordinal according
        to resolution.

        Parameters
        ----------
        label : object
        side : {'left', 'right'}
        kind : {'loc', 'getitem'}

        Returns
        -------
        bound : Period or object

        Notes
        -----
        Value of `side` parameter should be validated in caller.

        """
        assert kind in ["loc", "getitem"]

        if isinstance(label, datetime):
            return Period(label, freq=self.freq)
        elif isinstance(label, str):
            try:
                parsed, reso = parse_time_string(label, self.freq)
                bounds = self._parsed_string_to_bounds(reso, parsed)
                return bounds[0 if side == "left" else 1]
            except ValueError:
                # string cannot be parsed as datetime-like
                # TODO: we need tests for this case
                raise KeyError(label)
        elif is_integer(label) or is_float(label):
            self._invalid_indexer("slice", label)

        return label

    def _parsed_string_to_bounds(self, reso: str, parsed: datetime):
        if reso not in ["year", "month", "quarter", "day", "hour", "minute", "second"]:
            raise KeyError(reso)

        grp = resolution.Resolution.get_freq_group(reso)
        iv = Period(parsed, freq=(grp, 1))
        return (iv.asfreq(self.freq, how="start"), iv.asfreq(self.freq, how="end"))

    def _get_string_slice(self, key: str, use_lhs: bool = True, use_rhs: bool = True):
        # TODO: Check for non-True use_lhs/use_rhs
        parsed, reso = parse_time_string(key, self.freq)
        grp = resolution.Resolution.get_freq_group(reso)
        freqn = resolution.get_freq_group(self.freq)

        if not grp < freqn:
            # TODO: we used to also check for
            #  reso in ["day", "hour", "minute", "second"]
            #  why is that check not needed?
            raise ValueError(key)

        t1, t2 = self._parsed_string_to_bounds(reso, parsed)
        i8vals = self.asi8

        if self.is_monotonic:

            # we are out of range
            if len(self) and (
                (use_lhs and t1 < self[0] and t2 < self[0])
                or ((use_rhs and t1 > self[-1] and t2 > self[-1]))
            ):
                raise KeyError(key)

            # TODO: does this depend on being monotonic _increasing_?
            #  If so, DTI will also be affected.

            # a monotonic (sorted) series can be sliced
            # Use asi8.searchsorted to avoid re-validating Periods
            left = i8vals.searchsorted(t1.ordinal, side="left") if use_lhs else None
            right = i8vals.searchsorted(t2.ordinal, side="right") if use_rhs else None
            return slice(left, right)

        else:
            lhs_mask = (i8vals >= t1.ordinal) if use_lhs else True
            rhs_mask = (i8vals <= t2.ordinal) if use_rhs else True

            # try to find a the dates
            return (lhs_mask & rhs_mask).nonzero()[0]

    def _convert_tolerance(self, tolerance, target):
        tolerance = DatetimeIndexOpsMixin._convert_tolerance(self, tolerance, target)
        if target.size != tolerance.size and tolerance.size > 1:
            raise ValueError("list-like tolerance size must match target index size")
        return self._maybe_convert_timedelta(tolerance)

    def insert(self, loc, item):
        if not isinstance(item, Period) or self.freq != item.freq:
            return self.astype(object).insert(loc, item)

        idx = np.concatenate(
            (self[:loc].asi8, np.array([item.ordinal]), self[loc:].asi8)
        )
        return self._shallow_copy(idx)

    def join(self, other, how="left", level=None, return_indexers=False, sort=False):
        """
        See Index.join
        """
        self._assert_can_do_setop(other)

        if not isinstance(other, PeriodIndex):
            return self.astype(object).join(
                other, how=how, level=level, return_indexers=return_indexers, sort=sort
            )

        result = Int64Index.join(
            self,
            other,
            how=how,
            level=level,
            return_indexers=return_indexers,
            sort=sort,
        )

        if return_indexers:
            result, lidx, ridx = result
            return self._apply_meta(result), lidx, ridx
        return self._apply_meta(result)

    # ------------------------------------------------------------------------
    # Set Operation Methods

    def _assert_can_do_setop(self, other):
        super()._assert_can_do_setop(other)

        # *Can't* use PeriodIndexes of different freqs
        # *Can* use PeriodIndex/DatetimeIndex
        if isinstance(other, PeriodIndex) and self.freq != other.freq:
            raise raise_on_incompatible(self, other)

    def intersection(self, other, sort=False):
        self._validate_sort_keyword(sort)
        self._assert_can_do_setop(other)
        res_name = get_op_result_name(self, other)
        other = ensure_index(other)

        if self.equals(other):
            return self._get_reconciled_name_object(other)

        if not is_dtype_equal(self.dtype, other.dtype):
            # TODO: fastpath for if we have a different PeriodDtype
            this = self.astype("O")
            other = other.astype("O")
            return this.intersection(other, sort=sort)

        i8self = Int64Index._simple_new(self.asi8)
        i8other = Int64Index._simple_new(other.asi8)
        i8result = i8self.intersection(i8other, sort=sort)

        result = self._shallow_copy(np.asarray(i8result, dtype=np.int64), name=res_name)
        return result

    def difference(self, other, sort=None):
        self._validate_sort_keyword(sort)
        self._assert_can_do_setop(other)
        res_name = get_op_result_name(self, other)
        other = ensure_index(other)

        if self.equals(other):
            # pass an empty PeriodArray with the appropriate dtype
            return self._shallow_copy(self._data[:0])

        if is_object_dtype(other):
            return self.astype(object).difference(other).astype(self.dtype)

        elif not is_dtype_equal(self.dtype, other.dtype):
            return self

        i8self = Int64Index._simple_new(self.asi8)
        i8other = Int64Index._simple_new(other.asi8)
        i8result = i8self.difference(i8other, sort=sort)

        result = self._shallow_copy(np.asarray(i8result, dtype=np.int64), name=res_name)
        return result

    def _union(self, other, sort):
        if not len(other) or self.equals(other) or not len(self):
            return super()._union(other, sort=sort)

        # We are called by `union`, which is responsible for this validation
        assert isinstance(other, type(self))

        if not is_dtype_equal(self.dtype, other.dtype):
            this = self.astype("O")
            other = other.astype("O")
            return this._union(other, sort=sort)

        i8self = Int64Index._simple_new(self.asi8)
        i8other = Int64Index._simple_new(other.asi8)
        i8result = i8self._union(i8other, sort=sort)

        res_name = get_op_result_name(self, other)
        result = self._shallow_copy(np.asarray(i8result, dtype=np.int64), name=res_name)
        return result

    # ------------------------------------------------------------------------

    def _apply_meta(self, rawarr) -> "PeriodIndex":
        if not isinstance(rawarr, PeriodIndex):
            if not isinstance(rawarr, PeriodArray):
                rawarr = PeriodArray(rawarr, freq=self.freq)
            rawarr = PeriodIndex._simple_new(rawarr, name=self.name)
        return rawarr

    def memory_usage(self, deep=False):
        result = super().memory_usage(deep=deep)
        if hasattr(self, "_cache") and "_int64index" in self._cache:
            result += self._int64index.memory_usage(deep=deep)
        return result


PeriodIndex._add_numeric_methods_disabled()
PeriodIndex._add_logical_methods_disabled()


def period_range(
    start=None, end=None, periods=None, freq=None, name=None
) -> PeriodIndex:
    """
    Return a fixed frequency PeriodIndex.

    The day (calendar) is the default frequency.

    Parameters
    ----------
    start : str or period-like, default None
        Left bound for generating periods.
    end : str or period-like, default None
        Right bound for generating periods.
    periods : int, default None
        Number of periods to generate.
    freq : str or DateOffset, optional
        Frequency alias. By default the freq is taken from `start` or `end`
        if those are Period objects. Otherwise, the default is ``"D"`` for
        daily frequency.
    name : str, default None
        Name of the resulting PeriodIndex.

    Returns
    -------
    PeriodIndex

    Notes
    -----
    Of the three parameters: ``start``, ``end``, and ``periods``, exactly two
    must be specified.

    To learn more about the frequency strings, please see `this link
    <https://pandas.pydata.org/pandas-docs/stable/user_guide/timeseries.html#offset-aliases>`__.

    Examples
    --------

    >>> pd.period_range(start='2017-01-01', end='2018-01-01', freq='M')
    PeriodIndex(['2017-01', '2017-02', '2017-03', '2017-04', '2017-05',
                 '2017-06', '2017-06', '2017-07', '2017-08', '2017-09',
                 '2017-10', '2017-11', '2017-12', '2018-01'],
                dtype='period[M]', freq='M')

    If ``start`` or ``end`` are ``Period`` objects, they will be used as anchor
    endpoints for a ``PeriodIndex`` with frequency matching that of the
    ``period_range`` constructor.

    >>> pd.period_range(start=pd.Period('2017Q1', freq='Q'),
    ...                 end=pd.Period('2017Q2', freq='Q'), freq='M')
    PeriodIndex(['2017-03', '2017-04', '2017-05', '2017-06'],
                dtype='period[M]', freq='M')
    """
    if com.count_not_none(start, end, periods) != 2:
        raise ValueError(
            "Of the three parameters: start, end, and periods, "
            "exactly two must be specified"
        )
    if freq is None and (not isinstance(start, Period) and not isinstance(end, Period)):
        freq = "D"

    data, freq = PeriodArray._generate_range(start, end, periods, freq, fields={})
    data = PeriodArray(data, freq=freq)
    return PeriodIndex(data, name=name)
