"""Regression tests for zero-based lexer error positions."""

import pytest

from toolkit.lexer import LexerError, tokenize


@pytest.mark.parametrize(
    ("expression", "position"),
    [
        ("1 + @", 4),
        ("12.", 2),
    ],
)
def test_lexer_errors_identify_position(expression: str, position: int) -> None:
    with pytest.raises(LexerError, match=rf"\bposition {position}\b"):
        tokenize(expression)
