# mac-fleet-canary

A canary project for the `mac` multi-agent fleet control plane. Its purpose
is not the code it produces — it's a controlled stress test of how the fleet
handles **genuinely parallel, independent work landing on the same `main`
branch**: git worktree isolation, PR review, merge-conflict avoidance, and
CI-gated integration.

## What this project is

A small Python utility library, `toolkit/`, made of independent,
self-contained algorithm modules. Each module is:

- A single file under `toolkit/<name>.py`
- Fully type-hinted
- Covered by its own test file `tests/test_<name>.py` with real edge-case
  coverage, not just a happy-path smoke test
- Exported from `toolkit/__init__.py`
- Documented in this README's module table (one row, added by the same PR
  that implements the module)

Modules are deliberately chosen to have **no dependencies on each other** —
implementing `toolkit/lru_cache.py` should never require touching
`toolkit/trie.py`. This is the parallelism property the canary is testing:
if the fleet's worktree/dispatch/merge machinery is healthy, N agents should
be able to implement N independent modules concurrently and land all N on
`main` without manual conflict resolution.

## Roadmap / module checklist

Each unchecked row is an open, independently claimable task. Check it off
(and fill in the PR link) only once its module + tests are merged to `main`
with CI green.

| Module | Description | Status | PR |
|---|---|---|---|
| `lru_cache` | Fixed-capacity LRU cache, O(1) get/put | ⬜ open | |
| `trie` | Prefix tree: insert, search, starts_with, delete | ⬜ open | |
| `union_find` | Disjoint-set with path compression + union by rank | ✅ merged | PR pending publication |
| `lexer` | Tiny arithmetic-expression tokenizer (`+ - * / ( ) numbers`) | ⬜ open | |
| `graph_topo_sort` | Kahn's algorithm topological sort, cycle detection | ⬜ open | |
| `bloom_filter` | Bit-array Bloom filter with configurable false-positive rate | ⬜ open | |
| `interval_tree` | Interval insert + overlap query | ⬜ open | |
| `rate_limiter` | Token-bucket rate limiter, thread-safe | ⬜ open | |
| `bktree` | BK-tree for approximate string matching (edit distance) | ⬜ open | |
| `skiplist` | Probabilistic skip list: insert, search, delete | ⬜ open | |

## Victory conditions

This canary run is considered **successful** when, without any manual
conflict resolution or human git intervention:

1. All 10 modules above are merged to `main`.
2. Each module's own test file passes in CI.
3. `main`'s CI is green on the final merge (no broken intermediate state).
4. At least 2 of the 10 modules were implemented and merged **concurrently**
   by different agents (overlapping wall-clock time between claim and merge)
   — proving real parallelism, not serialized turn-taking.
5. No PR required a force-push or manual rebase to resolve a conflict caused
   by another agent's concurrent work landing first (a normal `git pull
   --rebase` picking up someone else's unrelated merged module is fine and
   expected; an actual line-level conflict on shared code is not, since no
   module should touch another's file).

## Contributing (for fleet agents)

1. Claim exactly one unchecked module from the table above.
2. Work in your own git worktree, on a branch named `add-<module>`.
3. Implement `toolkit/<module>.py`, `tests/test_<module>.py`, add the
   `__init__.py` export, and update this README's table row (status + your
   PR link once opened).
4. Open a PR. CI must pass before merge.
5. Do not touch any other module's files in your PR — if your work
   genuinely needs to touch shared infrastructure (`toolkit/__init__.py`,
   this README, `pyproject.toml`), keep that diff minimal and additive only.

## Setup

```bash
python3 -m venv .venv && source .venv/bin/activate
pip install -e ".[dev]"
pytest
```

CI (`.github/workflows/ci.yml`) runs `pytest` and a type check on every PR
and on `main`.
