r"""E001 — Taylor error landscapes for sin(x).

This module runs an experiment that visualizes how Taylor polynomial approximations of
:math:`\sin(x)` behave across a fixed domain when varying:

* the Taylor polynomial degree, and
* the expansion center: math:`x_0`.

The experiment produces a small set of figures and a short Markdown report in the experiment output
directory.

Usage (repository convention):
    make run EXP=e001_taylor_error_landscapes

Notes:
    This is intentionally a minimal “warm-up” experiment. It focuses on reproducibility and readability,
    not on optimizing performance or exhaustively exploring approximation theory.
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
from mathxlab.num.series import taylor_sin
from mathxlab.plots.helpers import finalize_figure


# ------------------------------------------------------------------------------
logger = get_logger(__name__)


# ------------------------------------------------------------------------------
@dataclass(frozen=True, slots=True)
class Params:
    """Experiment parameters.

    Args:
        x_min: Minimum x-value of the evaluation domain.
        x_max: Maximum x-value of the evaluation domain.
        num_points: Number of sample points in the evaluation grid.
        degrees: Taylor polynomial degrees to plot.
        centers: Taylor expansion centers :math:`x_0` to plot.
    """

    x_min: float
    x_max: float
    num_points: int
    degrees: tuple[int, ...]
    centers: tuple[float, ...]


# ------------------------------------------------------------------------------
def _linspace(params: Params) -> np.ndarray:
    """Create the evaluation grid.

    Args:
        params: Experiment parameters.

    Returns:
        A 1D NumPy array of x-values.
    """

    return np.linspace(params.x_min, params.x_max, params.num_points, dtype=np.float64)


# ------------------------------------------------------------------------------
def _write_report(*, report_path: Path, params: Params, seed: int) -> None:
    """Write a short Markdown report.

    Args:
        report_path: Path to the report file.
        params: Experiment parameters.
        seed: Random seed used for this run.
    """

    degrees_str = ", ".join(str(d) for d in params.degrees)
    centers_str = ", ".join(f"{c:g}" for c in params.centers)

    report_md = f"""    # E001 — Taylor error landscapes for sin(x)

**Reproduce:**

```bash
make run EXP=e001_taylor_error_landscapes
```

**Seed:** `{seed}`

## Parameters

- Domain: `[x_min, x_max] = [{params.x_min}, {params.x_max}]`
- num_points: `{params.num_points}`
- degrees: `{degrees_str}`
- centers: `{centers_str}`

## What this run produces

- `figures/fig_01_sin_and_taylor_center_*.png` — overlay of sin(x) and Taylor polynomials for one center
- `figures/fig_02_error_landscape_center_*.png` — absolute error curves for each center, overlaid by degree

## Notes

- Taylor approximations are *local*: accuracy is highest near the expansion center and generally degrades away from it.
- If you increase degrees or the domain size, floating-point roundoff may become visible.
"""

    report_path.write_text(report_md, encoding="utf-8")


# ------------------------------------------------------------------------------
def _plot_overlay(
    *, x: np.ndarray, y_true: np.ndarray, params: Params, center: float
) -> fig.Figure:
    """Plot sin(x) together with Taylor approximations for one center.

    Args:
        x: Evaluation grid.
        y_true: True values sin(x).
        params: Experiment parameters.
        center: Expansion center x0.

    Returns:
        A Matplotlib figure.
    """

    fig_obj, ax = plt.subplots()

    ax.plot(x, y_true, label="sin(x)")
    for d in params.degrees:
        y_hat = taylor_sin(x=x, x0=center, degree=d)
        ax.plot(x, y_hat, label=f"T_{d} around x0={center:g}")

    ax.set_title(f"sin(x) and Taylor polynomials around x0={center:g}")
    ax.set_xlabel("x")
    ax.set_ylabel("y")
    ax.legend(loc="best")
    finalize_figure(fig_obj)
    return fig_obj


# ------------------------------------------------------------------------------
def _plot_error_landscape(
    *, x: np.ndarray, y_true: np.ndarray, params: Params, center: float
) -> fig.Figure:
    """Plot absolute error curves for a fixed center and multiple degrees.

    Args:
        x: Evaluation grid.
        y_true: True values sin(x).
        params: Experiment parameters.
        center: Expansion center x0.

    Returns:
        A Matplotlib figure.
    """

    fig_obj, ax = plt.subplots()

    for d in params.degrees:
        y_hat = taylor_sin(x=x, x0=center, degree=d)
        err = np.abs(y_true - y_hat)
        ax.plot(x, err, label=f"degree={d}")

    ax.set_title(f"Absolute error |sin(x) - T_n(x)| around x0={center:g}")
    ax.set_xlabel("x")
    ax.set_ylabel("absolute error")
    ax.set_yscale("log")
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
        experiment_id="e001",
        description="Taylor error landscapes for sin(x)",
    )

    setup_logging(config=LoggingConfig(verbose=args.verbose))

    logger.info("Starting experiment E001: Taylor error landscapes")

    set_global_seed(args.seed)

    params = Params(
        x_min=-6.0,
        x_max=6.0,
        num_points=4000,
        degrees=(1, 3, 5, 9, 15),
        centers=(0.0, 1.0, 2.0),
    )

    out_paths = prepare_out_dir(out_dir=args.out_dir)

    logger.debug("Creating grid with %d points", params.num_points)
    x = _linspace(params)
    y_true = np.sin(x)

    # 1) Overlay plot for the first center (a readable “anchor” figure).
    overlay_center = params.centers[0]
    logger.info("Generating overlay plot for center x0=%g", overlay_center)
    fig_obj = _plot_overlay(x=x, y_true=y_true, params=params, center=overlay_center)
    save_figure(
        out_dir=out_paths.figures_dir,
        name=f"fig_01_sin_and_taylor_center_{overlay_center:g}",
        fig=fig_obj,
    )

    # 2) Error landscapes for all centers.
    for center in params.centers:
        logger.info("Generating error landscape for center x0=%g", center)
        fig_obj = _plot_error_landscape(x=x, y_true=y_true, params=params, center=center)
        save_figure(
            out_dir=out_paths.figures_dir,
            name=f"fig_02_error_landscape_center_{center:g}",
            fig=fig_obj,
        )

    write_json(out_paths.params_path, data=asdict(params))
    _write_report(report_path=out_paths.report_path, params=params, seed=args.seed)

    logger.info("Experiment E001 completed successfully. Artifacts saved to: %s", args.out_dir)

    return 0


# ------------------------------------------------------------------------------
if __name__ == "__main__":
    raise SystemExit(main())
