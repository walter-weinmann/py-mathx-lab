"""Experiment E092: 1/zeta(s) via the Möbius Dirichlet series.

For Re(s) > 1:
    1/zeta(s) = sum_{n>=1} mu(n) / n^s

We compare partial sums of the Möbius series to 1/zeta(s).

Artifacts:
    - out/e092/figures/fig_01_mobius_series_inverse_zeta.png
    - out/e092/params.json
    - out/e092/report.md
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
from mathxlab.nt.arithmetic import build_factor_sieve, compute_mobius


# ------------------------------------------------------------------------------
@dataclass(frozen=True, slots=True)
class Params:
    """Parameters for E092."""

    s: float = 2.0
    n_values: tuple[int, ...] = (10, 30, 100, 300, 1_000, 3_000, 10_000, 30_000)
    mp_dps: int = 70


def _mobius_partial_sums(s: float, n_values: list[int]) -> np.ndarray:
    """Compute partial sums of sum_{n<=N} mu(n)/n^s."""
    n_max = max(n_values)
    sieve = build_factor_sieve(n_max)
    mu_list = compute_mobius(n_max, sieve=sieve)
    mu = np.array(mu_list[1:], dtype=float)  # mu[1..n_max]

    x = np.arange(1, n_max + 1, dtype=float)
    terms = mu / np.power(x, s)
    partial = np.cumsum(terms)

    out = np.zeros(len(n_values), dtype=float)
    for i, n in enumerate(n_values):
        out[i] = float(partial[n - 1])
    return out


def main(argv: list[str] | None = None) -> int:
    """Run experiment E092."""
    args = parse_experiment_args(experiment_id="E092", description=__doc__, argv=argv)
    setup_logging(config=LoggingConfig(verbose=args.verbose))
    logger = get_logger(__name__)
    set_global_seed(12345)

    params = Params()
    paths = prepare_out_dir(out_dir=args.out_dir)

    with mp.workdps(params.mp_dps):
        inv_true = float(1 / mp.zeta(params.s))

    n_values = list(params.n_values)
    approx = _mobius_partial_sums(params.s, n_values)
    err = np.abs(approx - inv_true)

    fig, ax = plt.subplots()
    ax.plot(n_values, err, marker="o", linestyle="-")
    ax.set_xscale("log")
    ax.set_yscale("log")
    ax.set_xlabel("N")
    ax.set_ylabel("absolute error")
    ax.set_title(f"Möbius series for 1/zeta(s) (s={params.s})")
    ax.grid(True, which="both", linewidth=0.5)

    save_figure(out_dir=paths.figures_dir, name="fig_01_mobius_series_inverse_zeta", fig=fig)
    write_json(paths.params_path, data=asdict(params))

    report = """# E092 — Möbius series for 1/zeta(s)

We approximate 1/zeta(s) via the Dirichlet series sum mu(n)/n^s, which converges for Re(s) > 1.
"""
    write_text(paths.report_path, text=report)

    logger.info("Done.")
    return 0
