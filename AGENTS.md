# Agent Guidelines & Epistemic Protocol

When operating within the Phaistos Disc Lab, agents must uphold strict scientific integrity and avoid statistical self-deception.

## 1. The Skeptic Rule
Before any hypothesis is considered supported:
* It **must** be evaluated against a randomized control corpus (fully shuffled, frequency-preserving, and Markov-preserving).
* It **must** be evaluated against the unicity distance limit. If the model degrees of freedom exceed the information content of 241 signs, report the result as unconstrained / overfit.
* The agent acting as **Skeptic** must attempt to falsify the result.

## 2. Immutability of Evidence
* Raw data (`corpus/`, `data/raw/`) is immutable.
* Never rewrite or invent scholarly citations.
* Distinguish clearly between **OBSERVATION** (physical clay marks, stamp overlaps) and **TRANSCRIPTION** (Evans sign numbers).
* Document erasures/palimpsests (A05, A08, B01) and incised stylus strokes separately from stamped glyphs.

## 3. Remote Execution on Fedora Worker
* Never attempt heavy Docker/Kubernetes setups.
* Use `scripts/remote_worker.sh` to run batch CPU jobs on the Fedora machine.
* Respect memory limits (16 GB total class, keep single-process footprint < 8 GB).
