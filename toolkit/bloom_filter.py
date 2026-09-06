"""Space-efficient probabilistic membership testing."""

from __future__ import annotations

import hashlib
import math
from collections.abc import Iterator


class BloomFilter:
    """A Bloom filter sized for an expected load and false-positive rate."""

    def __init__(self, expected_items: int, false_positive_rate: float) -> None:
        if expected_items <= 0:
            raise ValueError("expected_items must be greater than zero")
        if not 0.0 < false_positive_rate < 1.0:
            raise ValueError("false_positive_rate must be between zero and one")

        log_two = math.log(2.0)
        self.bit_count = max(
            1,
            math.ceil(
                -expected_items * math.log(false_positive_rate) / (log_two**2)
            ),
        )
        self.hash_count = max(1, round(self.bit_count / expected_items * log_two))
        self._bits = bytearray((self.bit_count + 7) // 8)

    @staticmethod
    def _encode(item: object) -> bytes:
        if isinstance(item, bytes):
            return item
        if isinstance(item, str):
            return item.encode("utf-8")
        raise TypeError("BloomFilter items must be str or bytes")

    def _indexes(self, item: object) -> Iterator[int]:
        digest = hashlib.sha256(self._encode(item)).digest()
        first = int.from_bytes(digest[:16], "big")
        second = int.from_bytes(digest[16:], "big") or 1
        for index in range(self.hash_count):
            yield (first + index * second) % self.bit_count

    def add(self, item: object) -> None:
        """Add a string or byte sequence to the filter."""
        for index in self._indexes(item):
            self._bits[index // 8] |= 1 << (index % 8)

    def might_contain(self, item: object) -> bool:
        """Return whether *item* may have been added."""
        return all(
            self._bits[index // 8] & (1 << (index % 8))
            for index in self._indexes(item)
        )

    def __contains__(self, item: object) -> bool:
        return self.might_contain(item)
