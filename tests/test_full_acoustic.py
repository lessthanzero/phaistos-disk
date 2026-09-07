"""Unit tests for full two-sided acoustic resynthesis of the Phaistos Disc."""

from pathlib import Path
import pytest
from phaistos.prosody.acoustic import (
    FullAcousticSynthesisResult,
    render_full_disc_audio,
    synthesize_stroke_click,
)


def test_synthesize_stroke_click():
    click = synthesize_stroke_click(sample_rate=44100, duration=0.08)
    assert len(click) == int(44100 * 0.08)
    assert max(abs(click)) > 0.5


def test_render_full_disc_audio(tmp_path: Path):
    res = render_full_disc_audio(output_dir=tmp_path, sample_rate=44100)

    assert isinstance(res, FullAcousticSynthesisResult)
    assert 40.0 <= res.duration_side_a_sec <= 50.0
    assert 38.0 <= res.duration_side_b_sec <= 48.0
    assert 80.0 <= res.total_duration_sec <= 95.0

    # Total morae count
    assert res.total_morae_side_a == 133
    assert res.total_morae_side_b == 127
    assert res.total_morae_combined == 260
    assert res.total_stroke_cadences == 18

    # Check files exist
    assert Path(res.side_a_path).exists()
    assert Path(res.side_b_path).exists()
    assert Path(res.full_audio_path).exists()
    assert Path(res.full_audio_path).stat().st_size > 1_000_000
