"""Probabilistic ordered set implemented as a skip list."""

from __future__ import annotations

import random
from dataclasses import dataclass, field
from typing import Generic, Iterator, TypeVar


T = TypeVar("T")


@dataclass
class _Node(Generic[T]):
    value: T | None
    forward: list[_Node[T] | None] = field(default_factory=list)


class SkipList(Generic[T]):
    """Maintain unique comparable values in sorted order."""

    def __init__(self, max_level: int = 16, probability: float = 0.5) -> None:
        if max_level < 1:
            raise ValueError("max_level must be at least 1")
        if not 0 < probability < 1:
            raise ValueError("probability must be between 0 and 1")

        self._max_level = max_level
        self._probability = probability
        self._level = 0
        self._head: _Node[T] = _Node(None, [None] * (max_level + 1))
        self._size = 0

    def __len__(self) -> int:
        return self._size

    def __contains__(self, value: object) -> bool:
        current = self._head
        for level in range(self._level, -1, -1):
            next_node = current.forward[level]
            while next_node is not None and next_node.value < value:  # type: ignore[operator]
                current = next_node
                next_node = current.forward[level]
        candidate = current.forward[0]
        return candidate is not None and candidate.value == value

    def __iter__(self) -> Iterator[T]:
        current = self._head.forward[0]
        while current is not None:
            assert current.value is not None
            yield current.value
            current = current.forward[0]

    def _random_level(self) -> int:
        level = 0
        while level < self._max_level and random.random() < self._probability:
            level += 1
        return level

    def insert(self, value: T) -> bool:
        """Insert *value*, returning whether it was newly added."""
        update = [self._head] * (self._max_level + 1)
        current = self._head
        for level in range(self._level, -1, -1):
            next_node = current.forward[level]
            while next_node is not None and next_node.value < value:  # type: ignore[operator]
                current = next_node
                next_node = current.forward[level]
            update[level] = current

        candidate = current.forward[0]
        if candidate is not None and candidate.value == value:
            return False

        new_level = self._random_level()
        if new_level > self._level:
            for level in range(self._level + 1, new_level + 1):
                update[level] = self._head
            self._level = new_level

        node = _Node(value, [None] * (new_level + 1))
        for level in range(new_level + 1):
            node.forward[level] = update[level].forward[level]
            update[level].forward[level] = node
        self._size += 1
        return True

    def search(self, value: T) -> bool:
        """Return whether *value* is present."""
        return value in self

    def delete(self, value: T) -> bool:
        """Delete *value*, returning whether it was present."""
        update = [self._head] * (self._max_level + 1)
        current = self._head
        for level in range(self._level, -1, -1):
            next_node = current.forward[level]
            while next_node is not None and next_node.value < value:  # type: ignore[operator]
                current = next_node
                next_node = current.forward[level]
            update[level] = current

        candidate = current.forward[0]
        if candidate is None or candidate.value != value:
            return False

        for level in range(self._level + 1):
            if update[level].forward[level] is not candidate:
                break
            update[level].forward[level] = candidate.forward[level]
        while self._level > 0 and self._head.forward[self._level] is None:
            self._level -= 1
        self._size -= 1
        return True
