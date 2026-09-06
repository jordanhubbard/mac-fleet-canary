import math

import pytest

from toolkit.interval_tree import Interval, IntervalTree


def test_overlap_query_returns_all_overlapping_intervals() -> None:
    tree = IntervalTree[str]()
    for low, high, data in [
        (15, 20, "middle"),
        (10, 30, "wide"),
        (17, 19, "inside"),
        (5, 8, "before"),
        (25, 40, "after"),
    ]:
        tree.insert(low, high, data)

    assert set(tree.query_overlap(18, 26)) == {
        Interval(10, 30, "wide"),
        Interval(15, 20, "middle"),
        Interval(17, 19, "inside"),
        Interval(25, 40, "after"),
    }


def test_point_query_includes_exact_boundaries() -> None:
    tree = IntervalTree[str]()
    tree.insert(1, 5, "ends here")
    tree.insert(5, 9, "starts here")

    assert set(tree.query(5)) == {
        Interval(1, 5, "ends here"),
        Interval(5, 9, "starts here"),
    }


def test_query_with_no_matches_returns_empty_list() -> None:
    tree = IntervalTree[str]()
    tree.insert(1, 3, "first")
    tree.insert(7, 10, "second")

    assert tree.query(5) == []
    assert tree.query_overlap(11, 15) == []


def test_sorted_insertions_remain_queryable() -> None:
    tree = IntervalTree[int]()
    for value in range(2_000):
        tree.insert(value, value + 1, value)

    assert set(tree.query(1_000)) == {
        Interval(999, 1_000, 999),
        Interval(1_000, 1_001, 1_000),
    }


@pytest.mark.parametrize("invalid", [math.nan, math.inf, -math.inf])
def test_non_finite_endpoints_are_rejected(invalid: float) -> None:
    tree = IntervalTree[None]()

    with pytest.raises(ValueError, match="finite"):
        tree.insert(invalid, 3, None)
    with pytest.raises(ValueError, match="finite"):
        tree.query_overlap(1, invalid)
    with pytest.raises(ValueError, match="finite"):
        tree.query(invalid)


def test_reversed_interval_is_rejected() -> None:
    tree = IntervalTree[None]()

    with pytest.raises(ValueError, match="low"):
        tree.insert(4, 3, None)
    with pytest.raises(ValueError, match="low"):
        tree.query_overlap(4, 3)
