"""Tests for the trie module."""

from toolkit import Trie


def test_empty_trie_has_no_words_or_prefixes() -> None:
    trie = Trie()

    assert not trie.search("anything")
    assert not trie.starts_with("any")
    assert not trie.search("")
    assert not trie.starts_with("")


def test_search_requires_an_exact_word() -> None:
    trie = Trie()
    trie.insert("apple")

    assert trie.search("apple")
    assert not trie.search("app")
    assert trie.starts_with("app")
    assert not trie.starts_with("banana")


def test_insert_is_idempotent() -> None:
    trie = Trie()
    trie.insert("repeat")
    trie.insert("repeat")

    assert trie.search("repeat")
    assert trie.delete("repeat")
    assert not trie.search("repeat")


def test_delete_word_that_is_prefix_of_another() -> None:
    trie = Trie()
    trie.insert("app")
    trie.insert("apple")

    assert trie.delete("app")
    assert not trie.search("app")
    assert trie.starts_with("app")
    assert trie.search("apple")


def test_delete_longer_word_preserves_shared_prefix_word() -> None:
    trie = Trie()
    trie.insert("car")
    trie.insert("cart")
    trie.insert("carbon")

    assert trie.delete("cart")
    assert trie.search("car")
    assert trie.search("carbon")
    assert not trie.search("cart")


def test_delete_missing_word_does_not_change_trie() -> None:
    trie = Trie()
    trie.insert("known")

    assert not trie.delete("unknown")
    assert not trie.delete("know")
    assert trie.search("known")


def test_empty_string_can_be_stored_and_deleted() -> None:
    trie = Trie()

    trie.insert("")
    assert trie.search("")
    assert trie.starts_with("")
    assert trie.delete("")
    assert not trie.search("")
    assert not trie.starts_with("")


def test_words_with_prefix_is_sorted_and_reflects_deletion() -> None:
    trie = Trie()
    for word in ["dog", "cat", "cart", "car", "car"]:
        trie.insert(word)

    assert trie.words_with_prefix("car") == ["car", "cart"]
    assert trie.delete("car")
    assert trie.words_with_prefix("car") == ["cart"]


def test_words_with_prefix_handles_empty_and_missing_prefixes_without_mutation() -> None:
    trie = Trie()
    for word in ["dog", "cart", "car", "cat"]:
        trie.insert(word)

    expected = ["car", "cart", "cat", "dog"]
    assert trie.words_with_prefix("") == expected
    assert trie.words_with_prefix("z") == []
    assert trie.words_with_prefix("") == expected
    assert all(trie.search(word) for word in expected)
