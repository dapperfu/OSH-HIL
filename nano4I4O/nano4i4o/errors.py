"""Domain errors for the nano4I4O host.

@relation(SRS-004, scope=file)
"""

from __future__ import annotations


class Nano4I4OError(Exception):
    """Base error for bench orchestration failures."""


class MissingPortError(Nano4I4OError):
    """A serial port was not given on the command line or in the environment."""

    def __init__(self, name: str) -> None:
        """Remember which port was missing.

        Parameters
        ----------
        name : str
            CLI option or environment variable that was empty.
        """
        self.name = name
        super().__init__(f"serial port {name} is not set")


class FlashError(Nano4I4OError):
    """PlatformIO upload failed."""


class ProtocolError(Nano4I4OError):
    """Reader text was not a checkout frame."""


class CatalogError(Nano4I4OError):
    """A checkout case names a PlatformIO environment that is not declared."""


class BenchError(Nano4I4OError):
    """The bench did not produce the expected walk."""
