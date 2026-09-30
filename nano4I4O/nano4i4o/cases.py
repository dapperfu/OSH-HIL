"""Hardware checkout cases.

@relation(STD-001, scope=file)
@relation(STD-002, scope=file)
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Final

from nano4i4o.constants import DRIVE_ENV, READ_ENV


@dataclass(frozen=True)
class CheckoutCase:
    """One pair of firmware environments and the board that reports.

    Parameters
    ----------
    test_id : str
        Stable name used by pytest.
    hil_env : str
        PlatformIO environment flashed to nanoHIL.
    hut_env : str
        PlatformIO environment flashed to the hardware under test.
    reporter : str
        ``hil`` or ``hut``, the board whose serial text is judged.
    """

    test_id: str
    hil_env: str
    hut_env: str
    reporter: str


CHECKOUT_CASES: Final[tuple[CheckoutCase, ...]] = (
    CheckoutCase(
        test_id="hut_drives_hil_reads",
        hil_env=READ_ENV,
        hut_env=DRIVE_ENV,
        reporter="hil",
    ),
    CheckoutCase(
        test_id="hil_drives_hut_reads",
        hil_env=DRIVE_ENV,
        hut_env=READ_ENV,
        reporter="hut",
    ),
)
