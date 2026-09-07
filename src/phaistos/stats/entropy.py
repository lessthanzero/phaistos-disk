"""Information theoretic measures and compressibility analysis."""

from collections import Counter
import math
import zlib
import lzma
from typing import Dict, Tuple
from phaistos.core.models import DiscCorpus
from phaistos.stats.ngrams import extract_group_ngrams
from phaistos.stats.frequency import compute_sign_frequencies


def compute_unigram_entropy(corpus: DiscCorpus) -> float:
    """H(X) = -sum p(x) log2 p(x)."""
    counts = compute_sign_frequencies(corpus)
    total = sum(counts.values())
    if total == 0:
        return 0.0
    return -sum((c / total) * math.log2(c / total) for c in counts.values() if c > 0)


def compute_bigram_joint_and_conditional_entropy(corpus: DiscCorpus) -> Tuple[float, float, float]:
    """
    Compute:
    1. Joint bigram entropy: H(X, Y) = -sum p(x, y) log2 p(x, y)
    2. Conditional entropy: H(Y | X) = H(X, Y) - H(X_first)
    3. Mutual information: I(X; Y) = H(X_first) + H(Y_second) - H(X, Y)
    """
    bigrams = extract_group_ngrams(corpus, n=2)
    total_bigrams = sum(bigrams.values())
    if total_bigrams == 0:
        return 0.0, 0.0, 0.0

    # Marginal counts of first and second signs in bigrams
    x_counts = Counter()
    y_counts = Counter()
    for (x, y), c in bigrams.items():
        x_counts[x] += c
        y_counts[y] += c

    h_xy = -sum((c / total_bigrams) * math.log2(c / total_bigrams) for c in bigrams.values() if c > 0)
    h_x = -sum((c / total_bigrams) * math.log2(c / total_bigrams) for c in x_counts.values() if c > 0)
    h_y = -sum((c / total_bigrams) * math.log2(c / total_bigrams) for c in y_counts.values() if c > 0)

    h_cond = h_xy - h_x
    mi = max(0.0, h_x + h_y - h_xy)

    return h_xy, h_cond, mi


def compute_compressibility_metrics(corpus: DiscCorpus) -> Dict[str, float]:
    """
    Evaluate compressibility of the raw sequence and group representation.
    Compression ratio = compressed_size / raw_size.
    """
    # Create raw byte representations
    seq_str = " ".join("-".join(g.signs) for g in corpus.all_groups())
    raw_bytes = seq_str.encode("utf-8")
    raw_size = len(raw_bytes)

    zlib_compressed = zlib.compress(raw_bytes, level=9)
    lzma_compressed = lzma.compress(raw_bytes)

    return {
        "raw_bytes": float(raw_size),
        "zlib_bytes": float(len(zlib_compressed)),
        "zlib_ratio": len(zlib_compressed) / float(raw_size),
        "lzma_bytes": float(len(lzma_compressed)),
        "lzma_ratio": len(lzma_compressed) / float(raw_size),
    }
