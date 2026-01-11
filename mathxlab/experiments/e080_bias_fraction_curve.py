"""E080: Chebyshev bias: leader fraction vs x.

For the mod 4 race D(x)=π(x;4,3)-π(x;4,1), define the empirical leader fraction:

    F(x_k) = #{i <= k : D(x_i) > 0} / k

for a chosen increasing sample grid {x_i}. This gives a simple "bias curve".

Usage:
    make run EXP=e080

Artifacts:
    - figures/fig_01_bias_fraction.png
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
from mathxlab.experiments._ap_utils import counts_in_residue_class, sample_grid
from mathxlab.experiments._prime_utils import primes_up_to

# ------------------------------------------------------------------------------
logger = get_logger(__name__)


# ------------------------------------------------------------------------------
@dataclass(frozen=True)
class Params:
    """Parameters for E080."""

    x_max: int = 12_000_000
    n_points: int = 4000


# ------------------------------------------------------------------------------
def _plot(*, xs: np.ndarray, frac: np.ndarray) -> fig.Figure:
    fig_obj, ax = plt.subplots()
    ax.plot(xs, frac)
    ax.set_title(r"Leader fraction for mod 4 race (D(x)>0) on log-grid")
    ax.set_xlabel("x")
    ax.set_ylabel("fraction")
    ax.set_ylim(0.0, 1.0)
    ax.axhline(0.5, linestyle="--", linewidth=1.2)
    return fig_obj


# ------------------------------------------------------------------------------
def main(argv: list[str] | None = None) -> int:
    """Run E080."""
    args = parse_experiment_args(
        experiment_id="e080",
        description="Chebyshev bias: leader fraction vs x.",
        argv=argv,
    )

    run_log = infer_run_log_file(out_dir=args.out_dir, experiment_slug="e080")
    setup_logging(config=LoggingConfig(verbose=args.verbose, log_file=run_log.log_file))
    logger.info("Starting experiment E080: Chebyshev bias: leader fraction vs x.")
    set_global_seed(args.seed)
    params = Params()
    paths = prepare_out_dir(out_dir=args.out_dir)

    primes = primes_up_to(params.x_max)
    xs = sample_grid(x_max=params.x_max, n=params.n_points, log=True)

    pi_1 = counts_in_residue_class(primes=primes, q=4, a=1, xs=xs).astype(np.int64)
    pi_3 = counts_in_residue_class(primes=primes, q=4, a=3, xs=xs).astype(np.int64)
    diff = (pi_3 - pi_1).astype(np.int64)

    pos = (diff > 0).astype(np.int64)
    frac = np.cumsum(pos) / np.arange(1, pos.size + 1)

    fig1 = _plot(xs=xs, frac=frac)
    save_figure(out_dir=paths.figures_dir, name="fig_01_bias_fraction", fig=fig1)

    lines = [
        "# E080: Chebyshev bias fraction curve",
        "",
        f"- x_max: {params.x_max}",
        f"- n_points: {params.n_points}",
        f"- final fraction (D>0): {float(frac[-1]):.3f}",
        "",
        "Figure:",
        "- fig_01_bias_fraction.png",
        "",
        "Notes:",
        "- This is sample-grid dependent; it is a qualitative bias indicator, not a rigorous density.",
        "",
    ]

    write_json(paths.params_path, asdict(params))
    write_text(paths.report_path, "\n".join(lines))
    return 0
