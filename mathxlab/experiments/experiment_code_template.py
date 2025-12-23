"""EXXX — <Experiment title>.

This module is a template for experiments in **py-mathx-lab**.

Design goals:
    - reproducible runs (seeded, deterministic outputs),
    - readable code (small functions, typed, well documented),
    - useful artifacts (figures/tables + short Markdown report),
    - stable documentation (optional hero image under docs/_static).

Usage (repository convention):
    make run EXP=exxx_<module_name> ARGS="--out out/exxx --seed 1"
"""

from __future__ import annotations

import logging
from dataclasses import asdict, dataclass
from pathlib import Path

import matplotlib.figure as fig
import matplotlib.pyplot as plt
import numpy as np

from mathxlab.exp.cli import parse_experiment_args
from mathxlab.exp.io import prepare_out_dir, save_figure, write_json
from mathxlab.exp.logging import get_logger, setup_logging
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
        n: Example integer parameter.
        x_min: Minimum x-value (if applicable).
        x_max: Maximum x-value (if applicable).
        num_points: Number of sample points for a grid (if applicable).
    """

    seed: int
    n: int
    x_min: float
    x_max: float
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
make run EXP=exxx_<module_name> ARGS="--out out/exxx --seed {params.seed}"
```

## Parameters

- seed: `{params.seed}`
- n: `{params.n}`
- domain: `[{params.x_min}, {params.x_max}]`
- num_points: `{params.num_points}`

## Outputs

- `figures/fig_01_*.png`
- `params.json`
- `report.md`

## Notes

- Add 3-8 sentences describing what you observed in this run.
"""

    report_path.write_text(report_md, encoding="utf-8")


# ------------------------------------------------------------------------------
def _make_grid(params: Params) -> np.ndarray:
    """Create a stable evaluation grid.

    Args:
        params: Experiment parameters.

    Returns:
        A 1D grid of x-values.
    """

    return np.linspace(params.x_min, params.x_max, params.num_points, dtype=np.float64)


# ------------------------------------------------------------------------------
def _plot_example(*, x: np.ndarray) -> fig.Figure:
    """Create a simple figure (template).

    Args:
        x: Evaluation grid.

    Returns:
        A Matplotlib figure.
    """

    fig_obj, ax = plt.subplots()
    ax.plot(x, np.sin(x), label="sin(x)")
    ax.set_title("EXXX — template figure")
    ax.set_xlabel("x")
    ax.set_ylabel("y")
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

    setup_logging(
        level=logging.DEBUG if args.verbose else logging.INFO,
    )

    logger.info("Starting experiment EXXX")

    params = Params(
        seed=args.seed,
        n=1000,
        x_min=-6.0,
        x_max=6.0,
        num_points=2000,
    )

    set_global_seed(params.seed)

    out_paths = prepare_out_dir(out_dir=args.out_dir)

    logger.debug("Creating grid with %d points", params.num_points)
    x = _make_grid(params)

    logger.debug("Generating example plot")
    fig_obj = _plot_example(x=x)
    save_figure(out_dir=out_paths.figures_dir, name="fig_01_template", fig=fig_obj)

    write_json(out_paths.params_path, data=asdict(params))
    _write_report(report_path=out_paths.report_path, params=params)

    logger.info("Experiment EXXX completed successfully. Artifacts saved to: %s", args.out_dir)

    return 0


# ------------------------------------------------------------------------------
if __name__ == "__main__":
    raise SystemExit(main())
