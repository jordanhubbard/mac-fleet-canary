"""Regression test for token ends around skipped whitespace."""

from toolkit.lexer import tokenize


def test_token_end_excludes_surrounding_whitespace() -> None:
    source = " \t12.5 +\n3  "
    tokens = tokenize(source)

    assert [token.value for token in tokens] == ["12.5", "+", "3"]
    assert [(token.position, token.end) for token in tokens] == [
        (2, 6),
        (7, 8),
        (9, 10),
    ]
    assert [source[token.position : token.end] for token in tokens] == [
        token.value for token in tokens
    ]
