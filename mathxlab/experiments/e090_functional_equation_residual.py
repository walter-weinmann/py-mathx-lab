"""Experiment E090: Functional equation residual heatmap.

The zeta functional equation can be written as:
    zeta(s) = chi(s) * zeta(1 - s)

We sample the residual:
    R(s) = zeta(s) - chi(s) * zeta(1 - s)

and visualize log10|R(s)| on a coarse grid.

Artifacts:
    - out/e090/figures/fig_01_functional_residual_heatmap.png
    - out/e090/params.json
    - out/e090/report.md
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
from mathxlab.nt.zeta import chi_factor


# ------------------------------------------------------------------------------
@dataclass(frozen=True, slots=True)
class Params:
    """Parameters for E090."""

    sigma_min: float = -1.0
    sigma_max: float = 2.0
    t_min: float = -15.0
    t_max: float = 15.0
    n_sigma: int = 25
    n_t: int = 31
    mp_dps: int = 70


def main(argv: list[str] | None = None) -> int:
    """Run experiment E090."""
    args = parse_experiment_args(experiment_id="E090", description=__doc__, argv=argv)

    run_log = infer_run_log_file(out_dir=args.out_dir, experiment_slug="e090")
    setup_logging(config=LoggingConfig(verbose=args.verbose, log_file=run_log.log_file))
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
                    lhs = mp.zeta(s)
                    rhs = mp.mpc(chi_factor(complex(s))) * mp.zeta(1 - s)
                    grid[i, j] = float(abs(lhs - rhs))
                except ValueError:
                    # zeta(1) pole
                    grid[i, j] = np.nan

    log_abs = np.log10(grid + 1e-40)

    fig, ax = plt.subplots()
    im = ax.imshow(
        log_abs,
        origin="lower",
        aspect="auto",
        extent=(params.sigma_min, params.sigma_max, params.t_min, params.t_max),
    )
    fig.colorbar(im, ax=ax, label="log10 |residual|")
    ax.set_xlabel("sigma = Re(s)")
    ax.set_ylabel("t = Im(s)")
    ax.set_title("Functional equation residual log10|zeta(s) - chi(s) zeta(1-s)|")

    save_figure(out_dir=paths.figures_dir, name="fig_01_functional_residual_heatmap", fig=fig)
    write_json(paths.params_path, data=asdict(params))

    report = """# E090: Functional equation residual

We visualize log10|zeta(s) - chi(s) zeta(1-s)| on a coarse grid. Away from the pole at s=1, the residual should be close to numerical precision.
"""
    write_text(paths.report_path, text=report)

    logger.info("Done.")
    return 0
