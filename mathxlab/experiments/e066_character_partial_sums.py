"""E066 — Character partial sums: cancellation profiles.

For a Dirichlet character χ modulo q, consider partial sums:

    S(N) = ∑_{n=1}^N χ(n)

For "nontrivial" χ one expects substantial cancellation (S(N) grows slowly
compared to N). This experiment computes S(N) for all characters modulo q and
plots:

- max_{N<=Nmax} |S(N)| for each character,
- one example trajectory S(N) (real/imag) for a selected character.

Usage:
    make run EXP=e066

Artifacts:
    - figures/fig_01_max_partial_sums.png
    - figures/fig_02_example_partial_sum.png
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
from mathxlab.nt.dirichlet import all_characters, character_table, euler_phi


# ------------------------------------------------------------------------------
@dataclass(frozen=True)
class Params:
    """Parameters for E066.

    Attributes:
        q: Modulus.
        n_max: Maximum N for partial sums.
        example_index: Which character index to plot as example.
    """

    q: int = 15
    n_max: int = 30_000
    example_index: int = 1


# ------------------------------------------------------------------------------
def _partial_sums_from_table(*, table: np.ndarray, q: int, n_max: int) -> np.ndarray:
    """Compute cumulative sums S(N) for each character using periodicity.

    Args:
        table: Character table (phi(q), q), entries for residues 0..q-1.
        q: Modulus.
        n_max: Maximum N.

    Returns:
        Complex array of shape (phi(q), n_max) with S(N) for N=1..n_max.
    """
    residues = (np.arange(1, n_max + 1) % q).astype(np.int64)
    vals = table[:, residues]  # (phi(q), n_max)
    return np.cumsum(vals, axis=1)


# ------------------------------------------------------------------------------
def _plot_max_abs(*, max_abs: np.ndarray, q: int) -> fig.Figure:
    """Plot max |S(N)| per character index."""
    fig_obj, ax = plt.subplots()
    x = np.arange(len(max_abs))
    ax.bar(x, max_abs)
    ax.set_title(rf"Max partial sums $\max_{{N\leq N_{{\max}}}} |S(N)|$ (q={q})")
    ax.set_xlabel("Character index")
    ax.set_ylabel("Max |S(N)|")
    return fig_obj


# ------------------------------------------------------------------------------
def _plot_example(*, S: np.ndarray, q: int, idx: int) -> fig.Figure:
    """Plot real and imaginary parts of one partial-sum trajectory."""
    fig_obj, ax = plt.subplots()
    n = np.arange(1, S.size + 1)
    ax.plot(n, S.real, label="Re S(N)")
    ax.plot(n, S.imag, label="Im S(N)")
    ax.set_title(rf"Example partial sums $S(N)$ (q={q}, index={idx})")
    ax.set_xlabel("N")
    ax.set_ylabel("Value")
    ax.legend(loc="best")
    return fig_obj


# ------------------------------------------------------------------------------
def main(argv: list[str] | None = None) -> int:
    """Run E066."""
    args = parse_experiment_args(argv=argv)
    params = Params()

    paths = prepare_out_dir(out_dir=Path(args.out_dir))

    table = character_table(params.q)
    S = _partial_sums_from_table(table=table, q=params.q, n_max=params.n_max)
    max_abs = np.max(np.abs(S), axis=1)

    fig1 = _plot_max_abs(max_abs=max_abs, q=params.q)
    save_figure(out_dir=paths.figures_dir, name="fig_01_max_partial_sums", fig=fig1)

    idx = int(np.clip(params.example_index, 0, S.shape[0] - 1))
    fig2 = _plot_example(S=S[idx], q=params.q, idx=idx)
    save_figure(out_dir=paths.figures_dir, name="fig_02_example_partial_sum", fig=fig2)

    lines = [
        "# E066 — Character partial sums",
        "",
        f"- q: {params.q}",
        f"- phi(q): {euler_phi(params.q)}",
        f"- n_max: {params.n_max}",
        f"- max over characters of max|S(N)|: {float(max_abs.max()):.2f}",
        "",
        "Figures:",
        "- fig_01_max_partial_sums.png",
        "- fig_02_example_partial_sum.png",
        "",
        "Notes:",
        "- The principal character typically shows linear growth on units (less cancellation).",
        "- Nontrivial characters usually exhibit strong cancellation (slow growth).",
        "",
    ]

    write_json(paths.params_path, asdict(params))
    write_text(paths.report_path, "\n".join(lines))
    return 0
