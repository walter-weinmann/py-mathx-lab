"""Experiment E093: Logarithmic derivative -zeta'(s)/zeta(s) via von Mangoldt series.

For Re(s) > 1:
    -zeta'(s)/zeta(s) = sum_{n>=1} Lambda(n) / n^s

where Lambda is the von Mangoldt function.

We compare partial sums of the series to the value obtained from mpmath.

Artifacts:
    - out/e093/figures/fig_01_log_derivative_series.png
    - out/e093/params.json
    - out/e093/report.md
"""

from __future__ import annotations

from dataclasses import asdict, dataclass

import mpmath as mp
import numpy as np
from matplotlib import pyplot as plt

from mathxlab.exp.cli import parse_experiment_args
from mathxlab.exp.io import prepare_out_dir, save_figure, write_json, write_text
from mathxlab.exp.logging import LoggingConfig, get_logger, setup_logging
from mathxlab.exp.random import set_global_seed
from mathxlab.nt.arithmetic import build_factor_sieve, compute_von_mangoldt


# ------------------------------------------------------------------------------
@dataclass(frozen=True, slots=True)
class Params:
    """Parameters for E093."""

    s: float = 2.0
    n_values: tuple[int, ...] = (10, 30, 100, 300, 1_000, 3_000, 10_000, 30_000)
    mp_dps: int = 80


def _von_mangoldt_partial_sums(s: float, n_values: list[int]) -> np.ndarray:
    """Compute partial sums of sum_{n<=N} Lambda(n)/n^s."""
    n_max = max(n_values)
    sieve = build_factor_sieve(n_max)
    lam_list = compute_von_mangoldt(n_max, sieve=sieve)
    lam = np.array(lam_list[1:], dtype=float)  # lam[1..n_max]

    x = np.arange(1, n_max + 1, dtype=float)
    terms = lam / np.power(x, s)
    partial = np.cumsum(terms)

    out = np.zeros(len(n_values), dtype=float)
    for i, n in enumerate(n_values):
        out[i] = float(partial[n - 1])
    return out


def main(argv: list[str] | None = None) -> int:
    """Run experiment E093."""
    args = parse_experiment_args(experiment_id="E093", description=__doc__, argv=argv)
    setup_logging(config=LoggingConfig(verbose=args.verbose))
    logger = get_logger(__name__)
    set_global_seed(12345)

    params = Params()
    paths = prepare_out_dir(out_dir=args.out_dir)

    with mp.workdps(params.mp_dps):
        s_mp = mp.mpf(params.s)
        z = mp.zeta(s_mp)
        z_prime = mp.diff(mp.zeta, s_mp)
        target = float(-z_prime / z)

    n_values = list(params.n_values)
    approx = _von_mangoldt_partial_sums(params.s, n_values)
    err = np.abs(approx - target)

    fig, ax = plt.subplots()
    ax.plot(n_values, err, marker="o", linestyle="-")
    ax.set_xscale("log")
    ax.set_yscale("log")
    ax.set_xlabel("N")
    ax.set_ylabel("absolute error")
    ax.set_title(f"Von Mangoldt series for -zeta'(s)/zeta(s) (s={params.s})")
    ax.grid(True, which="both", linewidth=0.5)

    save_figure(out_dir=paths.figures_dir, name="fig_01_log_derivative_series", fig=fig)
    write_json(paths.params_path, data=asdict(params))

    report = """# E093 — Logarithmic derivative series

We approximate -zeta'(s)/zeta(s) by partial sums of the von Mangoldt Dirichlet series.
"""
    write_text(paths.report_path, text=report)

    logger.info("Done.")
    return 0
