# Copyright 2018 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# Lowering of jaxprs into XLA (HLO) computations.

from collections import defaultdict
import collections.abc
import dataclasses
import functools
from functools import partial
import itertools as it
import operator
import re
from typing import (Any, Callable, Dict, List, NamedTuple, Optional,
                    Sequence, Set, Type, Tuple, Union)
from typing_extensions import Protocol

import numpy as np

from jax.config import config
from jax import core
from jax._src import device_array
from jax._src import dtypes
from jax import linear_util as lu
from jax._src import source_info_util
from jax._src.abstract_arrays import (make_shaped_array, array_types)
from jax.core import (ConcreteArray, ShapedArray,
                      Literal, str_eqn_compact, abstract_token)
import jax._src.pretty_printer as pp
from jax._src import util
from jax._src.util import (prod, new_name_stack, safe_zip, safe_map,
                           partition_list)

# TODO: update callers to refer to new location.
from jax._src.util import extend_name_stack as extend_name_stack  # noqa: F401
from jax._src.util import wrap_name as wrap_name  # noqa: F401

from jax._src.lib import xla_client as xc
from jax.interpreters import partial_eval as pe
from jax.interpreters import ad

map, unsafe_map = safe_map, map
zip, unsafe_zip = safe_zip, zip

xe = xc._xla
xops = xc._xla.ops

# Types
Backend = xe.Client
Device = xc.Device
Buffer = xe.Buffer

XlaOp = xc.XlaOp
XlaShape = xc.Shape
XlaBuilder = xc.XlaBuilder
XlaExecutable = xc.Executable

# apply_primitive is defined in jax._src.dispatch.
apply_primitive: Callable
backend_compile: Callable
device_put: Callable

# TODO(phawkins): update code to point to new locations.
DeviceArray = device_array.DeviceArray
_DeviceArray = device_array._DeviceArray
_CppDeviceArray = xe.Buffer
make_device_array = device_array.make_device_array


def identity(x): return x

_scalar_types = dtypes.python_scalar_dtypes.keys()

# unit representation
def _make_unit_constant(c): return [
    xops.Constant(c, np.zeros((), dtype=np.dtype('bool')))]
def _make_unit_shape(_): return (xc.Shape.array_shape(np.dtype('bool'), ()),)
def _make_array_shape(a: ShapedArray) -> Sequence[XlaShape]:
  if a.dtype is dtypes.float0:
    return (xc.Shape.array_shape(np.dtype('bool'), a.shape),)
  else:
    return (xc.Shape.array_shape(a.dtype, a.shape),)

def _get_canonical_source_file(frame: source_info_util.Frame):
  source_file = frame.file_name
  if config.jax_hlo_source_file_canonicalization_regex:
    source_file = re.sub(config.jax_hlo_source_file_canonicalization_regex,
                         '', source_file)
  return source_file

tracebacks = {}
def make_op_metadata(primitive: core.Primitive,
                     params: Dict, *,
                     source_info: source_info_util.SourceInfo,
                     name_stack: Union[str, source_info_util.NameStack] = "",
                     ) -> xc.OpMetadata:
  if config.jax_experimental_name_stack:
    eqn_str = str(source_info.name_stack) + '/' + str_eqn_compact(primitive.name, params)
  else:
    assert isinstance(name_stack, str)
    eqn_str = name_stack + str_eqn_compact(primitive.name, params)
  tracebacks[eqn_str] = source_info.traceback
  frame = source_info_util.user_frame(source_info)
  return xc.OpMetadata(
        op_type=primitive.name,
        op_name=eqn_str,
        source_file=_get_canonical_source_file(frame) if frame else None,
        source_line=frame.line_num if frame else None)

# Utilities

def parameter(builder, num, shape, name=None, replicated=None):
  if name is None:
    name = ''
  if replicated is None:
    replicated = []
  elif isinstance(replicated, bool):
    replicated = [replicated] * shape.leaf_count()

  return xops.Parameter(builder, num,
                        shape.with_major_to_minor_layout_if_absent(), name,
                        replicated)

# HLO instructions optionally can be annotated to say how the output should be
# spatially partitioned (represented in XLA as OpSharding protos, see
# sharding_to_proto). For array outputs, the annotation is either an int per
# dimension specifying the number of ways that dimension divided (i.e. the total
# number of shards is the product), or None to indicate the array should be
# replicated. Tuple outputs are represented as tuples thereof. XLA supports
# arbitrary tuple nesting, but JAX only uses one level of tupling (and our type
# checkers don't support recursive types), so we only represent one level of
# nesting in this type definition.
SpatialSharding = Union[Tuple[int, ...],
                        None,
                        Tuple[Optional[Tuple[int, ...]], ...]]

def sharding_to_proto(sharding: SpatialSharding):
  """Converts a SpatialSharding to an OpSharding.

  See
  https://github.com/tensorflow/tensorflow/blob/main/tensorflow/compiler/xla/xla_data.proto#L601
  for details on the OpSharding proto.
  """
  proto = xc.OpSharding()
  if isinstance(sharding, tuple) and not isinstance(sharding[0], int):
    assert all(s is None or isinstance(s, tuple) for s in sharding)
    return tuple_sharding_proto(list(map(sharding_to_proto, sharding)))  # type: ignore

  if sharding is None:
    proto.type = xc.OpSharding.Type.REPLICATED
  else:
    proto.type = xc.OpSharding.Type.OTHER
    proto.tile_assignment_dimensions = list(sharding)  # type: ignore
    proto.tile_assignment_devices = list(range(np.product(sharding)))  # type: ignore
  return proto

def tuple_sharding_proto(elems):
  proto = xc.OpSharding()
  assert all(isinstance(e, type(proto)) for e in elems)
  proto.type = xc.OpSharding.Type.TUPLE
  proto.tuple_shardings = elems
  return proto


def set_sharding_proto(builder, op, sharding_proto, unspecified_dims=None):
  """Uses CustomCall to annotate a value as sharded."""
  # "Sharding" is a built-in custom call target that acts like an identity
  # function, and is used to attach an OpSharding to.
  def _create_custom_call(x):
    # unspecified_dims indicate dimensions whose shardings are not specified and
    # XLA sharding propagation can change them.
    if unspecified_dims:
      opaque = 'unspecified_dims=[' + ','.join(
          [str(i) for i in unspecified_dims]) + ']'
      opaque = bytes(opaque, 'utf-8')
      return xops.CustomCall(
          builder, b'Sharding', [x], builder.get_shape(x), opaque=opaque)
    else:
      return xops.CustomCall(builder, b'Sharding', [x], builder.get_shape(x))

  return with_sharding_proto(builder, sharding_proto, _create_custom_call, op)


def with_sharding_proto(builder, sharding_proto, op_fn, *args, **kwargs):
  """Builds op_fn(*args, **kwargs) with sharding annotation."""
  builder.set_sharding(sharding_proto)
  try:
    return op_fn(*args, **kwargs)
  finally:
    builder.clear_sharding()

def set_sharding(builder, op, sharding: SpatialSharding, unspecified_dims=None):
  """Uses CustomCall to annotate a value as sharded."""
  return set_sharding_proto(builder, op, sharding_to_proto(sharding),
                            unspecified_dims)

def with_sharding(builder, sharding: SpatialSharding, op_fn, *args, **kwargs):
  """Builds op_fn(*args, **kwargs) with sharding annotation."""
  return with_sharding_proto(builder, sharding_to_proto(sharding), op_fn, *args,
                             **kwargs)


### handlers

# Numpy dtypes -> XLA primitive types

_dtype_to_primitive_type: Dict[np.dtype, xc.PrimitiveType] = {
  np.dtype('bool'): xc.PrimitiveType.PRED,
  np.dtype('int8'): xc.PrimitiveType.S8,
  np.dtype('int16'): xc.PrimitiveType.S16,
  np.dtype('int32'): xc.PrimitiveType.S32,
  np.dtype('int64'): xc.PrimitiveType.S64,
  np.dtype('uint8'): xc.PrimitiveType.U8,
  np.dtype('uint16'): xc.PrimitiveType.U16,
  np.dtype('uint32'): xc.PrimitiveType.U32,
  np.dtype('uint64'): xc.PrimitiveType.U64,
  np.dtype(dtypes.bfloat16): xc.PrimitiveType.BF16,
  np.dtype('float16'): xc.PrimitiveType.F16,
  np.dtype('float32'): xc.PrimitiveType.F32,
  np.dtype('float64'): xc.PrimitiveType.F64,
  np.dtype('complex64'): xc.PrimitiveType.C64,
  np.dtype('complex128'): xc.PrimitiveType.C128,
}

def dtype_to_primitive_type(dtype: np.dtype) -> xc.PrimitiveType:
  """Converts a NumPy dtype into an XLA PrimitiveType."""
  # Many things (e.g., strings, scalar types) can be compared with NumPy dtypes,
  # but may not hash correctly. Make sure we have a true np.dtype.
  assert isinstance(dtype, np.dtype), type(dtype)
  try:
    return _dtype_to_primitive_type[dtype]
  except KeyError as err:
    raise TypeError(f"No XLA lowering for NumPy dtype: {dtype}") from err


# JAX abstract values -> XLA shapes

def aval_to_xla_shapes(aval: core.AbstractValue) -> Sequence[XlaShape]:
  try:
    return xla_shape_handlers[type(aval)](aval)
  except KeyError as err:
    raise TypeError(f"No xla_shape_handler for type: {type(aval)}") from err

xla_shape_handlers: Dict[Type[core.AbstractValue],
                         Callable[[Any], Sequence[XlaShape]]] = {
    core.AbstractUnit: _make_unit_shape,
    ShapedArray: _make_array_shape,
    ConcreteArray: _make_array_shape,
}
xla_shape_handlers[core.AbstractToken] = lambda _: (xc.Shape.token_shape(),)



# IR constants

_constant_handlers: Dict[type, Callable] = {}

def pyval_to_ir_constants(builder, py_val, canonicalize_types=True):
  """Translate a general constant `py_val` to a constant, canonicalizing its dtype.

  Args:
    py_val: a Python value to be translated to a constant.

  Returns:
    A representation of the constant as a list of xla ops.
  """
  for t in type(py_val).__mro__:
    handler = _constant_handlers.get(t)
    if handler: return handler(builder, py_val, canonicalize_types)
  if hasattr(py_val, '__jax_array__'):
    return pyval_to_ir_constants(builder, py_val.__jax_array__(),
                                 canonicalize_types)
  raise TypeError("No constant handler for type: {}".format(type(py_val)))

def pyval_to_ir_constant(builder, py_val, canonicalize_types=True):
  """Translate constant `py_val` to a constant, canonicalizing its dtype.

  Args:
    py_val: a Python value to be translated to a constant.

  Returns:
    A representation of the constant, either a ComputationDataHandle or None
  """
  const = pyval_to_ir_constants(builder, py_val, canonicalize_types=canonicalize_types)
  assert len(const) == 1, f"Internal error: cannot create constant from object of type {type(py_val)}"
  return const[0]


def register_constant_handler(type_, handler_fun):
  _constant_handlers[type_] = handler_fun

register_constant_handler(core.Unit, lambda c, *_: _make_unit_constant(c))


# TODO(mattjj,frostig): try to remove this function
def _normalize_to_xla_dtypes(val):
  """Normalize dtypes in a value."""
  if hasattr(val, '__array__') or np.isscalar(val):
    return np.asarray(val, dtype=dtypes.canonicalize_dtype(dtypes.result_type(val)))
  elif isinstance(val, (tuple, list)):
    return tuple(_normalize_to_xla_dtypes(x) for x in val)
  raise TypeError('Can\'t convert to XLA: {}'.format(val))

def _numpy_array_constant(builder, value, canonicalize_types=True):
  if canonicalize_types:
    value = _normalize_to_xla_dtypes(value)
  return [xops.Constant(builder, value)]


def _ndarray_constant_handler(c, val, canonicalize_types=True):
  """Constant handler for ndarray literals, handling zero-size strides.

  This function essentially calls _numpy_array_constant(val) except it has
  special handling of arrays with any strides of size zero: for those, it
  generates appropriate calls to NumpyArrayConstant, Broadcast, and Transpose
  to avoid staging in large literals that might arise from np.zeros or np.ones
  or the output of lax.broadcast (which uses np.broadcast_to which in turn
  uses size-zero strides).

  Args:
    c: an XlaBuilder
    val: an ndarray.

  Returns:
    An XLA ComputationDataHandle / XlaOp representing the constant ndarray
    staged into the XLA Computation.
  """
  # TODO(mattjj): revise this to use xops.BroadcastInDim rather than Transpose
  if dtypes.result_type(val) == dtypes.float0:
    return _numpy_array_constant(c, np.zeros(val.shape, dtype=np.bool_))
  elif np.any(np.equal(0, val.strides)) and val.size > 0:
    zero_stride_axes, = np.where(np.equal(0, val.strides))
    other_axes, = np.where(np.not_equal(0, val.strides))
    collapsed_val = val[tuple(0 if ax in zero_stride_axes else slice(None)
                              for ax in range(val.ndim))]
    xla_val = xops.Broadcast(
        _numpy_array_constant(c, collapsed_val, canonicalize_types)[0],
        np.take(val.shape, zero_stride_axes))
    permutation = np.argsort(tuple(zero_stride_axes) + tuple(other_axes))
    return [xops.Transpose(xla_val, permutation)]
  else:
    return _numpy_array_constant(c, val, canonicalize_types)
register_constant_handler(np.ndarray, _ndarray_constant_handler)


def _scalar_constant_handler(c, val, canonicalize_types=True):
  return _numpy_array_constant(c, val, canonicalize_types)

for scalar_type in [np.int8, np.int16, np.int32, np.int64,
                    np.uint8, np.uint16, np.uint32, np.uint64,
                    np.float16, np.float32, np.float64,
                    np.bool_, np.longlong,
                    dtypes.bfloat16]:
  register_constant_handler(scalar_type, _scalar_constant_handler)

# https://github.com/winpython/winpython/issues/613#issuecomment-380121523
if hasattr(np, "float128"):
  register_constant_handler(np.float128, _scalar_constant_handler)

def _python_scalar_handler(dtype, c, val, canonicalize_dtypes=True):
  return _numpy_array_constant(c, dtype.type(val))

for ptype, dtype in dtypes.python_scalar_dtypes.items():
  register_constant_handler(ptype, partial(_python_scalar_handler, dtype))

def _device_array_constant_handler(c, val, canonicalize_types=True):
  return pyval_to_ir_constants(c, val.device_buffer.to_py())
for t in device_array.device_array_types:
  register_constant_handler(t, _device_array_constant_handler)


register_constant_handler(core.Token, lambda c, _, __: [xops.CreateToken(c)])

# TODO(mattjj): try to remove this canonicalize_dtype stuff
def canonicalize_dtype(x):
  typ = type(x)
  handler = canonicalize_dtype_handlers.get(typ)
  if handler: return handler(x)
  for typ in typ.__mro__:
    handler = canonicalize_dtype_handlers.get(typ)
    if handler: return handler(x)
  if hasattr(x, '__jax_array__'):
    return canonicalize_dtype(x.__jax_array__())
  raise TypeError(f"No canonicalize_dtype handler for type: {type(x)}")

def _canonicalize_ndarray_dtype(x):
  return np.asarray(x, dtypes.canonicalize_dtype(dtypes.result_type(x)))

def _canonicalize_python_scalar_dtype(typ, x):
  return np.asarray(
      x, dtypes.canonicalize_dtype(dtypes._scalar_type_to_dtype(typ, x)))

canonicalize_dtype_handlers: Dict[Any, Callable] = {core.Unit: identity}
for t in device_array.device_array_types:
  canonicalize_dtype_handlers[t] = lambda x: x
canonicalize_dtype_handlers.update(
    (t, _canonicalize_ndarray_dtype) for t in array_types)
canonicalize_dtype_handlers.update(
    (t, partial(_canonicalize_python_scalar_dtype, t)) for t in _scalar_types)
canonicalize_dtype_handlers[core.Token] = lambda x: x

def abstractify(x) -> core.AbstractValue:
  typ = type(x)
  aval_fn = pytype_aval_mappings.get(typ)
  if aval_fn: return aval_fn(x)
  for typ in typ.__mro__:
    aval_fn = pytype_aval_mappings.get(typ)
    if aval_fn: return aval_fn(x)
  if hasattr(x, '__jax_array__'):
    return abstractify(x.__jax_array__())
  raise TypeError(f"Argument '{x}' of type '{type(x)}' is not a valid JAX type")

def _make_abstract_python_scalar(typ, val):
  return ShapedArray((), dtypes._scalar_type_to_dtype(typ, val), weak_type=True)

pytype_aval_mappings: Dict[Any, Callable[[Any], core.AbstractValue]] = {
    core.Unit: lambda _: core.abstract_unit,
}
for t in device_array.device_array_types:
  pytype_aval_mappings[t] = operator.attrgetter('aval')
pytype_aval_mappings[core.Token] = lambda _: core.abstract_token
pytype_aval_mappings.update((t, make_shaped_array) for t in array_types)
pytype_aval_mappings.update(
    (t, partial(_make_abstract_python_scalar, t)) for t in _scalar_types)


def primitive_subcomputation(platform: str, axis_env: 'AxisEnv',
                             prim: core.Primitive,
                             *avals: core.AbstractValue, **params):
  c = xc.XlaBuilder(f"primitive_computation_{prim.name}")
  xla_args, _ = _xla_callable_args(c, avals, tuple_args=False,
                                   filter_tokens=False)
  ctx = TranslationContext(builder=c, platform=platform, axis_env=axis_env,
                           name_stack=new_name_stack())
  wrapped_fun = lu.wrap_init(prim.bind, params)
  if not prim.multiple_results:
    wrapped_fun = _tuple_output(wrapped_fun)
  with core.extend_axis_env_nd(zip(ctx.axis_env.names, ctx.axis_env.sizes)):
    jaxpr, _, consts = pe.trace_to_jaxpr_dynamic(wrapped_fun, avals)
  ans = _jaxpr_subcomp(ctx, jaxpr, _xla_consts(ctx.builder, consts),
                       *xla_args)
  if prim.multiple_results:
    return c.build(xops.Tuple(c, ans))
  else:
    x, = ans
    return c.build(x)


# Used within _xla_callable_args and _xla_param to distinguish between None (no
# sharding annotation set) and replicated.
_replicated_param = object()

def _token_param_shape():
  """Shape used in place of tokens as top-level computation arguments."""
  return xc.Shape.array_shape(np.dtype(np.bool_), [])

def _make_token_return_value(c):
  """Value used in place of tokens as a top-level computation return value."""
  return xops.Constant(c, np.zeros((), dtype=np.dtype(np.bool_)))

def _xla_callable_args(
    c, avals, tuple_args, *,
    replicated=None,
    partitions=None,
    partitions_proto: bool = False,
    donated_invars=None,
    filter_tokens=True):
  assert partitions is None or len(partitions) == len(avals)
  if not tuple_args:
    if replicated is None:
      replicated = [None] * len(avals)
    if partitions is None:
      parts: List[object] = [None] * len(avals)
    elif partitions_proto:
      parts = partitions
    else:
      parts = [_replicated_param if part is None else part
               for part in partitions]
    counts = it.count()
    xla_args = [_xla_param(c, next(counts), xla_shape, r, p, partitions_proto,
                           filter_tokens)
                for (a, r, p) in safe_zip(avals, replicated, parts)
                for xla_shape in aval_to_xla_shapes(a)]
    if donated_invars is not None:
      donated_invars = [
          d for (a, _, _, d) in zip(avals, replicated, parts, donated_invars)
          for xla_shape in aval_to_xla_shapes(a)]
    return xla_args, donated_invars
  else:
    if replicated is not None:
      replicated = [r for a, r in zip(avals, replicated)
                    if a is not abstract_token]
    if partitions is None:
      tuple_parts = None
    elif partitions_proto:
      tuple_parts = tuple_sharding_proto(partitions)
    else:
      tuple_parts = tuple(partitions)
    tuple_shape = xc.Shape.tuple_shape(
        [shape if not (filter_tokens and a is abstract_token)
         else _token_param_shape()
         for a in avals for shape in aval_to_xla_shapes(a)])
    tuple_param = _xla_param(c, 0, tuple_shape, replicated, tuple_parts,
                             partitions_proto, filter_tokens)
    xla_args = [v if not (filter_tokens and a is abstract_token)
                else xops.CreateToken(c)
                for a, v in zip(avals, xla_destructure(c, tuple_param))]
    return xla_args, donated_invars

def _xla_param(builder, param_num, xla_shape, replicated, partitions,
               parts_proto, filter_tokens):
  is_token = xla_shape.is_token()
  if filter_tokens and is_token:
    xla_shape = _token_param_shape()
  make_param = partial(parameter, builder, param_num, xla_shape,
                       replicated=replicated)
  with_sharding_fn = with_sharding_proto if parts_proto else with_sharding
  if partitions is None:
    out = make_param()
  elif partitions is _replicated_param:
    out = with_sharding_fn(builder, None, make_param)
  else:
    out = with_sharding_fn(builder, partitions, make_param)
  if filter_tokens and is_token:
    out = xops.CreateToken(builder)
  return out


### compiling jaxprs


def _flatmap(func: Callable, vars: Sequence):
  return list(it.chain.from_iterable(map(func, vars)))

def _partitionmap(func: Callable, vars: Sequence, nodes: Sequence):
  return map(func, vars,
             util.unflatten(nodes,
                            [len(aval_to_xla_shapes(v.aval)) for v in vars]))

class AxisEnv(NamedTuple):
  """Represents a pmap mesh (only along the replica axes)."""
  nreps: int
  names: Tuple[Any, ...]
  sizes: Tuple[int, ...]

@dataclasses.dataclass
class TranslationContext:
  builder: xc.XlaBuilder
  # TODO(phawkins): make platform non-optional. We should always be translating
  # with a specific platform in mind.
  platform: Optional[str]
  axis_env: AxisEnv
  name_stack: Union[str, source_info_util.NameStack]

  def replace(self, **kw): return dataclasses.replace(self, **kw)


def _jaxpr_subcomp(ctx: TranslationContext, jaxpr: core.Jaxpr,
                   consts: Sequence[XlaOp], *args: XlaOp) -> Sequence[XlaOp]:
  assert ctx.platform is not None
  def read(v):
    if type(v) is Literal:
      return pyval_to_ir_constants(ctx.builder, canonicalize_dtype(v.val))
    else:
      return env[v]

  def aval(v):
    if type(v) is Literal:
      return abstractify(v.val)
    else:
      return v.aval

  def write(v, node):
    assert node is not None
    env[v] = node

  env: Dict[core.Var, Sequence[XlaOp]] = {}
  _partitionmap(write, [core.unitvar],
                pyval_to_ir_constants(ctx.builder, core.unit))
  _partitionmap(write, jaxpr.constvars, consts)
  _partitionmap(write, jaxpr.invars, args)
  for eqn in jaxpr.eqns:
    if config.jax_experimental_name_stack:
      assert isinstance(ctx.name_stack, source_info_util.NameStack), type(ctx.name_stack)
      source_info = eqn.source_info.replace(
          name_stack=ctx.name_stack + eqn.source_info.name_stack)
    else:
      source_info = eqn.source_info
    op_metadata = make_op_metadata(
        eqn.primitive, eqn.params, name_stack=ctx.name_stack,
        source_info=source_info)
    ctx.builder.set_op_metadata(op_metadata)
    in_nodes = _flatmap(read, eqn.invars)
    if (ctx.platform is not None and
        eqn.primitive in _backend_specific_translations[ctx.platform]):
      rule = _backend_specific_translations[ctx.platform][eqn.primitive]
    elif eqn.primitive in _translations:
      rule = _translations[eqn.primitive]
    else:
      raise NotImplementedError(
          f"XLA translation rule for primitive '{eqn.primitive.name}' not found")

    with source_info_util.user_context(eqn.source_info.traceback):
      eqn_ctx = (ctx.replace(name_stack=source_info.name_stack) if
          config.jax_experimental_name_stack else ctx)
      ans = rule(eqn_ctx, map(aval, eqn.invars), map(aval, eqn.outvars),
                 *in_nodes, **eqn.params)

    assert isinstance(ans, collections.abc.Sequence), (ans, eqn)
    assert all(isinstance(x, xe.XlaOp) for x in ans), (ans, eqn)
    map(ctx.builder.get_shape, ans)  # force xla to do shape error checking
    ctx.builder.clear_op_metadata()
    _partitionmap(write, eqn.outvars, ans)
  return _flatmap(read, jaxpr.outvars)


def xla_destructure(c, ans):
  num_elements = len(c.get_shape(ans).tuple_shapes())
  return [xops.GetTupleElement(ans, i) for i in range(num_elements)]

def check_backend_matches(inner_backend, outer_backend):
  # For nested calls, the outermost call sets the backend for all inner calls;
  # it's an error if the inner call has a conflicting explicit backend spec.
  if inner_backend and inner_backend != outer_backend:
    raise ValueError(
        f"Outer-jit backend specification {outer_backend} must match explicit "
        f"inner-jit backend specification {inner_backend}.")


def extend_axis_env(env: AxisEnv, name, size: int):
  return AxisEnv(env.nreps, env.names + (name,), env.sizes + (size,))

def axis_read(axis_env, axis_name):
  try:
    return max(i for i, name in enumerate(axis_env.names) if name == axis_name)
  except ValueError:
    raise NameError("unbound axis name: {}".format(axis_name)) from None

def axis_groups(axis_env: AxisEnv, name) -> Tuple[Tuple[int, ...]]:
  if not isinstance(name, (list, tuple)):
    name = (name,)
  mesh_axes = tuple(unsafe_map(partial(axis_read, axis_env), name))
  trailing_size, ragged = divmod(axis_env.nreps, prod(axis_env.sizes))
  assert not ragged
  mesh_spec = axis_env.sizes + (trailing_size,)
  return _axis_groups(mesh_spec, mesh_axes)

def _axis_groups(mesh_spec, mesh_axes):
  """Computes replica group ids for a collective performed over a subset of the mesh.

  Args:
    mesh_spec: A sequence of integers representing the mesh shape.
    mesh_axes: A sequence of integers between 0 and `len(mesh_spec)` (exclusive)
      indicating over which axes the collective is performed.
  Returns:
    A tuple of replica groups (i.e. tuples containing replica ids).
  """
  iota = np.arange(prod(mesh_spec)).reshape(mesh_spec)
  groups = np.reshape(
      np.moveaxis(iota, mesh_axes, np.arange(len(mesh_axes))),
      (prod(np.take(mesh_spec, mesh_axes)), -1))
  return tuple(unsafe_map(tuple, groups.T))


# TODO(mattjj,skyewm): the functions here are utilities for checking if
# not-yet-supported features are used with multi-host programming


def jaxpr_collectives(jaxpr):
  """Generates all the collective primitives anywhere inside a Jaxpr."""
  for eqn in jaxpr.eqns:
    if eqn.primitive in _collective_primitives:
      yield eqn.primitive
  for subjaxpr in core.subjaxprs(jaxpr): yield from jaxpr_collectives(subjaxpr)


### xla_call underlying jit



def _xla_consts(c, consts):
  unique_consts = {id(const): const for const in consts}
  xla_consts = {
      id_: pyval_to_ir_constants(c, const) for id_, const in unique_consts.items()}
  return [c for const in consts for c in xla_consts[id(const)]]




xla_call_p: core.CallPrimitive = core.CallPrimitive('xla_call')
xla_call = xla_call_p.bind

def _xla_call_partial_eval_update_params(params, kept_inputs, num_new_inputs):
  donated_invars = params['donated_invars']
  if not kept_inputs and donated_invars:
    # JaxprTrace.post_process_call creates a call with no input tracers
    donated_invars = (False,) * num_new_inputs
  else:
    assert len(kept_inputs) == len(donated_invars)
    # JaxprTrace.process_call drops known input tracers
    donated_invars = [d for d, kept in zip(donated_invars, kept_inputs) if kept]
    # Any new inputs are prepended to the left, so mark those as not donated.
    donated_invars = [False] * num_new_inputs + donated_invars
  return dict(params, donated_invars=tuple(donated_invars))
pe.call_param_updaters[xla_call_p] = _xla_call_partial_eval_update_params

def _xla_call_jvp_update_params(params, nz_tangents):
  donated_invars = params['donated_invars']
  donated_tangents = [d for d, nz in zip(donated_invars, nz_tangents) if nz]
  new_donated_invars = (*donated_invars, *donated_tangents)
  return dict(params, donated_invars=new_donated_invars)
ad.call_param_updaters[xla_call_p] = _xla_call_jvp_update_params

def _xla_call_transpose_update_params(params, undef_primals, nonzero_cts):
  donated_invars = params['donated_invars']
  donated_primals = [d for d, u in zip(donated_invars, undef_primals) if not u]
  donated_cotangents = [False for nz in nonzero_cts if nz]
  return dict(params, donated_invars=(*donated_primals, *donated_cotangents))
ad.call_transpose_param_updaters[xla_call_p] = _xla_call_transpose_update_params


ad.primitive_transposes[xla_call_p] = partial(ad.call_transpose, xla_call_p)


def _xla_call_partial_eval_custom_params_updater(
    unks_in: Sequence[bool],
    kept_outs_known: Sequence[bool], kept_outs_staged: Sequence[bool],
    num_res: int, params_known: dict, params_staged: dict
  ) -> Tuple[dict, dict]:
  # pruned inputs to jaxpr_known according to unks_in, so prune donated_invars
  donated_invars_known, _ = partition_list(unks_in, params_known['donated_invars'])
  new_params_known = dict(params_known, donated_invars=tuple(donated_invars_known))
  # added num_res new inputs to jaxpr_staged, so extend donated_invars
  donated_invars_staged = [*([False] * num_res), *params_staged['donated_invars']]
  new_params_staged = dict(params_staged, donated_invars=tuple(donated_invars_staged))
  return new_params_known, new_params_staged
pe.partial_eval_jaxpr_custom_rules[xla_call_p] = \
    partial(pe.call_partial_eval_custom_rule, 'call_jaxpr',
            _xla_call_partial_eval_custom_params_updater)
pe.dce_rules[xla_call_p] = pe.dce_jaxpr_call_rule

pe.padding_rules[xla_call_p] = partial(pe.call_padding_rule, xla_call_p)


def _pp_xla_call(eqn: core.JaxprEqn, context: core.JaxprPpContext,
                 settings: core.JaxprPpSettings,
                 ) -> List[pp.Doc]:
  printed_params = {k:v for k, v in eqn.params.items() if
                    k == 'call_jaxpr' or k == 'name' or
                    k == 'backend' and v is not None or
                    k == 'device' and v is not None or
                    k == 'donated_invars' and any(v)}
  return [pp.text(eqn.primitive.name),
          core.pp_kv_pairs(sorted(printed_params.items()), context, settings),
          pp.text(" ") + core.pp_vars(eqn.invars, context)]
core.pp_eqn_rules[xla_call_p] = _pp_xla_call


### translation tables

MYPY = False
if not MYPY:
  class TranslationRule(Protocol):
    def __call__(self, ctx: TranslationContext,
                 avals_in: Sequence[core.AbstractValue],
                 avals_out: Sequence[core.AbstractValue],
                 *args: XlaOp, **kw
                ) -> Sequence[XlaOp]:
      """A translation rule lowers a primitive invocation into an XLA HLO."""
else:
  TranslationRule = Any

_translations: Dict[core.Primitive, TranslationRule] = {}
_backend_specific_translations: Dict[str, Dict[core.Primitive, TranslationRule]]
_backend_specific_translations = defaultdict(dict)

_collective_primitives: Set[core.Primitive] = set()
_initial_style_primitives: Set[core.Primitive] = set()

def register_initial_style_primitive(prim: core.Primitive):
  _initial_style_primitives.add(prim)

def register_collective_primitive(prim: core.Primitive):
  _collective_primitives.add(prim)

def register_translation(prim: core.Primitive, rule: TranslationRule, *,
                         platform: Optional[str] = None) -> None:
  ts = (_translations if platform is None
        else _backend_specific_translations[platform])
  ts[prim] = rule

# As a temporary backward compatibility measure, we use an adapter class to
# convert from the old styles of translation rules to the newer ones.
# TODO(phawkins): update users of the older translation rule styles and remove
# the adapters.
class _TranslationRuleAdapter:
  def __init__(self, translations,
               wrap_fn: Callable[[core.Primitive, Callable], TranslationRule]):
    self._translations = translations
    self._wrap_fn = wrap_fn

  def __setitem__(self, key: core.Primitive, value: Callable):
    self._translations[key] = self._wrap_fn(key, value)


def _wrap_old_translation(prim: core.Primitive, f: Callable) -> TranslationRule:
  @functools.wraps(f)
  def wrapped(ctx: TranslationContext, avals_in: Sequence[core.AbstractValue],
              avals_out: Sequence[core.AbstractValue],
               *args: XlaOp, **kw) -> Sequence[XlaOp]:
    ans = f(ctx.builder, *args, **kw)
    if (prim.multiple_results or
        any(len(aval_to_xla_shapes(aval)) > 1 for aval in avals_out)):
      return xla_destructure(ctx.builder, ans)
    else:
      return [ans]
  return wrapped


def _wrap_old_call_translation(prim: core.Primitive,
                               f: Callable) -> TranslationRule:
  @functools.wraps(f)
  def wrapped(ctx: TranslationContext, avals_in: Sequence[core.AbstractValue],
              avals_out: Sequence[core.AbstractValue],
               *args: XlaOp, **kw) -> Sequence[XlaOp]:
    platform = kw.pop("backend", None)
    check_backend_matches(platform, ctx.platform)
    ans = f(ctx.builder, ctx.axis_env, args, ctx.name_stack,
            backend=ctx.platform, **kw)
    if (prim.multiple_results or
        any(len(aval_to_xla_shapes(aval)) > 1 for aval in avals_out)):
      return xla_destructure(ctx.builder, ans)
    else:
      return [ans]
  return wrapped

translations : _TranslationRuleAdapter
translations = _TranslationRuleAdapter(_translations, _wrap_old_translation)

class _BackendSpecificTranslationsAdapter(defaultdict):
  def __missing__(self, key):
    ret = self[key] = _TranslationRuleAdapter(
        _backend_specific_translations[key], _wrap_old_translation)
    return ret

backend_specific_translations: Dict[str, _TranslationRuleAdapter]
backend_specific_translations = _BackendSpecificTranslationsAdapter()
call_translations : _TranslationRuleAdapter
call_translations = _TranslationRuleAdapter(
    _translations, _wrap_old_call_translation)



@lu.transformation
def _tuple_output(*args, **kwargs):
  ans = yield args, kwargs
  yield (ans,)

# TODO(phawkins): remove lower_fun completely after updating users.
def lower_fun(fun: Callable, *, multiple_results: bool, backend=None,
              new_style: bool = False) -> Callable:
  def f(*args, **kw):
    raise RuntimeError("XLA translation rules are deprecated and "
                       "jax.interpreters.xla.lower_fun is no longer supported. "
                       "Add an MLIR (MHLO) lowering via jax.interpreters.mlir "
                       "instead.")
  return f


ad.primitive_transposes[core.named_call_p] = partial(ad.call_transpose,
                                                     core.named_call_p)
