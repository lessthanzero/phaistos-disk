# Scientific Limitations (v0.2.0 research preview)

This repository is a computational workbench for the Phaistos Disc. It does **not** decipher the Disc, recover a language, or establish a historical liturgy.

## Observation vs hypothesis vs speculation

| Tier | Meaning | Examples |
|------|---------|----------|
| **Observation** | Reproducible from the transcription / corpus arithmetic | Token/group/sign counts; A16/A19/A22 = `02-12-31-26` with group-final strokes |
| **Hypothesis** | Interpretable models that need controls and can fail | Mora/meter; hymn/paean genre; “God” / divine-prefix readings; Hagia Triada homology |
| **Speculation** | Narrative or numeric claims without auditable derivation | Hard-coded language-fit %, fabricated typometry/petrography, unconstrained libretto glosses |

Do not promote hypotheses or speculation to observation without surrogate tests, exchangeable nulls, and independent review.

## Flagship observation

Groups **A16, A19, and A22** are each transcribed as **`02-12-31-26`**, each with an oblique stroke. That repetition is the strongest in-corpus structural regularity this lab treats as reportable. Surrounding claims (strophic responsion, silent honorific prefix, musical rests) are **hypotheses**, not observations.

## Mora / hymn / God

- **Morae, cola, catalexis, responsion** presuppose phonetic value and syllabification that the Disc does not supply.
- **Hymn / paean / liturgical reconstruction** and **Goddess / divine cartouche** readings are interpretive overlays. Semantic glosses in libretto modules are speculation unless independently anchored.

## Hardcoded and historical-stats caveats

Several headline figures in older monograph prose or dataclasses (language-family fit percentages, Bayes factors, open-syllable rates, comparative concordance %, some homology *Z* values) are **constants or hand-tuned knobs**, not regenerated likelihoods. Treat any statistic that cannot be recomputed from code + seeds + documented priors as **non-evidential**.

Shannon-style “unicity” modules here are **parsimony / overfitting heuristics**, not Shannon’s cipher unicity distance, and depend on free parameters (redundancy, lexicon size, DoF knobs).

## 241 vs 242 census ambiguity

Scholarship often cites **241** signs; some modern transcriptions count **242** (damaged/ambiguous A8). This lab’s live corpus arithmetic commonly uses **242** (Side A 123 + Side B 119). Capacity and unicity figures must state which census they use; do not switch opportunistically between 241 and 242.

## What would falsify or anchor claims

- A **bilingual** or a second object stamped with the **same punches**.
- **Preregistered, blind** motif matching with an exchangeable null (not curated best-case overlap vs random draw).
- Independent physical metrology (RTI / µ-CT / pXRF on comparanda) for manufacturing and provenance claims.
- Surrogate tests (shuffle, frequency-preserving, Markov-preserving) that **fail** for any structural hypothesis advanced as supported.
- For phonetic or language-family claims: independently assigned sound values — without them, phonotactic “fits” are circular.

See also [NOTICE](NOTICE) for license carve-outs and [INDEPENDENT_REVIEW.md](INDEPENDENT_REVIEW.md) for peer-review disposition.
