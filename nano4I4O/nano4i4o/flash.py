"""Flash one PlatformIO environment onto a Nano.

@relation(SRS-002, scope=file)
@relation(SDD-003, scope=file)
"""

from __future__ import annotations

import logging
import subprocess
from collections.abc import Callable
from pathlib import Path

from nano4i4o.catalog import role_directory
from nano4i4o.errors import FlashError

logger = logging.getLogger("nano4i4o.flash")
Runner = Callable[..., subprocess.CompletedProcess[str]]


def upload_command(environment: str, port: str) -> list[str]:
    """Build the PlatformIO upload command.

    Parameters
    ----------
    environment : str
        PlatformIO environment name.
    port : str
        Upload serial port.

    Returns
    -------
    list of str
        Argument vector for ``pio``.
    """
    return ["pio", "run", "-t", "upload", "-e", environment, "--upload-port", port]


def flash_environment(
    role: str,
    environment: str,
    port: str,
    *,
    runner: Runner = subprocess.run,
) -> None:
    """Upload ``environment`` to the board for ``role``.

    Parameters
    ----------
    role : str
        ``hil`` or ``hut``.
    environment : str
        PlatformIO environment name.
    port : str
        Upload serial port.
    runner : callable
        Function with the ``subprocess.run`` signature. Tests inject a fake.

    Raises
    ------
    FlashError
        The upload command returned a non-zero status.
    """
    project = role_directory(role)
    command = upload_command(environment, port)
    logger.info("flash %s %s on %s", role, environment, port)
    result = runner(
        command,
        cwd=project,
        check=False,
        capture_output=True,
        text=True,
    )
    if result.returncode != 0:
        detail = (result.stderr or result.stdout or "").strip()
        raise FlashError(f"upload failed for {role} {environment}: {detail}") from None


def project_for(role: str) -> Path:
    """Return the firmware directory that ``flash_environment`` uploads.

    Parameters
    ----------
    role : str
        ``hil`` or ``hut``.

    Returns
    -------
    pathlib.Path
        PlatformIO project directory.
    """
    return role_directory(role)
