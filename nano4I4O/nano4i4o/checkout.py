"""Flash both boards and judge the reader walk.

@relation(SDD-003, scope=file)
@relation(SRS-004, scope=file)
"""

from __future__ import annotations

import logging
from collections.abc import Callable

import serial

from nano4i4o.cases import CheckoutCase
from nano4i4o.constants import BAUD, FRAME_TIMEOUT_SECONDS, WALK
from nano4i4o.errors import BenchError
from nano4i4o.flash import flash_environment
from nano4i4o.ports import resolve_hil_port, resolve_hut_port
from nano4i4o.protocol import parse_stream, walk_in_order

logger = logging.getLogger("nano4i4o.checkout")
TextReader = Callable[[str], str]


def read_serial_text(port: str, timeout_s: float = FRAME_TIMEOUT_SECONDS) -> str:
    """Read reader text until the timeout.

    Parameters
    ----------
    port : str
        Serial device path.
    timeout_s : float
        Read timeout in seconds. The port is left open for several
        timeout slices so a full walk can arrive.

    Returns
    -------
    str
        Captured text.

    Raises
    ------
    BenchError
        The port cannot be opened.
    """
    try:
        handle = serial.Serial(port, BAUD, timeout=timeout_s)
    except serial.SerialException as exc:
        raise BenchError(f"cannot open {port}") from exc
    chunks: list[str] = []
    try:
        for _slice in range(4):
            raw = handle.read(4096)
            if raw:
                chunks.append(raw.decode("utf-8", errors="replace"))
    finally:
        handle.close()
    return "".join(chunks)


def run_checkout(
    case: CheckoutCase,
    hil_cli: str | None,
    hut_cli: str | None,
    *,
    flash: Callable[[str, str, str], None] = flash_environment,
    read_text: TextReader = read_serial_text,
) -> None:
    """Flash the case and require the walk from the reporter.

    The HUT image is uploaded first, then the HIL image. A missing port,
    a failed flash, or a walk that never appears raises and fails the test.

    Parameters
    ----------
    case : CheckoutCase
        Environments and reporter.
    hil_cli : str or None
        ``--hil-port`` value.
    hut_cli : str or None
        ``--hut-port`` value.
    flash : callable
        Upload function. Tests pass a fake.
    read_text : callable
        Reader that returns serial text for a port.

    Raises
    ------
    MissingPortError
        A required port was not provided.
    FlashError
        An upload failed.
    BenchError
        The reporter text did not contain the walk.
    """
    hil_port = resolve_hil_port(hil_cli)
    hut_port = resolve_hut_port(hut_cli)
    logger.info("checkout %s", case.test_id)
    flash("hut", case.hut_env, hut_port)
    flash("hil", case.hil_env, hil_port)
    reporter_port = hil_port if case.reporter == "hil" else hut_port
    observed = parse_stream(read_text(reporter_port))
    if not walk_in_order(observed, WALK):
        raise BenchError(f"{case.test_id} did not observe the checkout walk")
