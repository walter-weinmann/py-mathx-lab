"""E069: L(1,χ): slow convergence and smoothing.

At s=1, the Dirichlet series for L(1,χ) converges very slowly. For the
nontrivial character modulo 4:

    χ(n) = 0 if n even
           1 if n ≡ 1 (mod 4)
          -1 if n ≡ 3 (mod 4)

we have the classical identity:

    L(1,χ) = 1 - 1/3 + 1/5 - 1/7 + ... = π/4.

This experiment shows:
- the raw partial sums up to n_max,
- a simple exponentially-smoothed variant that stabilizes earlier.

Usage:
    make run EXP=e069

Artifacts:
    - figures/fig_01_l1_partial_sums.png
    - figures/fig_02_l1_smoothed.png
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
from mathxlab.nt.dirichlet import DirichletCharacter, all_characters

# ------------------------------------------------------------------------------
logger = get_logger(__name__)


# ------------------------------------------------------------------------------
@dataclass(frozen=True)
class Params:
    """Parameters for E069.

    Attributes:
        q: Modulus (default 4 for the alternating odd harmonic series).
        n_max: Maximum cutoff for raw partial sums.
        smooth_scales: A few smoothing scales N (in exp(-n/N)).
    """

    q: int = 4
    n_max: int = 300_000
    smooth_scales: tuple[int, ...] = (2_000, 8_000, 32_000)


# ------------------------------------------------------------------------------
def _raw_partial_sums(*, chi: DirichletCharacter, n_max: int) -> np.ndarray:
    """Compute partial sums ∑_{n<=N} χ(n)/n for N=1..n_max."""
    n = np.arange(1, n_max + 1, dtype=np.float64)
    chi_vals = np.array([chi(int(k)) for k in n], dtype=np.complex128)
    terms = chi_vals / n
    return np.cumsum(terms).astype(np.complex128)


# ------------------------------------------------------------------------------
def _smoothed_sum(*, chi: DirichletCharacter, N: int, n_max: int) -> complex:
    """Compute ∑_{n<=n_max} χ(n)/n * exp(-n/N)."""
    n = np.arange(1, n_max + 1, dtype=np.float64)
    chi_vals = np.array([chi(int(k)) for k in n], dtype=np.complex128)
    w = np.exp(-n / float(N))
    return complex(np.sum((chi_vals / n) * w))


# ------------------------------------------------------------------------------
def _plot_raw(*, S: np.ndarray) -> fig.Figure:
    """Plot raw partial sums."""
    fig_obj, ax = plt.subplots()
    n = np.arange(1, S.size + 1)
    ax.plot(n, S.real, label="partial sum (real)")
    ax.axhline(np.pi / 4.0, linestyle="--", linewidth=1.5, label=r"$\pi/4$")
    ax.set_title(r"Raw partial sums for $L(1,\chi_4)$")
    ax.set_xlabel("N")
    ax.set_ylabel("Value")
    ax.legend(loc="best")
    return fig_obj


# ------------------------------------------------------------------------------
def _plot_smoothed(*, scales: list[int], vals: list[complex]) -> fig.Figure:
    """Plot smoothed approximations vs smoothing scale."""
    fig_obj, ax = plt.subplots()
    x = np.array(scales, dtype=np.float64)
    y = np.array([v.real for v in vals], dtype=np.float64)
    ax.plot(x, y, marker="o")
    ax.axhline(np.pi / 4.0, linestyle="--", linewidth=1.5, label=r"$\pi/4$")
    ax.set_title(r"Exponentially smoothed approximations to $L(1,\chi_4)$")
    ax.set_xlabel("smoothing scale N")
    ax.set_ylabel("approximation (real)")
    ax.legend(loc="best")
    return fig_obj


# ------------------------------------------------------------------------------
def main(argv: list[str] | None = None) -> int:
    """Run E069."""
    args = parse_experiment_args(
        experiment_id="e069",
        description="L(1,χ): slow convergence and smoothing.",
        argv=argv,
    )

    run_log = infer_run_log_file(out_dir=args.out_dir, experiment_slug="e069")
    setup_logging(config=LoggingConfig(verbose=args.verbose, log_file=run_log.log_file))
    logger.info("Starting experiment E069: L(1,χ): slow convergence and smoothing.")
    set_global_seed(args.seed)
    params = Params()
    paths = prepare_out_dir(out_dir=args.out_dir)

    chars = all_characters(params.q)
    if len(chars) < 2:
        raise ValueError("Need a nontrivial character.")
    chi = chars[1]

    S = _raw_partial_sums(chi=chi, n_max=params.n_max)
    fig1 = _plot_raw(S=S)
    save_figure(out_dir=paths.figures_dir, name="fig_01_l1_partial_sums", fig=fig1)

    smooth_vals: list[complex] = []
    for N in params.smooth_scales:
        smooth_vals.append(_smoothed_sum(chi=chi, N=int(N), n_max=params.n_max))
    fig2 = _plot_smoothed(scales=list(params.smooth_scales), vals=smooth_vals)
    save_figure(out_dir=paths.figures_dir, name="fig_02_l1_smoothed", fig=fig2)

    err_last = abs(S[-1].real - (np.pi / 4.0))
    lines = [
        "# E069: L(1,χ): slow convergence and smoothing",
        "",
        f"- q: {params.q}",
        f"- n_max: {params.n_max}",
        f"- last raw partial sum error vs pi/4: {float(err_last):.3e}",
        f"- smoothed scales: {list(params.smooth_scales)}",
        "",
        "Figures:",
        "- fig_01_l1_partial_sums.png",
        "- fig_02_l1_smoothed.png",
        "",
    ]

    write_json(paths.params_path, asdict(params))
    write_text(paths.report_path, "\n".join(lines))
    return 0
