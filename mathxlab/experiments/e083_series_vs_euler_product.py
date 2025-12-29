"""Experiment E083: Zeta(s) series vs Euler product (partial approximations).

For Re(s) > 1, zeta(s) admits both:
  - Dirichlet series:  sum_{n>=1} n^{-s}
  - Euler product:    prod_p (1 - p^{-s})^{-1}

We compare partial approximations for a fixed real s.

Artifacts:
    - out/e083/figures/fig_01_series_vs_product.png
    - out/e083/params.json
    - out/e083/report.md
"""

from __future__ import annotations

from collections.abc import Sequence
from dataclasses import asdict, dataclass

import mpmath as mp
import numpy as np
from matplotlib import pyplot as plt

from mathxlab.exp.cli import parse_experiment_args
from mathxlab.exp.io import prepare_out_dir, save_figure, write_json, write_text
from mathxlab.exp.logging import LoggingConfig, get_logger, setup_logging
from mathxlab.exp.seeding import set_global_seed
from mathxlab.experiments._prime_utils import primes_up_to


# ------------------------------------------------------------------------------
@dataclass(frozen=True, slots=True)
class Params:
    """Parameters for E083."""

    s: float = 2.0
    n_values: tuple[int, ...] = (10, 30, 100, 300, 1_000, 3_000, 10_000)
    prime_cutoffs: tuple[int, ...] = (10, 30, 100, 300, 1_000, 3_000)
    mp_dps: int = 60


def _partial_zeta_series(s: float, n_values: Sequence[int]) -> np.ndarray:
    out = np.zeros(len(n_values), dtype=float)
    for i, n in enumerate(n_values):
        x = np.arange(1, n + 1, dtype=float)
        out[i] = float(np.sum(np.power(x, -s)))
    return out


def _partial_euler_product(s: float, prime_cutoffs: Sequence[int], mp_dps: int) -> np.ndarray:
    out = np.zeros(len(prime_cutoffs), dtype=float)
    with mp.workdps(mp_dps):
        for i, p_max in enumerate(prime_cutoffs):
            primes = primes_up_to(int(p_max))
            prod = mp.mpf(1)
            for p in primes:
                prod *= 1 / (1 - mp.power(p, -s))
            out[i] = float(prod)
    return out


def main(argv: list[str] | None = None) -> int:
    """Run experiment E083."""
    args = parse_experiment_args(experiment_id="E083", description=__doc__, argv=argv)
    setup_logging(config=LoggingConfig(verbose=args.verbose))
    logger = get_logger(__name__)
    set_global_seed(args.seed)

    params = Params()
    paths = prepare_out_dir(out_dir=args.out_dir)

    with mp.workdps(params.mp_dps):
        z_true = float(mp.zeta(params.s))

    series_vals = _partial_zeta_series(params.s, params.n_values)
    product_vals = _partial_euler_product(params.s, params.prime_cutoffs, params.mp_dps)

    fig, ax = plt.subplots()
    ax.plot(
        params.n_values, np.abs(series_vals - z_true), marker="o", label="Dirichlet series error"
    )
    ax.plot(
        params.prime_cutoffs, np.abs(product_vals - z_true), marker="o", label="Euler product error"
    )
    ax.set_xscale("log")
    ax.set_yscale("log")
    ax.set_xlabel("cutoff (N or p_max)")
    ax.set_ylabel("absolute error")
    ax.set_title(f"Series vs Euler product convergence (s={params.s})")
    ax.grid(True, which="both", linewidth=0.5)
    ax.legend(loc="best")

    save_figure(out_dir=paths.figures_dir, name="fig_01_series_vs_product", fig=fig)
    write_json(paths.params_path, data=asdict(params))

    report = """# E083 — Series vs Euler product

We compare partial approximations to zeta(s) coming from the series and the Euler product.

Note: both approximations converge for Re(s) > 1, but their practical behavior depends on the cutoff choices.
"""
    write_text(paths.report_path, text=report)

    logger.info("Done.")
    return 0
