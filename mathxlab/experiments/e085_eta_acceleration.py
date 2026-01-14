"""Experiment E085: Eta-series acceleration for zeta(s) near s=1.

The Dirichlet series for zeta(s) converges slowly as s approaches 1.
The alternating eta-series converges for Re(s) > 0 and can be used via:

    zeta(s) = eta(s) / (1 - 2^{1-s})

We compare the naive partial zeta series to the eta-based reconstruction.

Artifacts:
    - out/e085/figures/fig_01_eta_acceleration.png
    - out/e085/params.json
    - out/e085/report.md
"""

from __future__ import annotations

from dataclasses import asdict, dataclass

import mpmath as mp
import numpy as np
from matplotlib import pyplot as plt

from mathxlab.exp.cli import parse_experiment_args
from mathxlab.exp.io import prepare_out_dir, save_figure, write_json, write_text
from mathxlab.exp.logging import LoggingConfig, get_logger, setup_logging
from mathxlab.exp.run_logging import infer_run_log_file
from mathxlab.exp.seeding import set_global_seed
from mathxlab.nt.zeta import eta_series_partial, zeta_series_partial, zeta_via_eta


# ------------------------------------------------------------------------------
@dataclass(frozen=True, slots=True)
class Params:
    """Parameters for E085."""

    s: float = 1.1
    n_values: tuple[int, ...] = (10, 30, 100, 300, 1_000, 3_000, 10_000, 30_000)
    mp_dps: int = 60


def main(argv: list[str] | None = None) -> int:
    """Run experiment E085."""
    args = parse_experiment_args(experiment_id="E085", description=__doc__, argv=argv)

    run_log = infer_run_log_file(out_dir=args.out_dir, experiment_slug="e085")
    setup_logging(config=LoggingConfig(verbose=args.verbose, log_file=run_log.log_file))
    logger = get_logger(__name__)
    set_global_seed(args.seed)

    params = Params()
    paths = prepare_out_dir(out_dir=args.out_dir)

    with mp.workdps(params.mp_dps):
        z_true = complex(mp.zeta(params.s))

    n_values = list(params.n_values)
    err_zeta = np.zeros(len(n_values), dtype=float)
    err_eta = np.zeros(len(n_values), dtype=float)

    for i, n in enumerate(n_values):
        z_partial = zeta_series_partial(params.s, n, settings=None)
        eta_partial = eta_series_partial(params.s, n, settings=None)
        z_from_eta = zeta_via_eta(params.s, eta_partial)
        err_zeta[i] = abs(z_partial - z_true)
        err_eta[i] = abs(z_from_eta - z_true)

    fig, ax = plt.subplots()
    ax.plot(n_values, err_zeta, marker="o", label="zeta series error")
    ax.plot(n_values, err_eta, marker="o", label="eta-based error")
    ax.set_xscale("log")
    ax.set_yscale("log")
    ax.set_xlabel("N (number of terms)")
    ax.set_ylabel("absolute error")
    ax.set_title(f"Eta acceleration near s={params.s}")
    ax.grid(True, which="both", linewidth=0.5)
    ax.legend(loc="best")

    save_figure(out_dir=paths.figures_dir, name="fig_01_eta_acceleration", fig=fig)
    write_json(paths.params_path, data=asdict(params))

    report = """# E085: Eta acceleration

We compare:

- naive partial sums of zeta(s)
- partial sums of eta(s), mapped back to zeta(s)

for s close to 1. The eta-based approach typically reduces cancellation issues and improves convergence.
"""
    write_text(paths.report_path, text=report)

    logger.info("Done.")
    return 0
