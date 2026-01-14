"""Experiment E091: Partial Euler products on the critical line.

The Euler product for zeta(s) converges for Re(s) > 1, but it does not converge
on the critical line Re(s) = 1/2. We illustrate this by comparing partial Euler
products to zeta(1/2 + i t) for a fixed t.

Artifacts:
    - out/e091/figures/fig_01_euler_product_critical_line.png
    - out/e091/params.json
    - out/e091/report.md
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
from mathxlab.experiments._prime_utils import primes_up_to
from mathxlab.nt.zeta import euler_product_partial


# ------------------------------------------------------------------------------
@dataclass(frozen=True, slots=True)
class Params:
    """Parameters for E091."""

    t: float = 10.0
    prime_cutoffs: tuple[int, ...] = (10, 30, 100, 300, 1_000, 3_000, 10_000)
    mp_dps: int = 70


def main(argv: list[str] | None = None) -> int:
    """Run experiment E091."""
    args = parse_experiment_args(experiment_id="E091", description=__doc__, argv=argv)
    run_log = infer_run_log_file(out_dir=args.out_dir, experiment_slug="e091")
    setup_logging(config=LoggingConfig(verbose=args.verbose, log_file=run_log.log_file))
    logger = get_logger(__name__)
    logger.info("Starting experiment E091 (log_file=%s)", run_log.log_file)
    logger.info("seed=%d out_dir=%s", args.seed, args.out_dir)
    set_global_seed(args.seed)

    params = Params()
    paths = prepare_out_dir(out_dir=args.out_dir)

    with mp.workdps(params.mp_dps):
        s = mp.mpc(0.5, params.t)
        z_true = complex(mp.zeta(s))

    mags_true = abs(z_true)

    cutoffs = list(params.prime_cutoffs)
    prod_vals = np.zeros(len(cutoffs), dtype=complex)
    for i, p_max in enumerate(cutoffs):
        primes = primes_up_to(int(p_max))
        prod_vals[i] = euler_product_partial(complex(0.5, params.t), primes)

    prod_mags = np.abs(prod_vals)

    fig, ax = plt.subplots()
    ax.plot(cutoffs, prod_mags, marker="o", label="|partial Euler product|")
    ax.axhline(mags_true, linewidth=1.0, label="|zeta(1/2 + i t)|")
    ax.set_xscale("log")
    ax.set_yscale("log")
    ax.set_xlabel("prime cutoff p_max")
    ax.set_ylabel("magnitude")
    ax.set_title(f"Partial Euler product on Re(s)=1/2 (t={params.t})")
    ax.grid(True, which="both", linewidth=0.5)
    ax.legend(loc="best")

    save_figure(out_dir=paths.figures_dir, name="fig_01_euler_product_critical_line", fig=fig)
    write_json(paths.params_path, data=asdict(params))

    report = f"""# E091: Euler products on the critical line

We compare zeta(1/2 + i t) (t={params.t}) to partial Euler products truncated at primes <= p_max.

The Euler product does not converge on the critical line, so the partial products
do not stabilize as p_max grows (in contrast to the Re(s) > 1 case).
"""
    write_text(paths.report_path, text=report)

    logger.info("Done.")
    return 0
