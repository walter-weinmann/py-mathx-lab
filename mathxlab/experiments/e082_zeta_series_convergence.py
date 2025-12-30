"""Experiment E082: Zeta(s) Dirichlet series convergence for different s.

We compare partial sums of:

    zeta(s) = sum_{n>=1} n^{-s}   (Re(s) > 1)

for a couple of real s values. The convergence rate differs drastically as
s approaches 1.

Artifacts:
    - out/e082/figures/fig_01_series_convergence.png
    - out/e082/params.json
    - out/e082/report.md
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


# ------------------------------------------------------------------------------
@dataclass(frozen=True, slots=True)
class Params:
    """Parameters for E082."""

    s_values: tuple[float, ...] = (2.0, 1.2)
    n_values: tuple[int, ...] = (10, 30, 100, 300, 1_000, 3_000, 10_000, 30_000)
    mp_dps: int = 60


def _partial_sums_real(s: float, n_values: Sequence[int]) -> np.ndarray:
    """Compute partial sums of n^{-s} for a list of N values."""
    out = np.zeros(len(n_values), dtype=float)
    for i, n in enumerate(n_values):
        x = np.arange(1, n + 1, dtype=float)
        out[i] = float(np.sum(np.power(x, -s)))
    return out


def main(argv: list[str] | None = None) -> int:
    """Run experiment E082."""
    args = parse_experiment_args(experiment_id="E082", description=__doc__, argv=argv)
    setup_logging(config=LoggingConfig(verbose=args.verbose))
    logger = get_logger(__name__)
    set_global_seed(args.seed)

    params = Params()
    paths = prepare_out_dir(out_dir=args.out_dir)

    with mp.workdps(params.mp_dps):
        zeta_true = {s: float(mp.zeta(s)) for s in params.s_values}

    n_values = list(params.n_values)
    fig, ax = plt.subplots()
    for s in params.s_values:
        partial = _partial_sums_real(s, n_values)
        err = np.abs(partial - zeta_true[s])
        ax.plot(n_values, err, marker="o", linestyle="-", label=f"s={s}")

    ax.set_xscale("log")
    ax.set_yscale("log")
    ax.set_xlabel("N (number of terms)")
    ax.set_ylabel("absolute error |partial - zeta(s)|")
    ax.set_title("Zeta(s) series convergence (Dirichlet partial sums)")
    ax.grid(True, which="both", linewidth=0.5)
    ax.legend(loc="best")

    save_figure(out_dir=paths.figures_dir, name="fig_01_series_convergence", fig=fig)
    write_json(paths.params_path, data=asdict(params))

    report = """# E082 — Zeta(s) series convergence

We approximate zeta(s) by partial sums of the Dirichlet series for two real s values.

- As s approaches 1, convergence becomes much slower.
- The plot shows the absolute error relative to a high-precision mpmath zeta(s).
"""
    write_text(paths.report_path, text=report)

    logger.info("Done.")
    return 0
