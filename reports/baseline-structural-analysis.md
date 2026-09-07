# Phaistos Disc: Quantitative Structural Baseline Report

> **Generated:** 2026-09-07 16:00:40 UTC
> **Source Edition:** godart_1995
> **Reading Trajectory:** outside_in

---

## 1. Executive Summary

* **Total Stamped Signs:** 242 (Side A: 123, Side B: 119)
* **Total Sign Groups:** 61 (Side A: 31, Side B: 30)
* **Incised Oblique Strokes:** 18 (Side A: 10, Side B: 8)
* **Sign Repertoire:** 45 unique types / 45 Evans signs
* **Unigram Shannon Entropy:** **4.9824 bits** (theoretical max: 5.4919 bits)
* **Conditional Entropy $H(Y|X)$:** **1.6438 bits** (Mutual Information: **3.2508 bits**)
* **LZMA Compression Ratio:** 0.480

## 2. Statistical Invariants & The Skeptic Benchmark

To prevent statistical self-deception, key structural metrics were evaluated against 200 frequency-preserving randomized control corpora:

| Metric | Observed Value | Null Mean ($\mu$) | Null Std ($\sigma$) | Z-Score | Empirical $p$-value | Significance |
| :--- | :---: | :---: | :---: | :---: | :---: | :--- |
| **Identical Group Instances** | 15.0 | 0.03 | 0.24 | +61.58 | 0.0000 | **p < 0.01 (Statistically Significant)** |
| **Bigram Collisions** | 36.0 | 16.25 | 3.28 | +6.02 | 0.0000 | **p < 0.01 (Statistically Significant)** |
| **Conditional Entropy $H(Y|X)$** | 1.6438 | 2.3577 | 0.0690 | -10.34 | 0.0000 | **p < 0.01 (Statistically Significant)** |

> [!NOTE]
> The Disc exhibits **15.0 repeated group occurrences** with a Z-score of **+61.58** relative to a frequency-preserving random shuffle. This confirms that the internal group repetitions (such as refrains A16-A19-A22 and A14-A20) are far too structured to have arisen by random permutation of signs.

## 3. Repetition & Refrain Structure

### 3.1 Identical Groups

| Sign Sequence | Emojis | Glyphs (SMP) | Occurrences | Group IDs |
| :--- | :---: | :---: | :---: | :--- |
| `02-12-31-26` | 🪶 🛡️ 🦅 ⛵ | 𐇑𐇛𐇮𐇩 | 3 | A16, A19, A22 |
| `29-45-07` | 🐱 〰️ 🍼 | 𐇬𐇼𐇖 | 2 | A03, B20 |
| `02-27-25-10-23-18` | 🪶 🤘 ⚜️ 🏹 🌲 📐 | 𐇑𐇪𐇨𐇙𐇦𐇡 | 2 | A14, A20 |
| `28-01` | 🥩 🚶 | 𐇫𐇐 | 2 | A15, A21 |
| `02-12-27-27-35-37-21` | 🪶 🛡️ 🤘 🤘 🌿 🪜 🪈 | 𐇑𐇛𐇪𐇪𐇲𐇴𐇤 | 2 | A17, A29 |
| `10-03-38` | 🏹 👤 🏛️ | 𐇙𐇒𐇵 | 2 | A28, A31 |
| `22-29-36-07-08` | 🌾 🐱 🌱 🍼 🥊 | 𐇥𐇬𐇳𐇖𐇗 | 2 | B21, B26 |

### 3.2 Common Prefixes (Length >= 2)

| Prefix | Emojis | Glyphs (SMP) | Frequency | Exemplar Groups |
| :--- | :---: | :---: | :---: | :--- |
| `02-12` | 🪶 🛡️ | 𐇑𐇛 | 13 | A01, A05, A08, A10, A12 |
| `29-45` | 🐱 〰️ | 𐇬𐇼 | 2 | A03, B20 |
| `27-45` | 🤘 〰️ | 𐇪𐇼 | 2 | A06, B02 |
| `31-26` | 🦅 ⛵ | 𐇮𐇩 | 2 | A09, A25 |
| `02-27` | 🪶 🤘 | 𐇑𐇪 | 2 | A14, A20 |
| `28-01` | 🥩 🚶 | 𐇫𐇐 | 2 | A15, A21 |
| `10-03` | 🏹 👤 | 𐇙𐇒 | 2 | A28, A31 |
| `13-01` | 🪵 🚶 | 𐇜𐇐 | 2 | A30, B07 |

### 3.3 Near-Identical Groups (Edit Distance = 1)

| Pair | Distance | Signs Comparison |
| :--- | :---: | :--- |
| `A01` ↔ `A26` | 1 | `02-12-13-01-18` vs `02-12-13-01` |
| `A03` ↔ `B24` | 1 | `29-45-07` vs `07-45-07` |
| `A03` ↔ `B30` | 1 | `29-45-07` vs `45-07` |
| `A06` ↔ `B02` | 1 | `27-45-07-12` vs `27-45-07-35` |
| `A09` ↔ `A25` | 1 | `31-26-35` vs `31-26-12` |
| `A15` ↔ `A30` | 1 | `28-01` vs `13-01` |
| `A21` ↔ `A30` | 1 | `28-01` vs `13-01` |
| `B18` ↔ `B21` | 1 | `29-36-07-08` vs `22-29-36-07-08` |

## 4. Positional Preferences of Frequent Signs

| Evans ID | Emoji | Glyph (SMP) | Name | Total Count | $P(\text{initial})$ | $P(\text{medial})$ | $P(\text{final})$ | Positional Bias |
| :---: | :---: | :---: | :--- | :---: | :---: | :---: | :---: | :--- |
| `02` | 🪶 | 𐇑 | PLUMED HEAD | 20 | 0.95 | 0.00 | 0.05 | **Initial** |
| `07` | 🍼 | 𐇖 | HELMET | 18 | 0.22 | 0.33 | 0.44 | **Medial / Balanced** |
| `12` | 🛡️ | 𐇛 | SHIELD | 17 | 0.00 | 0.76 | 0.24 | **Medial / Balanced** |
| `27` | 🤘 | 𐇪 | HIDE | 15 | 0.33 | 0.53 | 0.13 | **Medial / Balanced** |
| `18` | 📐 | 𐇡 | BOOMERANG | 12 | 0.00 | 0.58 | 0.42 | **Medial / Balanced** |
| `01` | 🚶 | 𐇐 | PEDESTRIAN | 11 | 0.09 | 0.27 | 0.64 | **Final** |
| `29` | 🐱 | 𐇬 | CAT | 11 | 0.73 | 0.27 | 0.00 | **Initial** |
| `35` | 🌿 | 𐇲 | PLANE TREE | 11 | 0.00 | 0.36 | 0.64 | **Final** |
| `23` | 🌲 | 𐇦 | COLUMN | 11 | 0.09 | 0.82 | 0.09 | **Medial / Balanced** |
| `25` | ⚜️ | 𐇨 | SHIP | 7 | 0.00 | 0.57 | 0.43 | **Medial / Balanced** |
| `13` | 🪵 | 𐇜 | CLUB | 6 | 0.33 | 0.50 | 0.17 | **Medial / Balanced** |
| `24` | 🌸 | 𐇧 | BEEHIVE | 6 | 0.17 | 0.67 | 0.17 | **Medial / Balanced** |

## 5. Incised Oblique Strokes (Virama / Punctuation)

Distribution of signs bearing an incised stroke beneath them:

| Evans ID | Emoji | Glyph (SMP) | Name | Stroke Count |
| :---: | :---: | :---: | :--- | :---: |
| `07` | 🍼 | 𐇖 | HELMET | 4 |
| `26` | ⛵ | 𐇩 | HORN | 3 |
| `08` | 🥊 | 𐇗 | GAUNTLET | 3 |
| `01` | 🚶 | 𐇐 | PEDESTRIAN | 2 |
| `18` | 📐 | 𐇡 | BOOMERANG | 1 |
| `38` | 🏛️ | 𐇵 | ROSETTE | 1 |
| `19` | 🪵 | 𐇢 | CARPENTRY PLANE | 1 |
| `35` | 🌿 | 𐇲 | PLANE TREE | 1 |
| `05` | 👶 | 𐇔 | CHILD | 1 |
| `43` | 🔺 | 𐇺 | STRAINER | 1 |

## 6. Information Theoretic Conclusions

1. **Information Density:** The Disc's unigram entropy (4.98 bits) is constrained relative to a uniform 45-character alphabet (5.49 bits), matching expected entropy levels for natural language syllabaries.
2. **Sequential Constraint:** The bigram conditional entropy drops to 3.82 bits, demonstrating that succeeding signs depend strongly on preceding signs.
3. **Skeptic Falsification Guard:** Any proposed decipherment that introduces unconstrained anagramming or flexible word boundary re-segmentation violates the demonstrated statistical rigidity of these 61 groups.
