"""Shared pytest options for the nano4I4O bench.

@relation(SRS-003, scope=file)
"""

from __future__ import annotations

import pytest


def pytest_addoption(parser: pytest.Parser) -> None:
    """Register the two serial-port options.

    Parameters
    ----------
    parser : pytest.Parser
        Pytest command-line parser.
    """
    parser.addoption("--hil-port", default=None, help="nanoHIL serial port")
    parser.addoption("--hut-port", default=None, help="Hardware-under-test serial port")


@pytest.fixture
def hil_port(request: pytest.FixtureRequest) -> str | None:
    """Return ``--hil-port`` when the user passed it.

    Parameters
    ----------
    request : pytest.FixtureRequest
        Active test request.

    Returns
    -------
    str or None
        Port path or None.
    """
    value = request.config.getoption("--hil-port")
    return value if isinstance(value, str) else None


@pytest.fixture
def hut_port(request: pytest.FixtureRequest) -> str | None:
    """Return ``--hut-port`` when the user passed it.

    Parameters
    ----------
    request : pytest.FixtureRequest
        Active test request.

    Returns
    -------
    str or None
        Port path or None.
    """
    value = request.config.getoption("--hut-port")
    return value if isinstance(value, str) else None
