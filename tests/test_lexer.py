import pytest

from toolkit.lexer import LexerError, Token, TokenType, tokenize


def test_tokenizes_operators_and_ignores_whitespace() -> None:
    assert tokenize(" 12 +\t34.50 / 2\n") == [
        Token(TokenType.NUMBER, "12", 1),
        Token(TokenType.PLUS, "+", 4),
        Token(TokenType.NUMBER, "34.50", 6),
        Token(TokenType.SLASH, "/", 12),
        Token(TokenType.NUMBER, "2", 14),
    ]


def test_tokenizes_nested_parentheses() -> None:
    assert [token.type for token in tokenize("((10-2)*(.5+3.))")] == [
        TokenType.LEFT_PAREN,
        TokenType.LEFT_PAREN,
        TokenType.NUMBER,
        TokenType.MINUS,
        TokenType.NUMBER,
        TokenType.RIGHT_PAREN,
        TokenType.STAR,
        TokenType.LEFT_PAREN,
        TokenType.NUMBER,
        TokenType.PLUS,
        TokenType.NUMBER,
        TokenType.RIGHT_PAREN,
        TokenType.RIGHT_PAREN,
    ]


def test_negative_number_keeps_unary_minus_separate() -> None:
    assert tokenize("-42.75") == [
        Token(TokenType.MINUS, "-", 0),
        Token(TokenType.NUMBER, "42.75", 1),
    ]


@pytest.mark.parametrize("expression", ["1..2", ".", "2 + @", "2 + ²"])
def test_invalid_character_raises_clear_error(expression: str) -> None:
    with pytest.raises(LexerError, match=r"invalid character .* at position \d+"):
        tokenize(expression)
