"""Tokenizer for simple arithmetic expressions."""

from dataclasses import dataclass
from enum import Enum


class TokenType(str, Enum):
    """Kinds of tokens recognized by the arithmetic lexer."""

    NUMBER = "NUMBER"
    PLUS = "PLUS"
    MINUS = "MINUS"
    STAR = "STAR"
    SLASH = "SLASH"
    LEFT_PAREN = "LEFT_PAREN"
    RIGHT_PAREN = "RIGHT_PAREN"


@dataclass(frozen=True)
class Token:
    """A token and its zero-based location in the source expression."""

    type: TokenType
    value: str
    position: int


class LexerError(ValueError):
    """Raised when an expression contains a character that cannot be tokenized."""


_SINGLE_CHARACTER_TOKENS = {
    "+": TokenType.PLUS,
    "-": TokenType.MINUS,
    "*": TokenType.STAR,
    "/": TokenType.SLASH,
    "(": TokenType.LEFT_PAREN,
    ")": TokenType.RIGHT_PAREN,
}


def tokenize(expression: str) -> list[Token]:
    """Convert an arithmetic expression into tokens.

    A minus sign is always emitted separately, allowing a parser to decide
    whether it is unary or binary. Numeric literals may contain one decimal
    point and must contain an ASCII digit on each side of it.
    """

    tokens: list[Token] = []
    index = 0

    while index < len(expression):
        character = expression[index]

        if character.isspace():
            index += 1
            continue

        token_type = _SINGLE_CHARACTER_TOKENS.get(character)
        if token_type is not None:
            tokens.append(Token(token_type, character, index))
            index += 1
            continue

        if "0" <= character <= "9":
            start = index
            while index < len(expression) and "0" <= expression[index] <= "9":
                index += 1

            if index < len(expression) and expression[index] == ".":
                decimal_position = index
                index += 1
                if index == len(expression) or not "0" <= expression[index] <= "9":
                    raise LexerError(
                        f"Invalid decimal point at position {decimal_position}"
                    )
                while index < len(expression) and "0" <= expression[index] <= "9":
                    index += 1

            tokens.append(Token(TokenType.NUMBER, expression[start:index], start))
            continue

        raise LexerError(f"Invalid character {character!r} at position {index}")

    return tokens
