from toolkit.trie import Trie


def test_empty_trie_has_no_words_or_prefixes() -> None:
    trie = Trie()

    assert not trie.search("")
    assert not trie.search("missing")
    assert not trie.starts_with("")
    assert not trie.starts_with("miss")


def test_insert_supports_exact_and_prefix_queries() -> None:
    trie = Trie()
    trie.insert("apple")

    assert trie.search("apple")
    assert not trie.search("app")
    assert trie.starts_with("app")
    assert trie.starts_with("")


def test_delete_word_that_is_prefix_of_another_word() -> None:
    trie = Trie()
    trie.insert("app")
    trie.insert("apple")

    trie.delete("app")

    assert not trie.search("app")
    assert trie.search("apple")
    assert trie.starts_with("app")


def test_delete_longer_word_preserves_shorter_word() -> None:
    trie = Trie()
    trie.insert("app")
    trie.insert("apple")

    trie.delete("apple")

    assert trie.search("app")
    assert not trie.search("apple")
    assert not trie.starts_with("appl")


def test_delete_shared_branch_and_missing_word_are_safe() -> None:
    trie = Trie()
    trie.insert("car")
    trie.insert("cat")

    trie.delete("car")
    trie.delete("can")

    assert not trie.search("car")
    assert trie.search("cat")
    assert trie.starts_with("ca")


def test_empty_string_can_be_inserted_and_deleted() -> None:
    trie = Trie()

    trie.insert("")
    assert trie.search("")
    assert trie.starts_with("")

    trie.delete("")
    assert not trie.search("")
    assert not trie.starts_with("")
