"""E065 — Orthogonality matrix for Dirichlet characters.

For characters χ_i modulo q, orthogonality says:

    (1/φ(q)) * ∑_{a mod q, gcd(a,q)=1} χ_i(a) * conj(χ_j(a)) = δ_{i,j}.

This experiment computes the orthogonality matrix numerically and visualizes
the absolute error from the identity.

Usage:
    make run EXP=e065

Artifacts:
    - figures/fig_01_orthogonality_error.png
    - params.json
    - report.md
"""

from __future__ import annotations

from dataclasses import asdict, dataclass
from pathlib import Path

import matplotlib.figure as fig
import matplotlib.pyplot as plt
import numpy as np

from mathxlab.exp.cli import parse_experiment_args
from mathxlab.exp.logging import LoggingConfig, get_logger, setup_logging
from mathxlab.exp.random import set_global_seed
from mathxlab.exp.io import prepare_out_dir, save_figure, write_json, write_text
from mathxlab.nt.dirichlet import euler_phi, orthogonality_matrix

# ------------------------------------------------------------------------------
logger = get_logger(__name__)



# ------------------------------------------------------------------------------
@dataclass(frozen=True)
class Params:
    """Parameters for E065.

    Attributes:
        q: Modulus.
    """

    q: int = 12


# ------------------------------------------------------------------------------
def _plot_error(*, err: np.ndarray, q: int) -> fig.Figure:
    """Plot an absolute error matrix as a heatmap."""
    fig_obj, ax = plt.subplots()
    im = ax.imshow(err, aspect="auto")
    ax.set_title(rf"Orthogonality error for Dirichlet characters ($q={q}$)")
    ax.set_xlabel("j")
    ax.set_ylabel("i")
    fig_obj.colorbar(im, ax=ax, fraction=0.046, pad=0.04, label="|M - I|")
    return fig_obj


# ------------------------------------------------------------------------------
def main(argv: list[str] | None = None) -> int:
    """Run E065."""
    args = parse_experiment_args(
        experiment_id="e065",
        description="Orthogonality matrix for Dirichlet characters.",
        argv=argv,
    )

    setup_logging(config=LoggingConfig(verbose=args.verbose))
    logger.info("Starting experiment E065: Orthogonality matrix for Dirichlet characters.")
    set_global_seed(args.seed)
    params = Params()

    paths = prepare_out_dir(out_dir=args.out_dir)

    M = orthogonality_matrix(params.q)
    I = np.eye(M.shape[0], dtype=np.complex128)
    err = np.abs(M - I)

    fig1 = _plot_error(err=err, q=params.q)
    save_figure(out_dir=paths.figures_dir, name="fig_01_orthogonality_error", fig=fig1)

    lines = [
        "# E065 — Dirichlet orthogonality",
        "",
        f"- q: {params.q}",
        f"- phi(q): {euler_phi(params.q)}",
        f"- max |M - I|: {float(err.max()):.3e}",
        "",
        "Figure:",
        "- fig_01_orthogonality_error.png",
        "",
    ]

    write_json(paths.params_path, asdict(params))
    write_text(paths.report_path, "\n".join(lines))
    return 0