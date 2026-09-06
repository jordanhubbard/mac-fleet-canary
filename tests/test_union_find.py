"""Tests for the union-find data structure."""

from toolkit.union_find import UnionFind


def test_connectivity_before_and_after_unions() -> None:
    sets = UnionFind(["a", "b", "c", "d"])

    assert not sets.connected("a", "b")
    assert sets.union("a", "b")
    assert sets.connected("a", "b")
    assert not sets.connected("a", "c")

    assert sets.union("c", "d")
    assert sets.union("b", "c")
    assert sets.connected("a", "d")
    assert not sets.union("a", "d")


def test_find_adds_previously_unseen_values() -> None:
    sets: UnionFind[int] = UnionFind()

    assert sets.find(10) == 10
    assert sets.connected(20, 20)
    assert not sets.connected(10, 20)


def test_path_compression_collapses_a_deep_union_tree() -> None:
    sets = UnionFind(range(8))
    for first, second in ((0, 1), (2, 3), (0, 2), (4, 5), (6, 7), (4, 6), (0, 4)):
        sets.union(first, second)

    root = sets.find(0)
    assert sets._parent[7] != root

    assert sets.find(7) == root
    assert sets._parent[7] == root
    assert sets._parent[6] == root
    assert sets._parent[4] == root


def test_union_by_rank_keeps_the_larger_tree_root() -> None:
    sets = UnionFind(range(4))
    sets.union(0, 1)
    sets.union(0, 2)

    root = sets.find(0)
    sets.union(3, 2)

    assert sets.find(3) == root
    assert sets._rank[root] == 1


def test_nan_is_a_valid_value() -> None:
    nan = float("nan")
    other_nan = float("nan")
    sets = UnionFind([nan, other_nan])

    assert sets.find(nan) is nan
    assert sets.connected(nan, nan)
    assert not sets.connected(nan, other_nan)
    assert sets.union(nan, other_nan)
    assert sets.connected(nan, other_nan)
