"""An augmented AVL tree for inclusive interval queries."""

from __future__ import annotations

from dataclasses import dataclass
from math import isfinite
from typing import Generic, TypeVar


DataT = TypeVar("DataT")


@dataclass(frozen=True)
class Interval(Generic[DataT]):
    """An inclusive interval and its associated value."""

    low: float
    high: float
    data: DataT


@dataclass
class _Node(Generic[DataT]):
    interval: Interval[DataT]
    max_high: float
    height: int = 1
    left: _Node[DataT] | None = None
    right: _Node[DataT] | None = None


class IntervalTree(Generic[DataT]):
    """Store intervals and efficiently find inclusive overlaps."""

    def __init__(self) -> None:
        self._root: _Node[DataT] | None = None

    def insert(self, low: float, high: float, data: DataT) -> None:
        """Insert an inclusive interval with finite endpoints."""
        self._validate(low, high)
        self._root = self._insert(self._root, Interval(low, high, data))

    def query(self, point: float) -> list[Interval[DataT]]:
        """Return every interval containing ``point``."""
        if not isfinite(point):
            raise ValueError("point must be finite")
        return self.query_overlap(point, point)

    def query_overlap(self, low: float, high: float) -> list[Interval[DataT]]:
        """Return every interval overlapping the inclusive query range."""
        self._validate(low, high)
        matches: list[Interval[DataT]] = []
        stack: list[_Node[DataT]] = []
        if self._root is not None:
            stack.append(self._root)

        while stack:
            node = stack.pop()
            interval = node.interval
            if interval.low <= high and low <= interval.high:
                matches.append(interval)
            if node.right is not None and interval.low <= high:
                stack.append(node.right)
            if node.left is not None and node.left.max_high >= low:
                stack.append(node.left)
        return matches

    @staticmethod
    def _validate(low: float, high: float) -> None:
        if not isfinite(low) or not isfinite(high):
            raise ValueError("interval endpoints must be finite")
        if low > high:
            raise ValueError("low must not be greater than high")

    def _insert(
        self, node: _Node[DataT] | None, interval: Interval[DataT]
    ) -> _Node[DataT]:
        if node is None:
            return _Node(interval, interval.high)

        if (interval.low, interval.high) < (
            node.interval.low,
            node.interval.high,
        ):
            node.left = self._insert(node.left, interval)
        else:
            node.right = self._insert(node.right, interval)

        self._update(node)
        balance = self._height(node.left) - self._height(node.right)
        if balance > 1:
            if node.left is not None and (
                interval.low,
                interval.high,
            ) >= (node.left.interval.low, node.left.interval.high):
                node.left = self._rotate_left(node.left)
            return self._rotate_right(node)
        if balance < -1:
            if node.right is not None and (
                interval.low,
                interval.high,
            ) < (node.right.interval.low, node.right.interval.high):
                node.right = self._rotate_right(node.right)
            return self._rotate_left(node)
        return node

    @staticmethod
    def _height(node: _Node[DataT] | None) -> int:
        return 0 if node is None else node.height

    def _update(self, node: _Node[DataT]) -> None:
        node.height = 1 + max(self._height(node.left), self._height(node.right))
        node.max_high = max(
            node.interval.high,
            float("-inf") if node.left is None else node.left.max_high,
            float("-inf") if node.right is None else node.right.max_high,
        )

    def _rotate_left(self, node: _Node[DataT]) -> _Node[DataT]:
        root = node.right
        if root is None:
            return node
        node.right = root.left
        root.left = node
        self._update(node)
        self._update(root)
        return root

    def _rotate_right(self, node: _Node[DataT]) -> _Node[DataT]:
        root = node.left
        if root is None:
            return node
        node.left = root.right
        root.right = node
        self._update(node)
        self._update(root)
        return root
