"""CLI smoke tests for experiments that accept a --size parameter."""

from __future__ import annotations

import importlib
import sys
from pathlib import Path

import matplotlib
import pytest

# ------------------------------------------------------------------------------
matplotlib.use("Agg", force=True)


# ------------------------------------------------------------------------------
def _run_entry_module(*, module_name: str) -> int:
    """Import an experiment entry module and call its main() function.

    Args:
        module_name: Fully-qualified module name, e.g. ``mathxlab.experiments.e024``.

    Returns:
        Exit code returned by the experiment's ``main()`` function.
    """
    mod = importlib.import_module(module_name)
    main = mod.main
    return int(main())


# ------------------------------------------------------------------------------
def test_experiments_accept_size_flag(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    """Experiments that expose --size should run successfully with small sizes.

    This test ensures that:
      - the CLI parser accepts ``--size``,
      - the experiment executes end-to-end,
      - artifacts are written to the chosen output directory.

    Args:
        tmp_path: Pytest temporary directory.
        monkeypatch: Pytest monkeypatch fixture.
    """
    # Defer pyplot import until after the backend is fixed.
    import matplotlib.pyplot as plt

    experiments = ("e024", "e124", "e125", "e126")
    for exp_id in experiments:
        out_dir = tmp_path / exp_id
        monkeypatch.setattr(
            sys,
            "argv",
            [exp_id, "--out", str(out_dir), "--seed", "1", "--size", "101"],
        )

        try:
            code = _run_entry_module(module_name=f"mathxlab.experiments.{exp_id}")
            assert code == 0
            assert out_dir.exists()
            assert (out_dir / "figures").exists()
            assert (out_dir / "report.md").exists()
            assert (out_dir / "params.json").exists()
        finally:
            plt.close("all")
