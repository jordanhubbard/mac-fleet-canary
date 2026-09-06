"""Disjoint-set data structure with path compression and union by rank."""

from collections.abc import Hashable
from typing import Generic, TypeVar


T = TypeVar("T", bound=Hashable)


class UnionFind(Generic[T]):
    """Maintain disjoint sets of hashable values."""

    def __init__(self) -> None:
        self._parent: dict[T, T] = {}
        self._rank: dict[T, int] = {}

    @staticmethod
    def _same(left: T, right: T) -> bool:
        return left is right or left == right

    def find(self, value: T) -> T:
        """Return the representative for value, adding value if necessary."""
        if value not in self._parent:
            self._parent[value] = value
            self._rank[value] = 0
            return value

        root = value
        while not self._same(self._parent[root], root):
            root = self._parent[root]

        while not self._same(self._parent[value], value):
            parent = self._parent[value]
            self._parent[value] = root
            value = parent
        return root

    def union(self, left: T, right: T) -> bool:
        """Join two sets and return whether they were previously separate."""
        left_root = self.find(left)
        right_root = self.find(right)
        if self._same(left_root, right_root):
            return False

        if self._rank[left_root] < self._rank[right_root]:
            left_root, right_root = right_root, left_root
        self._parent[right_root] = left_root
        if self._rank[left_root] == self._rank[right_root]:
            self._rank[left_root] += 1
        return True

    def connected(self, left: T, right: T) -> bool:
        """Return whether two values belong to the same set."""
        return self._same(self.find(left), self.find(right))
