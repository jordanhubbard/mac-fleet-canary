import pytest

from toolkit.interval_tree import Interval, IntervalTree


def test_overlap_query_returns_all_overlapping_intervals() -> None:
    tree = IntervalTree[str]()
    tree.insert(15, 20, "middle")
    tree.insert(10, 30, "wide")
    tree.insert(17, 19, "inside")
    tree.insert(5, 8, "before")
    tree.insert(25, 40, "after")

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


def test_duplicate_intervals_are_preserved() -> None:
    tree = IntervalTree[str]()
    tree.insert(2, 4, "first")
    tree.insert(2, 4, "second")

    assert tree.query(3) == [
        Interval(2, 4, "first"),
        Interval(2, 4, "second"),
    ]


def test_reversed_interval_is_rejected() -> None:
    tree = IntervalTree[None]()

    with pytest.raises(ValueError, match="low"):
        tree.insert(4, 3, None)
    with pytest.raises(ValueError, match="low"):
        tree.query_overlap(4, 3)
