"""Tests for the arithmetic lexer."""

import pytest

from toolkit.lexer import LexerError, Token, TokenType, tokenize


def test_tokenizes_operators_and_ignores_whitespace() -> None:
    assert tokenize(" 12 +\t3.5 / 7\n") == [
        Token(TokenType.NUMBER, "12", 1),
        Token(TokenType.PLUS, "+", 4),
        Token(TokenType.NUMBER, "3.5", 6),
        Token(TokenType.SLASH, "/", 10),
        Token(TokenType.NUMBER, "7", 12),
    ]


def test_tokenizes_nested_parentheses() -> None:
    assert [token.type for token in tokenize("((10-2)*3)")] == [
        TokenType.LEFT_PAREN,
        TokenType.LEFT_PAREN,
        TokenType.NUMBER,
        TokenType.MINUS,
        TokenType.NUMBER,
        TokenType.RIGHT_PAREN,
        TokenType.STAR,
        TokenType.NUMBER,
        TokenType.RIGHT_PAREN,
    ]


def test_negative_number_keeps_unary_minus_separate() -> None:
    assert tokenize("-42.75") == [
        Token(TokenType.MINUS, "-", 0),
        Token(TokenType.NUMBER, "42.75", 1),
    ]


@pytest.mark.parametrize(
    "expression", ["2 ^ 3", "1 + \u00b2", ".5", "5.", "1.2.3"]
)
def test_rejects_invalid_characters_and_malformed_decimals(expression: str) -> None:
    with pytest.raises(LexerError, match="position"):
        tokenize(expression)


def test_empty_and_whitespace_only_expressions_have_no_tokens() -> None:
    assert tokenize("") == []
    assert tokenize(" \t\n") == []
