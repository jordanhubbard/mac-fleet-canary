"""Approximate string matching with a Burkhard-Keller tree."""


def levenshtein_distance(left: str, right: str) -> int:
    """Return the Levenshtein edit distance between two strings."""
    if len(left) < len(right):
        left, right = right, left

    previous = list(range(len(right) + 1))
    for left_index, left_character in enumerate(left, start=1):
        current = [left_index]
        for right_index, right_character in enumerate(right, start=1):
            current.append(
                min(
                    current[-1] + 1,
                    previous[right_index] + 1,
                    previous[right_index - 1]
                    + (left_character != right_character),
                )
            )
        previous = current
    return previous[-1]


class _Node:
    def __init__(self, word: str) -> None:
        self.word = word
        self.children: dict[int, _Node] = {}


class BKTree:
    """A BK-tree using Levenshtein distance as its metric."""

    def __init__(self) -> None:
        self._root: _Node | None = None

    def insert(self, word: str) -> None:
        """Insert *word* into the tree, ignoring duplicate insertions."""
        if self._root is None:
            self._root = _Node(word)
            return

        node = self._root
        while True:
            distance = levenshtein_distance(word, node.word)
            if distance == 0:
                return
            child = node.children.get(distance)
            if child is None:
                node.children[distance] = _Node(word)
                return
            node = child

    def search(self, word: str, max_distance: int) -> list[tuple[str, int]]:
        """Return ``(matching_word, distance)`` pairs within *max_distance*."""
        if max_distance < 0:
            raise ValueError("max_distance must be non-negative")
        if self._root is None:
            return []

        matches: list[tuple[str, int]] = []
        pending = [self._root]
        while pending:
            node = pending.pop()
            distance = levenshtein_distance(word, node.word)
            if distance <= max_distance:
                matches.append((node.word, distance))

            lower = distance - max_distance
            upper = distance + max_distance
            pending.extend(
                child
                for edge, child in node.children.items()
                if lower <= edge <= upper
            )

        return sorted(matches)
