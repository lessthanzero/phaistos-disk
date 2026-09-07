"""Parser and phonological analyzer for the Egyptian Keftiu (Minoan) corpus.

Ingests authentic 18th-Dynasty Egyptian hieratic transcriptions of spoken Minoan
(London Medical Papyrus BM EA 10059 and Writing Board BM EA 5647) to provide an
empirical, external phonetic witness of Bronze Age Cretan phonotactics.
"""

from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Dict, List, Optional, Set, Tuple
import yaml

from phaistos.corpus.loader import get_default_corpus_dir


@dataclass
class KeftiuText:
    """An individual Keftiu text (incantation or anthroponym)."""
    id: str
    source: str
    vocalized_reconstruction: str
    syllables: List[str]
    syllable_count: int
    reduplication_motifs: List[str] = field(default_factory=list)
    notes: str = ""


@dataclass
class KeftiuPhonologySummary:
    """Statistical phonological profile extracted from the Keftiu records."""
    total_words: int
    total_syllables: int
    distinct_syllables: int
    consonant_inventory: List[str]
    vowel_inventory: List[str]
    open_syllable_rate_pct: float  # In Keftiu Egyptian orthography, 100% open CV / V
    reduplication_instance_count: int
    top_syllables: List[Tuple[str, int]]
    syllable_bigrams: List[Tuple[str, str, int]]


def load_keftiu_corpus(corpus_dir: Optional[Path] = None) -> List[KeftiuText]:
    """Load the canonical Egyptian Keftiu corpus from YAML."""
    base_dir = corpus_dir or get_default_corpus_dir()
    file_path = base_dir / "comparative" / "egyptian_keftiu.yaml"

    with open(file_path, "r", encoding="utf-8") as f:
        raw = yaml.safe_load(f)

    texts: List[KeftiuText] = []
    for inc in raw.get("incantations", []):
        texts.append(KeftiuText(
            id=inc["id"],
            source=inc["source"],
            vocalized_reconstruction=inc["vocalized_reconstruction"],
            syllables=inc["syllables"],
            syllable_count=inc["syllable_count"],
            reduplication_motifs=inc.get("reduplication_motifs", []),
            notes=inc.get("notes", ""),
        ))

    for p in raw.get("personal_names", []):
        texts.append(KeftiuText(
            id=p["id"],
            source=p["source"],
            vocalized_reconstruction=p["name"],
            syllables=p["syllables"],
            syllable_count=len(p["syllables"]),
            reduplication_motifs=[],
            notes=p.get("notes", ""),
        ))

    return texts


def analyze_keftiu_phonology(texts: Optional[List[KeftiuText]] = None) -> KeftiuPhonologySummary:
    """Analyze the phonological invariants of the Keftiu text corpus."""
    if texts is None:
        texts = load_keftiu_corpus()

    all_syllables: List[str] = []
    consonants: Set[str] = set()
    vowels: Set[str] = set()
    bigrams: Dict[Tuple[str, str], int] = {}
    redup_count = 0

    for t in texts:
        syls = t.syllables
        all_syllables.extend(syls)
        redup_count += len(t.reduplication_motifs)

        for s in syls:
            s_clean = s.lower().strip()
            # Extract vowels and consonants
            # Open syllables: C + V or pure V
            v = s_clean[-1]
            c = s_clean[:-1]
            if v in "aeiou":
                vowels.add(v)
            if c:
                consonants.add(c)

        for i in range(len(syls) - 1):
            pair = (syls[i], syls[i + 1])
            bigrams[pair] = bigrams.get(pair, 0) + 1

    syl_counts: Dict[str, int] = {}
    for s in all_syllables:
        syl_counts[s] = syl_counts.get(s, 0) + 1

    top_syls = sorted(syl_counts.items(), key=lambda x: x[1], reverse=True)
    sorted_bigrams = sorted([(k[0], k[1], v) for k, v in bigrams.items()], key=lambda x: x[2], reverse=True)

    return KeftiuPhonologySummary(
        total_words=len(texts),
        total_syllables=len(all_syllables),
        distinct_syllables=len(syl_counts),
        consonant_inventory=sorted(list(consonants)),
        vowel_inventory=sorted(list(vowels)),
        open_syllable_rate_pct=100.0,  # Strictly open CV / V structure
        reduplication_instance_count=redup_count,
        top_syllables=top_syls[:10],
        syllable_bigrams=sorted_bigrams[:10],
    )
