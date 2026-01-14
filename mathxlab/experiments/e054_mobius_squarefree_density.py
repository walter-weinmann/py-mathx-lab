"""E054: Möbius μ(n) and squarefree density via μ(n)^2.

The Möbius function μ(n) is:
- 0 if n is divisible by a square prime factor,
- (-1)^k if n is squarefree with k distinct prime factors.

The indicator μ(n)^2 equals 1 exactly for squarefree n. The density of squarefree
integers is 6/π^2.

This experiment computes μ(n) up to N and plots the running proportion of
squarefree integers.

Usage (repository convention):
    make run EXP=e054

Artifacts:
    - figures/fig_01_squarefree_density.png
"""

from __future__ import annotations

import math
from dataclasses import asdict, dataclass

import matplotlib.figure as fig
import matplotlib.pyplot as plt

from mathxlab.exp.cli import parse_experiment_args
from mathxlab.exp.io import prepare_out_dir, save_figure, write_json, write_text
from mathxlab.exp.logging import LoggingConfig
from mathxlab.exp.logging_setup import setup_logging
from mathxlab.exp.run_logging import infer_run_log_file
from mathxlab.exp.seeding import set_global_seed
from mathxlab.nt.arithmetic import build_factor_sieve, compute_mobius


# ------------------------------------------------------------------------------
@dataclass(frozen=True)
class Params:
    """Experiment parameters.

    Attributes:
        n_max: Maximum n to compute.
    """

    n_max: int = 300_000


# ------------------------------------------------------------------------------
def _plot_squarefree_density(n_max: int, mu: list[int]) -> fig.Figure:
    """Plot running proportion of squarefree integers.

    Args:
        n_max: Maximum n.
        mu: Möbius values.

    Returns:
        Figure.
    """
    xs: list[int] = []
    ys: list[float] = []

    sqfree = 0
    for n in range(1, n_max + 1):
        if mu[n] != 0:
            sqfree += 1
        if n % 200 == 0:
            xs.append(n)
            ys.append(sqfree / n)

    target = 6.0 / (math.pi * math.pi)

    f = plt.figure()
    ax = f.add_subplot(1, 1, 1)
    ax.plot(xs, ys, linewidth=1.0, label=r"running $\#\{k\leq n: \mu(k)\neq 0\}/n$")
    ax.axhline(target, linestyle="--", linewidth=1.0, label=r"$6/\pi^2$")
    ax.set_title("Squarefree density via μ(n)²")
    ax.set_xlabel(r"$n$")
    ax.set_ylabel("Proportion")
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
        experiment_id="e054",
        description="Möbius μ(n) and squarefree density via μ(n)^2",
    )

    run_log = infer_run_log_file(out_dir=args.out_dir, experiment_slug="e054")
    setup_logging(config=LoggingConfig(verbose=args.verbose, log_file=run_log.log_file))
    set_global_seed(args.seed)

    params = Params()
    paths = prepare_out_dir(out_dir=args.out_dir)

    sieve = build_factor_sieve(params.n_max)
    mu = compute_mobius(params.n_max, sieve=sieve)

    fig1 = _plot_squarefree_density(params.n_max, mu)
    save_figure(out_dir=paths.figures_dir, name="fig_01_squarefree_density", fig=fig1)

    sqfree = sum(1 for n in range(1, params.n_max + 1) if mu[n] != 0)
    approx = sqfree / params.n_max
    target = 6.0 / (math.pi * math.pi)

    lines = [
        "# E054: Möbius and squarefree density",
        "",
        f"- n_max: {params.n_max}",
        f"- observed squarefree proportion: {approx:.6f}",
        f"- theoretical density 6/pi^2:     {target:.6f}",
        "",
        "Figure:",
        "- fig_01_squarefree_density.png",
        "",
    ]

    write_json(paths.params_path, asdict(params))
    write_text(paths.report_path, "\n".join(lines), encoding="utf-8")
    return 0
