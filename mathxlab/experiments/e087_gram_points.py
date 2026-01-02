"""Experiment E087: Gram points and Hardy Z(t).

Gram points g_n are defined by theta(g_n) = n*pi, where theta is the Riemann-Siegel theta function.
A classic observation (Gram's law) relates sign changes of Z(t) at Gram points to zeros of zeta.

We sample Z(g_n) for a small range of n.

Artifacts:
    - out/e087/figures/fig_01_gram_points_Z.png
    - out/e087/params.json
    - out/e087/report.md
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
from mathxlab.nt.zeta import hardy_Z


# ------------------------------------------------------------------------------
@dataclass(frozen=True, slots=True)
class Params:
    """Parameters for E087."""

    n_start: int = 1
    n_end: int = 35
    mp_dps: int = 60


def main(argv: list[str] | None = None) -> int:
    """Run experiment E087."""
    args = parse_experiment_args(experiment_id="E087", description=__doc__, argv=argv)

    run_log = infer_run_log_file(out_dir=args.out_dir, experiment_slug="e087")
    setup_logging(config=LoggingConfig(verbose=args.verbose, log_file=run_log.log_file))
    logger = get_logger(__name__)
    set_global_seed(args.seed)

    params = Params()
    paths = prepare_out_dir(out_dir=args.out_dir)

    n_values = list(range(params.n_start, params.n_end + 1))

    with mp.workdps(params.mp_dps):
        gram_points = [float(mp.grampoint(n)) for n in n_values]

    z_vals = np.array([hardy_Z(g) for g in gram_points], dtype=float)

    fig, ax = plt.subplots()
    ax.plot(n_values, z_vals, marker="o", linestyle="-", linewidth=1.0)
    ax.axhline(0.0, linewidth=1.0)
    ax.set_xlabel("n")
    ax.set_ylabel("Z(g_n)")
    ax.set_title("Hardy Z at Gram points")
    ax.grid(True, linewidth=0.5)

    save_figure(out_dir=paths.figures_dir, name="fig_01_gram_points_Z", fig=fig)
    write_json(paths.params_path, data=asdict(params))

    sign_changes = int(np.sum(z_vals[:-1] * z_vals[1:] < 0))
    report = f"""# E087 — Gram points

We computed Gram points g_n for n in [{params.n_start}, {params.n_end}] and sampled Hardy Z(g_n).

Observed sign changes between consecutive Gram points (simple count): **{sign_changes}**.
"""
    write_text(paths.report_path, text=report)

    logger.info("Done.")
    return 0
