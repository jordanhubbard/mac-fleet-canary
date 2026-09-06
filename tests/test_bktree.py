import pytest

from toolkit.bktree import BKTree, levenshtein_distance


WORDS = ["book", "books", "boo", "boon", "cook", "cake", "cape"]


def reference_distance(left: str, right: str) -> int:
    if not left:
        return len(right)
    if not right:
        return len(left)
    return min(
        reference_distance(left[1:], right) + 1,
        reference_distance(left, right[1:]) + 1,
        reference_distance(left[1:], right[1:]) + (left[0] != right[0]),
    )


def make_tree() -> BKTree:
    tree = BKTree()
    for word in WORDS:
        tree.insert(word)
    return tree


def test_exact_match() -> None:
    assert make_tree().search("book", 0) == [("book", 0)]


def test_search_with_no_results() -> None:
    assert make_tree().search("xyz", 1) == []


@pytest.mark.parametrize(("query", "limit"), [("bok", 1), ("cape", 2), ("", 4)])
def test_search_matches_brute_force(query: str, limit: int) -> None:
    expected = sorted(
        (word, distance)
        for word in WORDS
        if (distance := reference_distance(query, word)) <= limit
    )
    assert make_tree().search(query, limit) == expected


@pytest.mark.parametrize(
    ("left", "right", "expected"),
    [("", "", 0), ("kitten", "sitting", 3), ("book", "back", 2)],
)
def test_levenshtein_known_distances(
    left: str, right: str, expected: int
) -> None:
    assert levenshtein_distance(left, right) == expected


def test_empty_tree_and_duplicate_insert() -> None:
    tree = BKTree()
    assert tree.search("word", 2) == []
    tree.insert("word")
    tree.insert("word")
    assert tree.search("word", 0) == [("word", 0)]


def test_negative_max_distance_is_rejected() -> None:
    with pytest.raises(ValueError, match="non-negative"):
        make_tree().search("book", -1)
