r"""EXXX — <Experiment title>.

This module is the **implementation** for an experiment in **py-mathx-lab**.

Repository convention:
    - Stable entry module: `mathxlab/experiments/exxx.py` (imports and runs `main`)
    - Descriptive implementation module: `mathxlab/experiments/exxx_<slug>.py` (this file)

Design goals:
    - reproducible runs (seeded, deterministic outputs),
    - readable code (small functions, typed, well documented),
    - useful artifacts (figures/tables + short Markdown report),
    - stable documentation (optional hero image under docs/_static).

Figure math (portable):
    Use Matplotlib *mathtext* in labels/titles, e.g. r"$F_n = 2^{2^n}+1$".
    Avoid LaTeX-only macros like ``\pmod``; prefer ``(\mathrm{mod}\ n)``.

Usage (repository convention):
    make run EXP=exxx

Notes on LaTeX in figures:
    Matplotlib uses *mathtext* (a LaTeX-like subset) in most environments.
    Prefer simple symbols such as ``\varphi``, ``\mu``, ``\sigma`` and avoid
    commands that require full LaTeX (e.g., ``\text{...}``, ``\pmod``).

"""

from __future__ import annotations

from dataclasses import asdict, dataclass
from pathlib import Path

import matplotlib.figure as fig
import matplotlib.pyplot as plt
import numpy as np

from mathxlab.exp.cli import parse_experiment_args
from mathxlab.exp.io import prepare_out_dir, save_figure, write_json
from mathxlab.exp.logging import LoggingConfig, get_logger, setup_logging
from mathxlab.exp.random import set_global_seed
from mathxlab.plots.helpers import finalize_figure

# ------------------------------------------------------------------------------
logger = get_logger(__name__)


# ------------------------------------------------------------------------------
@dataclass(frozen=True, slots=True)
class Params:
    """Experiment parameters.

    Args:
        seed: Random seed for reproducibility.
        n_max: Upper bound for an integer range (inclusive).
        num_points: Number of grid points for a plot (if applicable).
    """

    seed: int
    n_max: int
    num_points: int


# ------------------------------------------------------------------------------
def _write_report(*, report_path: Path, params: Params) -> None:
    """Write a short Markdown report.

    Args:
        report_path: Path to the report file to write.
        params: Parameters used for this run.
    """
    report_md = f"""\
# EXXX — <Experiment title>

**Reproduce:**

```bash
make run EXP=exxx ARGS="--out out/exxx --seed {params.seed}"
```

## Parameters

- seed: `{params.seed}`
- n_max: `{params.n_max}`
- num_points: `{params.num_points}`

## Outputs

- `figures/fig_01_*.png`
- `params.json`
- `report.md`

## Notes

- Add 3–8 sentences describing what you observed in this run.
- Mention any surprising behavior, numerical caveats, or limitations.
"""
    report_path.write_text(report_md, encoding="utf-8")


# ------------------------------------------------------------------------------
def _make_grid(*, params: Params) -> np.ndarray:
    """Create a stable evaluation grid.

    Args:
        params: Experiment parameters.

    Returns:
        A 1D grid of x-values.
    """
    return np.linspace(0.0, 1.0, params.num_points, dtype=np.float64)


# ------------------------------------------------------------------------------
def _plot_example(*, x: np.ndarray) -> fig.Figure:
    """Create a simple figure (template).

    Args:
        x: Evaluation grid.

    Returns:
        A Matplotlib figure.
    """
    fig_obj, ax = plt.subplots()
    ax.plot(x, np.sin(2.0 * np.pi * x), label=r"$\sin(2\pi x)$")
    ax.set_title("EXXX — template figure")
    ax.set_xlabel(r"$x$")
    ax.set_ylabel(r"$y$")
    ax.legend(loc="best")
    finalize_figure(fig_obj)
    return fig_obj


# ------------------------------------------------------------------------------
def main() -> int:
    """Run the experiment.

    Returns:
        Process exit code (0 for success).
    """
    args = parse_experiment_args(
        experiment_id="exxx",
        description="<Experiment title>",
    )

    setup_logging(config=LoggingConfig(verbose=args.verbose))

    logger.info("Starting experiment EXXX")

    params = Params(
        seed=args.seed,
        n_max=50_000,
        num_points=1_000,
    )

    set_global_seed(params.seed)

    run_paths = prepare_out_dir(out_dir=args.out_dir)

    logger.debug("Creating grid with %d points", params.num_points)
    x = _make_grid(params=params)

    logger.debug("Generating example plot")
    fig_obj = _plot_example(x=x)
    save_figure(out_dir=run_paths.figures_dir, name="fig_01_template", fig=fig_obj)

    write_json(run_paths.params_path, data=asdict(params))
    _write_report(report_path=run_paths.report_path, params=params)

    logger.info("Experiment EXXX completed successfully. Artifacts saved to: %s", run_paths.root)

    return 0


# ------------------------------------------------------------------------------
if __name__ == "__main__":
    raise SystemExit(main())
