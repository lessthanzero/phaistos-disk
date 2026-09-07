"""Tests for Codex consultation client and sign data models."""

from pathlib import Path
import pytest
from phaistos.consultation.codex_client import CodexClient
from phaistos.consultation.models import SignConsultationDossier


def test_codex_client_cached_or_fallback(tmp_path):
    """Verify CodexClient can retrieve cached or fallback dossiers without error."""
    client = CodexClient(cache_dir=tmp_path)
    dossier = client.consult_sign("02", force_refresh=False, use_codex=False)

    assert isinstance(dossier, SignConsultationDossier)
    assert dossier.sign_id == "02"
    assert dossier.iconography.canonical_name == "Plumed Head"
    assert "CH_040" in dossier.iconography.cretan_hieroglyphic_parallel
    assert len(dossier.phonetics.proposed_phonetic_values) > 0

    # Test cache retrieval
    dossier_cached = client.consult_sign("02", force_refresh=False, use_codex=False)
    assert dossier_cached.cached is True


def test_codex_client_unknown_sign(tmp_path):
    """Verify graceful handling of uncataloged sign ID."""
    client = CodexClient(cache_dir=tmp_path)
    dossier = client.consult_sign("99", force_refresh=False, use_codex=False)

    assert dossier.sign_id == "99"
    assert "Sign 99" in dossier.iconography.canonical_name
