"""Regression test for tokenizing a signed decimal expression."""

from toolkit.lexer import tokenize


def test_signed_decimal_tokens_include_complete_triples() -> None:
    assert [
        (token.type.value, token.value, token.position)
        for token in tokenize("0.5 + -2")
    ] == [
        ("NUMBER", "0.5", 0),
        ("PLUS", "+", 4),
        ("MINUS", "-", 6),
        ("NUMBER", "2", 7),
    ]
