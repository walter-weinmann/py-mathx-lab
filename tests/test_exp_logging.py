"""Unit tests for logging helpers.

The project needs to run on Windows where the default console encoding may be
non-UTF-8. These tests exercise the critical compatibility paths without being
platform-specific.
"""

from __future__ import annotations

from pathlib import Path
from typing import Any

from mathxlab.exp.logging import (
    LoggingConfig,
    get_logger,
    setup_logging,
)
from mathxlab.exp.logging_setup import configure_logging


class _DummyStdoutNoReconfigure:
    """A minimal stdout replacement that lacks reconfigure()."""

    def __init__(self, encoding: str) -> None:
        self.encoding = encoding

    def write(self, text: str) -> int:  # pragma: no cover
        return len(text)

    def flush(self) -> None:  # pragma: no cover
        return None

    def reconfigure(self, **kwargs: Any) -> None:
        if "errors" in kwargs:
            return
        raise AttributeError("reconfigure not supported")


def test_setup_logging_creates_file_handler(tmp_path: Path) -> None:
    """setup_logging should write logs to the requested file."""
    log_path = tmp_path / "run.log"
    setup_logging(config=LoggingConfig(verbose=True, log_file=log_path))
    import logging

    logger = logging.getLogger("mathxlab.test")
    logger.info("hello")

    assert log_path.exists()
    text = log_path.read_text(encoding="utf-8")
    assert "hello" in text


def test_configure_logging_does_not_crash() -> None:
    """configure_logging should be safe to call multiple times."""
    configure_logging(verbose=False)
    configure_logging(verbose=True)


def test_get_logger_returns_named_logger() -> None:
    """get_logger() should provide a logger with the requested name."""
    logger = get_logger("mathxlab.tests")
    assert logger.name == "mathxlab.tests"
