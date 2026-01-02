"""Utilities for run log file discovery.

The repository's ``make run EXP=e###`` workflow typically prints a log file path
like::

    out/e094/logs/run_e094.log

Depending on how the Makefile is implemented, stdout/stderr may or may not be
redirected to that file. To make experiment logging robust across platforms and
shells, we attempt to *reuse* the freshest ``run_<exp>.log`` file in
``out_dir/logs/`` if it exists, otherwise we create a new one.

This module is intentionally tiny and dependency-free.
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path


# ------------------------------------------------------------------------------
@dataclass(frozen=True, slots=True)
class RunLogDiscovery:
    """Result of run log discovery.

    Attributes:
        log_file: The discovered or newly created log file path.
        was_created: True if the file did not exist and was created by discovery.
    """

    log_file: Path
    was_created: bool


# ------------------------------------------------------------------------------
def infer_run_log_file(*, out_dir: Path, experiment_slug: str) -> RunLogDiscovery:
    """Infer the run log file for an experiment.

    The Makefile convention is a single deterministic log file per experiment::

        out/e094/logs/run_e094.log

    This makes it easy to diff runs and avoids leaking timestamps into filenames.
    The file is created if missing. It may be overwritten by the Makefile (e.g. the
    initial header lines), so experiments should treat it as an *optional* sink.

    Args:
        out_dir: Output directory for the experiment (e.g. ``out/e094``).
        experiment_slug: Experiment slug used by the Makefile (e.g. ``"e094"``).

    Returns:
        A :class:`RunLogDiscovery` with a log file path.
    """
    logs_dir = out_dir / "logs"
    logs_dir.mkdir(parents=True, exist_ok=True)

    slug = experiment_slug.lower()
    path = logs_dir / f"run_{slug}.log"
    if path.exists():
        return RunLogDiscovery(log_file=path, was_created=False)

    path.write_text("", encoding="utf-8")
    return RunLogDiscovery(log_file=path, was_created=True)
