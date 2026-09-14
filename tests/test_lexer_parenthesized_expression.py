"""Regression test for tokenizing a parenthesized arithmetic expression."""

from toolkit.lexer import tokenize


def test_parenthesized_expression_tokens_include_complete_triples() -> None:
    assert [
        (token.type.value, token.value, token.position)
        for token in tokenize("(8 - 3) * 2")
    ] == [
        ("LEFT_PAREN", "(", 0),
        ("NUMBER", "8", 1),
        ("MINUS", "-", 3),
        ("NUMBER", "3", 5),
        ("RIGHT_PAREN", ")", 6),
        ("STAR", "*", 8),
        ("NUMBER", "2", 10),
    ]
