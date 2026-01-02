from __future__ import annotations

import time
from pathlib import Path

from mathxlab.exp.run_logging import infer_run_log_file


def _touch(path: Path, *, mtime: float, content: str = "") -> None:
    """Create a file at *path* with the given mtime and content."""
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")
    os_time = (mtime, mtime)
    # Path.touch() cannot set arbitrary mtime portably; use os.utime.
    import os

    os.utime(path, os_time)


def test_infer_run_log_file_reuses_newest(tmp_path: Path) -> None:
    """infer_run_log_file should reuse the newest matching legacy run log.

    New behavior: migrate the newest legacy log to the deterministic name.
    """
    out_dir = tmp_path / "out" / "e094"
    logs = out_dir / "logs"
    older = logs / "run_e094_20200101_000000.log"
    newer = logs / "run_e094_20200102_000000.log"

    base = time.time()
    _touch(older, mtime=base - 10.0, content="older")
    _touch(newer, mtime=base - 1.0, content="newer")

    res = infer_run_log_file(out_dir=out_dir, experiment_slug="e094")
    canonical = logs / "run_e094.log"

    assert res.log_file == canonical
    assert canonical.exists()
    assert canonical.read_text(encoding="utf-8") == "newer"


def test_infer_run_log_file_creates_when_missing(tmp_path: Path) -> None:
    """infer_run_log_file should create a deterministic run log when none exists."""
    out_dir = tmp_path / "out" / "e091"
    res = infer_run_log_file(out_dir=out_dir, experiment_slug="e091")

    assert res.log_file.exists()
    assert res.log_file.parent == out_dir / "logs"
    assert res.log_file.name == "run_e091.log"
