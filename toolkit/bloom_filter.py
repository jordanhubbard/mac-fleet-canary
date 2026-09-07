"""Space-efficient probabilistic membership testing."""

from __future__ import annotations

import hashlib
import math
from collections.abc import Iterator


class BloomFilter:
    """A bit-array Bloom filter for strings and bytes."""

    def __init__(self, expected_items: int, false_positive_rate: float) -> None:
        if expected_items <= 0:
            raise ValueError("expected_items must be positive")
        if not 0.0 < false_positive_rate < 1.0:
            raise ValueError("false_positive_rate must be between 0 and 1")

        self.bit_count = max(
            1,
            math.ceil(
                -expected_items * math.log(false_positive_rate) / math.log(2) ** 2
            ),
        )
        self.hash_count = max(
            1, round(self.bit_count / expected_items * math.log(2))
        )
        self._bits = bytearray((self.bit_count + 7) // 8)

    @staticmethod
    def _encode(item: str | bytes) -> bytes:
        if isinstance(item, str):
            return b"s" + item.encode("utf-8")
        if isinstance(item, bytes):
            return b"b" + item
        raise TypeError("item must be str or bytes")

    def _indexes(self, item: str | bytes) -> Iterator[int]:
        digest = hashlib.sha256(self._encode(item)).digest()
        first = int.from_bytes(digest[:16], "big")
        second = int.from_bytes(digest[16:], "big")
        for index in range(self.hash_count):
            yield (first + index * second) % self.bit_count

    def add(self, item: str | bytes) -> None:
        """Add *item* to the filter."""
        for index in self._indexes(item):
            self._bits[index // 8] |= 1 << (index % 8)

    def might_contain(self, item: str | bytes) -> bool:
        """Return whether *item* may have been added."""
        return all(
            self._bits[index // 8] & (1 << (index % 8))
            for index in self._indexes(item)
        )

    def __contains__(self, item: object) -> bool:
        if not isinstance(item, (str, bytes)):
            return False
        return self.might_contain(item)
