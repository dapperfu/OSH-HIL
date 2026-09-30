"""Port resolution tests.

@relation(SRS-003, scope=file)
@relation(STD-003, scope=file)
"""

from __future__ import annotations

import pytest

from nano4i4o.constants import HIL_PORT_ENV, HUT_PORT_ENV
from nano4i4o.errors import MissingPortError
from nano4i4o.ports import resolve_hil_port, resolve_hut_port, resolve_port


def test_cli_value_wins_over_the_environment(monkeypatch: pytest.MonkeyPatch) -> None:
    """A CLI port is used even when the environment variable is set."""
    monkeypatch.setenv(HIL_PORT_ENV, "/dev/from-env")
    assert resolve_port("/dev/from-cli", HIL_PORT_ENV) == "/dev/from-cli"


def test_environment_is_used_when_cli_is_empty(monkeypatch: pytest.MonkeyPatch) -> None:
    """The environment variable supplies the port when the CLI omits it."""
    monkeypatch.setenv(HUT_PORT_ENV, "/dev/hut")
    assert resolve_hut_port(None) == "/dev/hut"


def test_missing_port_raises(monkeypatch: pytest.MonkeyPatch) -> None:
    """An unset CLI value and an unset variable fail the lookup."""
    monkeypatch.delenv(HIL_PORT_ENV, raising=False)
    with pytest.raises(MissingPortError):
        resolve_hil_port(None)
