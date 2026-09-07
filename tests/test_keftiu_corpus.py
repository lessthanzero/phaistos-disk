"""Unit tests for the Egyptian Keftiu (Minoan) Corpus Module."""

import pytest
from phaistos.linguistics.keftiu_corpus import load_keftiu_corpus, analyze_keftiu_phonology


def test_keftiu_corpus_loading():
    """Verify loading of London Medical Papyrus spells and BM 5647 name lists."""
    texts = load_keftiu_corpus()
    assert len(texts) >= 14

    # Check presence of Spell 32 (curative incantation)
    sp32 = next(t for t in texts if t.id == "KEFTIU_SPELL_32")
    assert "London Medical Papyrus" in sp32.source
    assert sp32.syllable_count == 15
    assert "pu-pu" in sp32.reduplication_motifs
    assert "ka-ka" in sp32.reduplication_motifs

    # Check presence of anthroponyms
    name1 = next(t for t in texts if t.id == "KEFTIU_NAME_01")
    assert name1.vocalized_reconstruction == "A-SA-KA-RA-TU"
    assert len(name1.syllables) == 5


def test_keftiu_phonology_summary():
    """Verify phonological profile extraction from Keftiu inscriptions."""
    texts = load_keftiu_corpus()
    summary = analyze_keftiu_phonology(texts)

    assert summary.total_words >= 14
    assert summary.total_syllables > 50
    assert summary.open_syllable_rate_pct == 100.0  # 100% open CV / V syllables
    assert summary.reduplication_instance_count >= 3

    # Check consonant and vowel inventories
    assert "a" in summary.vowel_inventory
    assert "i" in summary.vowel_inventory
    assert "u" in summary.vowel_inventory
    assert "k" in summary.consonant_inventory
    assert "t" in summary.consonant_inventory
    assert "r" in summary.consonant_inventory
