"""Unit tests for the LLM client and Skeptic review engine."""

import pytest
from phaistos.decipherment.models import DeciphermentResult
from phaistos.llm.client import OllamaClient
from phaistos.llm.skeptic import conduct_skeptic_review
from phaistos.core.provenance import ProvenanceCategory


def test_ollama_client_instantiation():
    client = OllamaClient()
    assert client.host == "http://localhost:11434"
    assert "qwen" in client.default_model


def test_skeptic_fallback_when_offline():
    # Force offline client to test deterministic fallback
    offline_client = OllamaClient(host="http://127.0.0.1:9999")

    dummy_res = DeciphermentResult(
        hypothesis_id="H_TEST",
        target_language="test",
        observed_score=-250.0,
        null_mean_score=-260.0,
        null_std_score=10.0,
        z_score=1.0,
        p_value=0.20,
        is_falsified=True,
        skeptic_verdict="FALSIFIED",
        unicity_ratio=0.5,
        sample_transliteration={"A01": "test"},
        contradictions=["Test contradiction"],
    )

    review = conduct_skeptic_review(dummy_res, client=offline_client)
    assert review.category == ProvenanceCategory.MODEL_INFERENCE
    assert "SKEPTIC REVIEW" in review.data
    assert "Methodological Vulnerability" in review.data
