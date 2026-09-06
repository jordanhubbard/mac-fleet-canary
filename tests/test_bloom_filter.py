import pytest

from toolkit.bloom_filter import BloomFilter


@pytest.mark.parametrize(
    ("expected_items", "false_positive_rate"),
    [(0, 0.1), (-1, 0.1), (10, 0.0), (10, 1.0), (10, -0.1)],
)
def test_rejects_invalid_configuration(
    expected_items: int, false_positive_rate: float
) -> None:
    with pytest.raises(ValueError):
        BloomFilter(expected_items, false_positive_rate)


def test_has_no_false_negatives_for_large_set() -> None:
    bloom = BloomFilter(10_000, 0.01)
    added = [f"item-{index}" for index in range(10_000)]
    for item in added:
        bloom.add(item)

    assert all(item in bloom for item in added)
    assert all(bloom.might_contain(item) for item in added)


def test_false_positive_rate_is_near_configured_target() -> None:
    target_rate = 0.01
    bloom = BloomFilter(10_000, target_rate)
    for index in range(10_000):
        bloom.add(f"added-{index}")

    trials = 20_000
    false_positives = sum(
        f"not-added-{index}" in bloom for index in range(trials)
    )
    assert false_positives / trials <= target_rate * 2


def test_string_and_bytes_are_distinct_inputs() -> None:
    bloom = BloomFilter(1, 1e-9)
    bloom.add("same")

    assert "same" in bloom
    assert b"same" not in bloom


def test_empty_and_binary_values() -> None:
    bloom = BloomFilter(3, 0.001)
    values = ["", b"", b"\x00\xff"]
    for value in values:
        bloom.add(value)

    assert all(value in bloom for value in values)


def test_contains_returns_false_for_unsupported_type() -> None:
    bloom = BloomFilter(10, 0.01)

    assert 123 not in bloom
    with pytest.raises(TypeError):
        bloom.add(123)  # type: ignore[arg-type]
