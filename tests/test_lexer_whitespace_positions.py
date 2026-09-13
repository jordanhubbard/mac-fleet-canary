"""Tests for token positions across skipped whitespace."""

from toolkit import tokenize


def test_whitespace_preserves_original_token_positions() -> None:
    assert [(token.type.value, token.value, token.position) for token in tokenize("\t7\n+ 8")] == [
        ("NUMBER", "7", 1),
        ("PLUS", "+", 3),
        ("NUMBER", "8", 5),
    ]
