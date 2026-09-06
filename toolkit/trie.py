"""A prefix tree for storing and querying strings."""


class _TrieNode:
    def __init__(self) -> None:
        self.children: dict[str, _TrieNode] = {}
        self.is_word = False


class Trie:
    """A mutable prefix tree."""

    def __init__(self) -> None:
        self._root = _TrieNode()

    def insert(self, word: str) -> None:
        """Insert *word* into the trie."""
        node = self._root
        for character in word:
            node = node.children.setdefault(character, _TrieNode())
        node.is_word = True

    def search(self, word: str) -> bool:
        """Return whether *word* is stored as an exact match."""
        node = self._find(word)
        return node is not None and node.is_word

    def starts_with(self, prefix: str) -> bool:
        """Return whether any stored word starts with *prefix*."""
        node = self._find(prefix)
        return node is not None and (bool(prefix) or node.is_word or bool(node.children))

    def delete(self, word: str) -> bool:
        """Delete *word*, returning whether it was present."""
        node = self._root
        path: list[tuple[_TrieNode, str]] = []
        for character in word:
            child = node.children.get(character)
            if child is None:
                return False
            path.append((node, character))
            node = child

        if not node.is_word:
            return False

        node.is_word = False
        for parent, character in reversed(path):
            child = parent.children[character]
            if child.is_word or child.children:
                break
            del parent.children[character]
        return True

    def _find(self, text: str) -> _TrieNode | None:
        node = self._root
        for character in text:
            child = node.children.get(character)
            if child is None:
                return None
            node = child
        return node
