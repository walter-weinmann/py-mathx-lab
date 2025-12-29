"""E067 — Gauss sums: magnitude vs sqrt(q).

For a Dirichlet character χ modulo q, define the Gauss sum

    τ(χ) = ∑_{a=0}^{q-1} χ(a) * exp(2π i a / q).

For primitive characters, a classical theorem gives |τ(χ)| = sqrt(q)
(up to conventions). For prime q=p, every nonprincipal character is primitive,
so the pattern becomes very clean.

Usage:
    make run EXP=e067

Artifacts:
    - figures/fig_01_gauss_sum_magnitudes.png
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
from mathxlab.exp.io import prepare_out_dir, save_figure, write_json, write_text
from mathxlab.nt.dirichlet import all_characters, euler_phi


# ------------------------------------------------------------------------------
@dataclass(frozen=True)
class Params:
    """Parameters for E067.

    Attributes:
        q: Modulus (choose a prime for the clearest picture).
    """

    q: int = 7


# ------------------------------------------------------------------------------
def _gauss_sum(*, q: int, chi_vals: np.ndarray) -> complex:
    """Compute τ(χ) from χ(a) values for a=0..q-1."""
    a = np.arange(q, dtype=np.float64)
    z = np.exp(2j * np.pi * a / float(q))
    return complex(np.sum(chi_vals * z))


# ------------------------------------------------------------------------------
def _plot_magnitudes(*, mags: np.ndarray, q: int) -> fig.Figure:
    """Plot |τ(χ)| for each character index."""
    fig_obj, ax = plt.subplots()
    x = np.arange(mags.size)
    ax.bar(x, mags)
    ax.axhline(np.sqrt(float(q)), linestyle="--", linewidth=1.5, label=r"$\sqrt{q}$")
    ax.set_title(rf"Gauss sum magnitudes $|\tau(\chi)|$ (q={q})")
    ax.set_xlabel("Character index")
    ax.set_ylabel(r"$|\tau(\chi)|$")
    ax.legend(loc="best")
    return fig_obj


# ------------------------------------------------------------------------------
def main(argv: list[str] | None = None) -> int:
    """Run E067."""
    args = parse_experiment_args(argv=argv)
    params = Params()

    paths = prepare_out_dir(out_dir=Path(args.out_dir))

    chars = all_characters(params.q)
    tables = np.array([c.table() for c in chars], dtype=np.complex128)  # (phi(q), q)
    taus = np.array([_gauss_sum(q=params.q, chi_vals=row) for row in tables], dtype=np.complex128)
    mags = np.abs(taus).astype(np.float64)

    fig1 = _plot_magnitudes(mags=mags, q=params.q)
    save_figure(out_dir=paths.figures_dir, name="fig_01_gauss_sum_magnitudes", fig=fig1)

    # A quick summary excluding the principal character (index 0 by construction).
    nontrivial = mags[1:] if mags.size > 1 else mags
    lines = [
        "# E067 — Gauss sums",
        "",
        f"- q: {params.q}",
        f"- phi(q): {euler_phi(params.q)}",
        f"- sqrt(q): {float(np.sqrt(float(params.q))):.6f}",
        f"- mean |tau| (nontrivial): {float(nontrivial.mean()):.6f}",
        f"- min/max |tau| (nontrivial): {float(nontrivial.min()):.6f} / {float(nontrivial.max()):.6f}",
        "",
        "Figure:",
        "- fig_01_gauss_sum_magnitudes.png",
        "",
        "Notes:",
        "- For prime q, nonprincipal characters are primitive, and |tau(chi)| clusters near sqrt(q).",
        "",
    ]

    write_json(paths.params_path, asdict(params))
    write_text(paths.report_path, "\n".join(lines))
    return 0
