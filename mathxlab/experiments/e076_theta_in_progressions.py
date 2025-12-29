"""E076 — Chebyshev θ(x;q,a): weighted prime counts in progressions.

Define the Chebyshev theta function in a residue class:

    θ(x; q, a) = ∑_{p <= x, p ≡ a (mod q)} log p.

For reduced residue classes, one expects θ(x;q,a) ≈ x/φ(q).

This experiment visualizes the ratio:

    R_a(x) = θ(x;q,a) / (x/φ(q))

for the mod 4 classes a=1 and a=3.

Usage:
    make run EXP=e076

Artifacts:
    - figures/fig_01_theta_ratios.png
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
from mathxlab.exp.logging import LoggingConfig, get_logger, setup_logging
from mathxlab.exp.random import set_global_seed
from mathxlab.exp.io import prepare_out_dir, save_figure, write_json, write_text
from mathxlab.experiments._prime_utils import primes_up_to
from mathxlab.experiments._ap_utils import sample_grid
from mathxlab.nt.dirichlet import euler_phi

# ------------------------------------------------------------------------------
logger = get_logger(__name__)



# ------------------------------------------------------------------------------
@dataclass(frozen=True)
class Params:
    """Parameters for E076."""

    q: int = 4
    residues: tuple[int, ...] = (1, 3)
    x_max: int = 5_000_000
    n_points: int = 900
    log_grid: bool = True


# ------------------------------------------------------------------------------
def _theta_trace(*, primes: np.ndarray, q: int, a: int, xs: np.ndarray) -> np.ndarray:
    """Compute θ(xs; q,a) using cumulative sums over primes."""
    mask = (primes % q) == (a % q)
    p_a = primes[mask]
    logs = np.log(p_a.astype(np.float64))
    csum = np.cumsum(logs)
    idx = np.searchsorted(p_a, xs, side="right") - 1
    out = np.zeros_like(xs, dtype=np.float64)
    ok = idx >= 0
    out[ok] = csum[idx[ok]]
    return out


# ------------------------------------------------------------------------------
def _plot(*, xs: np.ndarray, ratios: dict[int, np.ndarray], q: int) -> fig.Figure:
    fig_obj, ax = plt.subplots()
    for a, y in ratios.items():
        ax.plot(xs, y, label=rf"$a={a}$")
    ax.axhline(1.0, linestyle="--", linewidth=1.2)
    ax.set_title(rf"Ratios $\theta(x;q,a)/(x/\varphi(q))$ for q={q}")
    ax.set_xlabel("x")
    ax.set_ylabel("ratio")
    ax.legend(loc="best")
    return fig_obj


# ------------------------------------------------------------------------------
def main(argv: list[str] | None = None) -> int:
    """Run E076."""
    args = parse_experiment_args(
        experiment_id="e076",
        description="Chebyshev θ(x;q,a): weighted prime counts in progressions.",
        argv=argv,
    )

    setup_logging(config=LoggingConfig(verbose=args.verbose))
    logger.info("Starting experiment E076: Chebyshev θ(x;q,a): weighted prime counts in progressions.")
    set_global_seed(args.seed)
    params = Params()
    paths = prepare_out_dir(out_dir=args.out_dir)

    for a in params.residues:
        if gcd(a, params.q) != 1:
            raise ValueError(f"Residue {a} is not coprime to q={params.q}")

    primes = primes_up_to(params.x_max)
    xs = sample_grid(x_max=params.x_max, n=params.n_points, log=params.log_grid)

    phi_q = euler_phi(params.q)
    ratios: dict[int, np.ndarray] = {}
    for a in params.residues:
        theta = _theta_trace(primes=primes, q=params.q, a=a, xs=xs)
        ratios[a] = theta / (xs / float(phi_q))

    fig1 = _plot(xs=xs, ratios=ratios, q=params.q)
    save_figure(out_dir=paths.figures_dir, name="fig_01_theta_ratios", fig=fig1)

    lines = [
        "# E076 — Chebyshev theta in progressions",
        "",
        f"- q: {params.q}",
        f"- residues: {list(params.residues)}",
        f"- x_max: {params.x_max}",
        "",
        "Figure:",
        "- fig_01_theta_ratios.png",
        "",
        "Notes:",
        "- Ratios fluctuate around 1 and encode distribution information beyond plain counts.",
        "",
    ]

    write_json(paths.params_path, asdict(params))
    write_text(paths.report_path, "\n".join(lines))
    return 0