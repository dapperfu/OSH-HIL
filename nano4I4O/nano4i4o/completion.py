"""Shell completion install and uninstall for the nano4i4o CLI.

@relation(SRS-003, scope=file)
"""

from __future__ import annotations

import importlib
import os
import shutil
import sys
from pathlib import Path

import click
from click.shell_completion import ShellComplete

COMPLETION_COMMENT = "# nano4i4o completions"


def get_supported_shells() -> list[str]:
    """Return the shell names Click can complete.

    Returns
    -------
    list of str
        Shell names discovered from Click.
    """
    module = importlib.import_module("click.shell_completion")
    available = getattr(module, "_available_shells", None)
    if isinstance(available, dict) and available:
        return sorted(str(name) for name in available)
    names: list[str] = []
    for value in vars(module).values():
        if isinstance(value, type) and issubclass(value, ShellComplete) and value is not ShellComplete:
            shell_name = getattr(value, "name", None)
            if isinstance(shell_name, str):
                names.append(shell_name)
    return sorted(names)


def detect_shell() -> str:
    """Detect the current shell from ``SHELL``.

    Returns
    -------
    str
        A shell name Click supports. Unknown shells fall back to bash
        when bash is supported.
    """
    shell_name = os.path.basename(os.environ.get("SHELL", "")).lower()
    supported = get_supported_shells()
    if shell_name in supported:
        return shell_name
    if "bash" in supported:
        return "bash"
    if not supported:
        raise click.ClickException("Click did not report any completion shells")
    return supported[0]


def get_rc_file(shell: str) -> Path:
    """Return the rc file for ``shell``.

    Parameters
    ----------
    shell : str
        Shell name.

    Returns
    -------
    pathlib.Path
        Rc path under the home directory.

    Raises
    ------
    ValueError
        Click does not support ``shell``.
    """
    supported = get_supported_shells()
    if shell not in supported:
        raise ValueError(f"unsupported shell: {shell}")
    home = Path.home()
    if shell == "bash":
        bashrc = home / ".bashrc"
        return bashrc if bashrc.exists() else home / ".bash_profile"
    if shell == "zsh":
        return home / ".zshrc"
    if shell == "fish":
        return home / ".config" / "fish" / "config.fish"
    return home / f".{shell}rc"


def get_command_absolute_path() -> Path:
    """Return an absolute executable used to source completions.

    Returns
    -------
    pathlib.Path
        ``nano4i4o`` on ``PATH``, or the current Python executable.

    Raises
    ------
    RuntimeError
        No executable path could be verified.
    """
    located = shutil.which("nano4i4o")
    if located:
        path = Path(located).resolve()
        if path.is_file() and os.access(path, os.X_OK):
            return path
    executable = Path(sys.executable).resolve()
    if executable.is_file() and os.access(executable, os.X_OK):
        return executable
    raise RuntimeError("cannot determine the nano4i4o executable path")


def completion_source_line(shell: str, command: Path) -> str:
    """Build the eval line Click expects for ``shell``.

    Parameters
    ----------
    shell : str
        Shell name.
    command : pathlib.Path
        Absolute command path.

    Returns
    -------
    str
        Shell snippet.
    """
    variable = "_NANO4I4O_COMPLETE"
    return f'eval "$({variable}={shell}_source {command})"'


def _require_shell(shell: str | None) -> str:
    chosen = shell or detect_shell()
    supported = get_supported_shells()
    if chosen not in supported:
        raise click.ClickException(f"shell {chosen} is not supported; supported shells: {', '.join(supported)}")
    return chosen


@click.group()
def completion() -> None:
    """Install or remove shell completions."""


@completion.command("install")
@click.option("--shell", default=None, help="Shell name. Detected when omitted.")
@click.option("--rc", is_flag=True, help="Append the completion line to the shell rc file.")
def install_command(shell: str | None, rc: bool) -> None:
    """Install completions for the detected or named shell.

    Parameters
    ----------
    shell : str or None
        Shell override.
    rc : bool
        When true, update the rc file.
    """
    chosen = _require_shell(shell)
    command = get_command_absolute_path()
    line = completion_source_line(chosen, command)
    click.echo(line)
    if not rc:
        return
    rc_file = get_rc_file(chosen)
    existing = rc_file.read_text(encoding="utf-8") if rc_file.exists() else ""
    if COMPLETION_COMMENT in existing:
        click.echo(f"completions already installed in {rc_file}")
        return
    rc_file.parent.mkdir(parents=True, exist_ok=True)
    with rc_file.open("a", encoding="utf-8") as handle:
        handle.write(f"\n{COMPLETION_COMMENT}\n{line}\n")
    click.echo(f"completions installed in {rc_file}")


@completion.command("uninstall")
@click.option("--shell", default=None, help="Shell name. Detected when omitted.")
@click.option("--rc", is_flag=True, help="Remove the completion line from the shell rc file.")
def uninstall_command(shell: str | None, rc: bool) -> None:
    """Remove completions for the detected or named shell.

    Parameters
    ----------
    shell : str or None
        Shell override.
    rc : bool
        When true, edit the rc file.
    """
    chosen = _require_shell(shell)
    if not rc:
        click.echo("completions removed")
        return
    rc_file = get_rc_file(chosen)
    if not rc_file.exists():
        click.echo(f"completions not installed in {rc_file}")
        return
    kept: list[str] = []
    skip_next = False
    found = False
    for line in rc_file.read_text(encoding="utf-8").splitlines():
        if COMPLETION_COMMENT in line:
            skip_next = True
            found = True
            continue
        if skip_next and "NANO4I4O_COMPLETE" in line:
            skip_next = False
            continue
        skip_next = False
        kept.append(line)
    if found:
        rc_file.write_text("\n".join(kept) + "\n", encoding="utf-8")
        click.echo(f"completions removed from {rc_file}")
    else:
        click.echo(f"completions not installed in {rc_file}")
