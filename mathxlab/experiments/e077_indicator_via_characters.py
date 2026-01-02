"""E077 — Indicator via character orthogonality (sanity check).

A standard identity expresses an indicator of a residue class using Dirichlet
characters. For gcd(a,q)=1 and gcd(n,q)=1:

    1_{n≡a (mod q)} = (1/φ(q)) * ∑_{χ mod q} χ(n) * conj(χ(a))

This experiment verifies the identity on residues modulo q and visualizes the
absolute error.

Usage:
    make run EXP=e077

Artifacts:
    - figures/fig_01_indicator_error.png
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
from mathxlab.nt.dirichlet import all_characters, euler_phi

# ------------------------------------------------------------------------------
logger = get_logger(__name__)


# ------------------------------------------------------------------------------
@dataclass(frozen=True)
class Params:
    """Parameters for E077."""

    q: int = 9
    a_target: int = 2


# ------------------------------------------------------------------------------
def _plot(*, errs: np.ndarray, q: int, a: int) -> fig.Figure:
    fig_obj, ax = plt.subplots()
    x = np.arange(q)
    ax.bar(x, errs)
    ax.set_title(rf"Indicator reconstruction error (q={q}, a={a})")
    ax.set_xlabel("n (mod q)")
    ax.set_ylabel("absolute error")
    return fig_obj


# ------------------------------------------------------------------------------
def main(argv: list[str] | None = None) -> int:
    """Run E077."""
    args = parse_experiment_args(
        experiment_id="e077",
        description="Indicator via character orthogonality (sanity check).",
        argv=argv,
    )

    run_log = infer_run_log_file(out_dir=args.out_dir, experiment_slug="e077")
    setup_logging(config=LoggingConfig(verbose=args.verbose, log_file=run_log.log_file))
    logger.info("Starting experiment E077: Indicator via character orthogonality (sanity check).")
    set_global_seed(args.seed)
    params = Params()
    paths = prepare_out_dir(out_dir=args.out_dir)

    if gcd(params.a_target, params.q) != 1:
        raise ValueError("a_target must be coprime to q")

    chars = all_characters(params.q)
    phi_q = euler_phi(params.q)

    # Compute reconstruction on residues n=0..q-1.
    n_vals = np.arange(params.q, dtype=int)
    recon = np.zeros(params.q, dtype=np.complex128)
    for chi in chars:
        recon += np.array([chi(int(n)) for n in n_vals], dtype=np.complex128) * np.conjugate(
            chi(params.a_target)
        )
    recon /= float(phi_q)

    # True indicator on units:
    truth = np.zeros(params.q, dtype=np.float64)
    for n in range(params.q):
        if gcd(n, params.q) == 1 and (n - params.a_target) % params.q == 0:
            truth[n] = 1.0

    errs = np.abs(recon.real - truth)
    fig1 = _plot(errs=errs, q=params.q, a=params.a_target)
    save_figure(out_dir=paths.figures_dir, name="fig_01_indicator_error", fig=fig1)

    lines = [
        "# E077 — Indicator via character orthogonality",
        "",
        f"- q: {params.q}",
        f"- a_target: {params.a_target}",
        f"- phi(q): {phi_q}",
        f"- max abs error: {float(errs.max()):.3e}",
        "",
        "Figure:",
        "- fig_01_indicator_error.png",
        "",
        "Notes:",
        "- The identity holds on units (gcd(n,q)=1). Non-units are outside the unit group, and χ(n)=0 there.",
        "",
    ]

    write_json(paths.params_path, asdict(params))
    write_text(paths.report_path, "\n".join(lines))
    return 0
