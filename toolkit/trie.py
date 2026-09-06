"""A prefix tree for storing strings."""


class _TrieNode:
    def __init__(self) -> None:
        self.children: dict[str, _TrieNode] = {}
        self.is_word = False


class Trie:
    """Store words and query them by exact value or prefix."""

    def __init__(self) -> None:
        self._root = _TrieNode()

    def insert(self, word: str) -> None:
        """Insert *word* into the trie."""
        node = self._root
        for character in word:
            node = node.children.setdefault(character, _TrieNode())
        node.is_word = True

    def search(self, word: str) -> bool:
        """Return whether *word* is stored as a complete word."""
        node = self._find_node(word)
        return node is not None and node.is_word

    def starts_with(self, prefix: str) -> bool:
        """Return whether any stored word starts with *prefix*."""
        node = self._find_node(prefix)
        return node is not None and (node.is_word or bool(node.children))

    def delete(self, word: str) -> None:
        """Remove *word* while preserving nodes shared with other words."""
        node = self._root
        path: list[tuple[_TrieNode, str]] = []
        for character in word:
            child = node.children.get(character)
            if child is None:
                return
            path.append((node, character))
            node = child

        if not node.is_word:
            return
        node.is_word = False

        for parent, character in reversed(path):
            child = parent.children[character]
            if child.is_word or child.children:
                break
            del parent.children[character]

    def _find_node(self, value: str) -> _TrieNode | None:
        node = self._root
        for character in value:
            child = node.children.get(character)
            if child is None:
                return None
            node = child
        return node
