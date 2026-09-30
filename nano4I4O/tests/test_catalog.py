"""Catalog tests against the real PlatformIO projects.

@relation(SRS-001, scope=file)
"""

from __future__ import annotations

import pytest

from nano4i4o.cases import CheckoutCase
from nano4i4o.catalog import environments, role_directory, validate_cases
from nano4i4o.constants import DRIVE_ENV, READ_ENV
from nano4i4o.errors import CatalogError


def test_both_projects_publish_read_and_drive() -> None:
    """HIL and HUT both build the two checkout environments."""
    for role in ("hil", "hut"):
        names = environments(role_directory(role) / "platformio.ini")
        assert READ_ENV in names
        assert DRIVE_ENV in names


def test_validate_cases_accepts_the_project_table() -> None:
    """The shipped cases name environments that exist."""
    validate_cases()


def test_validate_cases_rejects_an_unknown_environment() -> None:
    """A case that names a missing environment fails the catalog."""
    bogus = (
        CheckoutCase(
            test_id="missing",
            hil_env="not_an_env",
            hut_env=DRIVE_ENV,
            reporter="hil",
        ),
    )
    with pytest.raises(CatalogError):
        validate_cases(bogus)


def test_validate_cases_rejects_a_bad_reporter() -> None:
    """The reporter must be hil or hut."""
    bogus = (
        CheckoutCase(
            test_id="bad-reporter",
            hil_env=READ_ENV,
            hut_env=DRIVE_ENV,
            reporter="bench",
        ),
    )
    with pytest.raises(CatalogError):
        validate_cases(bogus)


def test_unknown_role_is_rejected() -> None:
    """Only hil and hut are firmware roles."""
    with pytest.raises(CatalogError):
        role_directory("other")
