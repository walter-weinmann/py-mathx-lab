"""Utilities for run log file discovery.

The repository runs experiments via ``make run EXP=e###`` and stores outputs under
``out/e###/``. Each experiment also writes a run log under ``out/e###/logs/``.

This project intentionally uses **deterministic** run log filenames without any
timestamp information:

    ``out/e094/logs/run_e094.log``

To keep compatibility with older runs that produced timestamped filenames like
``run_e094_YYYYMMDD_HHMMSS.log``, discovery will migrate the newest legacy log
to the deterministic name the first time it is called.

This module is intentionally tiny and dependency-free.
"""

from __future__ import annotations

import contextlib
from dataclasses import dataclass
from pathlib import Path
from typing import Final


# ------------------------------------------------------------------------------
@dataclass(frozen=True, slots=True)
class RunLogDiscovery:
    """Result of run log discovery.

    Attributes:
        log_file: The discovered or newly created log file path.
        was_created: True if the deterministic log file did not exist and was created
            (or migrated) by discovery.
    """

    log_file: Path
    was_created: bool


# ------------------------------------------------------------------------------
def infer_run_log_file(*, out_dir: Path, experiment_slug: str) -> RunLogDiscovery:
    """Infer the run log file for an experiment.

    Args:
        out_dir: Output directory for the experiment (e.g. ``out/e094``).
        experiment_slug: Experiment slug used by the Makefile (e.g. ``"e094"``).

    Returns:
        A :class:`RunLogDiscovery` with the deterministic log file path.
    """
    logs_dir = out_dir / "logs"
    logs_dir.mkdir(parents=True, exist_ok=True)

    slug = experiment_slug.lower()
    canonical: Final[Path] = logs_dir / f"run_{slug}.log"

    if canonical.exists():
        return RunLogDiscovery(log_file=canonical, was_created=False)

    # Backward compatibility: migrate the newest timestamped log (if present) to the
    # canonical filename. This preserves the "reuse newest" behavior while keeping
    # future runs timestamp-free.
    legacy_candidates = sorted(
        logs_dir.glob(f"run_{slug}_*.log"),
        key=lambda p: p.stat().st_mtime,
        reverse=True,
    )
    if legacy_candidates:
        newest = legacy_candidates[0]
        try:
            newest.replace(canonical)
        except OSError:
            # Some platforms/filesystems may not allow atomic replace across devices.
            # Fall back to copy + best-effort cleanup.
            data = newest.read_bytes()
            canonical.write_bytes(data)
            with contextlib.suppress(OSError):
                newest.unlink()

        return RunLogDiscovery(log_file=canonical, was_created=True)

    # No existing log files: create an empty deterministic log file.
    canonical.write_text("", encoding="utf-8")
    return RunLogDiscovery(log_file=canonical, was_created=True)
