"""Smoke test that executes all experiment entry points.

The goal of this test is to ensure that every experiment module can be executed
end-to-end without raising an exception. This protects the repository against
accidental breakage (import errors, API drift, missing dependencies, etc.).

The test runs the *entry modules* ``mathxlab.experiments.e###`` (not the descriptive
implementation modules). Each experiment is executed with a temporary output
directory and a deterministic seed.

Notes:
    - This test is intentionally integration-like: it executes the full experiment
      stack, including plotting and artifact writing.
    - Experiments should therefore keep default workloads reasonably small.
    - The matplotlib backend is forced to "Agg" so the test works in headless CI.

"""

from __future__ import annotations

import importlib
import re
import sys
from pathlib import Path

import matplotlib
import pytest

# ------------------------------------------------------------------------------
matplotlib.use("Agg", force=True)


# ------------------------------------------------------------------------------
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
        if not path.is_file():
            continue
        if not pattern.match(path.name):
            continue
        module_names.append(f"mathxlab.experiments.{path.stem}")

    # Sort numerically by experiment id.
    module_names.sort(key=lambda s: int(s.rsplit(".", 1)[-1][1:]))
    return module_names


# ------------------------------------------------------------------------------
def _run_experiment(*, module_name: str) -> int:
    """Run a single experiment module by calling its ``main()``.

    Args:
        module_name: Fully-qualified module name (e.g. ``mathxlab.experiments.e001``).

    Returns:
        Exit code returned by the experiment ``main()``.

    Raises:
        AssertionError: If the module has no ``main`` attribute or does not return
            an int exit code.
    """
    module = importlib.import_module(module_name)
    if not hasattr(module, "main"):
        raise AssertionError(f"{module_name} has no 'main' function")

    main = module.main
    result = main()
    if not isinstance(result, int):
        raise AssertionError(f"{module_name}.main() returned non-int: {type(result)!r}")
    return result


# ------------------------------------------------------------------------------
@pytest.mark.slow
def test_run_all_experiments(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    """Run all experiments and fail if any of them crashes.

    Args:
        tmp_path: Pytest temporary directory.
        monkeypatch: Pytest monkeypatch fixture.
    """
    repo_root = Path(__file__).resolve().parent.parent
    modules = _discover_experiment_entry_modules(repo_root=repo_root)
    assert modules, "No experiment entry modules were discovered."

    seed = "1"

    # Defer pyplot import until after the backend is fixed.
    import matplotlib.pyplot as plt

    failures: list[str] = []

    for module_name in modules:
        exp_id = module_name.rsplit(".", 1)[-1]
        out_dir = tmp_path / exp_id

        # Experiments parse standard args from sys.argv.
        monkeypatch.setattr(sys, "argv", [exp_id, "--out", str(out_dir), "--seed", seed])

        try:
            code = _run_experiment(module_name=module_name)
            if code != 0:
                failures.append(f"{exp_id}: exit_code={code}")
        except SystemExit as exc:
            failures.append(f"{exp_id}: SystemExit({exc.code})")
        except Exception as exc:
            failures.append(f"{exp_id}: {exc.__class__.__name__}: {exc}")
        finally:
            plt.close("all")

    assert not failures, "Some experiments failed:\n" + "\n".join(failures)
