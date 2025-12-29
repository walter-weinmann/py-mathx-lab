"""Experiment E084: |zeta(1/2 + i t)| on a moderate t-range.

We sample the magnitude of zeta on the critical line.

Artifacts:
    - out/e084/figures/fig_01_critical_line_magnitude.png
    - out/e084/params.json
    - out/e084/report.md
"""

from __future__ import annotations

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
    """Parameters for E084."""

    t_max: float = 50.0
    n_points: int = 300
    mp_dps: int = 50


def main(argv: list[str] | None = None) -> int:
    """Run experiment E084."""
    args = parse_experiment_args(experiment_id="E084", description=__doc__, argv=argv)
    setup_logging(config=LoggingConfig(verbose=args.verbose))
    logger = get_logger(__name__)
    set_global_seed(args.seed)

    params = Params()
    paths = prepare_out_dir(out_dir=args.out_dir)

    t_values = np.linspace(0.0, params.t_max, params.n_points)
    mags = np.zeros_like(t_values)

    with mp.workdps(params.mp_dps):
        for i, t in enumerate(t_values):
            s = mp.mpc(0.5, float(t))
            mags[i] = float(abs(mp.zeta(s)))

    fig, ax = plt.subplots()
    ax.plot(t_values, mags, linewidth=1.0)
    ax.set_xlabel("t")
    ax.set_ylabel("|zeta(1/2 + i t)|")
    ax.set_title("Magnitude of zeta on the critical line")
    ax.grid(True, linewidth=0.5)

    save_figure(out_dir=paths.figures_dir, name="fig_01_critical_line_magnitude", fig=fig)
    write_json(paths.params_path, data=asdict(params))

    report = """# E084 — |zeta(1/2 + i t)|

We sample the magnitude of zeta(s) along the critical line s = 1/2 + i t on a moderate t-range.
"""
    write_text(paths.report_path, text=report)

    logger.info("Done.")
    return 0
