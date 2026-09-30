"""Flash command tests that do not upload to a board.

@relation(SRS-002, scope=file)
"""

from __future__ import annotations

import subprocess

import pytest

from nano4i4o.errors import FlashError
from nano4i4o.flash import flash_environment, upload_command


def test_upload_command_names_the_environment_and_port() -> None:
    """The upload vector selects the environment and the port."""
    command = upload_command("read_d2_d5", "/dev/ttyUSB0")
    assert command == [
        "pio",
        "run",
        "-t",
        "upload",
        "-e",
        "read_d2_d5",
        "--upload-port",
        "/dev/ttyUSB0",
    ]


def test_flash_environment_raises_when_upload_fails() -> None:
    """A non-zero PlatformIO status becomes FlashError."""

    def runner(*_args: object, **_kwargs: object) -> subprocess.CompletedProcess[str]:
        return subprocess.CompletedProcess(args=["pio"], returncode=1, stdout="", stderr="port busy")

    with pytest.raises(FlashError, match="port busy"):
        flash_environment("hil", "read_d2_d5", "/dev/ttyUSB0", runner=runner)


def test_flash_environment_accepts_a_zero_status() -> None:
    """A zero status returns without raising."""
    seen: dict[str, object] = {}

    def runner(command: list[str], **kwargs: object) -> subprocess.CompletedProcess[str]:
        seen["command"] = command
        seen["cwd"] = kwargs["cwd"]
        return subprocess.CompletedProcess(args=command, returncode=0, stdout="", stderr="")

    flash_environment("hut", "drive_walk", "/dev/ttyUSB1", runner=runner)
    assert seen["command"] == upload_command("drive_walk", "/dev/ttyUSB1")
