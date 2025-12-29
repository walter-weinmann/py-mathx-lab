"""E072 — Prime race mod 4: pi(x;4,3) vs pi(x;4,1).

A classical "prime race" compares how often one residue class leads another in
prime counts. The most famous is mod 4:

    D(x) = π(x;4,3) - π(x;4,1)

Empirically, D(x) is often positive for moderate x (Chebyshev's bias), but it
does change sign infinitely often (Littlewood).

This experiment computes D(x) on a sample grid and plots it.

Usage:
    make run EXP=e072

Artifacts:
    - figures/fig_01_race_mod4_diff.png
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
from mathxlab.exp.io import prepare_out_dir, save_figure, write_json, write_text
from mathxlab.experiments._prime_utils import primes_up_to
from mathxlab.experiments._ap_utils import counts_in_residue_class, sample_grid


# ------------------------------------------------------------------------------
@dataclass(frozen=True)
class Params:
    """Parameters for E072."""

    x_max: int = 2_500_000
    n_points: int = 900
    log_grid: bool = True


# ------------------------------------------------------------------------------
def _plot(*, xs: np.ndarray, diff: np.ndarray) -> fig.Figure:
    """Plot D(x) over the sample grid."""
    fig_obj, ax = plt.subplots()
    ax.plot(xs, diff)
    ax.axhline(0.0, linestyle="--", linewidth=1.2)
    ax.set_title(r"Prime race mod 4: $\pi(x;4,3) - \pi(x;4,1)$")
    ax.set_xlabel("x")
    ax.set_ylabel("difference")
    return fig_obj


# ------------------------------------------------------------------------------
def _count_sign_changes(y: np.ndarray) -> int:
    """Count sign changes ignoring zeros."""
    s = np.sign(y)
    s = s[s != 0]
    if s.size <= 1:
        return 0
    return int(np.sum(s[1:] != s[:-1]))


# ------------------------------------------------------------------------------
def main(argv: list[str] | None = None) -> int:
    """Run E072."""
    args = parse_experiment_args(argv=argv)
    params = Params()
    paths = prepare_out_dir(out_dir=Path(args.out_dir))

    primes = primes_up_to(params.x_max)
    xs = sample_grid(x_max=params.x_max, n=params.n_points, log=params.log_grid)

    pi_1 = counts_in_residue_class(primes=primes, q=4, a=1, xs=xs).astype(np.float64)
    pi_3 = counts_in_residue_class(primes=primes, q=4, a=3, xs=xs).astype(np.float64)
    diff = pi_3 - pi_1

    fig1 = _plot(xs=xs, diff=diff)
    save_figure(out_dir=paths.figures_dir, name="fig_01_race_mod4_diff", fig=fig1)

    n_changes = _count_sign_changes(diff)
    lines = [
        "# E072 — Prime race mod 4",
        "",
        f"- x_max: {params.x_max}",
        f"- n_points: {params.n_points}",
        f"- log_grid: {params.log_grid}",
        f"- sign changes on sample grid: {n_changes}",
        "",
        "Figure:",
        "- fig_01_race_mod4_diff.png",
        "",
        "Notes:",
        "- The sample grid is not dense enough to capture every sign change; it gives a qualitative picture.",
        "",
    ]

    write_json(paths.params_path, asdict(params))
    write_text(paths.report_path, "\n".join(lines))
    return 0
