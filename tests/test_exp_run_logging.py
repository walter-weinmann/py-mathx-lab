"""Tests for experiment run log discovery utilities."""

from __future__ import annotations

import os
import time
from pathlib import Path

from mathxlab.exp.run_logging import infer_run_log_file


def _touch(path: Path, *, mtime: float) -> None:
    """Create a file (if missing) and set its modification time.

    Args:
        path: File path.
        mtime: Modification time as UNIX timestamp.
    """
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("", encoding="utf-8")
    os.utime(path, (mtime, mtime))


def test_infer_run_log_file_reuses_newest(tmp_path: Path) -> None:
    """infer_run_log_file should reuse the newest matching run log."""
    out_dir = tmp_path / "out" / "e094"
    logs = out_dir / "logs"
    older = logs / "run_e094_20200101_000000.log"
    newer = logs / "run_e094_20200102_000000.log"
    base = time.time()
    _touch(older, mtime=base - 10.0)
    _touch(newer, mtime=base - 1.0)

    res = infer_run_log_file(out_dir=out_dir, experiment_slug="e094")
    assert res.log_file == newer
    assert res.was_created is False


def test_infer_run_log_file_creates_when_missing(tmp_path: Path) -> None:
    """infer_run_log_file should create a new run log when none exists."""
    out_dir = tmp_path / "out" / "e091"
    res = infer_run_log_file(out_dir=out_dir, experiment_slug="e091")

    assert res.log_file.exists()
    assert res.log_file.parent == out_dir / "logs"
    assert res.log_file.name.startswith("run_e091_")
    assert res.log_file.suffix == ".log"
    assert res.was_created is True
