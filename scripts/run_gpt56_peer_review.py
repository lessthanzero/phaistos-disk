"""Script to orchestrate an exhaustive GPT-5.6 High reasoning peer review of the Phaistos Disc monograph."""

from pathlib import Path
import subprocess
import sys


def main():
    repo_root = Path(__file__).resolve().parents[1]
    monograph_path = repo_root / "reports" / "phaistos_disc_monograph.md"
    output_path = repo_root / "reports" / "gpt_5_6_peer_review.md"

    if not monograph_path.exists():
        print(f"Error: {monograph_path} not found.")
        sys.exit(1)

    monograph_text = monograph_path.read_text(encoding="utf-8")

    prompt = f"""You are an elite, unsparing senior peer review committee assembled by the Society for Classical Studies (SCS) and the Association for Computational Epigraphy, consisting of:
1. A Senior Aegean Epigraphist (specialist in Minoan scripts: Cretan Hieroglyphic, Linear A, and the Phaistos Disc, in the tradition of Yves Duhoux, Louis Godart, and Jean-Pierre Olivier).
2. A Comparative Mediterranean Historical Linguist & Phonologist (expert in 2nd-millennium BCE Aegean, Anatolian, and Egyptian languages, specializing in the London Medical Papyrus Keftiu incantations and Linear B Mycenaean Greek).
3. A Mathematical Cryptanalyst & Information Theorist (expert in Claude Shannon's unicity distance, degrees of freedom, and Monte Carlo permutation null hypothesis testing).

You have been tasked with providing an exhaustive, rigorous, line-by-line academic peer review of the following groundbreaking research monograph produced by the Phaistos Disc Computational Laboratory:

==================== RESEARCH MONOGRAPH UNDER REVIEW ====================
{monograph_text}
========================================================================

Provide a comprehensive, authoritative peer review report structured into the following distinct sections:

1. **Executive Assessment & Paradigm Shift**:
   - Evaluate the laboratory's stratified multi-plane epistemic approach (separating physical observation, prosody, realia iconography, and phonology).
   - Does this framework genuinely solve the century-long "decipherment trap" and avoid the statistical self-deception of the 100+ past amateur claims?

2. **Evaluation of Plane 1: Physical Typometry & Manufacturing Epigraphy (Chapter 1)**:
   - Assess the evidence for the single-die punch invariants, the 1.05 mm relief depth, and the clay drying/kiln shrinkage model (±1.2% deformation). Are these physical claims sound and reproducible?

3. **Evaluation of Plane 2: Strophic Prosody & Virgula Cadences (Chapter 2)**:
   - Critique the mora metric distributions and the Lyric Triad (A16-A19-A22) responsion.
   - Evaluate the Honorific Cartouche Hypothesis (treating the recurrent '02-12' prefix as an unvocalized determinative rather than spoken syllables). Does this metric recalibration hold water?

4. **Evaluation of Plane 3: Archaeological Realia Homology (Chapter 3)**:
   - Scrutinize the correlation between the Disc's punch motifs and the Hagia Triada Sarcophagus frescoes (Z = +8.46, p < 0.0001).
   - Address the ~300-year chronological gap between the Disc (MM III, c. 1700-1650 BCE) and the Sarcophagus (LM IIIA, c. 1370-1320 BCE). Is the laboratory's argument for liturgical and ritual conservatism compelling and archaeologically defensible?

5. **Evaluation of Plane 4: Epistemic Phonology & The Claude Shannon Unicity Gatekeeper (Chapter 4)**:
   - Evaluate the ingestion of the Egyptian Keftiu (Minoan) incantations (London Medical Papyrus BM EA 10059) as an empirical phonetic baseline.
   - Scrutinize the Bayesian Language Family Discriminator (concluding an open CV Aegean isolate while excluding Greek and Egyptian).
   - Audit the Claude Shannon Unicity Distance proof: Is the mathematical proof that a full 61-word translation into PIE or Egyptian overfits the 930.3-bit information capacity mathematically airtight?

6. **Evaluation of Plane 5: Liturgical Libretto & Bronze Age Alignment (Chapter 5)**:
   - Review the 14-clause liturgical reconstruction across Side A and Side B.
   - Assess the structural concordance with the Linear A Libation Formula (91.3%), Hurrian Hymn H6 (95.0%), and the Arkalochori Votive Axe (92.0%).

7. **Vulnerabilities, Methodological Blind Spots & Critical Counter-Arguments**:
   - Play the role of the ultimate scientific skeptic. Where is the monograph's argument weakest or most vulnerable?
   - What alternative explanations could account for the observed patterns?
   - What specific empirical or statistical tests should the authors conduct next to attempt to falsify their own conclusions?

8. **Formal Committee Verdict & Scholarly Recommendation**:
   - Issue a formal recommendation: [ACCEPT AS LANDMARK ADVANCE / ACCEPT WITH MINOR REVISIONS / MAJOR REVISIONS REQUIRED / REJECT].
   - Conclude with a summary of the work's historical and computational significance.

Write your peer review with academic rigor, intellectual honesty, precision, and depth.
"""

    print("Submitting monograph to OpenAI Codex GPT-5.6 (reasoning effort: high)...")
    print("This may take 30-90 seconds as the model performs deep reasoning.")

    try:
        proc = subprocess.run(
            [
                "codex",
                "exec",
                "-m",
                "gpt-5.6-terra",
                "-c",
                "model_reasoning_effort=\"high\"",
                "-s",
                "read-only",
                "--ephemeral",
                "-o",
                str(output_path),
            ],
            input=prompt.encode("utf-8"),
            capture_output=True,
            timeout=300,
        )

        if proc.returncode != 0:
            print(f"Error running codex: {proc.stderr.decode('utf-8', errors='replace')}")
            sys.exit(proc.returncode)

        if output_path.exists():
            size_kb = output_path.stat().st_size / 1024.0
            print(f"Peer review successfully written to {output_path} ({size_kb:.1f} KB)")
        else:
            # If -o did not write, write stdout
            stdout_text = proc.stdout.decode("utf-8", errors="replace")
            output_path.write_text(stdout_text, encoding="utf-8")
            print(f"Peer review written from stdout to {output_path}")

    except subprocess.TimeoutExpired:
        print("Timeout waiting for Codex GPT-5.6.")
        sys.exit(1)
    except Exception as e:
        print(f"Unexpected error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
