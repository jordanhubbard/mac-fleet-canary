"""A probabilistic ordered map implemented as a skip list."""

from __future__ import annotations

import random
from collections.abc import Callable, Iterator
from dataclasses import dataclass, field
from typing import Any, Generic, TypeVar, cast


K = TypeVar("K")
V = TypeVar("V")


@dataclass
class _Node(Generic[K, V]):
    key: K | None
    value: V | None
    forward: list[_Node[K, V] | None] = field(default_factory=list)


class SkipList(Generic[K, V]):
    """An ordered mapping with expected O(log n) operations.

    Keys must support ordering. ``rng`` is injectable so callers can make
    randomized level promotion deterministic in tests.
    """

    def __init__(
        self,
        *,
        max_level: int = 16,
        promotion_probability: float = 0.5,
        rng: Callable[[], float] | None = None,
    ) -> None:
        if max_level < 1:
            raise ValueError("max_level must be at least 1")
        if not 0.0 < promotion_probability < 1.0:
            raise ValueError("promotion_probability must be between 0 and 1")

        self._max_level = max_level
        self._probability = promotion_probability
        self._rng = rng if rng is not None else random.random
        self._level = 0
        self._head: _Node[K, V] = _Node(None, None, [None] * max_level)

    def _random_level(self) -> int:
        level = 0
        while level < self._max_level - 1 and self._rng() < self._probability:
            level += 1
        return level

    def _predecessors(self, key: K) -> list[_Node[K, V]]:
        update = [self._head] * self._max_level
        current = self._head
        for level in range(self._level, -1, -1):
            next_node = current.forward[level]
            while next_node is not None and cast(Any, next_node.key) < key:
                current = next_node
                next_node = current.forward[level]
            update[level] = current
        return update

    def insert(self, key: K, value: V) -> None:
        """Insert ``key`` and ``value``, replacing an existing value."""
        update = self._predecessors(key)
        existing = update[0].forward[0]
        if existing is not None and existing.key == key:
            existing.value = value
            return

        level = self._random_level()
        if level > self._level:
            for index in range(self._level + 1, level + 1):
                update[index] = self._head
            self._level = level

        node = _Node(key, value, [None] * (level + 1))
        for index in range(level + 1):
            node.forward[index] = update[index].forward[index]
            update[index].forward[index] = node

    def search(self, key: K) -> V | None:
        """Return the value for ``key``, or ``None`` when absent."""
        candidate = self._predecessors(key)[0].forward[0]
        if candidate is not None and candidate.key == key:
            return candidate.value
        return None

    def delete(self, key: K) -> None:
        """Delete ``key`` if present; otherwise do nothing."""
        update = self._predecessors(key)
        candidate = update[0].forward[0]
        if candidate is None or candidate.key != key:
            return

        for level in range(len(candidate.forward)):
            if update[level].forward[level] is candidate:
                update[level].forward[level] = candidate.forward[level]
        while self._level > 0 and self._head.forward[self._level] is None:
            self._level -= 1

    def __iter__(self) -> Iterator[tuple[K, V]]:
        """Yield key-value pairs in ascending key order."""
        current = self._head.forward[0]
        while current is not None:
            yield cast(K, current.key), cast(V, current.value)
            current = current.forward[0]
