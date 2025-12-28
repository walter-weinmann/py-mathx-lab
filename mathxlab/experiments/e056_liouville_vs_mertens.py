"""E056 — Liouville vs Möbius: two ±1 walks built from prime factors.

Liouville's function is:

    λ(n) = (-1)^{Ω(n)}

where Ω(n) counts prime factors with multiplicity. Like Möbius μ(n), it produces
a ±1 sequence (without zeros). Summatory functions of μ and λ can both be plotted
as "walks" to compare their behavior.

Usage (repository convention):
    make run EXP=e056

Artifacts:
    - figures/fig_01_walks.png
"""

from __future__ import annotations

from dataclasses import asdict, dataclass

import matplotlib.figure as fig
import matplotlib.pyplot as plt

from mathxlab.exp.cli import parse_experiment_args
from mathxlab.exp.io import prepare_out_dir, save_figure, write_json, write_text
from mathxlab.exp.logging import LoggingConfig
from mathxlab.exp.logging_setup import setup_logging
from mathxlab.exp.seeding import set_global_seed
from mathxlab.nt.arithmetic import build_factor_sieve, compute_big_omega, compute_mobius, liouville


# ------------------------------------------------------------------------------
@dataclass(frozen=True)
class Params:
    """Experiment parameters.

    Attributes:
        n_max: Maximum x.
    """

    n_max: int = 300_000


# ------------------------------------------------------------------------------
def _prefix_sum(values: list[int], n_max: int) -> list[int]:
    """Compute prefix sums.

    Args:
        values: Values indexed by n.
        n_max: Maximum index.

    Returns:
        Prefix sums s[x] = sum_{n<=x} values[n].
    """
    out = [0] * (n_max + 1)
    s = 0
    for x in range(1, n_max + 1):
        s += values[x]
        out[x] = s
    return out


# ------------------------------------------------------------------------------
def _plot_walks(n_max: int, M: list[int], L: list[int]) -> fig.Figure:
    """Plot Mertens and Liouville summatory walks.

    Args:
        n_max: Maximum x.
        M: Mertens prefix.
        L: Liouville prefix.

    Returns:
        Figure.
    """
    xs = list(range(1, n_max + 1))
    f = plt.figure()
    ax = f.add_subplot(1, 1, 1)
    ax.plot(xs, [M[x] for x in xs], linewidth=0.8, label=r"$M(x)=\sum_{n\leq x}\mu(n)$")
    ax.plot(xs, [L[x] for x in xs], linewidth=0.8, label=r"$L(x)=\sum_{n\leq x}\lambda(n)$")
    ax.set_title("Summatory walks: Möbius vs Liouville")
    ax.set_xlabel(r"$x$")
    ax.set_ylabel("Partial sum")
    ax.set_xlim(1, n_max)
    ax.legend()
    return f


# ------------------------------------------------------------------------------
def main() -> int:
    """Run the experiment.

    Returns:
        Exit code.
    """
    args = parse_experiment_args(
        experiment_id="e056",
        description="Liouville vs Möbius: compare summatory walks",
    )
    setup_logging(config=LoggingConfig(verbose=args.verbose))
    set_global_seed(args.seed)

    params = Params()
    paths = prepare_out_dir(out_dir=args.out_dir)

    sieve = build_factor_sieve(params.n_max)
    mu = compute_mobius(params.n_max, sieve=sieve)
    big_omega = compute_big_omega(params.n_max, sieve=sieve)
    lam = [0] * (params.n_max + 1)
    for n in range(1, params.n_max + 1):
        lam[n] = liouville(big_omega[n])

    M = _prefix_sum(mu, params.n_max)
    L = _prefix_sum(lam, params.n_max)

    fig1 = _plot_walks(params.n_max, M, L)
    save_figure(out_dir=paths.figures_dir, name="fig_01_walks", fig=fig1)

    lines = [
        "# E056 — Liouville vs Möbius",
        "",
        f"- n_max: {params.n_max}",
        f"- M(n_max) = {M[params.n_max]}",
        f"- L(n_max) = {L[params.n_max]}",
        "",
        "Figure:",
        "- fig_01_walks.png",
        "",
    ]

    write_json(paths.params_path, asdict(params))
    write_text(paths.report_path, "\n".join(lines), encoding="utf-8")
    return 0
