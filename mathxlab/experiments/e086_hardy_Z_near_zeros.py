"""Experiment E086: Hardy Z(t) around the first few zeta zeros.

Hardy Z(t) is a real-valued function whose zeros correspond to zeros of
zeta(1/2 + i t). We sample Z(t) in small windows around the first few zeros.

Artifacts:
    - out/e086/figures/fig_01_Z_near_zeros.png
    - out/e086/params.json
    - out/e086/report.md
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
    """Parameters for E086."""

    n_zeros: int = 3
    window: float = 0.6
    n_points: int = 400
    mp_dps: int = 60


def main(argv: list[str] | None = None) -> int:
    """Run experiment E086."""
    args = parse_experiment_args(experiment_id="E086", description=__doc__, argv=argv)

    run_log = infer_run_log_file(out_dir=args.out_dir, experiment_slug="e086")
    setup_logging(config=LoggingConfig(verbose=args.verbose, log_file=run_log.log_file))
    logger = get_logger(__name__)
    set_global_seed(args.seed)

    params = Params()
    paths = prepare_out_dir(out_dir=args.out_dir)

    with mp.workdps(params.mp_dps):
        zeros = [float(mp.zetazero(k).imag) for k in range(1, params.n_zeros + 1)]

    offsets = np.linspace(-params.window, params.window, params.n_points)
    fig, ax = plt.subplots()
    for idx, t0 in enumerate(zeros, start=1):
        vals = np.array([hardy_Z(float(t0 + dt)) for dt in offsets], dtype=float)
        ax.plot(offsets, vals, label=f"zero #{idx}")

    ax.axhline(0.0, linewidth=1.0)
    ax.set_xlabel("t - t0")
    ax.set_ylabel("Z(t)")
    ax.set_title("Hardy Z(t) near the first zeros")
    ax.grid(True, linewidth=0.5)
    ax.legend(loc="best")

    save_figure(out_dir=paths.figures_dir, name="fig_01_Z_near_zeros", fig=fig)
    write_json(paths.params_path, data=asdict(params))

    report = """# E086 — Hardy Z(t) near zeros

We locate the first few imaginary parts of non-trivial zeros (via mpmath) and sample Hardy's Z(t)
in a small window around each zero.
"""
    write_text(paths.report_path, text=report)

    logger.info("Done.")
    return 0
