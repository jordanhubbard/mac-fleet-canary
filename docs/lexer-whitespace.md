# Lexer whitespace positions

`tokenize` skips whitespace, but each token's zero-based `position` refers to
its location in the original input, including any skipped whitespace.

```python
from toolkit import tokenize

expression = "\t7\n+ 8"
triples = [(token.type.value, token.value, token.position) for token in tokenize(expression)]

assert triples == [
    ("NUMBER", "7", 1),
    ("PLUS", "+", 3),
    ("NUMBER", "8", 5),
]
```
