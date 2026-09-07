# Phaistos Disc Lab

A local-first computational research laboratory for structural, cryptographic, statistical, and comparative analysis of the **Phaistos Disc**.

## Mission & Principles

This is an experimental research project, not a machine translation engine.

We do **not** assume:
* the Disc is linguistic;
* the 61 groups are words;
* the reading direction is certain;
* the signs are syllabic;
* Linear A provides the correct key;
* any published decipherment is correct;
* a meaningful-looking translation is evidence of success.

The primary objective is discovering reproducible structural, computational, or comparative evidence about the Disc, including mathematically rigorous refutations of proposed decipherments.

### Core Epistemological Principle: Strict Evidence Separation
Every assertion belongs to exactly one category:
1. **OBSERVATION**: Physical traits (e.g. punch overlap, margin crowding, erasures/palimpsests).
2. **TRANSCRIPTION**: Symbolic representation according to an epigrapher (e.g. Evans sign 02).
3. **SCHOLARLY CLAIM**: Attested proposal in published literature.
4. **HYPOTHESIS**: Testable model (e.g. syllabic structure, Luwian language, game board rules).
5. **MODEL INFERENCE**: Computed score or statistical likelihood.

No category is ever silently promoted into another.

---

## Hardware Architecture

* **MacBook Pro (M1 Pro / 32 GB RAM)**:
  * Primary workstation for development, exploratory analysis, CLI commands, and local LLM evaluation via Ollama (`gemma3:12b`, `qwen2.5-coder:7b`).
* **Fedora PC (Bosgame E5 / 16 GB RAM / 332 GB storage)**:
  * Headless worker over SSH (`pc` / `pc-remote`) for long-running Monte Carlo simulations, permutation testing, and batch verification.

---

## Quick Start

Ensure `uv` is installed, then:

```bash
# Install dependencies into local venv
uv sync

# Run integrity validation suite
uv run pytest

# Run CLI commands
uv run phaistos validate
uv run phaistos stats
uv run phaistos signs
```
