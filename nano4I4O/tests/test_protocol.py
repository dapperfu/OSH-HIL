"""Parser tests for reader frames.

@relation(STD-004, scope=file)
"""

from __future__ import annotations

import pytest

from nano4i4o.constants import WALK
from nano4i4o.errors import ProtocolError
from nano4i4o.protocol import parse_frame, parse_stream, walk_in_order


def _frame(levels: tuple[int, int, int, int]) -> list[str]:
    pins = ("D2", "D3", "D4", "D5")
    lines = ["READY"]
    for pin, level in zip(pins, levels, strict=True):
        lines.append(f"SAMPLE {pin} {level}")
    lines.append("DONE")
    return lines


def test_parse_frame_accepts_ready_samples_done() -> None:
    """A complete frame returns the four pin levels."""
    assert parse_frame(_frame((0, 0, 0, 1))) == (0, 0, 0, 1)


def test_parse_frame_rejects_bad_level() -> None:
    """A level other than 0 or 1 is rejected."""
    lines = _frame((0, 0, 0, 1))
    lines[1] = "SAMPLE D2 2"
    with pytest.raises(ProtocolError):
        parse_frame(lines)


def test_parse_stream_reads_two_frames() -> None:
    """Back-to-back frames become two samples."""
    text = "\n".join(_frame((0, 0, 0, 1)) + _frame((0, 0, 1, 0)))
    assert parse_stream(text) == [(0, 0, 0, 1), (0, 0, 1, 0)]


def test_walk_in_order_accepts_extra_samples() -> None:
    """Repeated samples still match when the walk order is present."""
    observed = [WALK[0], WALK[0], *WALK[1:]]
    assert walk_in_order(observed, WALK)


def test_parse_frame_rejects_a_missing_pin() -> None:
    """A frame that omits a pin is rejected."""
    lines = _frame((0, 0, 0, 1))
    del lines[2]
    with pytest.raises(ProtocolError):
        parse_frame(lines)


def test_parse_frame_rejects_an_unknown_pin() -> None:
    """A pin outside D2-D5 is rejected."""
    lines = _frame((1, 0, 0, 0))
    lines[1] = "SAMPLE D9 1"
    with pytest.raises(ProtocolError):
        parse_frame(lines)


def test_parse_stream_ignores_noise_before_ready() -> None:
    """Lines before READY are ignored."""
    text = "boot\n\n" + "\n".join(_frame((1, 0, 0, 0)))
    assert parse_stream(text) == [(1, 0, 0, 0)]


def test_parse_frame_rejects_a_short_frame() -> None:
    """A frame without DONE is rejected."""
    with pytest.raises(ProtocolError):
        parse_frame(["READY"])


def test_walk_in_order_rejects_a_skipped_step() -> None:
    """A missing step fails the matcher."""
    assert walk_in_order(WALK[1:], WALK) is False
