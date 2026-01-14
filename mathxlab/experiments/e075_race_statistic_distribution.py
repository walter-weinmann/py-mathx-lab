"""E075: Prime race statistic: distribution on a log-grid.

For a prime race difference D(x), a common heuristic normalization is:

    Z(x) = D(x) * log(x) / sqrt(x)

This experiment samples x on a log grid and plots a histogram of Z(x) for the
mod 4 race:

    D(x) = π(x;4,3) - π(x;4,1)

Usage:
    make run EXP=e075

Artifacts:
    - figures/fig_01_statistic_hist.png
    - params.json
    - report.md
"""

from __future__ import annotations

from dataclasses import asdict, dataclass

import matplotlib.figure as fig
import matplotlib.pyplot as plt
import numpy as np

from mathxlab.exp.cli import parse_experiment_args
from mathxlab.exp.io import prepare_out_dir, save_figure, write_json, write_text
from mathxlab.exp.logging import LoggingConfig, get_logger, setup_logging
from mathxlab.exp.random import set_global_seed
from mathxlab.exp.run_logging import infer_run_log_file
from mathxlab.experiments._ap_utils import (
    counts_in_residue_class,
    normalized_race_statistic,
    sample_grid,
)
from mathxlab.experiments._prime_utils import primes_up_to

# ------------------------------------------------------------------------------
logger = get_logger(__name__)


# ------------------------------------------------------------------------------
@dataclass(frozen=True)
class Params:
    """Parameters for E075."""

    x_max: int = 8_000_000
    n_points: int = 2000
    bins: int = 60


# ------------------------------------------------------------------------------
def _plot_hist(*, z: np.ndarray, bins: int) -> fig.Figure:
    fig_obj, ax = plt.subplots()
    ax.hist(z, bins=bins)
    ax.set_title(r"Histogram of $Z(x)=D(x)\log x/\sqrt{x}$ for mod 4 race")
    ax.set_xlabel("Z(x)")
    ax.set_ylabel("count")
    return fig_obj


# ------------------------------------------------------------------------------
def main(argv: list[str] | None = None) -> int:
    """Run E075."""
    args = parse_experiment_args(
        experiment_id="e075",
        description="Prime race statistic: distribution on a log-grid.",
        argv=argv,
    )

    run_log = infer_run_log_file(out_dir=args.out_dir, experiment_slug="e075")
    setup_logging(config=LoggingConfig(verbose=args.verbose, log_file=run_log.log_file))
    logger.info("Starting experiment E075: Prime race statistic: distribution on a log-grid.")
    set_global_seed(args.seed)
    params = Params()
    paths = prepare_out_dir(out_dir=args.out_dir)

    primes = primes_up_to(params.x_max)
    xs = sample_grid(x_max=params.x_max, n=params.n_points, log=True)

    pi_1 = counts_in_residue_class(primes=primes, q=4, a=1, xs=xs).astype(np.float64)
    pi_3 = counts_in_residue_class(primes=primes, q=4, a=3, xs=xs).astype(np.float64)
    diff = pi_3 - pi_1
    z = normalized_race_statistic(xs=xs, diff=diff)

    fig1 = _plot_hist(z=z, bins=params.bins)
    save_figure(out_dir=paths.figures_dir, name="fig_01_statistic_hist", fig=fig1)

    lines = [
        "# E075: Prime race statistic distribution",
        "",
        f"- x_max: {params.x_max}",
        f"- n_points: {params.n_points}",
        f"- bins: {params.bins}",
        f"- mean(Z): {float(np.mean(z)):.3f}",
        f"- std(Z): {float(np.std(z)):.3f}",
        "",
        "Figure:",
        "- fig_01_statistic_hist.png",
        "",
    ]

    write_json(paths.params_path, asdict(params))
    write_text(paths.report_path, "\n".join(lines))
    return 0
