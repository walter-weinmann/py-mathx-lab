"""Smoke tests for experiment entry points.

This suite executes each experiment entry module ``mathxlab.experiments.e###`` as if it
were run via ``python -m ...``. The goal is to catch import errors, CLI drift, and
runtime crashes early.

Why the entry module?
    We intentionally execute the small wrapper module (``e###.py``) instead of the
    implementation module so we also test the public "run as module" contract.

Parallel execution:
    Each experiment is an independent pytest test case, so the slow suite can be
    distributed across workers with ``pytest-xdist`` (e.g. ``-n auto``) while still
    collecting coverage, because everything runs in-process inside the worker.

Notes:
    - The matplotlib backend is forced to "Agg" so the tests work in headless CI.
    - Experiments should keep default workloads reasonably small.
"""

from __future__ import annotations

import os
import re
import runpy
import sys
from pathlib import Path

import pytest

# Force a non-interactive matplotlib backend as early as possible.
os.environ.setdefault("MPLBACKEND", "Agg")

import matplotlib.pyplot as plt


def _discover_experiment_entry_modules(*, repo_root: Path) -> list[str]:
    """Discover entry modules ``mathxlab.experiments.e###``.

    Args:
        repo_root: Repository root (directory containing ``mathxlab/``).

    Returns:
        Sorted list of fully-qualified module names like ``mathxlab.experiments.e001``.
    """
    exp_dir = repo_root / "mathxlab" / "experiments"
    pattern = re.compile(r"^e\d{3}\.py$")

    module_names: list[str] = []
    for path in exp_dir.iterdir():
        if path.is_file() and pattern.match(path.name):
            module_names.append(f"mathxlab.experiments.{path.stem}")

    # Sort numerically by experiment id.
    module_names.sort(key=lambda s: int(s.rsplit(".", 1)[-1][1:]))
    return module_names


def _run_entry_module(*, module_name: str, argv: list[str]) -> int:
    """Run an entry module as ``__main__`` with a controlled argv.

    Args:
        module_name: Fully-qualified module name (e.g. ``mathxlab.experiments.e001``).
        argv: argv to install into ``sys.argv`` during execution.

    Returns:
        The integer exit code (0 means success).

    Raises:
        AssertionError: If the module exits with a non-integer, non-zero code.
    """
    old_argv = sys.argv[:]
    try:
        sys.argv = argv
        try:
            runpy.run_module(module_name, run_name="__main__", alter_sys=True)
        except SystemExit as exc:
            code = exc.code
            if code is None:
                return 0
            if isinstance(code, int):
                return code
            # argparse sometimes uses strings for exit codes; treat them as failure.
            raise AssertionError(f"{module_name} exited with non-int code: {code!r}") from exc
        return 0
    finally:
        sys.argv = old_argv


_REPO_ROOT = Path(__file__).resolve().parent.parent
_EXPERIMENT_MODULES = _discover_experiment_entry_modules(repo_root=_REPO_ROOT)


@pytest.mark.slow
@pytest.mark.parametrize(
    "module_name",
    _EXPERIMENT_MODULES,
    ids=lambda m: m.rsplit(".", 1)[-1],
)
def test_run_experiment_entrypoint(module_name: str, tmp_path: Path) -> None:
    """Execute a single experiment entrypoint with a temporary output directory.

    Args:
        module_name: Experiment entry module (``mathxlab.experiments.e###``).
        tmp_path: Pytest temporary directory.
    """
    exp_id = module_name.rsplit(".", 1)[-1]
    out_dir = tmp_path / exp_id
    seed = "1"

    exit_code = _run_entry_module(
        module_name=module_name,
        argv=[exp_id, "--out", str(out_dir), "--seed", seed],
    )
    try:
        assert exit_code == 0, f"{module_name} returned exit_code={exit_code}"
    finally:
        # Each experiment may create figures; close them to avoid state bleed.
        plt.close("all")


def test_experiment_discovery_is_nonempty() -> None:
    """Sanity check: ensure we discover at least one experiment."""
    assert _EXPERIMENT_MODULES, "No experiment entry modules were discovered."
