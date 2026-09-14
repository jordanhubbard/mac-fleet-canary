# Lexer signed decimal expression

`tokenize` reports decimal and sign tokens with their zero-based positions.

```python
from toolkit.lexer import tokenize

expression = "0.5 + -2"
triples = [(token.type.value, token.value, token.position) for token in tokenize(expression)]

assert triples == [
    ("NUMBER", "0.5", 0),
    ("PLUS", "+", 4),
    ("MINUS", "-", 6),
    ("NUMBER", "2", 7),
]
```
