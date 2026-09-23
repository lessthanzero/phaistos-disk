"""Keep unit-test inference metadata out of the production local ledger."""

import pytest


@pytest.fixture(autouse=True)
def isolate_local_model_metrics(monkeypatch: pytest.MonkeyPatch, tmp_path):
    """Redirect optional sibling telemetry before any test creates an LLM client."""
    monkeypatch.setenv("LOCAL_MODELS_LOG_FILE", str(tmp_path / "usage.jsonl"))
    monkeypatch.setenv("LOCAL_MODELS_METRICS_DB", str(tmp_path / "metrics.sqlite"))
