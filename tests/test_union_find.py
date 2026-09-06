"""Tests for the union-find data structure."""

from math import nan

from toolkit.union_find import UnionFind


def test_connectivity_before_and_after_unions() -> None:
    sets = UnionFind[str]()

    assert not sets.connected("a", "b")
    assert sets.union("a", "b")
    assert sets.connected("a", "b")
    assert not sets.union("a", "b")


def test_chain_is_collapsed_by_find() -> None:
    sets = UnionFind[int]()
    for value in range(7):
        sets.find(value)

    # Build a chain directly so the test exercises path compression independently
    # of union by rank, which normally prevents a tall tree from forming.
    sets._parent.update({0: 1, 1: 2, 2: 3, 3: 4, 4: 5, 5: 6})

    assert sets.find(0) == 6
    assert all(sets._parent[value] == 6 for value in range(7))


def test_union_by_rank_keeps_shallower_tree_under_deeper_tree() -> None:
    sets = UnionFind[int]()
    sets.union(1, 2)
    sets.union(3, 4)
    sets.union(1, 3)
    root = sets.find(1)

    sets.union(5, 6)
    sets.union(5, root)

    assert sets.find(5) == root
    assert sets.connected(2, 6)


def test_find_handles_nan_without_looping() -> None:
    sets = UnionFind[float]()

    assert sets.find(nan) is nan
    assert sets.find(nan) is nan
    assert sets.connected(nan, nan)
