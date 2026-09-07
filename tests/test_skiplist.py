from typing import Any

import pytest

from toolkit.skiplist import SkipList


def test_insert_search_and_iteration_are_ordered() -> None:
    values = SkipList[int]()

    for value in [7, 1, 9, 3, 5]:
        assert values.insert(value)

    assert list(values) == [1, 3, 5, 7, 9]
    assert all(values.search(value) for value in [1, 3, 5, 7, 9])
    assert not values.search(4)
    assert len(values) == 5


def test_duplicate_insert_does_not_change_set() -> None:
    values = SkipList[str]()

    assert values.insert("alpha")
    assert not values.insert("alpha")
    assert list(values) == ["alpha"]
    assert len(values) == 1


def test_delete_existing_and_missing_values() -> None:
    values = SkipList[int]()
    for value in range(20):
        values.insert(value)

    assert values.delete(0)
    assert values.delete(10)
    assert values.delete(19)
    assert not values.delete(10)
    assert not values.delete(30)
    assert list(values) == [value for value in range(20) if value not in {0, 10, 19}]
    assert len(values) == 17


def test_empty_skip_list() -> None:
    values = SkipList[int]()

    assert not values.search(1)
    assert not values.delete(1)
    assert list(values) == []
    assert len(values) == 0


@pytest.mark.parametrize(
    ("kwargs", "message"),
    [
        ({"max_level": 0}, "max_level must be at least 1"),
        ({"probability": 0.0}, "probability must be between 0 and 1"),
        ({"probability": 1.0}, "probability must be between 0 and 1"),
    ],
)
def test_invalid_configuration(kwargs: dict[str, Any], message: str) -> None:
    with pytest.raises(ValueError, match=message):
        SkipList[int](**kwargs)
