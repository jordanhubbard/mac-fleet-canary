"""Disjoint-set data structure with path compression and union by rank."""

from collections.abc import Hashable, Iterable
from typing import Generic, TypeVar


T = TypeVar("T", bound=Hashable)


class UnionFind(Generic[T]):
    """Maintain disjoint sets of hashable values.

    Values supplied at construction, or first passed to any operation, are
    added as singleton sets.
    """

    def __init__(self, values: Iterable[T] = ()) -> None:
        self._parent: dict[T, T] = {}
        self._rank: dict[T, int] = {}
        for value in values:
            self._add(value)

    def _add(self, value: T) -> None:
        if value not in self._parent:
            self._parent[value] = value
            self._rank[value] = 0

    def find(self, value: T) -> T:
        """Return the representative of the set containing ``value``."""
        self._add(value)

        root = value
        while True:
            parent = self._parent[root]
            if parent is root:
                break
            root = parent

        while True:
            parent = self._parent[value]
            if parent is value:
                break
            self._parent[value] = root
            value = parent
        return root

    def union(self, first: T, second: T) -> bool:
        """Merge two sets, returning whether they were previously separate."""
        first_root = self.find(first)
        second_root = self.find(second)
        if first_root is second_root:
            return False

        if self._rank[first_root] < self._rank[second_root]:
            first_root, second_root = second_root, first_root
        self._parent[second_root] = first_root
        if self._rank[first_root] == self._rank[second_root]:
            self._rank[first_root] += 1
        return True

    def connected(self, first: T, second: T) -> bool:
        """Return whether two values belong to the same set."""
        return self.find(first) is self.find(second)
