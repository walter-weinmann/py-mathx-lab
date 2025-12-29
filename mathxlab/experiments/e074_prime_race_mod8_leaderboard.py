"""E074 — Prime race mod 8: leaderboard among 1,3,5,7.

This experiment tracks four residue classes modulo 8:

    a ∈ {1,3,5,7}

and records which class is leading in π(x;8,a) on a sample grid. The output is a
simple "leaderboard" summary and a visualization of leader fractions.

Usage:
    make run EXP=e074

Artifacts:
    - figures/fig_01_leader_fractions.png
    - figures/fig_02_counts_minus_mean.png
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
    """Parameters for E074."""

    x_max: int = 3_000_000
    residues: tuple[int, ...] = (1, 3, 5, 7)
    n_points: int = 1000
    log_grid: bool = True


# ------------------------------------------------------------------------------
def _plot_fractions(*, residues: list[int], fracs: np.ndarray) -> fig.Figure:
    fig_obj, ax = plt.subplots()
    x = np.arange(len(residues))
    ax.bar(x, fracs)
    ax.set_xticks(x, [str(a) for a in residues])
    ax.set_title("Leader fractions on sample grid (mod 8)")
    ax.set_xlabel("Residue class a")
    ax.set_ylabel("fraction of samples leading")
    return fig_obj


# ------------------------------------------------------------------------------
def _plot_centered_counts(*, xs: np.ndarray, counts: dict[int, np.ndarray]) -> fig.Figure:
    fig_obj, ax = plt.subplots()
    Y = np.vstack([counts[a] for a in sorted(counts.keys())]).astype(np.float64)
    mean = Y.mean(axis=0)
    for a in sorted(counts.keys()):
        ax.plot(xs, counts[a] - mean, label=rf"$a={a}$")
    ax.axhline(0.0, linestyle="--", linewidth=1.2)
    ax.set_title(r"Centered counts $\pi(x;8,a) - \mathrm{mean}_a$")
    ax.set_xlabel("x")
    ax.set_ylabel("centered count")
    ax.legend(loc="best")
    return fig_obj


# ------------------------------------------------------------------------------
def main(argv: list[str] | None = None) -> int:
    """Run E074."""
    args = parse_experiment_args(argv=argv)
    params = Params()
    paths = prepare_out_dir(out_dir=Path(args.out_dir))

    primes = primes_up_to(params.x_max)
    xs = sample_grid(x_max=params.x_max, n=params.n_points, log=params.log_grid)

    counts: dict[int, np.ndarray] = {}
    for a in params.residues:
        counts[a] = counts_in_residue_class(primes=primes, q=8, a=a, xs=xs).astype(np.int64)

    # Leader per sample (tie-breaker: smallest residue).
    residues = list(params.residues)
    Y = np.vstack([counts[a] for a in residues])
    leaders = np.argmax(Y, axis=0)  # index into residues
    fracs = np.array([(leaders == i).mean() for i in range(len(residues))], dtype=np.float64)

    fig1 = _plot_fractions(residues=residues, fracs=fracs)
    save_figure(out_dir=paths.figures_dir, name="fig_01_leader_fractions", fig=fig1)

    fig2 = _plot_centered_counts(xs=xs, counts=counts)
    save_figure(out_dir=paths.figures_dir, name="fig_02_counts_minus_mean", fig=fig2)

    lines = [
        "# E074 — Prime race mod 8: leaderboard",
        "",
        f"- x_max: {params.x_max}",
        f"- residues: {list(params.residues)}",
        f"- n_points: {params.n_points}",
        f"- log_grid: {params.log_grid}",
        "",
        "Leader fractions on the sample grid:",
    ]
    for a, frac in zip(residues, fracs, strict=True):
        lines.append(f"- a={a}: {frac:.3f}")
    lines += [
        "",
        "Figures:",
        "- fig_01_leader_fractions.png",
        "- fig_02_counts_minus_mean.png",
        "",
        "Notes:",
        "- This uses a coarse sample grid, so fractions are approximate and depend on sampling.",
        "",
    ]

    write_json(paths.params_path, asdict(params))
    write_text(paths.report_path, "\n".join(lines))
    return 0
