import pytest

from toolkit.lru_cache import LRUCache


def test_put_evicts_least_recently_used_key() -> None:
    cache = LRUCache[str, int](2)
    cache.put("first", 1)
    cache.put("second", 2)
    assert cache.get("first") == 1

    cache.put("third", 3)

    with pytest.raises(KeyError):
        cache.get("second")
    assert cache.get("first") == 1
    assert cache.get("third") == 3


def test_capacity_one_evicts_previous_key() -> None:
    cache = LRUCache[str, int](1)
    cache.put("old", 1)
    cache.put("new", 2)

    with pytest.raises(KeyError):
        cache.get("old")
    assert cache.get("new") == 2


def test_reinserting_key_updates_value_and_recency() -> None:
    cache = LRUCache[str, int](2)
    cache.put("first", 1)
    cache.put("second", 2)
    cache.put("first", 10)
    cache.put("third", 3)

    assert cache.get("first") == 10
    with pytest.raises(KeyError):
        cache.get("second")


def test_get_missing_key_raises_key_error() -> None:
    cache = LRUCache[str, int](2)

    with pytest.raises(KeyError):
        cache.get("missing")


def test_non_positive_capacity_is_rejected() -> None:
    with pytest.raises(ValueError, match="capacity must be positive"):
        LRUCache[str, int](0)
