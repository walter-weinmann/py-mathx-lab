"""E055 — Mertens function walk: M(x)=∑_{n≤x} μ(n).

The Mertens function is the summatory Möbius function:

    M(x) = ∑_{n≤x} μ(n)

Empirically, M(x) behaves like a noisy walk. This experiment plots M(x) and a
scaled version M(x)/sqrt(x) on a finite prefix.

Usage (repository convention):
    make run EXP=e055

Artifacts:
    - figures/fig_01_mertens.png
    - figures/fig_02_mertens_scaled.png
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
        n_max: Maximum x.
    """

    n_max: int = 300_000


# ------------------------------------------------------------------------------
def _mertens_prefix(mu: list[int], n_max: int) -> list[int]:
    """Compute M(x) for x=0..n_max.

    Args:
        mu: Möbius values.
        n_max: Maximum x.

    Returns:
        List M where M[x] = sum_{n<=x} mu[n].
    """
    out = [0] * (n_max + 1)
    s = 0
    for x in range(1, n_max + 1):
        s += mu[x]
        out[x] = s
    return out


# ------------------------------------------------------------------------------
def _plot_mertens(n_max: int, M: list[int]) -> fig.Figure:
    """Plot M(x).

    Args:
        n_max: Maximum x.
        M: Mertens prefix.

    Returns:
        Figure.
    """
    xs = list(range(1, n_max + 1))
    ys = [M[x] for x in xs]

    f = plt.figure()
    ax = f.add_subplot(1, 1, 1)
    ax.plot(xs, ys, linewidth=0.8)
    ax.set_title(r"Mertens function $M(x)=\sum_{n\leq x}\mu(n)$")
    ax.set_xlabel(r"$x$")
    ax.set_ylabel(r"$M(x)$")
    ax.set_xlim(1, n_max)
    return f


# ------------------------------------------------------------------------------
def _plot_mertens_scaled(n_max: int, M: list[int]) -> fig.Figure:
    """Plot M(x)/sqrt(x).

    Args:
        n_max: Maximum x.
        M: Mertens prefix.

    Returns:
        Figure.
    """
    xs: list[int] = []
    ys: list[float] = []
    for x in range(1, n_max + 1, 5):
        xs.append(x)
        ys.append(M[x] / math.sqrt(x))

    f = plt.figure()
    ax = f.add_subplot(1, 1, 1)
    ax.plot(xs, ys, linewidth=0.8)
    ax.axhline(0.0, linewidth=1.0)
    ax.set_title(r"Scaled Mertens walk: $M(x)/\sqrt{x}$")
    ax.set_xlabel(r"$x$")
    ax.set_ylabel(r"$M(x)/\sqrt{x}$")
    ax.set_xlim(1, n_max)
    return f


# ------------------------------------------------------------------------------
def main() -> int:
    """Run the experiment.

    Returns:
        Exit code.
    """
    args = parse_experiment_args(
        experiment_id="e055",
        description="Mertens function walk: M(x)=sum_{n<=x} mu(n)",
    )

    run_log = infer_run_log_file(out_dir=args.out_dir, experiment_slug="e055")
    setup_logging(config=LoggingConfig(verbose=args.verbose, log_file=run_log.log_file))
    set_global_seed(args.seed)

    params = Params()
    paths = prepare_out_dir(out_dir=args.out_dir)

    sieve = build_factor_sieve(params.n_max)
    mu = compute_mobius(params.n_max, sieve=sieve)
    M = _mertens_prefix(mu, params.n_max)

    fig1 = _plot_mertens(params.n_max, M)
    fig2 = _plot_mertens_scaled(params.n_max, M)

    save_figure(out_dir=paths.figures_dir, name="fig_01_mertens", fig=fig1)
    save_figure(out_dir=paths.figures_dir, name="fig_02_mertens_scaled", fig=fig2)

    mx = max(abs(v) for v in M[1:])
    lines = [
        "# E055 — Mertens function walk",
        "",
        f"- n_max: {params.n_max}",
        f"- max |M(x)| in range: {mx}",
        "",
        "Figures:",
        "- fig_01_mertens.png",
        "- fig_02_mertens_scaled.png",
        "",
    ]

    write_json(paths.params_path, asdict(params))
    write_text(paths.report_path, "\n".join(lines), encoding="utf-8")
    return 0
