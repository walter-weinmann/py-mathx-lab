"""E068 — Dirichlet L(s,χ): series vs Euler product (partial approximations).

For Re(s) > 1, Dirichlet L-functions admit both:

    L(s,χ) = ∑_{n>=1} χ(n) / n^s
           = ∏_{p∤q} (1 - χ(p) / p^s)^{-1}

This experiment compares **partial sums** and **partial Euler products** for a
small character (default: the nontrivial character mod 4) at a fixed s.

Usage:
    make run EXP=e068

Artifacts:
    - figures/fig_01_series_vs_euler.png
    - params.json
    - report.md
"""

from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import cast

import matplotlib.figure as fig
import matplotlib.pyplot as plt
import numpy as np

from mathxlab.exp.cli import parse_experiment_args
from mathxlab.exp.io import prepare_out_dir, save_figure, write_json, write_text
from mathxlab.exp.logging import LoggingConfig, get_logger, setup_logging
from mathxlab.exp.random import set_global_seed
from mathxlab.exp.run_logging import infer_run_log_file
from mathxlab.experiments._prime_utils import primes_up_to
from mathxlab.nt.dirichlet import DirichletCharacter, all_characters

# ------------------------------------------------------------------------------
logger = get_logger(__name__)


# ------------------------------------------------------------------------------
@dataclass(frozen=True)
class Params:
    """Parameters for E068.

    Attributes:
        q: Modulus.
        s_re: Real part of s.
        s_im: Imaginary part of s.
        n_max: Series cutoff for the partial sum.
        p_max: Prime cutoff for the partial Euler product.
        n_points: Number of samples between small and large cutoffs.
    """

    q: int = 4
    s_re: float = 2.0
    s_im: float = 0.0
    n_max: int = 120_000
    p_max: int = 400_000
    n_points: int = 160


# ------------------------------------------------------------------------------
def _series_trace(
    *, chi: DirichletCharacter, s: complex, n_max: int, cutoffs: np.ndarray
) -> np.ndarray:
    """Compute partial sum trace at specified cutoffs.

    Args:
        chi: Dirichlet character callable.
        s: Complex exponent.
        n_max: Maximum N.
        cutoffs: Increasing integer cutoffs.

    Returns:
        Complex array of partial sums evaluated at cutoffs.
    """
    ks = np.arange(1, n_max + 1, dtype=np.float64)
    chi_vals = np.array([chi(int(k)) for k in ks], dtype=np.complex128)
    terms = chi_vals / (ks**s)
    csum = np.cumsum(terms).astype(np.complex128)
    return cast(np.ndarray, csum[cutoffs - 1].astype(np.complex128))


# ------------------------------------------------------------------------------
def _euler_trace(
    *, chi: DirichletCharacter, s: complex, q: int, p_max: int, cutoffs: np.ndarray
) -> np.ndarray:
    """Compute partial Euler product trace at specified prime cutoffs.

    Args:
        chi: Dirichlet character callable.
        s: Complex exponent.
        q: Modulus (exclude primes dividing q).
        p_max: Maximum prime cutoff.
        cutoffs: Increasing integer prime cutoffs.

    Returns:
        Complex array of partial Euler products evaluated at cutoffs.
    """
    primes = primes_up_to(p_max)
    # Exclude primes dividing q.
    primes = primes[np.array([q % int(p) != 0 for p in primes], dtype=bool)]

    # Build incremental product over primes.
    prods: list[complex] = []
    prod = 1.0 + 0.0j
    j = 0
    for P in cutoffs:
        while j < primes.size and primes[j] <= P:
            p = float(primes[j])
            cp = chi(int(primes[j]))
            prod *= 1.0 / (1.0 - cp / (complex(p) ** s))
            j += 1
        prods.append(prod)
    return np.array(prods, dtype=np.complex128)


# ------------------------------------------------------------------------------
def _plot(
    *, idx: np.ndarray, series_vals: np.ndarray, euler_vals: np.ndarray, q: int, s: complex
) -> fig.Figure:
    """Plot real parts of the two approximation traces."""
    fig_obj, ax = plt.subplots()
    ax.plot(idx, np.real(series_vals), label="Re partial series")
    ax.plot(idx, np.real(euler_vals), label="Re partial Euler product")
    ax.set_title(rf"Partial L(s,χ) approximations (q={q}, s={s})")
    ax.set_xlabel("sample index")
    ax.set_ylabel("Real part")
    ax.legend(loc="best")
    return fig_obj


# ------------------------------------------------------------------------------
def main(argv: list[str] | None = None) -> int:
    """Run E068."""
    args = parse_experiment_args(
        experiment_id="e068",
        description="Dirichlet L(s,χ): series vs Euler product (partial approximations).",
        argv=argv,
    )

    run_log = infer_run_log_file(out_dir=args.out_dir, experiment_slug="e068")
    setup_logging(config=LoggingConfig(verbose=args.verbose, log_file=run_log.log_file))
    logger.info(
        "Starting experiment E068: Dirichlet L(s,χ): series vs Euler product (partial approximations)."
    )
    set_global_seed(args.seed)
    params = Params()
    paths = prepare_out_dir(out_dir=args.out_dir)

    chars = all_characters(params.q)
    if len(chars) < 2:
        raise ValueError("Need a nontrivial character for this experiment.")
    chi = chars[1]  # principal is sorted first
    s = complex(params.s_re, params.s_im)

    # Sample cutoffs (avoid tiny values).
    t = np.linspace(0.02, 1.0, params.n_points)
    n_cut = np.maximum(50, (t * params.n_max).astype(np.int64))
    p_cut = np.maximum(50, (t * params.p_max).astype(np.int64))

    series_vals = _series_trace(chi=chi, s=s, n_max=params.n_max, cutoffs=n_cut)
    euler_vals = _euler_trace(chi=chi, s=s, q=params.q, p_max=params.p_max, cutoffs=p_cut)

    fig1 = _plot(
        idx=np.arange(params.n_points),
        series_vals=series_vals,
        euler_vals=euler_vals,
        q=params.q,
        s=s,
    )
    save_figure(out_dir=paths.figures_dir, name="fig_01_series_vs_euler", fig=fig1)

    diff_last = abs(series_vals[-1] - euler_vals[-1])
    lines = [
        "# E068 — Dirichlet L(s,χ): series vs Euler product",
        "",
        f"- q: {params.q}",
        f"- s: {s}",
        f"- n_max: {params.n_max}",
        f"- p_max: {params.p_max}",
        f"- |series - euler| (last sample): {diff_last:.3e}",
        "",
        "Figure:",
        "- fig_01_series_vs_euler.png",
        "",
        "Notes:",
        "- Both approximations converge to the same limit for Re(s)>1.",
        "- The Euler product is only over primes p not dividing q.",
        "",
    ]

    write_json(paths.params_path, asdict(params))
    write_text(paths.report_path, "\n".join(lines))
    return 0
