import pytest

from toolkit.skiplist import SkipList


def test_insert_search_and_iteration() -> None:
    values = SkipList[int]()
    for value in (7, 2, 9, 1, 5):
        assert values.insert(value)

    assert list(values) == [1, 2, 5, 7, 9]
    assert values.search(5)
    assert 9 in values
    assert not values.search(8)
    assert len(values) == 5


def test_duplicate_insert_is_ignored() -> None:
    values = SkipList[str]()
    assert values.insert("alpha")
    assert not values.insert("alpha")
    assert list(values) == ["alpha"]
    assert len(values) == 1


def test_delete_present_and_missing_values() -> None:
    values = SkipList[int]()
    for value in range(10):
        values.insert(value)

    assert values.delete(0)
    assert values.delete(5)
    assert values.delete(9)
    assert not values.delete(99)
    assert list(values) == [1, 2, 3, 4, 6, 7, 8]
    assert len(values) == 7


def test_empty_list() -> None:
    values = SkipList[int]()
    assert list(values) == []
    assert not values.search(1)
    assert not values.delete(1)
    assert len(values) == 0


@pytest.mark.parametrize(
    ("max_level", "probability"),
    [(0, 0.5), (4, 0.0), (4, 1.0), (4, -0.1), (4, 1.1)],
)
def test_invalid_configuration(max_level: int, probability: float) -> None:
    with pytest.raises(ValueError):
        SkipList[int](max_level=max_level, probability=probability)
