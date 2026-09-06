"""An augmented binary search tree for inclusive interval queries."""

from __future__ import annotations

from dataclasses import dataclass
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
    left: _Node[DataT] | None = None
    right: _Node[DataT] | None = None


class IntervalTree(Generic[DataT]):
    """Store intervals and efficiently find inclusive overlaps."""

    def __init__(self) -> None:
        self._root: _Node[DataT] | None = None

    def insert(self, low: float, high: float, data: DataT) -> None:
        """Insert an inclusive interval.

        Raises:
            ValueError: If ``low`` is greater than ``high``.
        """
        if low > high:
            raise ValueError("low must not be greater than high")

        interval = Interval(low, high, data)
        self._root = self._insert(self._root, interval)

    def query(self, point: float) -> list[Interval[DataT]]:
        """Return every interval containing ``point``."""
        return self.query_overlap(point, point)

    def query_overlap(self, low: float, high: float) -> list[Interval[DataT]]:
        """Return every interval overlapping the inclusive query range.

        Raises:
            ValueError: If ``low`` is greater than ``high``.
        """
        if low > high:
            raise ValueError("low must not be greater than high")

        matches: list[Interval[DataT]] = []
        self._query_overlap(self._root, low, high, matches)
        return matches

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

        node.max_high = max(node.max_high, interval.high)
        return node

    def _query_overlap(
        self,
        node: _Node[DataT] | None,
        low: float,
        high: float,
        matches: list[Interval[DataT]],
    ) -> None:
        if node is None:
            return

        if node.left is not None and node.left.max_high >= low:
            self._query_overlap(node.left, low, high, matches)

        interval = node.interval
        if interval.low <= high and low <= interval.high:
            matches.append(interval)

        if node.right is not None and interval.low <= high:
            self._query_overlap(node.right, low, high, matches)
