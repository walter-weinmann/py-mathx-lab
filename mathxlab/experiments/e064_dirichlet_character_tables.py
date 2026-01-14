"""E064: Dirichlet character tables (phase view).

This experiment enumerates all Dirichlet characters modulo a small modulus q and
visualizes the values χ(a) for residues a=0..q-1.

To make complex-valued characters visible in one heatmap, we plot the **phase**
(angle) of χ(a) on the unit circle, and treat non-units (gcd(a,q)>1) as missing.

Usage (repository convention):
    make run EXP=e064

Artifacts:
    - figures/fig_01_character_phases.png
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
from mathxlab.nt.dirichlet import character_table, euler_phi

# ------------------------------------------------------------------------------
logger = get_logger(__name__)


# ------------------------------------------------------------------------------
@dataclass(frozen=True)
class Params:
    """Parameters for E064.

    Attributes:
        q: Modulus for the character table.
    """

    q: int = 5


# ------------------------------------------------------------------------------
def _phase_matrix(*, table: np.ndarray, q: int) -> np.ndarray:
    """Convert a character table to a phase matrix with NaN for non-units.

    Args:
        table: Complex matrix of shape (phi(q), q).
        q: Modulus.

    Returns:
        Float matrix of phases in [-pi, pi], with NaN where gcd(a,q)>1.
    """
    phases = np.angle(table).astype(np.float64)
    for a in range(q):
        if gcd(a, q) != 1:
            phases[:, a] = np.nan
    return phases


# ------------------------------------------------------------------------------
def _plot_phases(*, phases: np.ndarray, q: int) -> fig.Figure:
    """Plot phase matrix as a heatmap.

    Args:
        phases: Phase matrix.
        q: Modulus.

    Returns:
        Matplotlib figure.
    """
    fig_obj, ax = plt.subplots()
    im = ax.imshow(phases, aspect="auto")
    ax.set_title(rf"Dirichlet characters modulo $q={q}$ (phase of $\chi(a)$)")
    ax.set_xlabel("Residue a (mod q)")
    ax.set_ylabel("Character index")
    ax.set_xticks(np.arange(q))
    fig_obj.colorbar(im, ax=ax, fraction=0.046, pad=0.04, label="phase (radians)")
    return fig_obj


# ------------------------------------------------------------------------------
def main(argv: list[str] | None = None) -> int:
    """Run E064.

    Args:
        argv: Optional CLI args (for testing).

    Returns:
        Process exit code.
    """
    args = parse_experiment_args(
        experiment_id="e064",
        description="Dirichlet character tables (phase view).",
        argv=argv,
    )

    run_log = infer_run_log_file(out_dir=args.out_dir, experiment_slug="e064")
    setup_logging(config=LoggingConfig(verbose=args.verbose, log_file=run_log.log_file))
    logger.info("Starting experiment E064: Dirichlet character tables (phase view).")
    set_global_seed(args.seed)
    params = Params()

    paths = prepare_out_dir(out_dir=args.out_dir)

    table = character_table(params.q)
    phases = _phase_matrix(table=table, q=params.q)
    fig1 = _plot_phases(phases=phases, q=params.q)
    save_figure(out_dir=paths.figures_dir, name="fig_01_character_phases", fig=fig1)

    lines = [
        "# E064: Dirichlet character tables",
        "",
        f"- q: {params.q}",
        f"- phi(q): {euler_phi(params.q)}",
        "",
        "Figure:",
        "- fig_01_character_phases.png",
        "",
        "Notes:",
        "- Non-units (gcd(a,q)>1) are shown as missing values.",
        "- The principal character appears as the first row (all phases 0 on units).",
        "",
    ]

    write_json(paths.params_path, asdict(params))
    write_text(paths.report_path, "\n".join(lines))
    return 0
