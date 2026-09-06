from collections.abc import Callable
from itertools import cycle

from toolkit.skiplist import SkipList


def deterministic_rng() -> Callable[[], float]:
    values = cycle((0.25, 0.75, 0.1, 0.1, 0.8))
    return lambda: next(values)


def test_search_empty_skip_list() -> None:
    skip_list: SkipList[int, str] = SkipList(rng=deterministic_rng())

    assert skip_list.search(42) is None


def test_insert_search_and_replace() -> None:
    skip_list: SkipList[int, str] = SkipList(rng=deterministic_rng())
    skip_list.insert(4, "first")
    skip_list.insert(4, "replacement")

    assert skip_list.search(4) == "replacement"
    assert list(skip_list) == [(4, "replacement")]


def test_delete_existing_key_and_missing_key_is_no_op() -> None:
    skip_list: SkipList[int, str] = SkipList(rng=deterministic_rng())
    for key in (3, 1, 2):
        skip_list.insert(key, str(key))

    skip_list.delete(2)
    skip_list.delete(99)

    assert skip_list.search(2) is None
    assert list(skip_list) == [(1, "1"), (3, "3")]


def test_many_inserts_remain_ordered() -> None:
    skip_list: SkipList[int, int] = SkipList(max_level=12, rng=deterministic_rng())
    keys = list(range(250))
    for key in reversed(keys):
        skip_list.insert(key, key * key)

    assert list(skip_list) == [(key, key * key) for key in keys]
    assert all(skip_list.search(key) == key * key for key in keys)
