"""A fixed-capacity least-recently-used cache."""

from collections import OrderedDict
from typing import Generic, TypeVar


K = TypeVar("K")
V = TypeVar("V")


class LRUCache(Generic[K, V]):
    """Store up to ``capacity`` values, evicting the least recently used."""

    def __init__(self, capacity: int) -> None:
        if capacity <= 0:
            raise ValueError("capacity must be positive")
        self._capacity = capacity
        self._values: OrderedDict[K, V] = OrderedDict()

    def get(self, key: K) -> V:
        """Return and mark ``key`` as recently used, or raise ``KeyError``."""
        value = self._values.pop(key)
        self._values[key] = value
        return value

    def put(self, key: K, value: V) -> None:
        """Insert ``value`` and mark ``key`` as the most recently used."""
        if key in self._values:
            del self._values[key]
        self._values[key] = value
        if len(self._values) > self._capacity:
            self._values.popitem(last=False)
