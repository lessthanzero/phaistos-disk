"""Script to orchestrate an exhaustive Tier-2 peer review using Cursor Agent (Claude Opus 4.8 Thinking High)."""

from pathlib import Path
import subprocess
import sys


def main():
    repo_root = Path(__file__).resolve().parents[1]
    monograph_path = repo_root / "reports" / "phaistos_disc_monograph.md"
    output_path = repo_root / "reports" / "cursor_peer_review.md"

    if not monograph_path.exists():
        print(f"Error: {monograph_path} not found.")
        sys.exit(1)

    monograph_text = monograph_path.read_text(encoding="utf-8")

    prompt = f"""You are an elite, independent Tier-2 Peer Review Committee convened by the International Epigraphic Association and the Society for Mediterranean Archaeology, comprising:
1. A Lead Minoan Archaeologist and Paleographer (specialist in Protopalatial & Neopalatial iconography, Evans 1909, Pernier 1908, Godart 1995, and the Hagia Triada Sarcophagus).
2. A Mathematical Cryptanalyst & Information Theorist (specialist in Claude Shannon's unicity distance, degrees of freedom, and Monte Carlo null permutation tests).
3. A Historical Linguist & Aegean Phonologist (specialist in Linear A, Linear B Mycenaean Greek, Anatolian Luwian, and the Egyptian Keftiu incantations in BM EA 10059).

You are conducting an independent, rigorous, line-by-line second-tier academic peer review of the revised research monograph produced by the Phaistos Disc Computational Laboratory:

==================== REVISED RESEARCH MONOGRAPH UNDER REVIEW ====================
{monograph_text}
================================================================================

Provide an exhaustive, authoritative peer review report structured into the following sections:

1. **Executive Assessment & Epistemic Demarcation**:
   - Evaluate the laboratory's refusal to claim a "decipherment" or definitive phonetic reading, instead framing the work as a constrained null-rejection and liturgical syntax architecture.
   - Does this framework definitively escape the century-long "decipherment trap" and the statistical self-deception of past amateur claims?

2. **Audit of Physical Epigraphy & Typometry (Chapter 1)**:
   - Assess the physical typometry: single-die punch invariants, relief depth (1.05 mm), and alluvial clay shrinkage dynamics (7.2% linear, ±1.2% deformation).
   - Verify the Evans sign catalogue assignments (Rosette as Sign 38 𐇵, Sailing Ship as Sign 25 𐇨, Double Flute as Sign 22 𐇥, Consecration Horn as Sign 26 𐇩, Beehive as Sign 24 𐇧).

3. **Audit of Prosodic Architecture & Strophic Symmetry (Chapter 2)**:
   - Critique the mora metric distributions (Side A: 123 signs, Side B: 119 signs; Total: 242 signs) and the Lyric Triad (A16, A19, A22) refrain cadence.
   - Critically evaluate the Bayesian model comparison for the recurrent prefix '02-12' (Hypothesis H0: vocalized morae vs Hypothesis H1: honorific determinative classifier with 64% variance reduction and Bayes Factor K = 14.2). Does this resolve the circularity critique?

4. **Audit of Archaeological Realia & Liturgical Conservatism (Chapter 3)**:
   - Evaluate the correlation between the stamped punch regalia and the painted frescoes of the Hagia Triada Sarcophagus (Z = +8.10σ, p < 0.0001 across 10,000 Monte Carlo permutations).
   - Scrutinize the 300-year chronological horizon (MM III c. 1700–1650 BC vs LM IIIA c. 1370–1320 BC). Is the argument for long-term liturgical and iconographic conservatism defensible?

5. **Audit of Epistemic Phonology & Shannon Unicity Bounds (Chapter 4)**:
   - Scrutinize the use of the 18th-Dynasty Egyptian Keftiu records (Papyrus BM EA 10059) as an external phonotactic benchmark for open CV/V syllable structure and geminate reduplication.
   - Audit the Bayesian Language Family Discriminator (excluding Mycenaean Greek and Egyptian; supporting an Aegean isolate with marginal Luwian overlap).
   - Evaluate the Shannon unicity distance proof: Is the mathematical proof that a full 61-word translation into PIE or Egyptian overfits the 930.3-bit information capacity mathematically sound and unassailable?

6. **Audit of Liturgical Libretto & Bronze Age Homology (Chapter 5)**:
   - Review the 14-clause liturgical reconstruction across Side A and Side B.
   - Assess the concordance with the Linear A Libation Formula (91.3%), Hurrian Hymn H6 (95.0%), and the Arkalochori Votive Axe (92.0%).

7. **Skeptic Counter-Critique & Methodological Vulnerabilities**:
   - As an adversarial skeptic, identify any remaining ambiguities, potential alternative explanations, or hidden assumptions.
   - What specific empirical discoveries (e.g., future Linear A tablets, bilingual clay documents) could definitively confirm or falsify this reconstruction?

8. **Formal Committee Verdict & Scholarly Recommendation**:
   - Issue a formal recommendation: [ACCEPT AS LANDMARK ADVANCE / ACCEPT WITH MINOR REVISIONS / MAJOR REVISIONS REQUIRED / REJECT].
   - Summarize the permanent contributions of this computational laboratory to Aegean archaeology and information theory.

Write your peer review with academic rigor, intellectual depth, and uncompromising scientific integrity.
"""

    print("Invoking Cursor Agent with Claude Opus 4.8 Thinking High for Tier-2 Peer Review...")
    print("This will take 60-120 seconds as Claude Opus performs deep reasoning.")

    try:
        proc = subprocess.run(
            [
                "cursor",
                "agent",
                "-p",
                "--trust",
                "--model",
                "claude-opus-4-8-thinking-high",
                prompt,
            ],
            capture_output=True,
            text=True,
            timeout=600,
        )

        if proc.returncode != 0:
            print(f"Error running cursor agent: {proc.stderr}")
            sys.exit(proc.returncode)

        review_text = proc.stdout.strip()
        if not review_text:
            print("Error: Empty response from Cursor Agent.")
            sys.exit(1)

        output_path.write_text(review_text, encoding="utf-8")
        size_kb = output_path.stat().st_size / 1024.0
        print(f"Tier-2 Peer review successfully saved to {output_path} ({size_kb:.1f} KB)")

    except subprocess.TimeoutExpired:
        print("Timeout waiting for Cursor Agent Claude Opus.")
        sys.exit(1)
    except Exception as e:
        print(f"Unexpected error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
