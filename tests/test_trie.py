from toolkit.trie import Trie


def test_empty_trie_has_no_words_or_prefixes() -> None:
    trie = Trie()

    assert not trie.search("")
    assert not trie.search("word")
    assert not trie.starts_with("")
    assert not trie.starts_with("w")


def test_insert_supports_exact_and_prefix_queries() -> None:
    trie = Trie()
    trie.insert("apple")

    assert trie.search("apple")
    assert not trie.search("app")
    assert trie.starts_with("app")
    assert trie.starts_with("")


def test_empty_string_can_be_stored_and_deleted() -> None:
    trie = Trie()
    trie.insert("")

    assert trie.search("")
    assert trie.starts_with("")
    assert trie.delete("")
    assert not trie.search("")
    assert not trie.delete("")


def test_delete_word_that_is_prefix_preserves_longer_word() -> None:
    trie = Trie()
    trie.insert("app")
    trie.insert("apple")

    assert trie.delete("app")
    assert not trie.search("app")
    assert trie.search("apple")
    assert trie.starts_with("app")


def test_delete_longer_word_preserves_prefix_word_and_sibling() -> None:
    trie = Trie()
    trie.insert("app")
    trie.insert("apple")
    trie.insert("apply")

    assert trie.delete("apple")
    assert trie.search("app")
    assert not trie.search("apple")
    assert trie.search("apply")


def test_delete_missing_word_does_not_change_trie() -> None:
    trie = Trie()
    trie.insert("cat")

    assert not trie.delete("car")
    assert not trie.delete("ca")
    assert trie.search("cat")
