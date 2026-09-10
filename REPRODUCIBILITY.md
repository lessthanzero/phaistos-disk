# Reproducibility

## Environment

- Python ≥ 3.12
- [uv](https://github.com/astral-sh/uv) for sync/lock/run
- macOS and Linux supported for the test suite

## Local

```bash
uv sync --group dev
uv run pytest
uv run ruff check src tests
uv run phaistos workbench --output reports/workbench.html
```

Third-party photos are excluded from the default public tree ([NOTICE](NOTICE)). The workbench generator still runs; media may be missing until you fetch and attribute sources yourself.

Monte Carlo / surrogate tools accept explicit seeds (commonly `42` in tests). Report seed, surrogate type, and iteration count with any published p-value.

## CI

GitHub Actions runs `uv sync`, `ruff`, and `pytest` on push/PR (Python 3.12).
