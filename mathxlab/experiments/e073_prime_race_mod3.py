"""E073 — Prime race mod 3: pi(x;3,2) vs pi(x;3,1).

Another small prime race compares the two reduced residue classes modulo 3:

    D(x) = π(x;3,2) - π(x;3,1)

Usage:
    make run EXP=e073

Artifacts:
    - figures/fig_01_race_mod3_diff.png
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
from mathxlab.experiments._ap_utils import counts_in_residue_class, sample_grid
from mathxlab.experiments._prime_utils import primes_up_to

# ------------------------------------------------------------------------------
logger = get_logger(__name__)


# ------------------------------------------------------------------------------
@dataclass(frozen=True)
class Params:
    """Parameters for E073."""

    x_max: int = 2_500_000
    n_points: int = 900
    log_grid: bool = True


# ------------------------------------------------------------------------------
def _plot(*, xs: np.ndarray, diff: np.ndarray) -> fig.Figure:
    fig_obj, ax = plt.subplots()
    ax.plot(xs, diff)
    ax.axhline(0.0, linestyle="--", linewidth=1.2)
    ax.set_title(r"Prime race mod 3: $\pi(x;3,2) - \pi(x;3,1)$")
    ax.set_xlabel("x")
    ax.set_ylabel("difference")
    return fig_obj


# ------------------------------------------------------------------------------
def main(argv: list[str] | None = None) -> int:
    """Run E073."""
    args = parse_experiment_args(
        experiment_id="e073",
        description="Prime race mod 3: pi(x;3,2) vs pi(x;3,1).",
        argv=argv,
    )

    setup_logging(config=LoggingConfig(verbose=args.verbose))
    logger.info("Starting experiment E073: Prime race mod 3: pi(x;3,2) vs pi(x;3,1).")
    set_global_seed(args.seed)
    params = Params()
    paths = prepare_out_dir(out_dir=args.out_dir)

    primes = primes_up_to(params.x_max)
    xs = sample_grid(x_max=params.x_max, n=params.n_points, log=params.log_grid)

    pi_1 = counts_in_residue_class(primes=primes, q=3, a=1, xs=xs).astype(np.float64)
    pi_2 = counts_in_residue_class(primes=primes, q=3, a=2, xs=xs).astype(np.float64)
    diff = pi_2 - pi_1

    fig1 = _plot(xs=xs, diff=diff)
    save_figure(out_dir=paths.figures_dir, name="fig_01_race_mod3_diff", fig=fig1)

    lines = [
        "# E073 — Prime race mod 3",
        "",
        f"- x_max: {params.x_max}",
        f"- n_points: {params.n_points}",
        f"- log_grid: {params.log_grid}",
        "",
        "Figure:",
        "- fig_01_race_mod3_diff.png",
        "",
    ]

    write_json(paths.params_path, asdict(params))
    write_text(paths.report_path, "\n".join(lines))
    return 0
