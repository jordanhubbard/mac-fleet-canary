import pytest

from toolkit.lru_cache import LRUCache


def test_overwrite_recency_survives_peek() -> None:
    cache = LRUCache[str, int](2)
    cache.put("older", 1)
    cache.put("newer", 2)

    cache.put("older", 10)
    assert cache.peek("newer") == 2
    cache.put("third", 3)

    with pytest.raises(KeyError):
        cache.get("newer")
    assert cache.get("older") == 10
    assert cache.get("third") == 3


def test_get_refreshes_recency_after_intervening_insert() -> None:
    cache = LRUCache[str, int](3)
    cache.put("first", 1)
    cache.put("second", 2)
    cache.put("third", 3)

    assert cache.get("first") == 1
    cache.put("fourth", 4)
    assert cache.get("third") == 3
    cache.put("fifth", 5)

    with pytest.raises(KeyError):
        cache.get("first")
    assert cache.get("third") == 3
    assert cache.get("fourth") == 4
    assert cache.get("fifth") == 5


def test_multiple_gets_preserve_correct_eviction() -> None:
    cache = LRUCache[str, int](3)
    cache.put("a", 1)
    cache.put("b", 2)
    cache.put("c", 3)

    assert cache.get("a") == 1
    assert cache.get("b") == 2
    cache.put("d", 4)

    with pytest.raises(KeyError):
        cache.get("c")
    assert cache.get("a") == 1
    assert cache.get("b") == 2
    assert cache.get("d") == 4
