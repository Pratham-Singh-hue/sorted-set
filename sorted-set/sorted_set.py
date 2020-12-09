from bisect import bisect_left
from collections.abc import Sequence, Set
from itertools import chain

class SortedSet(Sequence, Set):
    # we have implemented all methods from the Sequence class
    # except __reversed__() which implicitly gets implemented
    # by __len__() and __getitem__() methods so we can remove the
    # inheritance from Sequence class
    def __init__(self, item=None):
        self._item = sorted(set(item)) if item is not None else []

    def __contains__(self, item):
        try:
            self.index(item)
            return True
        except ValueError:
            return False

    def __len__(self):
        return len(self._item)

    def __iter__(self):
        return iter(self._item)

    def __getitem__(self, item):
        result = self._item[item]
        return SortedSet(result) if isinstance(item, slice) else result

    def __repr__(self):
        return "SortedSet({})".format(
            repr(self._item) if self._item else ''
        )

    def __eq__(self, rhs):
        if not isinstance(rhs, SortedSet):
            return NotImplemented
        return self._item == rhs._item

    def __ne__(self, rhs):
        if not isinstance(rhs, SortedSet):
            return NotImplemented
        return self._item != rhs._item

    def _is_unique_and_sorted(self):
        return all(self[i] < self[i+1] for i in range(len(self)-1))

    def index(self, item):
        assert self._is_unique_and_sorted(), "not unique and sorted"
        index = bisect_left(self._item, item)

        if (index != len(self._item)) and (self._item[index] == item):
            return index
        raise ValueError("{} not found".format(repr(item)))

    def count(self, item):
        assert self._is_unique_and_sorted(), "not unique and sorted"
        return int(item in self)

    def __add__(self, rhs):
        return SortedSet(chain(self._item, rhs._item))

    def __mul__(self, rhs):
        return self if rhs>0 else SortedSet()

    def __rmul__(self, lhs):
        return self * lhs

    def issubset(self, iterable):
        return self <= SortedSet(iterable)

    def issuperset(self, iterable):
        return self >= SortedSet(iterable)

    def intersection(self, iterable):
        return self & SortedSet(iterable)

    def union(self, iterable):
        return self | SortedSet(iterable)

    def symmetric_difference(self, iterable):
        return self ^ SortedSet(iterable)

    def difference(self, iterable):
        return self - SortedSet(iterable)