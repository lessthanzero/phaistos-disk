# Outreach drafts (do not send until public GitHub URLs exist)

## Researchers

| Priority | Name | Email | Notes |
|----------|------|-------|-------|
| 1 | Ester Salgarella | esalga@aias.au.dk | AIAS Aarhus |
| 2 | Silvia Ferrara | s.ferrara@unibo.it | Bologna / SAPIENCE |
| 3 | Brent Davis | bedavis@unimelb.edu.au | Melbourne |
| 4 | Michele Corazza | michele.corazza2@unibo.it | Computational methods (now legal NLP) |
| 5 | Barbara Montecchi | barbara.montecchi@unifi.it | Museum role; still public institutional email |
| 6 | John Younger | jyounger@ku.edu (historical) | Re-verify; emeritus |
| 7 | Judith Weingarten | — | No verified email; Academia only |

**Voice:** personal side project for fun / interactive workbench — **not** “independent researcher.”

Replace `{GITHUB_URLS}` after public remotes exist.

---

## Email template (individual)

Subject: Open-source Phaistos Disc / Linear A workbench — would welcome a critical look

Dear Professor {Name},

I built a couple of open-source tools around the Phaistos Disc and Linear A mainly for fun, and because I wanted a usable interactive workbench (spiral view, audio playback, simple statistical checks). I’m not claiming a decipherment, and I’m not writing this as an academic paper.

The software tries to keep observation, transcription, tests, and interpretation separate, and to poke patterns with null models so I don’t fool myself. The clearest structural thing that stands out so far is a repeated sign-group on the Disc (`02-12-31-26`); anything about genre or religion I treat only as a hypothesis.

If you have a moment when the repos are public, I’d genuinely appreciate critical feedback on whether the framing is misleading or the methods are off: {GITHUB_URLS}.

No need for a long reply — even a blunt “this bit is wrong” would help.

Thanks for your time,  
Alexander Katin

---

## Reddit draft

**Suggested subs (pick 1–2; read rules first):** r/linguistics, r/Archaeology, r/AncientWorld, r/computational_linguistics

**Title:** I built open-source interactive labs for the Phaistos Disc and Linear A (not a decipherment — looking for criticism)

**Body:**

I spent some spare time building two open-source projects: a Phaistos Disc workbench and a Linear A analysis harness, plus a small shared toolkit. This started as a fun side project — I mostly wanted something interactive I could click through (spiral view of both sides, teleprompter-style playback, synthetic audio, simple Monte Carlo null checks), not a “I solved it” post.

**What this is**
- Local-first Python + offline HTML workbenches
- Explicit separation of physical observation / transcription / statistical test / hypothesis
- Null models (shuffle / frequency / Markov-style surrogates) and unicity-style checks so pattern-hunting doesn’t go unchecked

**What I am *not* claiming**
- Not a decipherment of Linear A or the Disc
- Not peer-reviewed archaeology
- Genre / religious / “hymn” readings are **hypotheses only**

**What’s actually solid enough to show**
- On the Disc, groups A16 / A19 / A22 share the same sign sequence `02-12-31-26` (standard Godart-style transcription). That’s an observation, not a translation.

**Why post**
I’d rather get torn apart on method and presentation than quietly overclaim. If you work on Aegean scripts, stats, or research software: tell me what’s wrong, what’s missing, or what’s already known.

Repos: {GITHUB_URLS}

Happy to answer technical questions about the workbench / CLI. Please don’t read this as “AI deciphered Minoan.”

---

## LinkedIn draft

I built a small open-source side project around the Phaistos Disc and Linear A — mostly for fun, and because I wanted an interactive workbench I could actually use (dual-face spiral view, playback, simple statistical controls), not because I think I’ve deciphered anything.

The repos are computational labs, not a journal paper:
- reproducible CLI + offline HTML UI
- clear separation between observation, transcription, tests, and interpretation
- null-model checks so structural patterns don’t get sold as “proof”

The most straightforward structural finding I’m comfortable highlighting is a repeated sign-group sequence on the Disc. Anything about genre or religious reading stays labeled as hypothesis.

If you work in computational archaeology, historical linguistics, or research tooling, I’d welcome critical feedback once the GitHub release is up: {GITHUB_URLS}

#OpenSource #ComputationalArchaeology #DigitalHumanities #LinearA #PhaistosDisc
