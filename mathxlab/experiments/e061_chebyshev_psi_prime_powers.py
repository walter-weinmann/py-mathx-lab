"""E061: von Mangoldt Λ(n) and Chebyshev ψ(x): jumps at prime powers.

The von Mangoldt function is:
- Λ(n) = log p if n is a prime power p^k,
- 0 otherwise.

Chebyshev's ψ(x) is the summatory function:
    ψ(x) = ∑_{n≤x} Λ(n)

This experiment computes ψ(x) up to N and plots ψ(x) vs x and the error ψ(x)-x.

Usage (repository convention):
    make run EXP=e061

Artifacts:
    - figures/fig_01_psi_vs_x.png
    - figures/fig_02_psi_minus_x.png
"""

from __future__ import annotations

from dataclasses import asdict, dataclass

import matplotlib.figure as fig
import matplotlib.pyplot as plt

from mathxlab.exp.cli import parse_experiment_args
from mathxlab.exp.io import prepare_out_dir, save_figure, write_json, write_text
from mathxlab.exp.logging import LoggingConfig
from mathxlab.exp.logging_setup import setup_logging
from mathxlab.exp.run_logging import infer_run_log_file
from mathxlab.exp.seeding import set_global_seed
from mathxlab.nt.arithmetic import build_factor_sieve, chebyshev_psi


# ------------------------------------------------------------------------------
@dataclass(frozen=True)
class Params:
    """Experiment parameters.

    Attributes:
        n_max: Maximum x.
    """

    n_max: int = 400_000


# ------------------------------------------------------------------------------
def _plot_psi_vs_x(n_max: int, psi: list[float]) -> fig.Figure:
    """Plot ψ(x) and x.

    Args:
        n_max: Maximum x.
        psi: ψ values.

    Returns:
        Figure.
    """
    xs = list(range(1, n_max + 1))
    f = plt.figure()
    ax = f.add_subplot(1, 1, 1)
    ax.plot(xs, [psi[x] for x in xs], linewidth=0.8, label=r"$\psi(x)$")
    ax.plot(xs, xs, linewidth=0.8, label=r"$x$")
    ax.set_title(r"Chebyshev $\psi(x)$ vs $x$")
    ax.set_xlabel(r"$x$")
    ax.set_ylabel("Value")
    ax.set_xlim(1, n_max)
    ax.legend()
    return f


# ------------------------------------------------------------------------------
def _plot_psi_minus_x(n_max: int, psi: list[float]) -> fig.Figure:
    """Plot ψ(x)-x.

    Args:
        n_max: Maximum x.
        psi: ψ values.

    Returns:
        Figure.
    """
    xs = list(range(1, n_max + 1))
    ys = [psi[x] - x for x in xs]

    f = plt.figure()
    ax = f.add_subplot(1, 1, 1)
    ax.plot(xs, ys, linewidth=0.8)
    ax.axhline(0.0, linewidth=1.0)
    ax.set_title(r"Error curve: $\psi(x)-x$")
    ax.set_xlabel(r"$x$")
    ax.set_ylabel(r"$\psi(x)-x$")
    ax.set_xlim(1, n_max)
    return f


# ------------------------------------------------------------------------------
def main() -> int:
    """Run the experiment.

    Returns:
        Exit code.
    """
    args = parse_experiment_args(
        experiment_id="e061",
        description="von Mangoldt Λ(n) and Chebyshev ψ(x): jumps at prime powers",
    )

    run_log = infer_run_log_file(out_dir=args.out_dir, experiment_slug="e061")
    setup_logging(config=LoggingConfig(verbose=args.verbose, log_file=run_log.log_file))
    set_global_seed(args.seed)

    params = Params()
    paths = prepare_out_dir(out_dir=args.out_dir)

    sieve = build_factor_sieve(params.n_max)
    psi = chebyshev_psi(params.n_max, sieve=sieve)

    fig1 = _plot_psi_vs_x(params.n_max, psi)
    fig2 = _plot_psi_minus_x(params.n_max, psi)

    save_figure(out_dir=paths.figures_dir, name="fig_01_psi_vs_x", fig=fig1)
    save_figure(out_dir=paths.figures_dir, name="fig_02_psi_minus_x", fig=fig2)

    lines = [
        "# E061: Chebyshev ψ(x)",
        "",
        f"- n_max: {params.n_max}",
        f"- ψ(n_max) - n_max: {psi[params.n_max] - params.n_max:+.3f}",
        "",
        "Figures:",
        "- fig_01_psi_vs_x.png",
        "- fig_02_psi_minus_x.png",
        "",
    ]

    write_json(paths.params_path, asdict(params))
    write_text(paths.report_path, "\n".join(lines), encoding="utf-8")
    return 0
