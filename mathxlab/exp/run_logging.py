"""Utilities for run log file discovery.

The repository's ``make run EXP=e###`` workflow typically prints a log file path
like::

    out/e094/logs/run_e094_YYYYMMDD_HHMMSS.log

Depending on how the Makefile is implemented, stdout/stderr may or may not be
redirected to that file. To make experiment logging robust across platforms and
shells, we attempt to *reuse* the freshest ``run_<exp>_*.log`` file in
``out_dir/logs/`` if it exists, otherwise we create a new one.

This module is intentionally tiny and dependency-free.
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
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

    Args:
        out_dir: Output directory for the experiment (e.g. ``out/e094``).
        experiment_slug: Experiment slug used by the Makefile (e.g. ``"e094"``).

    Returns:
        A :class:`RunLogDiscovery` with a log file path.
    """
    logs_dir = out_dir / "logs"
    logs_dir.mkdir(parents=True, exist_ok=True)

    slug = experiment_slug.lower()
    candidates = sorted(
        logs_dir.glob(f"run_{slug}_*.log"),
        key=lambda p: p.stat().st_mtime,
        reverse=True,
    )
    if candidates:
        return RunLogDiscovery(log_file=candidates[0], was_created=False)

    stamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    path = logs_dir / f"run_{slug}_{stamp}.log"
    path.write_text("", encoding="utf-8")
    return RunLogDiscovery(log_file=path, was_created=True)
