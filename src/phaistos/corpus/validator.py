"""Validation engine for Phaistos Disc corpus integrity."""

from typing import Dict, List, Tuple
from phaistos.core.models import DiscCorpus


class ValidationError(Exception):
    """Raised when corpus fails structural invariants."""
    pass


def validate_corpus(corpus: DiscCorpus) -> Dict[str, bool]:
    """
    Validate canonical epigraphic invariants:
    1. Catalogue contains exactly 45 unique Evans signs.
    2. Side A contains exactly 31 groups.
    3. Side B contains exactly 30 groups (total 61 groups).
    4. Total sign count matches expected canon (242 signs in Godart 1995).
    5. Exactly 18 incised oblique strokes (10 on Side A, 8 on Side B).
    6. All referenced sign IDs exist in the catalogue.
    """
    results = {}

    # 1. Sign catalogue checks
    cat_ids = {s.evans_id for s in corpus.signs_catalogue}
    if len(corpus.signs_catalogue) != 45:
        raise ValidationError(f"Expected 45 signs in catalogue, found {len(corpus.signs_catalogue)}")
    if len(cat_ids) != 45:
        raise ValidationError(f"Duplicate Evans IDs found in catalogue: {len(cat_ids)} unique")
    results["signs_catalogue_45_unique"] = True

    # 2. Unicode hex check
    for sign in corpus.signs_catalogue:
        expected_char = chr(int(sign.unicode_hex, 16))
        if sign.unicode_char != expected_char:
            raise ValidationError(
                f"Unicode char mismatch for sign {sign.evans_id}: "
                f"given '{sign.unicode_char}' vs chr({sign.unicode_hex}) = '{expected_char}'"
            )
    results["unicode_code_points_match"] = True

    # 3. Group counts
    if corpus.side_a.group_count != 31:
        raise ValidationError(f"Side A expected 31 groups, found {corpus.side_a.group_count}")
    if corpus.side_b.group_count != 30:
        raise ValidationError(f"Side B expected 30 groups, found {corpus.side_b.group_count}")
    if corpus.total_groups != 61:
        raise ValidationError(f"Total groups expected 61, found {corpus.total_groups}")
    results["group_count_61"] = True

    # 4. Sign counts
    if corpus.total_signs != 242:
        raise ValidationError(f"Total signs expected 242, found {corpus.total_signs}")
    results["total_signs_242"] = True

    # 5. Oblique strokes
    if corpus.side_a.oblique_stroke_count != 10:
        raise ValidationError(f"Side A expected 10 oblique strokes, found {corpus.side_a.oblique_stroke_count}")
    if corpus.side_b.oblique_stroke_count != 8:
        raise ValidationError(f"Side B expected 8 oblique strokes, found {corpus.side_b.oblique_stroke_count}")
    if corpus.total_oblique_strokes != 18:
        raise ValidationError(f"Total oblique strokes expected 18, found {corpus.total_oblique_strokes}")
    results["oblique_strokes_18"] = True

    # 6. Check all referenced signs in groups exist
    for group in corpus.all_groups():
        for s_id in group.signs:
            if s_id not in cat_ids:
                raise ValidationError(f"Group {group.id} references unknown sign ID '{s_id}'")
    results["all_referenced_signs_valid"] = True

    return results
