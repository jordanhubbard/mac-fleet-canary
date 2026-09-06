"""Tokenize simple arithmetic expressions."""

from dataclasses import dataclass
from enum import Enum


class TokenType(Enum):
    """Kinds of tokens recognized by :func:`tokenize`."""

    NUMBER = "NUMBER"
    PLUS = "+"
    MINUS = "-"
    STAR = "*"
    SLASH = "/"
    LEFT_PAREN = "("
    RIGHT_PAREN = ")"


@dataclass(frozen=True)
class Token:
    """A token and its zero-based position in the source expression."""

    type: TokenType
    value: str
    position: int


class LexerError(ValueError):
    """Raised when an expression contains a character that cannot be tokenized."""


_SYMBOLS = {
    "+": TokenType.PLUS,
    "-": TokenType.MINUS,
    "*": TokenType.STAR,
    "/": TokenType.SLASH,
    "(": TokenType.LEFT_PAREN,
    ")": TokenType.RIGHT_PAREN,
}


def tokenize(expression: str) -> list[Token]:
    """Return the arithmetic tokens in *expression*.

    Whitespace is ignored. A number may contain one decimal point and must
    contain at least one digit. Minus is always emitted separately, allowing a
    parser to distinguish unary negation from subtraction.
    """

    tokens: list[Token] = []
    position = 0

    while position < len(expression):
        character = expression[position]

        if character.isspace():
            position += 1
            continue

        token_type = _SYMBOLS.get(character)
        if token_type is not None:
            tokens.append(Token(token_type, character, position))
            position += 1
            continue

        if character.isdigit() or (
            character == "."
            and position + 1 < len(expression)
            and expression[position + 1].isdigit()
        ):
            start = position
            seen_decimal = character == "."
            position += 1

            while position < len(expression):
                character = expression[position]
                if character.isdigit():
                    position += 1
                elif character == "." and not seen_decimal:
                    seen_decimal = True
                    position += 1
                else:
                    break

            if position < len(expression) and expression[position] == ".":
                raise LexerError(f"invalid character '.' at position {position}")

            tokens.append(Token(TokenType.NUMBER, expression[start:position], start))
            continue

        raise LexerError(f"invalid character {character!r} at position {position}")

    return tokens
