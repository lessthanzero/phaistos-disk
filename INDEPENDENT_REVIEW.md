# Independent Review Summary (v0.2.0)

In-repo adversarial reviews of the stratified monograph / empirical model:

| Source | Disposition |
|--------|-------------|
| [reports/gpt_5_6_peer_review.md](reports/gpt_5_6_peer_review.md) | **REJECT** |
| [reports/cursor_peer_review.md](reports/cursor_peer_review.md) | **MAJOR REVISIONS** (inferential chapters reject-leaning) |

Both reviews endorse descriptive spine items (corpus arithmetic; Lyric Triad `02-12-31-26`) and reject promoting liturgical reconstruction, hard-coded metrics, or Shannon “laws” as settled science.

## Adversarial themes

| Lens | Themes |
|------|--------|
| **Statistician** | Non-exchangeable / curated homology nulls; unreproducible *Z*; hard-coded fits and Bayes factors; misuse of Shannon unicity; 241 vs 242 inconsistency |
| **Archaeologist** | Fabricated typometry/petrography; Evans numbering category error; iconographic circularity; LM IIIA Hagia Triada chronology gap; unfalsifiable “liturgical conservatism” |
| **Software engineer** | Constants dressed as results; docstring/corpus census drift; modules that assert verdicts without computing likelihoods |

## Severity table

| ID | Finding | Severity | 0.2.0 resolution |
|----|---------|----------|------------------|
| R1 | Semantic libretto / hymn as decipherment-by-another-name | Critical | Documented as speculation in `SCIENTIFIC_LIMITATIONS.md`; no claim upgrade in this release |
| R2 | Hard-coded language fits, p-values, concordance % | Critical | Flagged; regeneration or deletion deferred beyond hygiene release |
| R3 | Homology Monte Carlo non-exchangeable / inconsistent *Z* | Critical | Flagged; exchangeable-null rebuild not claimed complete in 0.2.0 |
| R4 | Shannon “Epistemic Law” misattribution | High | Relabeled as heuristic caveat in limitations doc |
| R5 | Typometry / petrography precision without methods | High | Treated as unsupported; media/provenance carve-outs in `NOTICE` |
| R6 | 241 vs 242 census ambiguity | Medium | Explicitly declared in limitations |
| R7 | LAN IPs / personal endpoints in docs and clients | Medium | **Fixed** — `$OLLAMA_HOST` / localhost only |
| R8 | Uncleared museum / Wikimedia media under MIT tree | Medium | **Fixed** — `NOTICE` + `.gitignore` carve-outs |
| R9 | Lyric Triad observation buried under overclaim | Low (positive) | Elevated as flagship **observation**; meter/God remain hypotheses |

## What 0.2.0 does *not* claim

Passing tests, dual-node sync, or a research-preview tag does **not** overturn REJECT dispositions on inferential chapters. Residual open work: regenerate or delete non-corpus numbers; rebuild homology with blind coding; separate observation modules from narrative glosses.

Primary evidence for dispositions: the two peer-review reports linked above (read-only audits against the authors’ own code).
