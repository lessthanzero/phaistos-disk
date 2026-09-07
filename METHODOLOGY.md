# Methodological & Epistemic Specification

This document details the mathematical, computational, and physical methodologies utilized in the **Phaistos Disc Lab**. All algorithms enforce the **Skeptic Rule** to eliminate confirmation bias and prevent statistical self-deception.

---

## 1. The Evidence Separation Hierarchy

To maintain scientific integrity, all analytical data in the repository is strictly partitioned into four ontological strata:

```
[L0: PHYSICAL OBSERVATION]
    └── Clay marks, stamp relief overlaps, thumb palimpsests, incised burrs, sintered mineral fabric.
        │
        ▼
[L1: TRANSCRIPTION]
    └── Group boundary divisions, Evans sign numbers (01-45), stroke presence.
        │
        ▼
[L2: FORMAL PALEOGRAPHIC RESEMBLANCE]
    └── Iconographic analogies to Cretan Hieroglyphs or Linear A/B sign shapes (non-phonetic).
        │
        ▼
[L3: PHONETIC PROJECTION & HYPOTHESIS]
    └── Assigned sound values, target language vocabulary, metrical readings, or calendar models.
```

**Rule of Non-Promotability**: An inference at layer $L_{k}$ can never be treated as an immutable observation at layer $L_{<k}$. Any decipherment hypothesis that requires altering $L_0$ or $L_1$ evidence without physical epigraphic proof is rejected.

---

## 2. Information-Theoretic Bounds & The Unicity Guard

Claude Shannon demonstrated in *Communication Theory of Secrecy Systems* (1949) that any ciphertext shorter than the **unicity distance ($U$)** cannot be uniquely deciphered because multiple spurious keys produce equally plausible plaintexts.

### Mathematical Formulation
$$U = \frac{H(K)}{D} = \frac{H(K)}{R_{max} - R}$$

Where:
* $H(K)$ is the entropy of the cipher key space (the sign-to-sound assignment matrix).
* $D$ is the redundancy of the underlying language.
* $R_{max} = \log_2(|\Sigma|)$ is the absolute maximum entropy per character for alphabet/syllabary $\Sigma$.
* $R$ is the actual unigram/bigram entropy of the language.

### Application to the Phaistos Disc
For a 45-sign syllabary mapped to candidate phonetic values:
* Key space size: $45! \approx 1.196 \times 10^{56}$.
* Key entropy: $H(K) = \log_2(45!) \approx 265.8\text{ bits}$.
* For archaic Aegean scripts (Linear A / Linear B), language redundancy $D \approx 2.5\text{ bits/character}$.
* **Unicity Distance**:
  $$U \approx \frac{265.8}{2.5} \approx \mathbf{106\text{ characters}}$$

**The Combinatorial Trap**:
The Phaistos Disc contains 242 signs. While $242 > 106$, the unicity bound holds **only when the target language and vocabulary are known in advance**. If the decipherer permits free parameters (unknown dialect, arbitrary vocabulary cribs, flexible vocalic values), the effective key entropy $H(K)$ explodes to $> 1,000\text{ bits}$, raising $U > 400\text{ characters}$.

**Laboratory Policy**: Any unconstrained decipherment model that introduces more free parameters than the informational entropy of the 242 signs is reported as **OVERFIT / MATHEMATICALLY UNCONSTRAINED**.

---

## 3. Monte Carlo Null Hypothesis Controls

Before any observed structural pattern is considered supported, it must be tested against three tiers of randomized synthetic corpora:

```mermaid
graph TD
    Obs["Observed Metric (T_obs)"]
    
    subgraph Controls [Monte Carlo Null Baselines (N = 1,000 to 100,000)]
        C1["Level 1: Fully Shuffled Surrogates<br/>(Destroys frequency & syntax)"]
        C2["Level 2: Frequency-Preserving Anagrams<br/>(Preserves unigram sign frequencies)"]
        C3["Level 3: Markov-Preserving Surrogates<br/>(Preserves bigram transition matrix)"]
    end
    
    Obs --> C1 & C2 & C3
    C1 & C2 & C3 --> PVal["Empirical p-value: p = (1 + Σ[T_surr >= T_obs]) / (1 + N)"]
```

### Empirical Significance Criterion
An observed test statistic $T_{obs}$ is declared statistically significant if and only if:
1. $p_{surr} < 0.01$ across at least 1,000 frequency-preserving surrogates;
2. $Z\text{-score} = \frac{T_{obs} - \mu_{surr}}{\sigma_{surr}} > +3.00$ (or $< -3.00$);
3. The result survives Bonferroni / Look-Elsewhere corrections for multiple testing:
   $$p_{corrected} = 1 - (1 - p_{raw})^M$$

---

## 4. Metrical Prosody & Catalectic Distich Substitution

### Moraic Weight Modeling
In archaic Aegean poetics, syllable duration is measured in **morae ($\mu$)**:
* Light open syllable (CV): $1\text{ mora}$
* Heavy / prolonged syllable or sign with incised oblique stroke: $2\text{ morae}$

### Catalectic Distich Compensation Formulation
In Side A (A14–A22), groups form an $A-B-A$ strophic triad. The distich measure $M(w_1) + M(w_2)$ is mathematically invariant:
$$\text{Strophe 1: } M(\text{A14}) + M(\text{A15}) = 6\mu + 3\mu = \mathbf{9\mu}$$
$$\text{Antistrophe 2: } M(\text{A17}) + M(\text{A18}) = 7\mu + 2\mu = \mathbf{9\mu}$$
$$\text{Epode 3: } M(\text{A20}) + M(\text{A21}) = 6\mu + 3\mu = \mathbf{9\mu}$$

Both stanzas resolve to the identical 4-sign refrain (`02-12-31-26`) with an incised stroke:
$$M(\text{Refrain}) = 4 + 1 = \mathbf{5\mu\text{ (Paeonic Measure)}}$$

Total Strophic Equality:
$$\text{Strophe: } 9\mu + 5\mu = \mathbf{14\mu}$$
$$\text{Antistrophe: } 9\mu + 5\mu = \mathbf{14\mu}$$
$$\text{Epode: } 9\mu + 5\mu = \mathbf{14\mu}$$

---

## 5. Kinematic Spiral Modeling Physics

To evaluate whether the spiral track was drawn freehand or using a mechanical guide, polar coordinates $(r_i, \theta_i)$ extracted from physical photogrammetry are fitted against three competitive geometric models using non-linear least squares (`scipy.optimize`):

1. **Linear Archimedean Spiral (Taut Cord Unspooling)**:
   $$r_{arch}(\theta) = r_0 - \frac{h}{2\pi}\theta$$
   Where $h$ is track pitch ($h \approx 13.8\text{ mm}$).
2. **Kinematic Pin-and-Cord Model**:
   Accounts for finite pin radius $R_{pin}$ and cord accumulation thickness $d$:
   $$r_{kin}(\theta) = \sqrt{\left(r_0 - \frac{d}{2\pi}\theta\right)^2 + R_{pin}^2}$$
3. **Logarithmic Spiral (Organic Growth)**:
   $$r_{log}(\theta) = a \cdot e^{-k\theta}$$

### Residual Criteria
* Freehand drafting on soft clay exhibits standard deviations $\sigma > 2.0\text{ mm}$ and maximum residuals $> 3.5\text{ mm}$.
* Mechanical cord unspooling yields residuals within cord elasticity bounds ($\text{RMSE} < 0.60\text{ mm}$, $R^2 > 0.999$).

---

## 6. Karplus-Strong Physical Acoustic Synthesis

The audio synthesis engine reproduces the string physics of the ancient 7-stringed Minoan phorminx (depicted on the Hagia Triada sarcophagus) using the Karplus-Strong digital waveguide algorithm:

$$y[n] = \frac{1}{2} \left( y[n - L] + y[n - L - 1] \right) \cdot \alpha$$

Where:
* $L = \left\lfloor \frac{F_s}{f_0} \right\rfloor$ is the discrete delay line length for target string frequency $f_0$ at sample rate $F_s = 44,100\text{ Hz}$.
* $\alpha = 0.992$ is the physical gut string decay attenuation factor.
* Initial excitation buffer: Uniform white noise $x \sim \mathcal{U}(-1.0, 1.0)$.
* Output: Normalized 16-bit linear PCM audio.

---

## 7. Chomsky Hierarchy & Topological Entropy

The 45-sign transition sequences are modeled as a Directed Graph $G = (V, E)$.
The adjacency transition matrix $A \in \mathbb{R}^{45 \times 45}$ is defined as:
$$A_{ij} = \text{Count of transitions } s_i \to s_j$$

### Topological Entropy Formulation
By the Perron-Frobenius theorem, for a non-negative irreducible matrix $A$, there exists a maximal real eigenvalue $\lambda_{max} > 0$. The topological entropy is defined as:
$$H_{top} = \log_2(\lambda_{max})$$

* **Classification Rule**:
  * If the graph is finite, has sparse connectivity ($|E| \ll |V|^2$), and $H_{top} < \log_2(|V|)$, the formal language generated by the state transitions is strictly **Type 3 (Regular Grammar / Finite State Automaton)**.

---

## 8. Petrographic Geochemical Matching & Exclusion Filters

Clay fabric provenance is evaluated by computing the normalized Euclidean distance across major elemental oxides (CaO, $\text{Fe}_2\text{O}_3$, $\text{Al}_2\text{O}_3$) against archaeological database profiles:

$$D_{elem}(x, y) = \sqrt{ \sum_{k=1}^3 \left( \frac{x_k - y_k}{\sigma_k} \right)^2 }$$

### Hard Inclusion Exclusion Filters
* **Volcanic Tephra Filter**: Presence of volcanic glass shards or pumice (diagnostic of Thera / Cyclades).
* **Metamorphic Mica Filter**: Presence of large muscovite/biotite schist plates (diagnostic of Southwestern Anatolian Menderes Massif).

If the observed Disc fabric lacks diagnostic inclusions present in a regional source, that source's compatibility score is penalized by $\ge 85\%$.
