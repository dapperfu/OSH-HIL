"""Discover PlatformIO environments for HIL and HUT.

@relation(SRS-001, scope=file)
@relation(SDD-002, scope=file)
"""

from __future__ import annotations

import logging
import re
from pathlib import Path

from nano4i4o.cases import CHECKOUT_CASES, CheckoutCase
from nano4i4o.errors import CatalogError

_ENV_LINE = re.compile(r"^\[env:([A-Za-z0-9_]+)\]\s*$")
logger = logging.getLogger("nano4i4o.catalog")


def project_root() -> Path:
    """Return the nano4I4O directory that contains HIL and HUT.

    Returns
    -------
    pathlib.Path
        Absolute project root.
    """
    return Path(__file__).resolve().parents[1]


def environments(platformio_ini: Path) -> tuple[str, ...]:
    """List named PlatformIO environments in one ini file.

    Parameters
    ----------
    platformio_ini : pathlib.Path
        Path to ``platformio.ini``.

    Returns
    -------
    tuple of str
        Environment names in file order.
    """
    names: list[str] = []
    for line in platformio_ini.read_text(encoding="utf-8").splitlines():
        match = _ENV_LINE.match(line.strip())
        if match is not None:
            names.append(match.group(1))
    logger.debug("environments in %s: %s", platformio_ini, names)
    return tuple(names)


def role_directory(role: str) -> Path:
    """Return the PlatformIO project directory for ``hil`` or ``hut``.

    Parameters
    ----------
    role : str
        ``hil`` or ``hut``.

    Returns
    -------
    pathlib.Path
        Project directory.

    Raises
    ------
    CatalogError
        ``role`` is not a known board.
    """
    if role == "hil":
        return project_root() / "HIL"
    if role == "hut":
        return project_root() / "HUT"
    raise CatalogError(f"unknown role: {role}")


def validate_cases(cases: tuple[CheckoutCase, ...] = CHECKOUT_CASES) -> None:
    """Fail when a case names an environment the project does not build.

    Parameters
    ----------
    cases : tuple of CheckoutCase
        Cases to check. Defaults to the project table.

    Raises
    ------
    CatalogError
        An environment or reporter is missing.
    """
    hil_envs = set(environments(role_directory("hil") / "platformio.ini"))
    hut_envs = set(environments(role_directory("hut") / "platformio.ini"))
    for case in cases:
        if case.hil_env not in hil_envs:
            raise CatalogError(f"{case.test_id} missing HIL env {case.hil_env}")
        if case.hut_env not in hut_envs:
            raise CatalogError(f"{case.test_id} missing HUT env {case.hut_env}")
        if case.reporter not in {"hil", "hut"}:
            raise CatalogError(f"{case.test_id} reporter must be hil or hut")
