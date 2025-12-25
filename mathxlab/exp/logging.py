from __future__ import annotations

import logging
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import override


# ------------------------------------------------------------------------------
@dataclass(frozen=True, slots=True)
class LoggingConfig:
    """Configuration for experiment logging.

    Args:
        package_prefix: Logger name prefix considered "our code" (default: "mathxlab").
        verbose: If True, emit DEBUG logs for package_prefix only.
        log_file: Optional file path for logs (UTF-8). The file is overwritten each run.
    """

    package_prefix: str = "mathxlab"
    verbose: bool = False
    log_file: Path | None = None


# ------------------------------------------------------------------------------
class _PrefixAndExactLevelFilter(logging.Filter):
    """Allow records only if the logger name matches a prefix and level matches exactly."""

    def __init__(self, *, prefix: str, levelno: int) -> None:
        super().__init__()
        self._prefix = prefix
        self._levelno = levelno

    @override
    def filter(self, record: logging.LogRecord) -> bool:
        """Return True if the record should be logged."""
        return record.name.startswith(self._prefix) and record.levelno == self._levelno


# ------------------------------------------------------------------------------
def setup_logging(*, config: LoggingConfig | None = None) -> None:
    """Set up logging for experiment runs.

    Design goal:
        - Show INFO+ from all libraries (progress + warnings).
        - Show DEBUG only from *our* code (by logger name prefix).

    This prevents very noisy third-party DEBUG output (e.g. matplotlib/PIL) while still
    allowing you to turn on detailed debugging for the repository code.

    Args:
        config: Logging configuration. If omitted, defaults are used.
    """
    cfg = config or LoggingConfig()

    root = logging.getLogger()
    root.handlers.clear()

    # Let handlers decide what is emitted. We want to allow DEBUG to reach the DEBUG handler.
    root.setLevel(logging.DEBUG)

    fmt = logging.Formatter(
        fmt="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )

    # 1) General handler: INFO+ from everyone
    h_info = logging.StreamHandler(sys.stdout)
    h_info.setLevel(logging.INFO)
    h_info.setFormatter(fmt)
    root.addHandler(h_info)

    # 2) Optional debug handler: DEBUG only from our code
    if cfg.verbose:
        h_dbg = logging.StreamHandler(sys.stdout)
        h_dbg.setLevel(logging.DEBUG)
        h_dbg.setFormatter(fmt)
        h_dbg.addFilter(
            _PrefixAndExactLevelFilter(prefix=cfg.package_prefix, levelno=logging.DEBUG)
        )
        root.addHandler(h_dbg)

    # Optional file logging (same policy)
    if cfg.log_file is not None:
        cfg.log_file.parent.mkdir(parents=True, exist_ok=True)

        fh_info = logging.FileHandler(cfg.log_file, mode="w", encoding="utf-8")
        fh_info.setLevel(logging.INFO)
        fh_info.setFormatter(fmt)
        root.addHandler(fh_info)

        if cfg.verbose:
            fh_dbg = logging.FileHandler(cfg.log_file, mode="a", encoding="utf-8")
            fh_dbg.setLevel(logging.DEBUG)
            fh_dbg.setFormatter(fmt)
            fh_dbg.addFilter(
                _PrefixAndExactLevelFilter(prefix=cfg.package_prefix, levelno=logging.DEBUG)
            )
            root.addHandler(fh_dbg)

    # Keep typical noisy libraries at WARNING+ (defensive). This does not hide warnings/errors.
    for noisy in ("matplotlib", "PIL"):
        logging.getLogger(noisy).setLevel(logging.WARNING)


# ------------------------------------------------------------------------------
def get_logger(name: str) -> logging.Logger:
    """Get a logger for a specific module.

    Args:
        name: Name of the module.

    Returns:
        A logging.Logger instance.
    """
    return logging.getLogger(name)
