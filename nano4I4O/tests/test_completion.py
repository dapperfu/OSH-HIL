"""Completion helper tests that do not edit the real shell rc file.

@relation(SRS-003, scope=file)
"""

from __future__ import annotations

from pathlib import Path

import click
import pytest
from click.testing import CliRunner

from nano4i4o.cli import cli
from nano4i4o.completion import (
    COMPLETION_COMMENT,
    detect_shell,
    get_command_absolute_path,
    get_rc_file,
    get_supported_shells,
)


def test_supported_shells_include_bash() -> None:
    """Click reports bash among the shells it can complete."""
    assert "bash" in get_supported_shells()


def test_detect_shell_uses_the_environment(monkeypatch: pytest.MonkeyPatch) -> None:
    """SHELL selects a supported shell, and an unknown shell falls back to bash."""
    monkeypatch.setenv("SHELL", "/bin/zsh")
    if "zsh" in get_supported_shells():
        assert detect_shell() == "zsh"
    monkeypatch.setenv("SHELL", "/bin/not-a-shell")
    assert detect_shell() == "bash"


def test_detect_shell_uses_the_first_shell_when_bash_is_absent(monkeypatch: pytest.MonkeyPatch) -> None:
    """Without bash, detection returns the first supported name."""
    monkeypatch.setattr("nano4i4o.completion.get_supported_shells", lambda: ["zsh"])
    monkeypatch.setenv("SHELL", "/bin/not-a-shell")
    assert detect_shell() == "zsh"


def test_detect_shell_rejects_an_empty_click_list(monkeypatch: pytest.MonkeyPatch) -> None:
    """An empty Click shell list is an error."""
    monkeypatch.setattr("nano4i4o.completion.get_supported_shells", lambda: [])
    with pytest.raises(click.ClickException):
        detect_shell()


def test_get_rc_file_maps_known_shells(monkeypatch: pytest.MonkeyPatch, tmp_path: Path) -> None:
    """Bash, zsh, and fish map to their usual rc paths."""
    monkeypatch.setattr(Path, "home", staticmethod(lambda: tmp_path))
    (tmp_path / ".bashrc").write_text("", encoding="utf-8")
    assert get_rc_file("bash") == tmp_path / ".bashrc"
    (tmp_path / ".bashrc").unlink()
    assert get_rc_file("bash") == tmp_path / ".bash_profile"
    assert get_rc_file("zsh") == tmp_path / ".zshrc"
    assert get_rc_file("fish") == tmp_path / ".config" / "fish" / "config.fish"


def test_get_rc_file_rejects_an_unknown_shell() -> None:
    """A shell Click does not support is rejected."""
    with pytest.raises(ValueError):
        get_rc_file("not-a-shell")


def test_command_path_is_executable() -> None:
    """The completion command path exists and is executable."""
    assert get_command_absolute_path().is_file()


def test_install_and_uninstall_edit_a_temporary_rc(monkeypatch: pytest.MonkeyPatch, tmp_path: Path) -> None:
    """--rc writes and then removes the completion block in a temporary file."""
    rc_file = tmp_path / ".bashrc"
    monkeypatch.setattr("nano4i4o.completion.get_rc_file", lambda _shell: rc_file)
    runner = CliRunner()
    installed = runner.invoke(cli, ["completion", "install", "--shell", "bash", "--rc"])
    assert installed.exit_code == 0
    assert COMPLETION_COMMENT in rc_file.read_text(encoding="utf-8")
    again = runner.invoke(cli, ["completion", "install", "--shell", "bash", "--rc"])
    assert again.exit_code == 0
    assert "already installed" in again.output
    removed = runner.invoke(cli, ["completion", "uninstall", "--shell", "bash", "--rc"])
    assert removed.exit_code == 0
    assert COMPLETION_COMMENT not in rc_file.read_text(encoding="utf-8")
    missing = runner.invoke(cli, ["completion", "uninstall", "--shell", "bash", "--rc"])
    assert missing.exit_code == 0
    plain = runner.invoke(cli, ["completion", "uninstall", "--shell", "bash"])
    assert plain.exit_code == 0


def test_uninstall_rc_when_the_file_is_absent(monkeypatch: pytest.MonkeyPatch, tmp_path: Path) -> None:
    """Uninstall succeeds when the rc file does not exist."""
    monkeypatch.setattr("nano4i4o.completion.get_rc_file", lambda _shell: tmp_path / "missing")
    result = CliRunner().invoke(cli, ["completion", "uninstall", "--shell", "bash", "--rc"])
    assert result.exit_code == 0


def test_install_rejects_an_unsupported_shell() -> None:
    """A shell outside Click's list fails the command."""
    result = CliRunner().invoke(cli, ["completion", "install", "--shell", "not-a-shell"])
    assert result.exit_code != 0
