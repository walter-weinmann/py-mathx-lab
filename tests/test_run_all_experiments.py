"""Smoke test that executes all experiment entry points (one test per experiment).

This test ensures that each entry module ``mathxlab.experiments.e###`` can be
executed end-to-end without raising an exception.

Key design choices:
- Each experiment runs in its own subprocess to avoid shared global state
  (sys.argv, matplotlib globals, logging handlers, module import cache).
- We parameterize so pytest (and pytest-xdist) can run experiments in parallel.
- Stdout/stderr are captured and written to a per-experiment log file on failure.

Notes:
- Matplotlib backend is forced to "Agg" via environment for headless CI.
- The experiment output directory is unique per test (tmp_path/exp_id).
"""

from __future__ import annotations

import os
import re
import subprocess
import sys
from pathlib import Path

import pytest

pytestmark = pytest.mark.slow


def _discover_experiment_entry_modules(*, repo_root: Path) -> list[str]:
    """Discover experiment entry module names in ``mathxlab/experiments``.

    Args:
        repo_root: Repository root (directory containing ``mathxlab/``).

    Returns:
        A sorted list of fully-qualified module names like
        ``mathxlab.experiments.e001``.
    """
    exp_dir = repo_root / "mathxlab" / "experiments"
    pattern = re.compile(r"^e\d{3}\.py$")

    module_names: list[str] = []
    for path in exp_dir.iterdir():
        if path.is_file() and pattern.match(path.name):
            module_names.append(f"mathxlab.experiments.{path.stem}")

    module_names.sort(key=lambda s: int(s.rsplit(".", 1)[-1][1:]))
    return module_names


REPO_ROOT = Path(__file__).resolve().parent.parent
MODULES = _discover_experiment_entry_modules(repo_root=REPO_ROOT)
assert MODULES, "No experiment entry modules were discovered."


@pytest.mark.parametrize("module_name", MODULES)
def test_run_experiment_entrypoint(module_name: str, tmp_path: Path) -> None:
    """Run a single experiment in a subprocess and fail if it crashes.

    Args:
        module_name: Fully-qualified module name (e.g. ``mathxlab.experiments.e001``).
        tmp_path: Pytest temporary directory unique to this test invocation.
    """
    exp_id = module_name.rsplit(".", 1)[-1]
    out_dir = tmp_path / exp_id
    out_dir.mkdir(parents=True, exist_ok=True)

    seed = "1"

    env = os.environ.copy()
    env["MPLBACKEND"] = "Agg"
    # Make Windows console / captured output more robust for Greek letters, etc.
    env.setdefault("PYTHONUTF8", "1")
    env.setdefault("PYTHONIOENCODING", "utf-8")

    cmd = [
        sys.executable,
        "-m",
        module_name,
        "--out",
        str(out_dir),
        "--seed",
        seed,
    ]

    # Useful progress signal even without -s (shown on failure; with -s it shows live)
    print(f"[slow] running {module_name} -> {out_dir}", flush=True)

    completed = subprocess.run(
        cmd,
        env=env,
        cwd=str(REPO_ROOT),
        text=True,
        encoding="utf-8",
        errors="replace",
        capture_output=True,
    )

    if completed.returncode != 0:
        log_path = tmp_path / f"{exp_id}_subprocess.log"
        log_path.write_text(
            "COMMAND:\n"
            + " ".join(cmd)
            + "\n\nSTDOUT:\n"
            + (completed.stdout or "")
            + "\n\nSTDERR:\n"
            + (completed.stderr or ""),
            encoding="utf-8",
        )
        pytest.fail(
            f"{exp_id} failed with exit code {completed.returncode}. "
            f"See log: {log_path}"
        )
