# Lexer parenthesized expression

`tokenize` reports token values and their zero-based positions in a parenthesized expression.

```python
from toolkit.lexer import tokenize

expression = "(8 - 3) * 2"
triples = [(token.type.value, token.value, token.position) for token in tokenize(expression)]

assert triples == [
    ("LEFT_PAREN", "(", 0),
    ("NUMBER", "8", 1),
    ("MINUS", "-", 3),
    ("NUMBER", "3", 5),
    ("RIGHT_PAREN", ")", 6),
    ("STAR", "*", 8),
    ("NUMBER", "2", 10),
]
```
