"""Regression test for zero-based arithmetic operator positions."""

from toolkit.lexer import tokenize


def test_operator_tokens_include_original_positions() -> None:
    assert [
        (token.type.value, token.value, token.position)
        for token in tokenize("2 + 3 * 4")
    ] == [
        ("NUMBER", "2", 0),
        ("PLUS", "+", 2),
        ("NUMBER", "3", 4),
        ("STAR", "*", 6),
        ("NUMBER", "4", 8),
    ]
