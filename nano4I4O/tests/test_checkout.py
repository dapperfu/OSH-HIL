"""Checkout orchestration tests.

@relation(STD-001, scope=file)
@relation(STD-003, scope=file)
"""

from __future__ import annotations

import pytest

from nano4i4o.cases import CHECKOUT_CASES
from nano4i4o.checkout import run_checkout
from nano4i4o.constants import WALK
from nano4i4o.errors import BenchError, MissingPortError
from nano4i4o.protocol import parse_frame


def _capture(levels: tuple[tuple[int, int, int, int], ...]) -> str:
    lines: list[str] = []
    for sample in levels:
        pins = ("D2", "D3", "D4", "D5")
        lines.append("READY")
        for pin, level in zip(pins, sample, strict=True):
            lines.append(f"SAMPLE {pin} {level}")
        lines.append("DONE")
    return "\n".join(lines)


def test_run_checkout_flashes_hut_before_hil(monkeypatch: pytest.MonkeyPatch) -> None:
    """The fixture uploads the HUT image and then the HIL image."""
    monkeypatch.setenv("NANO_HIL_PORT", "/dev/hil")
    monkeypatch.setenv("NANO_HUT_PORT", "/dev/hut")
    order: list[tuple[str, str, str]] = []

    def flash(role: str, environment: str, port: str) -> None:
        order.append((role, environment, port))

    case = CHECKOUT_CASES[0]
    run_checkout(case, None, None, flash=flash, read_text=lambda _port: _capture(WALK))
    assert order == [
        ("hut", case.hut_env, "/dev/hut"),
        ("hil", case.hil_env, "/dev/hil"),
    ]


def test_run_checkout_fails_when_the_walk_is_absent(monkeypatch: pytest.MonkeyPatch) -> None:
    """Reader text that never shows the walk fails the checkout."""
    monkeypatch.setenv("NANO_HIL_PORT", "/dev/hil")
    monkeypatch.setenv("NANO_HUT_PORT", "/dev/hut")

    def flash(_role: str, _environment: str, _port: str) -> None:
        return None

    with pytest.raises(BenchError):
        run_checkout(
            CHECKOUT_CASES[1],
            None,
            None,
            flash=flash,
            read_text=lambda _port: _capture((WALK[0],)),
        )


@pytest.mark.hardware
@pytest.mark.parametrize("case", CHECKOUT_CASES, ids=lambda case: case.test_id)
def test_checkout_on_bench(case: object, hil_port: str | None, hut_port: str | None) -> None:
    """Flash the case on the real bench and require the walk.

    Parameters
    ----------
    case : CheckoutCase
        Parametrized checkout.
    hil_port : str or None
        ``--hil-port`` value.
    hut_port : str or None
        ``--hut-port`` value.
    """
    from nano4i4o.cases import CheckoutCase

    assert isinstance(case, CheckoutCase)
    run_checkout(case, hil_port, hut_port)


def test_hardware_checkout_fails_without_ports(monkeypatch: pytest.MonkeyPatch) -> None:
    """The bench checkout fails, rather than skipping, when ports are absent."""
    monkeypatch.delenv("NANO_HIL_PORT", raising=False)
    monkeypatch.delenv("NANO_HUT_PORT", raising=False)
    with pytest.raises(MissingPortError):
        run_checkout(CHECKOUT_CASES[0], None, None)


def test_read_serial_text_decodes_chunks(monkeypatch: pytest.MonkeyPatch) -> None:
    """A serial handle that returns bytes is decoded into text."""

    class FakeSerial:
        def __init__(self, port: str, baud: int, timeout: float) -> None:
            self.port = port
            self.baud = baud
            self.timeout = timeout
            self.reads = 0

        def read(self, _count: int) -> bytes:
            self.reads += 1
            if self.reads == 1:
                return b"READY\n"
            return b""

        def close(self) -> None:
            return None

    monkeypatch.setattr("nano4i4o.checkout.serial.Serial", FakeSerial)
    from nano4i4o.checkout import read_serial_text

    assert read_serial_text("/dev/fake") == "READY\n"


def test_read_serial_text_wraps_open_failure(monkeypatch: pytest.MonkeyPatch) -> None:
    """A port that cannot be opened becomes BenchError."""
    import serial

    def explode(*_args: object, **_kwargs: object) -> None:
        raise serial.SerialException("missing")

    monkeypatch.setattr("nano4i4o.checkout.serial.Serial", explode)
    from nano4i4o.checkout import read_serial_text
    from nano4i4o.errors import BenchError

    with pytest.raises(BenchError):
        read_serial_text("/dev/missing")


def test_sample_frame_helper_matches_parser() -> None:
    """The test frame builder agrees with the parser."""
    assert parse_frame(_capture((WALK[0],)).splitlines()) == WALK[0]
