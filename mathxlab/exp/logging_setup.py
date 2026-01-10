"""Backward-compatible logging entrypoint.

This module exists so older experiments can call `configure_logging()` while
new code uses `mathxlab.exp.logging.setup_logging()` directly.
"""

from __future__ import annotations

from pathlib import Path

from mathxlab.exp.logging import LoggingConfig
from mathxlab.exp.logging import setup_logging as setup_logging

__all__ = [
    "configure_logging",
]


# ------------------------------------------------------------------------------
def configure_logging(*, verbose: bool, log_file: Path | None = None) -> None:
    """
    Backward-compatible wrapper around :func:`mathxlab.exp.logging.setup_logging`.

    Args:
        verbose: If True, enable DEBUG only for ``mathxlab.*`` loggers.
        log_file: Optional log file path (UTF-8).

    Examples:
        >>> from mathxlab.exp.logging_setup import configure_logging
        >>> configure_logging(verbose=True)
    """
    setup_logging(config=LoggingConfig(verbose=verbose, log_file=log_file))
