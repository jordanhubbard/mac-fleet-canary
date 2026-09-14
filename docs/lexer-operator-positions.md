# Lexer operator positions

`tokenize` reports each token's zero-based position in the original expression.

```python
from toolkit.lexer import tokenize

expression = "2 + 3 * 4"
triples = [(token.type.value, token.value, token.position) for token in tokenize(expression)]

assert triples == [
    ("NUMBER", "2", 0),
    ("PLUS", "+", 2),
    ("NUMBER", "3", 4),
    ("STAR", "*", 6),
    ("NUMBER", "4", 8),
]
```
