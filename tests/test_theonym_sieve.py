"""Unit tests for the theonym structural sieve."""

import pytest
from phaistos.corpus.loader import load_transcription
from phaistos.comparative.theonym_sieve import (
    execute_theonym_sieve,
    extract_structural_skeleton,
    load_aegean_theonyms,
    find_skeleton_matches,
)
from phaistos.comparative.theonym_models import TheonymSieveResult


def test_extract_structural_skeleton():
    assert extract_structural_skeleton(["29", "24", "24", "20", "35"]) == "A-B-B-C-D"
    assert extract_structural_skeleton(["02", "12", "31", "26"]) == "A-B-C-D"
    assert extract_structural_skeleton(["JA", "SA", "SA", "RA", "ME"]) == "A-B-B-C-D"
    assert extract_structural_skeleton(["29", "29", "34"]) == "A-A-B"


def test_load_aegean_theonyms():
    theonyms = load_aegean_theonyms()
    assert len(theonyms) >= 10
    names = [t.name for t in theonyms]
    assert "JA-SA-SA-RA-ME" in names
    assert "PA-JA-WO-NE" in names
    assert "PO-TI-NI-JA" in names


def test_find_skeleton_matches():
    corpus = load_transcription("godart_1995")
    theonyms = load_aegean_theonyms()
    matches = find_skeleton_matches(corpus, theonyms)
    assert len(matches) > 0

    # B13 should match JA-SA-SA-RA-ME
    b13_match = next((m for m in matches if m.group_id == "B13" and m.theonym_name == "JA-SA-SA-RA-ME"), None)
    assert b13_match is not None
    assert b13_match.is_geminate_match is True


def test_execute_theonym_sieve():
    corpus = load_transcription("godart_1995")
    res = execute_theonym_sieve(corpus, num_surrogates=200, seed=42)

    assert isinstance(res, TheonymSieveResult)
    assert res.total_theonyms_evaluated >= 10
    assert len(res.phonotactic_trials) == 3
    assert "THEONYM STRUCTURAL SIEVE" in res.skeptic_verdict
