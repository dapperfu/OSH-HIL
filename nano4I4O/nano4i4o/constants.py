"""Shared checkout constants.

@relation(SDD-004, scope=file)
@relation(IRS-002, scope=file)
"""

from __future__ import annotations

from typing import Final

PINS: Final[tuple[str, ...]] = ("D2", "D3", "D4", "D5")
WALK: Final[tuple[tuple[int, int, int, int], ...]] = (
    (0, 0, 0, 1),
    (0, 0, 1, 0),
    (0, 1, 0, 0),
    (1, 0, 0, 0),
    (1, 1, 1, 0),
    (1, 1, 0, 1),
    (1, 0, 1, 1),
    (0, 1, 1, 1),
)
BAUD: Final[int] = 115200
HIL_PORT_ENV: Final[str] = "NANO_HIL_PORT"
HUT_PORT_ENV: Final[str] = "NANO_HUT_PORT"
READ_ENV: Final[str] = "read_d2_d5"
DRIVE_ENV: Final[str] = "drive_walk"
FRAME_TIMEOUT_SECONDS: Final[float] = 3.0
READY_LINE: Final[str] = "READY"
DONE_LINE: Final[str] = "DONE"
