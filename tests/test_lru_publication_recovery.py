import pytest

from toolkit.lru_cache import LRUCache


def test_overwrite_then_peek_preserves_the_other_keys_recency() -> None:
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
