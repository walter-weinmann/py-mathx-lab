from __future__ import annotations

from pathlib import Path

from mathxlab.exp.logging import LoggingConfig, setup_logging


def configure_logging(*, verbose: bool, log_file: Path | None = None) -> None:
    """Backward-compatible wrapper around :func:`mathxlab.exp.logging.setup_logging`.

    Args:
        verbose: If True, enable DEBUG only for ``mathxlab.*`` loggers.
        log_file: Optional log file path (UTF-8).
    """
    setup_logging(config=LoggingConfig(verbose=verbose, log_file=log_file))
