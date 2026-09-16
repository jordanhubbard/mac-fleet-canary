import pytest

from toolkit.lru_cache import LRUCache


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
