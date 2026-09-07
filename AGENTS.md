# Agent Guidelines & Epistemic Protocol

When operating within the Phaistos Disc Lab, agents must uphold strict scientific integrity and avoid statistical self-deception.

## 1. The Skeptic Rule
Before any hypothesis is considered supported:
* It **must** be evaluated against a randomized control corpus (fully shuffled, frequency-preserving, and Markov-preserving).
* It **must** be evaluated against the unicity distance limit. If the model degrees of freedom exceed the information content of 242 signs (930.3 bits), report the result as unconstrained / overfit.
* The agent acting as **Skeptic** must attempt to falsify the result.

## 2. Immutability of Evidence
* Raw data (`corpus/`, `data/raw/`) is immutable.
* Never rewrite or invent scholarly citations.
* Distinguish clearly between **OBSERVATION** (physical clay marks, stamp overlaps) and **TRANSCRIPTION** (Evans sign numbers).
* Document erasures/palimpsests (A05, A08, B01) and incised stylus strokes separately from stamped glyphs.

## 3. Remote Execution on Fedora Worker
* Never attempt heavy Docker/Kubernetes setups.
* Use `scripts/remote_worker.sh` to run batch CPU jobs on the Fedora machine (`pc`).
* Respect memory limits (16 GB total class, keep single-process footprint < 8 GB).
* Use `scripts/sync_artifacts.sh pc push` to mirror local code and data to the worker, and `scripts/sync_artifacts.sh pc pull` to retrieve experiment outputs.

## 4. Autonomous Distributed Compute & Model Protocol (All Nodes & Models)
* **Permanent Mandate**: The user should never have to repeat the instruction to use all available compute across all nodes. Whenever tasks require intensive computation, statistical surrogate testing, MCMC sampling, or verification:
  1. **Dual-Node Execution**: Automatically orchestrate jobs across both local Apple Silicon macOS and the remote Fedora Linux worker (`pc`).
  2. **Automated Sync**: Synchronize code before remote runs (`./scripts/sync_artifacts.sh pc push`) and pull back artifacts upon completion (`./scripts/sync_artifacts.sh pc pull`).
  3. **Local & Cloud Models**: Leverage local models running on Fedora via Ollama (`pc:11434` / `192.168.1.172:11434`) alongside frontier cloud models for synthesis, falsification, and verification.
  4. **Cross-Platform Test Invariant**: All test suites must pass on both local macOS (Python 3.12) and Fedora Linux (Python 3.13/3.14) environments before considering a milestone complete.

