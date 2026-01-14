"""Experiment E088: Riemann--von Mangoldt counting approximation for zeta zeros.

Let N(T) count non-trivial zeros with 0 < Im(rho) <= T (multiplicity).
The Riemann--von Mangoldt formula gives an asymptotic approximation.

We compare n (the index of the nth zero) with the main term evaluated at T = t_n.

Artifacts:
    - out/e088/figures/fig_01_zero_count_error.png
    - out/e088/params.json
    - out/e088/report.md
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
from mathxlab.nt.zeta import riemann_von_mangoldt_count


# ------------------------------------------------------------------------------
@dataclass(frozen=True, slots=True)
class Params:
    """Parameters for E088."""

    n_zeros: int = 40
    mp_dps: int = 70


def main(argv: list[str] | None = None) -> int:
    """Run experiment E088."""
    args = parse_experiment_args(experiment_id="E088", description=__doc__, argv=argv)

    run_log = infer_run_log_file(out_dir=args.out_dir, experiment_slug="e088")
    setup_logging(config=LoggingConfig(verbose=args.verbose, log_file=run_log.log_file))
    logger = get_logger(__name__)
    set_global_seed(args.seed)

    params = Params()
    paths = prepare_out_dir(out_dir=args.out_dir)

    with mp.workdps(params.mp_dps):
        zeros = np.array(
            [float(mp.zetazero(k).imag) for k in range(1, params.n_zeros + 1)], dtype=float
        )

    approx_counts = np.array([riemann_von_mangoldt_count(T) for T in zeros], dtype=float)
    true_counts = np.arange(1, params.n_zeros + 1, dtype=float)
    diff = true_counts - approx_counts

    fig, ax = plt.subplots()
    ax.plot(true_counts, diff, marker="o", linestyle="-", linewidth=1.0)
    ax.axhline(0.0, linewidth=1.0)
    ax.set_xlabel("zero index n")
    ax.set_ylabel("n - main_term(T_n)")
    ax.set_title("Zero counting: index minus RvM main term")
    ax.grid(True, linewidth=0.5)

    save_figure(out_dir=paths.figures_dir, name="fig_01_zero_count_error", fig=fig)
    write_json(paths.params_path, data=asdict(params))

    report = """# E088: Zero counting

We compare the index n of the nth non-trivial zero with the Riemann--von Mangoldt main-term approximation.
The difference should remain relatively small compared to n and reflects the lower-order terms and fluctuations.
"""
    write_text(paths.report_path, text=report)

    logger.info("Done.")
    return 0
