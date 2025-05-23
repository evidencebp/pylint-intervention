"""
The util_indexable module defines ``IndexableWalker`` which is a powerful
way to iterate through nested Python containers.
"""
import sys
from math import isclose
from collections.abc import Generator


class IndexableWalker(Generator):
    """
    Traverses through a nested tree-liked indexable structure.

    Generates a path and value to each node in the structure. The path is a
    list of indexes which if applied in order will reach the value.

    The ``__setitem__`` method can be used to modify a nested value based on the
    path returned by the generator.

    When generating values, you can use "send" to prevent traversal of a
    particular branch.

    RelatedWork:
        * https://pypi.org/project/python-benedict/ - implements a dictionary
            subclass with similar nested indexing abilities.

    Example:
        >>> # Given Nested Data
        >>> data = {
        >>>     'foo': {'bar': 1},
        >>>     'baz': [{'biz': 3}, {'buz': [4, 5, 6]}],
        >>> }
        >>> # Create an IndexableWalker
        >>> walker = IndexableWalker(data)
        >>> # We iterate over the data as if it was flat
        >>> # ignore the <want> string due to order issues on older Pythons
        >>> # xdoctest: +IGNORE_WANT
        >>> for path, val in walker:
        >>>     print(path)
        ['foo']
        ['baz']
        ['baz', 0]
        ['baz', 1]
        ['baz', 1, 'buz']
        ['baz', 1, 'buz', 0]
        ['baz', 1, 'buz', 1]
        ['baz', 1, 'buz', 2]
        ['baz', 0, 'biz']
        ['foo', 'bar']
        >>> # We can use "paths" as keys to getitem into the walker
        >>> path = ['baz', 1, 'buz', 2]
        >>> val = walker[path]
        >>> assert val == 6
        >>> # We can use "paths" as keys to setitem into the walker
        >>> assert data['baz'][1]['buz'][2] == 6
        >>> walker[path] = 7
        >>> assert data['baz'][1]['buz'][2] == 7
        >>> # We can use "paths" as keys to delitem into the walker
        >>> assert data['baz'][1]['buz'][1] == 5
        >>> del walker[['baz', 1, 'buz', 1]]
        >>> assert data['baz'][1]['buz'][1] == 7

    Example:
        >>> # Create nested data
        >>> # xdoctest: +REQUIRES(module:numpy)
        >>> import numpy as np
        >>> import ubelt as ub
        >>> data = ub.ddict(lambda: int)
        >>> data['foo'] = ub.ddict(lambda: int)
        >>> data['bar'] = np.array([1, 2, 3])
        >>> data['foo']['a'] = 1
        >>> data['foo']['b'] = np.array([1, 2, 3])
        >>> data['foo']['c'] = [1, 2, 3]
        >>> data['baz'] = 3
        >>> print('data = {}'.format(ub.repr2(data, nl=True)))
        >>> # We can walk through every node in the nested tree
        >>> walker = IndexableWalker(data)
        >>> for path, value in walker:
        >>>     print('walk path = {}'.format(ub.repr2(path, nl=0)))
        >>>     if path[-1] == 'c':
        >>>         # Use send to prevent traversing this branch
        >>>         got = walker.send(False)
        >>>         # We can modify the value based on the returned path
        >>>         walker[path] = 'changed the value of c'
        >>> print('data = {}'.format(ub.repr2(data, nl=True)))
        >>> assert data['foo']['c'] == 'changed the value of c'

    Example:
        >>> # Test sending false for every data item
        >>> # xdoctest: +REQUIRES(module:numpy)
        >>> import ubelt as ub
        >>> import numpy as np
        >>> data = {1: 1}
        >>> walker = IndexableWalker(data)
        >>> for path, value in walker:
        >>>     print('walk path = {}'.format(ub.repr2(path, nl=0)))
        >>>     walker.send(False)
        >>> data = {}
        >>> walker = IndexableWalker(data)
        >>> for path, value in walker:
        >>>     walker.send(False)
    """

    def __init__(self, data, dict_cls=(dict,), list_cls=(list, tuple)):
        self.data = data
        self.dict_cls = dict_cls
        self.list_cls = list_cls
        self.indexable_cls = self.dict_cls + self.list_cls

        self._walk_gen = None

    def __iter__(self):
        """
        Iterates through the indexable ``self.data``

        Can send a False flag to prevent a branch from being traversed

        Returns:
            Generator[Tuple[List, Any], Any, Any]:
                path (List): list of index operations to arrive at the value
                value (object): the value at the path
        """
        return self

    def __next__(self):
        """ returns next item from this generator """
        if self._walk_gen is None:
            self._walk_gen = self._walk()
        return next(self._walk_gen)

    def next(self):  # nocover
        # For Python 2.7
        return self.__next__()

    def send(self, arg):
        """
        send(arg) -> send 'arg' into generator,
        return next yielded value or raise StopIteration.
        """
        # Note: this will error if called before __next__
        self._walk_gen.send(arg)

    def throw(self, type=None, value=None, traceback=None):
        """
        throw(typ[,val[,tb]]) -> raise exception in generator,
        return next yielded value or raise StopIteration.
        """
        raise StopIteration

    def __setitem__(self, path, value):
        """
        Set nested value by path

        Args:
            path (List): list of indexes into the nested structure
            value (object): new value
        """
        d = self.data
        prefix, key = path[:-1], path[-1]
        # *prefix, key = path
        for k in prefix:
            d = d[k]
        d[key] = value

    def __getitem__(self, path):
        """
        Get nested value by path

        Args:
            path (List): list of indexes into the nested structure

        Returns:
            value
        """
        d = self.data
        prefix, key = path[:-1], path[-1]
        # *prefix, key = path
        for k in prefix:
            d = d[k]
        return d[key]

    def __delitem__(self, path):
        """
        Remove nested value by path

        Note:
            It can be dangerous to use this while iterating (because we may try
            to descend into a deleted location) or on leaf items that are
            list-like (because the indexes of all subsequent items will be
            modified).

        Args:
            path (List): list of indexes into the nested structure.
                The item at the last index will be removed.
        """
        d = self.data
        prefix, key = path[:-1], path[-1]
        # *prefix, key = path
        for k in prefix:
            d = d[k]
        del d[key]

    def _walk(self, data=None, prefix=[]):
        """
        Defines the underlying generator used by IndexableWalker

        Yields:
            Tuple[List, object] | None:
                path (List) - a "path" through the nested data structure
                value (object) - the value indexed by that "path".

            Can also yield None in the case that `send` is called on the
            generator.
        """
        if data is None:  # pragma: nobranch
            data = self.data
        stack = [(data, prefix)]
        while stack:
            _data, _prefix = stack.pop()
            # Create an items iterable of depending on the indexable data type
            if isinstance(_data, self.list_cls):
                items = enumerate(_data)
            elif isinstance(_data, self.dict_cls):
                items = _data.items()
            else:
                raise TypeError(type(_data))

            for key, value in items:
                # Yield the full path to this position and its value
                path = _prefix + [key]
                message = yield path, value
                # If the value at this path is also indexable, then continue
                # the traversal, unless the False message was explicitly sent
                # by the caller.
                if message is False:
                    # Because the `send` method will return the next value,
                    # we yield a dummy value so we don't clobber the next
                    # item in the traversal.
                    yield None
                else:
                    if isinstance(value, self.indexable_cls):
                        stack.append((value, path))


def indexable_allclose(dct1, dct2, rel_tol=1e-9, abs_tol=0.0, return_info=False):
    """
    Walks through two nested data structures and ensures that everything is
    roughly the same.

    Args:
        dct1 (dict):
            a nested indexable item

        dct2 (dict):
            a nested indexable item

        rel_tol (float):
            maximum difference for being considered "close", relative to the
            magnitude of the input values

        abs_tol (float):
            maximum difference for being considered "close", regardless of the
            magnitude of the input values

        return_info (bool, default=False): if true, return extra info

    Returns:
        bool | Tuple[bool, Dict] :
            A boolean result if ``return_info`` is false, otherwise a tuple of
            the boolean result and an "info" dict containing detailed results
            indicating what matched and what did not.

    Example:
        >>> import ubelt as ub
        >>> dct1 = {
        >>>     'foo': [1.222222, 1.333],
        >>>     'bar': 1,
        >>>     'baz': [],
        >>> }
        >>> dct2 = {
        >>>     'foo': [1.22222, 1.333],
        >>>     'bar': 1,
        >>>     'baz': [],
        >>> }
        >>> flag, return_info =  ub.indexable_allclose(dct1, dct2, return_info=True)
        >>> print('return_info = {}'.format(ub.repr2(return_info, nl=1)))
        >>> print('flag = {!r}'.format(flag))

        >>> walker1 = return_info['walker1']
        >>> for p1, v1, v2  in return_info['faillist']:
        >>>     v1_ = walker1[p1]
        >>>     print('*fail p1, v1, v2 = {}, {}, {}'.format(p1, v1, v2))
        >>> for p1 in return_info['passlist']:
        >>>     v1_ = walker1[p1]
        >>>     print('*pass p1, v1_ = {}, {}'.format(p1, v1_))
        >>> assert not flag

        >>> import ubelt as ub
        >>> dct1 = {
        >>>     'foo': [1.0000000000000000000000001, 1.],
        >>>     'bar': 1,
        >>>     'baz': [],
        >>> }
        >>> dct2 = {
        >>>     'foo': [0.9999999999999999, 1.],
        >>>     'bar': 1,
        >>>     'baz': [],
        >>> }
        >>> flag, return_info =  ub.indexable_allclose(dct1, dct2, return_info=True)
        >>> print('return_info = {}'.format(ub.repr2(return_info, nl=1)))
        >>> print('flag = {!r}'.format(flag))

    Example:
        >>> import ubelt as ub
        >>> flag, return_info =  ub.indexable_allclose([], [], return_info=True)
        >>> print('return_info = {!r}'.format(return_info))
        >>> print('flag = {!r}'.format(flag))

    Example:
        >>> import ubelt as ub
        >>> flag =  ub.indexable_allclose([], [], return_info=False)
        >>> print('flag = {!r}'.format(flag))

    Example:
        >>> import ubelt as ub
        >>> flag, return_info =  ub.indexable_allclose([], [1], return_info=True)
        >>> print('return_info = {!r}'.format(return_info))
        >>> print('flag = {!r}'.format(flag))
    """
    walker1 = IndexableWalker(dct1)
    walker2 = IndexableWalker(dct2)
    flat_items1 = [
        (path, value) for path, value in walker1
        if not isinstance(value, walker1.indexable_cls) or len(value) == 0]
    flat_items2 = [
        (path, value) for path, value in walker2
        if not isinstance(value, walker1.indexable_cls) or len(value) == 0]

    flat_items1 = sorted(flat_items1)
    flat_items2 = sorted(flat_items2)

    if len(flat_items1) != len(flat_items2):
        info = {
            'faillist': ['length mismatch']
        }
        final_flag = False
    else:
        passlist = []
        faillist = []

        for t1, t2 in zip(flat_items1, flat_items2):
            p1, v1 = t1
            p2, v2 = t2
            assert p1 == p2

            flag = (v1 == v2)
            if not flag:
                if isinstance(v1, float) and isinstance(v2, float) and isclose(v1, v2):
                    flag = True
            if flag:
                passlist.append(p1)
            else:
                faillist.append((p1, v1, v2))

        final_flag = len(faillist) == 0
        info = {
            'passlist': passlist,
            'faillist': faillist,
        }

    if return_info:
        info.update({
            'walker1': walker1,
            'walker2': walker2,
        })
        return final_flag, info
    else:
        return final_flag


