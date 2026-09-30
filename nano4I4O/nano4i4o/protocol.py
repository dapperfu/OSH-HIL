"""Parse reader frames and match the checkout walk.

@relation(SRS-005, scope=file)
@relation(IRS-003, scope=file)
@relation(STD-004, scope=file)
"""

from __future__ import annotations

import re
from collections.abc import Sequence

from nano4i4o.constants import DONE_LINE, PINS, READY_LINE
from nano4i4o.errors import ProtocolError

_SAMPLE = re.compile(r"^SAMPLE (D[0-9]+) ([01])$")
_LOGGER_NAME = "nano4i4o.protocol"


def parse_frame(lines: Sequence[str]) -> tuple[int, int, int, int]:
    """Parse one READY / SAMPLE / DONE frame.

    Parameters
    ----------
    lines : sequence of str
        Frame lines without trailing newlines.

    Returns
    -------
    tuple of int
        Levels for D2, D3, D4, and D5.

    Raises
    ------
    ProtocolError
        The frame is incomplete or a level is not 0 or 1.
    """
    if len(lines) < 2 or lines[0] != READY_LINE or lines[-1] != DONE_LINE:
        raise ProtocolError("frame must start with READY and end with DONE")
    levels: dict[str, int] = {}
    for line in lines[1:-1]:
        match = _SAMPLE.match(line)
        if match is None:
            raise ProtocolError(f"bad sample line: {line}")
        pin = match.group(1)
        if pin not in PINS:
            raise ProtocolError(f"unexpected pin: {pin}")
        levels[pin] = int(match.group(2))
    missing = [pin for pin in PINS if pin not in levels]
    if missing:
        raise ProtocolError(f"missing samples for {', '.join(missing)}")
    return tuple(levels[pin] for pin in PINS)  # type: ignore[return-value]


def parse_stream(text: str) -> list[tuple[int, int, int, int]]:
    """Parse every complete frame in a serial capture.

    Parameters
    ----------
    text : str
        Concatenated reader output.

    Returns
    -------
    list of tuple of int
        One sample tuple per frame, in arrival order.
    """
    frames: list[tuple[int, int, int, int]] = []
    current: list[str] = []
    for raw_line in text.splitlines():
        line = raw_line.strip()
        if line == "":
            continue
        if line == READY_LINE:
            current = [line]
            continue
        if not current:
            continue
        current.append(line)
        if line == DONE_LINE:
            frames.append(parse_frame(current))
            current = []
    return frames


def walk_in_order(
    observed: Sequence[tuple[int, ...]],
    expected: Sequence[tuple[int, ...]],
) -> bool:
    """Return whether ``expected`` appears in order inside ``observed``.

    Parameters
    ----------
    observed : sequence of tuple of int
        Samples from the reader.
    expected : sequence of tuple of int
        Checkout walk.

    Returns
    -------
    bool
        True when every expected pattern has been seen in order.
    """
    index = 0
    for sample in observed:
        if index < len(expected) and tuple(sample) == tuple(expected[index]):
            index += 1
    return index == len(expected)
