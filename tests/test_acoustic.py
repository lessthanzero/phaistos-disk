"""Unit tests for acoustic lyre resynthesis."""

import os
from pathlib import Path
import pytest
from phaistos.prosody.acoustic import render_central_triad_audio, karplus_strong_pluck, AcousticSynthesisResult


def test_karplus_strong_pluck():
    sample_rate = 44100
    duration = 0.5
    chunk = karplus_strong_pluck(440.0, duration, sample_rate=sample_rate)
    assert len(chunk) == int(duration * sample_rate)
    assert max(abs(chunk)) > 0.0


def test_render_central_triad_audio(tmp_path):
    res = render_central_triad_audio(output_dir=tmp_path, sample_rate=22050)
    assert isinstance(res, AcousticSynthesisResult)
    assert os.path.isfile(res.audio_file_path)
    assert res.total_strophes_rendered == 3
    assert res.total_morae_synthesized == 42
    assert res.duration_seconds > 8.0
    assert "D4" in res.tuning_system
