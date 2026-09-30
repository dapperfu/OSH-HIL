"""Command line for flashing a nano4I4O board.

@relation(SRS-002, scope=file)
"""

from __future__ import annotations

import click

from nano4i4o.completion import completion
from nano4i4o.flash import flash_environment
from nano4i4o.logging_setup import setup_logging


@click.group()
@click.option("-v", "--verbose", count=True, help="Increase log verbosity. Repeat for more detail.")
def cli(verbose: int) -> None:
    """Flash firmware for the nano4I4O smoke bench."""
    setup_logging(verbose)


@cli.command("flash")
@click.option("--role", type=click.Choice(["hil", "hut"]), required=True, help="Board to flash.")
@click.option("--env", "environment", required=True, help="PlatformIO environment name.")
@click.option("--port", required=True, help="Serial port used for upload.")
def flash_command(role: str, environment: str, port: str) -> None:
    """Upload one environment to one board.

    Parameters
    ----------
    role : str
        ``hil`` or ``hut``.
    environment : str
        PlatformIO environment.
    port : str
        Upload port.
    """
    flash_environment(role, environment, port)
    click.echo(f"flashed {role} {environment} on {port}")


cli.add_command(completion)
