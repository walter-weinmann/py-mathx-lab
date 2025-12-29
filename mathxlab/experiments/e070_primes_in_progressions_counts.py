"""E070 — Primes in residue classes: pi(x; q, a).

This experiment counts primes in selected reduced residue classes modulo q:

    π(x; q, a) = #{p <= x : p prime and p ≡ a (mod q)}.

We plot the count curves for a few classes to visualize the near-equidistribution
predicted by the prime number theorem in arithmetic progressions.

Usage:
    make run EXP=e070

Artifacts:
    - figures/fig_01_pi_x_q_a.png
    - params.json
    - report.md
"""

from __future__ import annotations

from dataclasses import asdict, dataclass
from math import gcd
from pathlib import Path

import matplotlib.figure as fig
import matplotlib.pyplot as plt
import numpy as np

from mathxlab.exp.cli import parse_experiment_args
from mathxlab.exp.io import prepare_out_dir, save_figure, write_json, write_text
from mathxlab.experiments._prime_utils import primes_up_to
from mathxlab.experiments._ap_utils import counts_in_residue_class, sample_grid
from mathxlab.nt.dirichlet import euler_phi


# ------------------------------------------------------------------------------
@dataclass(frozen=True)
class Params:
    """Parameters for E070.

    Attributes:
        q: Modulus.
        residues: Residue classes to track.
        x_max: Maximum x.
        n_points: Sample points for plotting.
    """

    q: int = 10
    residues: tuple[int, ...] = (1, 3, 7, 9)
    x_max: int = 1_000_000
    n_points: int = 700


# ------------------------------------------------------------------------------
def _plot(*, xs: np.ndarray, curves: dict[int, np.ndarray], q: int) -> fig.Figure:
    """Plot pi(x;q,a) curves."""
    fig_obj, ax = plt.subplots()
    for a, y in curves.items():
        ax.plot(xs, y, label=rf"$a={a}$")
    ax.set_title(rf"$\pi(x; q,a)$ for $q={q}$")
    ax.set_xlabel("x")
    ax.set_ylabel(r"$\pi(x; q,a)$")
    ax.legend(loc="best")
    return fig_obj


# ------------------------------------------------------------------------------
def main(argv: list[str] | None = None) -> int:
    """Run E070."""
    args = parse_experiment_args(argv=argv)
    params = Params()
    paths = prepare_out_dir(out_dir=Path(args.out_dir))

    # Validate residues.
    for a in params.residues:
        if gcd(a, params.q) != 1:
            raise ValueError(f"Residue {a} is not coprime to q={params.q}")

    primes = primes_up_to(params.x_max)
    xs = sample_grid(x_max=params.x_max, n=params.n_points, log=False)
    curves = {a: counts_in_residue_class(primes=primes, q=params.q, a=a, xs=xs) for a in params.residues}

    fig1 = _plot(xs=xs, curves=curves, q=params.q)
    save_figure(out_dir=paths.figures_dir, name="fig_01_pi_x_q_a", fig=fig1)

    phi_q = euler_phi(params.q)
    lines = [
        "# E070 — Primes in residue classes",
        "",
        f"- q: {params.q}",
        f"- phi(q): {phi_q}",
        f"- residues: {list(params.residues)}",
        f"- x_max: {params.x_max}",
        "",
        "Figure:",
        "- fig_01_pi_x_q_a.png",
        "",
        "Notes:",
        "- Curves should be close for large x (equidistribution among reduced residue classes).",
        "",
    ]

    write_json(paths.params_path, asdict(params))
    write_text(paths.report_path, "\n".join(lines))
    return 0
