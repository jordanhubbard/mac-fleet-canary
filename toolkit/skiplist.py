"""Probabilistic ordered set implemented as a skip list."""

from __future__ import annotations

import random
from dataclasses import dataclass, field
from typing import Generic, Iterator, Protocol, TypeVar


class _Comparable(Protocol):
    def __lt__(self, other: object, /) -> bool: ...


T = TypeVar("T", bound=_Comparable)


@dataclass
class _Node(Generic[T]):
    value: T | None
    forward: list[_Node[T] | None] = field(default_factory=list)


class SkipList(Generic[T]):
    """An ordered set with expected O(log n) insert, search, and delete."""

    def __init__(self, max_level: int = 16, probability: float = 0.5) -> None:
        if max_level < 1:
            raise ValueError("max_level must be at least 1")
        if not 0 < probability < 1:
            raise ValueError("probability must be between 0 and 1")

        self._max_level = max_level
        self._probability = probability
        self._level = 0
        self._size = 0
        self._head: _Node[T] = _Node(None, [None] * max_level)

    def __len__(self) -> int:
        return self._size

    def __contains__(self, value: object) -> bool:
        current = self._head
        for level in range(self._level, -1, -1):
            next_node = current.forward[level]
            while (
                next_node is not None
                and next_node.value is not None
                and next_node.value < value
            ):
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

    def search(self, value: T) -> bool:
        """Return whether *value* is present."""
        candidate = self._find_predecessors(value)[0].forward[0]
        return candidate is not None and candidate.value == value

    def insert(self, value: T) -> bool:
        """Insert *value*, returning ``False`` when it already exists."""
        update = self._find_predecessors(value)
        candidate = update[0].forward[0]
        if candidate is not None and candidate.value == value:
            return False

        level = self._random_level()
        if level > self._level:
            for index in range(self._level + 1, level + 1):
                update[index] = self._head
            self._level = level

        node = _Node(value, [None] * (level + 1))
        for index in range(level + 1):
            node.forward[index] = update[index].forward[index]
            update[index].forward[index] = node
        self._size += 1
        return True

    def delete(self, value: T) -> bool:
        """Delete *value*, returning whether it was present."""
        update = self._find_predecessors(value)
        candidate = update[0].forward[0]
        if candidate is None or candidate.value != value:
            return False

        for index in range(self._level + 1):
            if update[index].forward[index] is not candidate:
                break
            update[index].forward[index] = candidate.forward[index]

        while self._level > 0 and self._head.forward[self._level] is None:
            self._level -= 1
        self._size -= 1
        return True

    def _find_predecessors(self, value: T) -> list[_Node[T]]:
        update = [self._head] * self._max_level
        current = self._head
        for level in range(self._level, -1, -1):
            next_node = current.forward[level]
            while next_node is not None and next_node.value is not None and next_node.value < value:
                current = next_node
                next_node = current.forward[level]
            update[level] = current
        return update

    def _random_level(self) -> int:
        level = 0
        while level < self._max_level - 1 and random.random() < self._probability:
            level += 1
        return level
