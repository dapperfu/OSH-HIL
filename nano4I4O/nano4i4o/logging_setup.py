"""Logging levels for the nano4I4O host tools.

@relation(SRS-005, scope=file)
"""

from __future__ import annotations

import json
import logging
import os
import sys
from typing import Final

VERBOSE: Final[int] = 18
DETAIL: Final[int] = 16
TRACE: Final[int] = 14
FINE: Final[int] = 12

_LEVELS: Final[dict[int, int]] = {
    0: logging.INFO,
    1: VERBOSE,
    2: DETAIL,
    3: TRACE,
    4: FINE,
}


def verbose(self: logging.Logger, message: str, *args: object, **kwargs: object) -> None:
    """Log a message at VERBOSE.

    Parameters
    ----------
    message : str
        Format string.
    """
    if self.isEnabledFor(VERBOSE):
        self._log(VERBOSE, message, args, **kwargs)  # type: ignore[arg-type]


def detail(self: logging.Logger, message: str, *args: object, **kwargs: object) -> None:
    """Log a message at DETAIL.

    Parameters
    ----------
    message : str
        Format string.
    """
    if self.isEnabledFor(DETAIL):
        self._log(DETAIL, message, args, **kwargs)  # type: ignore[arg-type]


def trace(self: logging.Logger, message: str, *args: object, **kwargs: object) -> None:
    """Log a message at TRACE.

    Parameters
    ----------
    message : str
        Format string.
    """
    if self.isEnabledFor(TRACE):
        self._log(TRACE, message, args, **kwargs)  # type: ignore[arg-type]


def fine(self: logging.Logger, message: str, *args: object, **kwargs: object) -> None:
    """Log a message at FINE.

    Parameters
    ----------
    message : str
        Format string.
    """
    if self.isEnabledFor(FINE):
        self._log(FINE, message, args, **kwargs)  # type: ignore[arg-type]


def register_levels() -> None:
    """Register VERBOSE, DETAIL, TRACE, and FINE on the logging module."""
    logging.addLevelName(VERBOSE, "VERBOSE")
    logging.addLevelName(DETAIL, "DETAIL")
    logging.addLevelName(TRACE, "TRACE")
    logging.addLevelName(FINE, "FINE")
    logging.Logger.verbose = verbose  # type: ignore[attr-defined]
    logging.Logger.detail = detail  # type: ignore[attr-defined]
    logging.Logger.trace = trace  # type: ignore[attr-defined]
    logging.Logger.fine = fine  # type: ignore[attr-defined]


class JsonFormatter(logging.Formatter):
    """Format log records as one JSON object per line."""

    def format(self, record: logging.LogRecord) -> str:
        """Return the record as a JSON string.

        Parameters
        ----------
        record : logging.LogRecord
            Record emitted by the logging module.

        Returns
        -------
        str
            One JSON object.
        """
        payload = {
            "level": record.levelname,
            "logger": record.name,
            "message": record.getMessage(),
        }
        return json.dumps(payload)


def setup_logging(verbosity: int = 0) -> None:
    """Configure process logging from a ``-v`` count.

    Parameters
    ----------
    verbosity : int
        Number of ``-v`` flags. Zero is INFO. Five or more is DEBUG.
    """
    register_levels()
    level = _LEVELS.get(verbosity, logging.DEBUG)
    handler = logging.StreamHandler(sys.stderr)
    if os.environ.get("NANO4I4O_LOG_FORMAT") == "json":
        handler.setFormatter(JsonFormatter())
    else:
        handler.setFormatter(logging.Formatter("%(levelname)s %(name)s %(message)s"))
    root = logging.getLogger()
    root.handlers.clear()
    root.addHandler(handler)
    root.setLevel(level)
