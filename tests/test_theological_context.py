"""Unit and property tests for the Bronze Age Cretan theological context layer."""

import pytest
from phaistos.corpus.loader import load_transcription
from phaistos.theology.models import (
    ConfidenceHierarchyLevel,
    LiturgicalSyntaxRole,
    TheologicalAuditResult,
    TheologicalSemanticField,
)
from phaistos.theology.theological_layer import (
    SIGN_THEOLOGICAL_CATALOG,
    classify_group_liturgical_role,
    evaluate_theological_context,
)


def test_sign_theological_catalog_completeness():
    """Verify that all 45 Evans signs have complete cultic and theological profiles."""
    assert len(SIGN_THEOLOGICAL_CATALOG) == 45
    for i in range(1, 46):
        sign_id = f"{i:02d}"
        assert sign_id in SIGN_THEOLOGICAL_CATALOG
        prof = SIGN_THEOLOGICAL_CATALOG[sign_id]
        assert prof.sign_id == sign_id
        assert isinstance(prof.semantic_field, TheologicalSemanticField)
        assert prof.confidence_grade in (
            ConfidenceHierarchyLevel.HIGH_ARCHAEOLOGICAL_CULT,
            ConfidenceHierarchyLevel.MODERATE_LINEAR_B_CONTINUITY,
        )
        assert len(prof.cultic_context) > 0
        assert len(prof.falsified_classical_retrofit) > 0


def test_classify_liturgical_roles():
    """Verify functional liturgical syntax classification of key groups."""
    corpus = load_transcription("godart_1995")
    all_groups = {g.id: g for g in corpus.all_groups()}

    # 1. Refrain A16 (02-12-31-26) -> INVOCATION
    g_a16 = all_groups["A16"]
    role, conf, rat = classify_group_liturgical_role(g_a16)
    assert role == LiturgicalSyntaxRole.INVOCATION
    assert "refrain" in rat.lower()

    # 2. Geminate B13 (29-24-24-20-35, JA-SA-SA-RA-ME skeleton) -> DIVINE_TITLE
    g_b13 = all_groups["B13"]
    role_b13, conf_b13, rat_b13 = classify_group_liturgical_role(g_b13)
    assert role_b13 == LiturgicalSyntaxRole.DIVINE_TITLE
    assert conf_b13 == ConfidenceHierarchyLevel.MODERATE_LINEAR_B_CONTINUITY

    # 3. Stroke group A03 (has stroke) -> RITUAL_RESPONSE
    g_a03 = all_groups["A03"]
    if getattr(g_a03, "oblique_stroke", False):
        role_a03, _, rat_a03 = classify_group_liturgical_role(g_a03)
        assert role_a03 == LiturgicalSyntaxRole.RITUAL_RESPONSE
        assert "stroke" in rat_a03.lower()


def test_evaluate_theological_context():
    """Test full evaluation of the theological layer with Monte Carlo testing."""
    corpus = load_transcription("godart_1995")
    res = evaluate_theological_context(corpus, num_monte_carlo=200, seed=42)

    assert isinstance(res, TheologicalAuditResult)
    assert res.total_signs_analyzed == 45
    assert res.epistemic_guardrails_passed is True

    # Liturgical syntax audit
    assert res.liturgical_syntax.total_groups == 61
    assert res.liturgical_syntax.transition_adherence_pct > 50.0
    assert 0.0 <= res.liturgical_syntax.monte_carlo_p_value <= 1.0

    # Semantic fields representation
    assert len(res.field_token_counts) >= 8
    assert "DIVINE_INVOCATION" in res.field_token_counts
    assert "BULL_COMPLEX_SACRIFICE" in res.field_token_counts
    assert "SACRED_VEGETATION" in res.field_token_counts

    # Skeptic verdict presence
    assert "BRONZE AGE CRETAN THEOLOGICAL CONTEXT" in res.skeptic_verdict
    assert "The Skeptic Rule" in res.skeptic_verdict or "SKEPTIC" in res.skeptic_verdict
