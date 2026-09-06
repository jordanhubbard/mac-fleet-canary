"""Tests for the Bloom filter implementation."""

import pytest

from toolkit.bloom_filter import BloomFilter


def test_added_items_have_no_false_negatives() -> None:
    bloom = BloomFilter(expected_items=10_000, false_positive_rate=0.01)
    items = [f"added-{index}" for index in range(10_000)]

    for item in items:
        bloom.add(item)

    assert all(item in bloom for item in items)


def test_false_positive_rate_is_close_to_target() -> None:
    target_rate = 0.01
    bloom = BloomFilter(expected_items=5_000, false_positive_rate=target_rate)
    for index in range(5_000):
        bloom.add(f"member-{index}")

    trials = 50_000
    false_positives = sum(
        bloom.might_contain(f"absent-{index}") for index in range(trials)
    )

    assert false_positives / trials <= target_rate * 1.5


def test_supports_bytes_and_keeps_types_distinct() -> None:
    bloom = BloomFilter(expected_items=10, false_positive_rate=0.001)
    bloom.add(b"binary")

    assert b"binary" in bloom


@pytest.mark.parametrize(
    ("expected_items", "false_positive_rate"),
    [(0, 0.1), (-1, 0.1), (10, 0.0), (10, 1.0), (10, -0.1)],
)
def test_rejects_invalid_configuration(
    expected_items: int, false_positive_rate: float
) -> None:
    with pytest.raises(ValueError):
        BloomFilter(expected_items, false_positive_rate)


def test_rejects_unsupported_item_types() -> None:
    bloom = BloomFilter(expected_items=10, false_positive_rate=0.01)

    with pytest.raises(TypeError):
        bloom.add(42)
