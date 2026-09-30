"""Resolve the two bench serial ports.

@relation(SRS-003, scope=file)
@relation(STD-003, scope=file)
"""

from __future__ import annotations

import os

from nano4i4o.constants import HIL_PORT_ENV, HUT_PORT_ENV
from nano4i4o.errors import MissingPortError


def resolve_port(cli_value: str | None, env_name: str) -> str:
    """Choose a serial port from the CLI, then from the environment.

    Parameters
    ----------
    cli_value : str or None
        Value of ``--hil-port`` or ``--hut-port``.
    env_name : str
        Environment variable used when the CLI value is empty.

    Returns
    -------
    str
        Port path, for example ``/dev/ttyUSB0``.

    Raises
    ------
    MissingPortError
        Neither source provided a port.
    """
    if cli_value:
        return cli_value
    env_value = os.environ.get(env_name)
    if env_value:
        return env_value
    raise MissingPortError(env_name)


def resolve_hil_port(cli_value: str | None) -> str:
    """Resolve the nanoHIL serial port.

    Parameters
    ----------
    cli_value : str or None
        ``--hil-port`` value.

    Returns
    -------
    str
        Port path.
    """
    return resolve_port(cli_value, HIL_PORT_ENV)


def resolve_hut_port(cli_value: str | None) -> str:
    """Resolve the hardware-under-test serial port.

    Parameters
    ----------
    cli_value : str or None
        ``--hut-port`` value.

    Returns
    -------
    str
        Port path.
    """
    return resolve_port(cli_value, HUT_PORT_ENV)
