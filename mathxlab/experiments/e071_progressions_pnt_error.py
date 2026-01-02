"""E071 — PNT(AP) numerics: pi(x;q,a) - Li(x)/phi(q).

The prime number theorem in arithmetic progressions suggests:

    π(x; q, a) ~ Li(x) / φ(q)  (for gcd(a,q)=1)

This experiment visualizes the error term:

    E_a(x) = π(x; q, a) - Li(x)/φ(q)

for several residue classes a.

Usage:
    make run EXP=e071

Artifacts:
    - figures/fig_01_error_terms.png
    - params.json
    - report.md
"""

from __future__ import annotations

from dataclasses import asdict, dataclass
from math import gcd

import matplotlib.figure as fig
import matplotlib.pyplot as plt
import numpy as np

from mathxlab.exp.cli import parse_experiment_args
from mathxlab.exp.io import prepare_out_dir, save_figure, write_json, write_text
from mathxlab.exp.logging import LoggingConfig, get_logger, setup_logging
from mathxlab.exp.random import set_global_seed
from mathxlab.exp.run_logging import infer_run_log_file
from mathxlab.experiments._ap_utils import counts_in_residue_class, li_trap, sample_grid
from mathxlab.experiments._prime_utils import primes_up_to
from mathxlab.nt.dirichlet import euler_phi

# ------------------------------------------------------------------------------
logger = get_logger(__name__)


# ------------------------------------------------------------------------------
@dataclass(frozen=True)
class Params:
    """Parameters for E071."""

    q: int = 10
    residues: tuple[int, ...] = (1, 3, 7, 9)
    x_max: int = 1_000_000
    n_points: int = 650
    li_step: int = 200


# ------------------------------------------------------------------------------
def _plot(*, xs: np.ndarray, errors: dict[int, np.ndarray], q: int) -> fig.Figure:
    """Plot error curves E_a(x)."""
    fig_obj, ax = plt.subplots()
    for a, y in errors.items():
        ax.plot(xs, y, label=rf"$a={a}$")
    ax.set_title(rf"Error terms $\pi(x;q,a) - \mathrm{{Li}}(x)/\varphi(q)$ (q={q})")
    ax.set_xlabel("x")
    ax.set_ylabel("error")
    ax.legend(loc="best")
    return fig_obj


# ------------------------------------------------------------------------------
def main(argv: list[str] | None = None) -> int:
    """Run E071."""
    args = parse_experiment_args(
        experiment_id="e071",
        description="PNT(AP) numerics: pi(x;q,a) - Li(x)/phi(q).",
        argv=argv,
    )

    run_log = infer_run_log_file(out_dir=args.out_dir, experiment_slug="e071")
    setup_logging(config=LoggingConfig(verbose=args.verbose, log_file=run_log.log_file))
    logger.info("Starting experiment E071: PNT(AP) numerics: pi(x;q,a) - Li(x)/phi(q).")
    set_global_seed(args.seed)
    params = Params()
    paths = prepare_out_dir(out_dir=args.out_dir)

    for a in params.residues:
        if gcd(a, params.q) != 1:
            raise ValueError(f"Residue {a} is not coprime to q={params.q}")

    primes = primes_up_to(params.x_max)
    xs = sample_grid(x_max=params.x_max, n=params.n_points, log=False)
    phi_q = euler_phi(params.q)
    li_vals = li_trap(xs=xs, step=params.li_step)
    baseline = li_vals / float(phi_q)

    errors: dict[int, np.ndarray] = {}
    for a in params.residues:
        pi_a = counts_in_residue_class(primes=primes, q=params.q, a=a, xs=xs).astype(np.float64)
        errors[a] = pi_a - baseline

    fig1 = _plot(xs=xs, errors=errors, q=params.q)
    save_figure(out_dir=paths.figures_dir, name="fig_01_error_terms", fig=fig1)

    lines = [
        "# E071 — PNT(AP) error terms",
        "",
        f"- q: {params.q}",
        f"- residues: {list(params.residues)}",
        f"- x_max: {params.x_max}",
        f"- li_step: {params.li_step}",
        "",
        "Figure:",
        "- fig_01_error_terms.png",
        "",
        "Notes:",
        "- The errors oscillate; their fine behavior is linked to zeros of Dirichlet L-functions.",
        "",
    ]

    write_json(paths.params_path, asdict(params))
    write_text(paths.report_path, "\n".join(lines))
    return 0
