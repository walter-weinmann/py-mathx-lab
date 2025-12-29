"""E078 — Max partial sums across characters.

For each Dirichlet character χ modulo q, define

    M(χ) = max_{1<=N<=Nmax} | ∑_{n<=N} χ(n) |.

This experiment computes M(χ) for all characters modulo q and visualizes their
distribution.

Usage:
    make run EXP=e078

Artifacts:
    - figures/fig_01_max_sums_hist.png
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
from mathxlab.nt.dirichlet import character_table, euler_phi


# ------------------------------------------------------------------------------
@dataclass(frozen=True)
class Params:
    """Parameters for E078."""

    q: int = 20
    n_max: int = 50_000
    bins: int = 40


# ------------------------------------------------------------------------------
def _partial_sums(*, table: np.ndarray, q: int, n_max: int) -> np.ndarray:
    residues = (np.arange(1, n_max + 1) % q).astype(np.int64)
    vals = table[:, residues]
    return np.cumsum(vals, axis=1)


# ------------------------------------------------------------------------------
def _plot_hist(*, M: np.ndarray, q: int, bins: int) -> fig.Figure:
    fig_obj, ax = plt.subplots()
    ax.hist(M, bins=bins)
    ax.set_title(rf"Histogram of $M(\chi)$ for characters mod q={q}")
    ax.set_xlabel(r"$M(\chi)$")
    ax.set_ylabel("count")
    return fig_obj


# ------------------------------------------------------------------------------
def main(argv: list[str] | None = None) -> int:
    """Run E078."""
    args = parse_experiment_args(argv=argv)
    params = Params()
    paths = prepare_out_dir(out_dir=Path(args.out_dir))

    table = character_table(params.q)
    S = _partial_sums(table=table, q=params.q, n_max=params.n_max)
    M = np.max(np.abs(S), axis=1).astype(np.float64)

    fig1 = _plot_hist(M=M, q=params.q, bins=params.bins)
    save_figure(out_dir=paths.figures_dir, name="fig_01_max_sums_hist", fig=fig1)

    lines = [
        "# E078 — Max partial sums across characters",
        "",
        f"- q: {params.q}",
        f"- phi(q): {euler_phi(params.q)}",
        f"- n_max: {params.n_max}",
        f"- mean M(chi): {float(M.mean()):.2f}",
        f"- max M(chi): {float(M.max()):.2f}",
        "",
        "Figure:",
        "- fig_01_max_sums_hist.png",
        "",
    ]

    write_json(paths.params_path, asdict(params))
    write_text(paths.report_path, "\n".join(lines))
    return 0
