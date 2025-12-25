"""E003 — Abundancy index landscape.

This experiment computes the sum-of-divisors function σ(n) for all 1 ≤ n ≤ N using a
divisor-sum sieve, then visualizes the abundancy index:

    I(n) = σ(n) / n.

Perfect numbers satisfy I(n) = 2.

Usage (repository convention):
    make run EXP=e003

Artifacts:
    - figures/fig_01_hist_abundancy.png
    - figures/fig_02_scatter_abundancy.png
    - figures/fig_03_near_2.png
    - params.json
    - report.md
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
        n_max: Upper bound N (inclusive).
        stride_scatter: Downsampling stride for scatter plots.
        bins: Histogram bin count.
        near_band: Band width for "near 2" plot: show points where |I(n)-2| < near_band.
    """

    n_max: int
    stride_scatter: int
    bins: int
    near_band: float


# ------------------------------------------------------------------------------
def sigma_sieve(n_max: int) -> np.ndarray:
    """Compute σ(0..N) via a divisor-sum sieve.

    Args:
        n_max: Upper bound N (inclusive).

    Returns:
        NumPy array sigma of length N+1 with sigma[n] = σ(n).
    """
    if n_max < 1:
        raise ValueError("n_max must be >= 1")

    sigma = np.zeros(n_max + 1, dtype=np.int64)
    # Vectorized slicing: sigma[d::d] += d
    for d in range(1, n_max + 1):
        sigma[d::d] += d
    return sigma


# ------------------------------------------------------------------------------
def _write_report(*, report_path: Path, params: Params, count_perfect: int) -> None:
    """Write a short Markdown report.

    Args:
        report_path: Path to report.md.
        params: Experiment parameters.
        count_perfect: Number of perfect numbers found ≤ N.
    """
    report_md = f"""\
# E003 — Abundancy index landscape

**Reproduce:**

```bash
make run EXP=e003
```

## Parameters

- N: `{params.n_max}`
- scatter stride: `{params.stride_scatter}`
- histogram bins: `{params.bins}`
- near band: `{params.near_band}`

## Outputs

- `figures/fig_01_hist_abundancy.png`
- `figures/fig_02_scatter_abundancy.png`
- `figures/fig_03_near_2.png`
- `params.json`

## Findings

- Perfect numbers found (≤ N): `{count_perfect}`

## Notes

- Compare perfection using integers: σ(n) == 2n.
- For plotting, floats are acceptable, but classification should not depend on float rounding.
"""
    report_path.write_text(report_md, encoding="utf-8")


# ------------------------------------------------------------------------------
def _plot_hist(*, values: np.ndarray, bins: int) -> fig.Figure:
    """Plot a histogram.

    Args:
        values: Values to histogram.
        bins: Number of bins.

    Returns:
        Matplotlib figure.
    """
    fig_obj, ax = plt.subplots()
    ax.hist(values, bins=bins)
    ax.set_title("Histogram of abundancy index I(n) = σ(n)/n")
    ax.set_xlabel("I(n)")
    ax.set_ylabel("count")
    finalize_figure(fig_obj)
    return fig_obj


# ------------------------------------------------------------------------------
def _plot_scatter(*, n: np.ndarray, i_vals: np.ndarray) -> fig.Figure:
    """Scatter plot of I(n) vs n.

    Args:
        n: n values.
        i_vals: I(n) values.

    Returns:
        Matplotlib figure.
    """
    fig_obj, ax = plt.subplots()
    ax.scatter(n, i_vals, s=3)
    ax.set_title("Abundancy index landscape")
    ax.set_xlabel("n")
    ax.set_ylabel("I(n) = σ(n)/n")
    finalize_figure(fig_obj)
    return fig_obj


# ------------------------------------------------------------------------------
def main() -> int:
    """Run the experiment.

    Returns:
        Process exit code (0 for success).
    """
    args = parse_experiment_args(
        experiment_id="e003",
        description="Abundancy index landscape via σ(n)/n",
    )
    setup_logging(config=LoggingConfig(verbose=args.verbose))
    set_global_seed(args.seed)

    params = Params(
        n_max=300_000,
        stride_scatter=10,
        bins=250,
        near_band=0.02,
    )

    out_paths = prepare_out_dir(out_dir=args.out_dir)

    logger.info("Computing sigma sieve up to N=%d", params.n_max)
    sigma = sigma_sieve(params.n_max)

    n = np.arange(1, params.n_max + 1, dtype=np.int64)
    i_vals = sigma[1:] / n.astype(np.float64)

    # Perfect numbers: σ(n) == 2n
    perfect_mask = sigma[1:] == (2 * n)
    count_perfect = int(perfect_mask.sum())
    logger.info("Perfect numbers found up to N=%d: %d", params.n_max, count_perfect)

    fig1 = _plot_hist(values=i_vals, bins=params.bins)
    save_figure(out_dir=out_paths.figures_dir, name="fig_01_hist_abundancy", fig=fig1)

    # Scatter downsampled
    n_s = n[:: params.stride_scatter]
    i_s = i_vals[:: params.stride_scatter]
    fig2 = _plot_scatter(n=n_s, i_vals=i_s)
    save_figure(out_dir=out_paths.figures_dir, name="fig_02_scatter_abundancy", fig=fig2)

    # Near-2 band plot (downsample again for readability)
    near = np.abs(i_vals - 2.0) < params.near_band
    fig3 = _plot_scatter(
        n=n[near][:: max(1, params.stride_scatter)],
        i_vals=i_vals[near][:: max(1, params.stride_scatter)],
    )
    fig3.axes[0].set_title(f"Near misses: |I(n) - 2| < {params.near_band:g}")
    save_figure(out_dir=out_paths.figures_dir, name="fig_03_near_2", fig=fig3)

    write_json(out_paths.params_path, data=asdict(params))
    _write_report(report_path=out_paths.report_path, params=params, count_perfect=count_perfect)

    logger.info("Experiment E003 completed successfully. Artifacts saved to: %s", args.out_dir)
    return 0


# ------------------------------------------------------------------------------
if __name__ == "__main__":
    raise SystemExit(main())
