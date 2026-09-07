I have verified the monograph against the laboratory's own corpus and computational modules. The findings below are grounded in what the code actually computes versus what the text claims. Here is the committee report.

---

# TIER-2 PEER REVIEW REPORT

**Manuscript**: *The Phaistos Disc: A Stratified Computational & Liturgical Reconstruction*
**Convening bodies**: International Epigraphic Association; Society for Mediterranean Archaeology
**Panel**: Minoan Paleography (Reviewer 1) · Cryptanalysis & Information Theory (Reviewer 2) · Aegean Historical Linguistics (Reviewer 3)
**Disposition**: Verification performed against the authors' own repository (`corpus/`, `src/phaistos/stats`, `src/phaistos/linguistics`). Several headline statistics were re-executed.

---

## 1. Executive Assessment & Epistemic Demarcation

The committee commends the manuscript's central strategic decision: it declines to assert a phonetic "reading" and instead frames its contribution as (a) physical description, (b) internal structural statistics, and (c) null-rejection against surrogates. In principle this is the correct posture, and it distinguishes the work from the Gordon/Faucounau/Owens tradition of full pseudo-translations. The document's clearest, most defensible achievements are genuinely present in the data:

- We independently confirm the corpus arithmetic: **61 groups, 242 sign-tokens (Side A 123 / Side B 119), 45 distinct signs**. These are correct and match the canonical Godart 1995 transcription in the repository.
- We independently confirm the **Lyric Triad**: groups A16, A19, A22 are each exactly `02-12-31-26` and each carries an oblique stroke. This is a real, striking, and legitimately reportable structural regularity.

However, the manuscript does **not** escape the "decipherment trap"; it relocates it. The abstract renounces translation, but Chapter 5 then supplies a 14-clause semantic libretto ("Epiphany of the Goddess in her chariot," "blood aspersion," "honey offering"). Assigning liturgical meaning to every group *is* a decipherment in all but name — one that inherits exactly the confirmation bias the Skeptic Rule (`AGENTS.md`) was written to prevent. Worse, as documented in §5 below, the manuscript's quantitative scaffolding — the numbers that are supposed to license this move — is in several cases **hard-coded, circular, misattributed, or internally inconsistent**. The epistemic demarcation is therefore rhetorical rather than operational.

**Overall**: A sound descriptive layer is wrapped in an inferential layer whose statistics do not survive audit.

---

## 2. Audit of Physical Epigraphy & Typometry (Chapter 1)

**Sign-catalogue attributions — partially correct, one systematic error.** The Unicode code points are internally consistent and correct: every sign maps as `U+101D0 + (n−1)` (Sign 02 → U+101D1, Sign 12 → U+101DB, Sign 25 → U+101E8, Sign 38 → U+101F5, Sign 26 → U+101E9, Sign 24 → U+101E7). Good.

However, the repeated label **"Evans Sign 38 / Evans Sign 26"** is a **category error**. The Phaistos Disc sign inventory is not Evans's catalogue (Evans catalogued Cretan Hieroglyphic and Linear signs). The standard Disc numbering is the Pernier/Godart–Olivier (GORILA/CHIC-adjacent) PD list 01–45. Attributing it to Evans should be corrected throughout.

**Iconographic glosses — several are interpretive impositions, not accepted readings.** "Plumed head" (02), "round shield/buckler" (12), "ship" (25), "beehive/hive" (24), and "rosette/flower" (38) are broadly accepted descriptive labels. But **"Sign 26 = horns of consecration," "Sign 22 = double flute/aulos," and "Sign 28 = sacrificial bull haunch"** are not standard PD glyph identifications; they are semantic guesses selected precisely because they support the Hagia Triada homology of Chapter 3. This is textbook circularity: the sign meanings that feed the "independent" homology test are chosen *from* the homology hypothesis.

**Typometry — fabricated precision.** The values presented as measured fact — uniform relief depth $1.05\text{ mm}$, tilt variance $\pm 9.2^\circ$, "mean relief surface area $142.3\text{ mm}^2$," rim diameter $12.4\text{ mm}$ with "12 interior raised bosses" — have no published micro-topographic source. The Disc has never been subjected to a published metric survey yielding these figures. Presenting them as "micro-epigraphic examination confirms" is not defensible.

**Clay petrography — overclaimed.** The provenance of the Disc's fabric remains genuinely unresolved in the literature (it has never been destructively thin-sectioned given its unique status). The stated "$7.2\% \pm 0.4\%$ linear / $20.1\% \pm 1.1\%$ volumetric shrinkage … identical to Phaistian MM III fabrics" is invented precision, and the inference that A/B dimensional differences arise from firing shrinkage "rather than distinct punch dies" is speculation dressed as a result.

**The one defensible physical claim** is the *qualitative* single-punch (movable-type-like) hypothesis, which does have real scholarly standing (the reuse of identical stamps is the Disc's most famous physical feature). But "world's earliest movable-type **printed** artifact" overstates: there is no evidence of typesetting or a press. Recommend downgrading to "earliest known use of reusable type-punches (typographic stamping)."

---

## 3. Audit of Prosodic Architecture & Strophic Symmetry (Chapter 2)

**Mora metrics.** The group-length statistics (means 3.97 / 3.93) are arithmetically correct given 123/31 and 119/30. Reporting group-length distributions is legitimate. But "morae," "cola," "catalectic pause," and "strophic responsion" import Greek metrical categories that presuppose the phonetic reading the abstract disclaims. There is no independent evidence any sign is vocalized, so "mora" is undefined for this corpus.

**The Lyric Triad** (A16/A19/A22 = `02-12-31-26`) is real and is the paper's strongest observation. We endorse reporting it. We do **not** endorse the surrounding claim that A17–A18/A20–A21 "maintain symmetrical cola lengths" — this is asserted without a test, and the intervening groups are not equal in length.

**The `02-12` Bayesian comparison — does NOT resolve circularity.** We verified that `02-12` is genuinely over-represented; the discriminator module computes a real permutation z-score for the prefix against frequency-preserving shuffles, and prefix enrichment is a legitimate finding. **But**:

1. The variance reduction ($\sigma^2\!: 0.81\to0.29$, "64%") and **Bayes Factor $K=14.2$** are **not computed anywhere in the codebase** we could locate; they are asserted constants.
2. The reduction is **definitional, not evidential**: $H_1$ deletes a fixed-length recurring prefix from the counted units, so of course residual length-variance falls. Choosing to treat `02-12` as "unvocalized" *because* it regularizes the meter is precisely the model-tuning the Skeptic Rule forbids.
3. A Bayes factor requires explicit priors and likelihoods; none are specified, so $K=14.2$ is uninterpretable.

The determinative hypothesis is a reasonable *conjecture* (comparison to `DINGIR` is apt rhetorically), but the manuscript presents it with a spurious quantitative certificate.

---

## 4. Audit of Archaeological Realia & Liturgical Conservatism (Chapter 3)

**The qualitative parallels are real; the significance test is rigged.** The Hagia Triada Sarcophagus (HM, LM IIIA) genuinely depicts double-axes surmounted by birds, a libation into a situla/krater, a double-flute (aulos) player, a trussed bull on a sacrificial table, and boat/animal models presented at the tomb. That these overlap thematically with a Minoan cult object is unsurprising and plausible.

**But the $Z$ statistic is not reproducible and is internally contradictory.** The manuscript reports **three mutually inconsistent values**:

- Abstract & Chapter 3 headline: **$Z = +8.46\sigma$**, with the arithmetic printed as $(19-3.94)/1.86$.
- That arithmetic is simply **wrong**: $(19-3.94)/1.86 = \mathbf{8.10}$, not 8.46. (Your own §4 brief cites $+8.10\sigma$.)
- Re-executing the actual module (`evaluate_homology_significance`, seed 42, N=10,000) yields **$Z = 8.51$, mean 3.93, std 1.77, p = 0.0** — a third value.

Three figures (8.10 / 8.46 / 8.51) for one statistic in a document whose banner claims "131/131 tests passing" is a serious reproducibility failure.

**More fundamentally, the null is non-exchangeable (rigged).** The "observed overlap" of 19 is nothing but the cardinality of a hand-curated set:

```34:52:src/phaistos/stats/homology_surrogate.py
    OBSERVED_HOMOLOGY_SIGNS = {
        "02", "06", "12", "16", "21", "23", "24", "26", "27",
        "28", "30", "31", "32", "35", "37", "38", "39", "41", "44",
    }
    k_observed = len(OBSERVED_HOMOLOGY_SIGNS)  # 19 signs
    total_disc_signs = 45
    ...
    bg_universe_size = 320
    ht_motif_count = 28
    ...
    for i in range(n_iterations):
        sample = rng.choice(bg_universe_size, size=total_disc_signs, replace=False)
        # Assume HT motifs are represented by indices 0..ht_motif_count-1
        overlap = np.sum(sample < ht_motif_count)
```

The comment says "18 Phaistos signs" while the set contains 19 (a further internal contradiction). The random arm draws 45 motifs from 320 and counts hits in a designated block of 28; the "observed" arm is a **confirmatory hand-selection maximised against the same target**. Comparing a curated best-case count to a blind random draw is not a valid permutation test — it is guaranteed to produce a large $Z$ by construction. The background parameters (320 universe, 28 HT motifs) are also unsourced. The verdict string even names realia ("phorminx," "griffin chariot") absent from the manuscript's own table.

**Chronology / conservatism.** The ~300–350-year gap (MM III–LM I vs LM IIIA) is stated correctly. The conservatism argument is not unreasonable *in itself*, but it is **unfalsifiable** as deployed: double-axes, horns of consecration, birds, and libation are pan-Minoan across the whole period and the whole island. Their recurrence demonstrates broad cultic continuity, **not** a specific textual link between this Disc and this sarcophagus. The "Rosetta Split" framing is therefore misleading — nothing here functions as a bilingual.

---

## 5. Audit of Epistemic Phonology & Shannon Unicity Bounds (Chapter 4)

**Keftiu / BM EA 10059 — genuine source, tautological use.** The London Medical Papyrus does contain a Keftiu-language spell, and BM EA 5647 does preserve Aegean names; citing them is fair. But:

- The "**100.0% open-syllable rate**" is **hard-coded**, not measured:

```120:121:src/phaistos/linguistics/keftiu_corpus.py
        open_syllable_rate_pct=100.0,  # Strictly open CV / V structure
```

- More importantly, the 100% figure is an **artifact of Egyptian group-writing**, which cannot notate closed syllables — a fact the manuscript itself concedes ("filtered through … Egyptian New Kingdom syllabic group-writing") and then ignores when calling it "independent external evidence." Both Linear A and Linear B also systematically under-write final consonants; open-CV appearance is a property of these **scripts**, not proof of Minoan **phonology**. "14 words / 83 syllables" is unverifiable invented precision atop a corpus of a few contested lines.

**Bayesian Language-Family Discriminator — not Bayesian; outputs pre-ordained.** The fit percentages (94.5 / 68 / 52 / 31) and the p-values (0.0001 / 0.024 / 0.085 / 0.45) are **literal constants written into the dataclasses**; only the LLR is derived, and it is merely the `02-12` prefix z-score times arbitrary hand-chosen multipliers (1.5, 0.45, 0.20, −0.30):

```106:116:src/phaistos/linguistics/language_discriminator.py
            syllable_structure_fit_pct=94.5,
            prefix_suffix_topology_score=92.0,
            reduplication_concordance_pct=88.0,
            log_likelihood_ratio_vs_null=round(z_pref * 1.5, 2),
            p_value=0.0001,
            epistemic_status="HIGHEST_STATISTICAL_CONCORDANCE",
```

There is no likelihood model over Linear A, Luwian, Greek, or Egyptian corpora; therefore the "exclusion of Greek/Egyptian" and "support for an Aegean isolate" are **assertions with numeric costumes**, not results. (The prefix-enrichment permutation test is the one real computation, and it speaks only to internal structure, not to language family.)

**Shannon unicity "proof" — misattributed and non-binding.** We re-ran the sieve. Two decisive problems:

1. **It is not Shannon's unicity distance.** Shannon's $U = H(K)/D$ concerns key entropy vs. language redundancy for *unique key recovery*. The module instead computes a hypothesis "degrees-of-freedom" bit-count and divides by a token count times an **assumed** redundancy. Note that it computes the *empirical* entropy of the Disc ($H \approx 4.98$ bits/symbol) and then **discards it**, substituting an arbitrary $R_L = 0.70$:

```71:74:src/phaistos/stats/unicity_sieve.py
    # For natural language written in a syllabary, language redundancy R_L is typically ~0.70
    # The effective information distance D_L = R_L * log2(|A|) ~ 0.70 * 5.49 ~ 3.84 bits/symbol
    d_l = 0.70 * max_h
    total_capacity = total_tokens * d_l  # ~929.3 bits
```

2. **The "proof" is a pure function of freely chosen knobs.** Capacity $= 242 \times 3.844 = 930.3$ bits. PIE DoF $= 45\log_2 60 + 61\log_2 3000 = 970.4$, giving ratio 1.043 — *barely* over the arbitrary 1.0 threshold. This is entirely driven by the analyst's choices of "60 candidate syllables," "3000 roots," and "translate 61 words." Set the lexicon to 2,600 roots and the "Epistemic Law" flips to "constrained." A theorem cannot pivot on a hand-picked dictionary size. The verdict thresholds (0.20, 1.0) are likewise arbitrary.

(As a minor consistency note, the code docstring and `AGENTS.md` say "241 signs / ~929.3 bits," while the live corpus and the reported 930.3 bits use 242. 242 sign-tokens is the correct, standard figure; the 241/929.3 relics should be purged.)

The *intuition* — that a full lexical translation adds more free parameters than the text can constrain — is sound and worth stating qualitatively as a **parsimony/overfitting caution**. But it is **not** a mathematical proof, it is **not** Shannon's unicity distance, and it should not be branded an "Epistemic Law." The header's "$U \approx 106$ symbols" is also underived.

---

## 6. Audit of Liturgical Libretto & Bronze Age Homology (Chapter 5)

The 14-clause parse is the manuscript's most speculative section and contradicts its own abstract. Clause boundaries drawn on strokes/headers are defensible as *segmentation*; the **glosses** ("Epiphany of the Goddess in her chariot," "blood aspersion," "honey offering," "cosmic cycle") are unconstrained narrative superimposed on unread signs. This is decipherment by another name.

The comparative concordances are **not empirically derived** in any module we located and bear the same signature as Chapter 4's constants:

- "Linear A Libation Formula 91.3%," "Hurrian Hymn H6 95.0%," "Arkalochori Votive Axe 92.0%," "$Z=+9.58\sigma$" — all presented without a reproducible alignment procedure.
- Cross-culturally, **Hurrian Hymn H6** (a Ugaritic Hurrian musical-notation text) shares nothing structurally comparable with a Minoan stamped disc; a "95% cadence concordance" is not a meaningful quantity. The Arkalochori Axe and the Linear A libation formula (`a-ta-i-*301-wa-ja …`) are at least Aegean and relevant, but a percentage concordance with an unread text is undefined.

Recommend deleting the numeric concordances entirely or replacing them with an explicit, reproducible alignment algorithm and surrogate control.

---

## 7. Skeptic Counter-Critique & Methodological Vulnerabilities

Acting as adversarial Skeptic (per `AGENTS.md`), the core vulnerabilities are:

1. **Confirmation-selected inputs.** Sign glosses are chosen to match the sarcophagus, then the sarcophagus match is tested as if independent (§2, §4). Break this loop: fix sign identifications *before* any homology test, from an external catalogue, blind to the hypothesis.
2. **Rigged / non-exchangeable nulls.** The homology test compares a curated set against a random draw. A valid design would apply the *same* automated motif-matching rule to both the Disc and to many random Aegean objects of equal size.
3. **Hard-coded "results."** Language fits, p-values, open-syllable rate, Bayes factor, and comparative concordances are constants, not computations. Every headline number outside the raw corpus counts must be regenerated from data or removed.
4. **Misused information theory.** The Shannon claim is a parsimony heuristic mislabeled as a theorem and tuned via free parameters.
5. **Internal inconsistency.** Three different homology $Z$-values; 241 vs 242 tokens; "18" vs "19" homology signs — in a document advertising dual-node test parity.
6. **Unfalsifiable narrative.** "Liturgical conservatism" can absorb any iconographic overlap or non-overlap.

**What would actually confirm or falsify the reconstruction:**
- A **bilingual** (Disc-script + Linear A/B or Egyptian) or a second stamped object using the *same punches* — the only thing that could anchor sign values.
- New **Linear A** material establishing the phonotactics the paper currently borrows tautologically from Egyptian orthography.
- **Non-destructive analytical imaging** (RTI, µ-CT, XRF/pXRF, NAA on comparanda) to test the single-die and Messara-provenance claims with real metrics.
- A **pre-registered, blind** motif-matching protocol with a genuinely exchangeable null to re-test the sarcophagus homology.

---

## 8. Formal Committee Verdict & Scholarly Recommendation

### Recommendation: **MAJOR REVISIONS REQUIRED** (currently leaning toward reject on the inferential chapters as written).

The descriptive spine — 242 tokens / 61 groups / 45 signs, the `02-12` prefix enrichment, and above all the A16/A19/A22 Lyric Triad — is correct, reproducible, and publishable. Around it, the manuscript has draped a layer of statistics that our audit shows to be **hard-coded, circular, misattributed to Shannon, and internally inconsistent** (three conflicting values for its own flagship $Z$). The paper cannot be accepted until:

1. Every non-corpus number is **regenerated from data or deleted** (language fits, p-values, Keftiu 100%, Bayes factor $K=14.2$, comparative concordances, the $Z$ statistics).
2. The homology test is **rebuilt with an exchangeable null** and blind, externally-sourced sign identifications.
3. The "Shannon unicity" section is **relabeled** an overfitting/parsimony heuristic, with all thresholds and knob-values justified or removed; the false "Epistemic Law" and "$U\approx106$" claims struck.
4. Chapter 5's semantic glosses are **removed or explicitly demarcated** as unfalsifiable conjecture, resolving the contradiction with the abstract's anti-decipherment stance.
5. The Evans-numbering error, the 241/242 and 18/19 inconsistencies, and the fabricated typometric/petrographic precision are corrected.

### Permanent contributions (what should survive revision)

- A **clean, reproducible computational corpus** of the Disc with an automated segmentation and repetition pipeline — genuinely useful infrastructure.
- A crisp, quantitative restatement of the **Lyric Triad** and `02-12` prefix as bona fide non-random internal structure, properly surrogate-tested.
- A valuable **methodological stance** — separating physical observation from linguistic inference and demanding null controls — which, *if actually enforced on its own outputs*, is the correct future direction for Aegean computational epigraphy.

The ambition is welcome and the framing instinct is right. But a manuscript invoking the Skeptic Rule must first survive it. At present the strongest falsification of the monograph comes from re-running the monograph's own code.

*Respectfully submitted by the Tier-2 Committee (Paleography · Information Theory · Aegean Linguistics).*

---

Note: I re-executed `evaluate_homology_significance` and `evaluate_model_unicity` from the repo (venv) and recomputed the arithmetic to substantiate the discrepancies above; I did not modify any laboratory files.