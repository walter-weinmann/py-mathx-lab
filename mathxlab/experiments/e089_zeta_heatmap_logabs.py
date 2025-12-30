"""Experiment E089: Heatmap of log|zeta(s)| in a small critical-strip window.

We sample zeta(s) on a coarse grid in the (sigma, t) plane and visualize log10|zeta(s)|
to highlight poles/zeros and rapid growth regions.

Artifacts:
    - out/e089/figures/fig_01_logabs_heatmap.png
    - out/e089/params.json
    - out/e089/report.md
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
    """Parameters for E089."""

    sigma_min: float = 0.0
    sigma_max: float = 2.0
    t_min: float = -20.0
    t_max: float = 20.0
    n_sigma: int = 31
    n_t: int = 41
    mp_dps: int = 50


def main(argv: list[str] | None = None) -> int:
    """Run experiment E089."""
    args = parse_experiment_args(experiment_id="E089", description=__doc__, argv=argv)
    setup_logging(config=LoggingConfig(verbose=args.verbose))
    logger = get_logger(__name__)
    set_global_seed(args.seed)

    params = Params()
    paths = prepare_out_dir(out_dir=args.out_dir)

    sigmas = np.linspace(params.sigma_min, params.sigma_max, params.n_sigma)
    ts = np.linspace(params.t_min, params.t_max, params.n_t)

    grid = np.zeros((params.n_t, params.n_sigma), dtype=float)

    with mp.workdps(params.mp_dps):
        for i, t in enumerate(ts):
            for j, sigma in enumerate(sigmas):
                s = mp.mpc(float(sigma), float(t))
                try:
                    val = mp.zeta(s)
                    grid[i, j] = float(abs(val))
                except ValueError:
                    # zeta(1) pole
                    grid[i, j] = np.inf

    log_abs = np.log10(grid + 1e-30)

    fig, ax = plt.subplots()
    im = ax.imshow(
        log_abs,
        origin="lower",
        aspect="auto",
        extent=(params.sigma_min, params.sigma_max, params.t_min, params.t_max),
    )
    fig.colorbar(im, ax=ax, label="log10 |zeta(s)|")
    ax.set_xlabel("sigma = Re(s)")
    ax.set_ylabel("t = Im(s)")
    ax.set_title("Heatmap of log10|zeta(s)| (coarse grid)")

    save_figure(out_dir=paths.figures_dir, name="fig_01_logabs_heatmap", fig=fig)
    write_json(paths.params_path, data=asdict(params))

    report = """# E089 — Heatmap of log|zeta(s)|

We plot log10|zeta(s)| on a coarse grid in the (sigma, t) plane. The pole at s=1 manifests as a bright region near sigma=1, t=0.
"""
    write_text(paths.report_path, text=report)

    logger.info("Done.")
    return 0
