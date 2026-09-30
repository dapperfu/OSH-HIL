"""CLI tests that do not upload firmware.

@relation(SRS-002, scope=file)
"""

from __future__ import annotations

import pytest
from click.testing import CliRunner

from nano4i4o.cli import cli
from nano4i4o.logging_setup import DETAIL, VERBOSE, setup_logging


def test_flash_command_delegates(monkeypatch: pytest.MonkeyPatch) -> None:
    """The flash command calls the upload helper with the CLI values."""
    seen: dict[str, str] = {}

    def fake_flash(role: str, environment: str, port: str) -> None:
        seen["role"] = role
        seen["environment"] = environment
        seen["port"] = port

    monkeypatch.setattr("nano4i4o.cli.flash_environment", fake_flash)
    result = CliRunner().invoke(
        cli,
        ["flash", "--role", "hil", "--env", "read_d2_d5", "--port", "/dev/ttyUSB0"],
    )
    assert result.exit_code == 0
    assert seen == {"role": "hil", "environment": "read_d2_d5", "port": "/dev/ttyUSB0"}


def test_setup_logging_accepts_verbose_counts(monkeypatch: pytest.MonkeyPatch) -> None:
    """Verbosity flags map onto the custom levels and JSON output."""
    setup_logging(1)
    import logging

    assert logging.getLogger().level == VERBOSE
    setup_logging(2)
    assert logging.getLogger().level == DETAIL
    setup_logging(5)
    assert logging.getLogger().level == logging.DEBUG
    monkeypatch.setenv("NANO4I4O_LOG_FORMAT", "json")
    setup_logging(4)
    logger = logging.getLogger("nano4i4o")
    logger.verbose("visible")  # type: ignore[attr-defined]
    logger.detail("visible")  # type: ignore[attr-defined]
    logger.trace("visible")  # type: ignore[attr-defined]
    logger.fine("visible")  # type: ignore[attr-defined]


def test_completion_install_prints_a_source_line() -> None:
    """Completion install without --rc prints a source line and does not edit rc files."""
    result = CliRunner().invoke(cli, ["completion", "install", "--shell", "bash"])
    assert result.exit_code == 0
    assert "_NANO4I4O_COMPLETE=bash_source" in result.output
