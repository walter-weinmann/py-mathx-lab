"""E059 — Abundancy index: σ(n)/n and the perfect-number threshold.

The abundancy index is σ(n)/n where σ(n) is the sum-of-divisors function.
Perfect numbers satisfy σ(n)/n = 2.

This experiment computes σ(n)/n up to N and highlights:
- the distribution of σ(n)/n,
- the top values in the range.

Usage (repository convention):
    make run EXP=e059

Artifacts:
    - figures/fig_01_sigma_over_n.png
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
from mathxlab.nt.arithmetic import build_factor_sieve, compute_tau_sigma


# ------------------------------------------------------------------------------
@dataclass(frozen=True)
class Params:
    """Experiment parameters.

    Attributes:
        n_max: Maximum n.
        top_k: Number of top abundancy values to list in the report.
    """

    n_max: int = 200_000
    top_k: int = 12


# ------------------------------------------------------------------------------
def _plot_sigma_over_n(n_max: int, sigma: list[int]) -> fig.Figure:
    """Plot σ(n)/n and the line y=2.

    Args:
        n_max: Maximum n.
        sigma: σ values.

    Returns:
        Figure.
    """
    xs = list(range(1, n_max + 1))
    ys = [sigma[n] / n for n in xs]

    f = plt.figure()
    ax = f.add_subplot(1, 1, 1)
    ax.plot(xs, ys, linewidth=0.7)
    ax.axhline(2.0, linestyle="--", linewidth=1.0, label=r"perfect threshold $\sigma(n)/n=2$")
    ax.set_title(r"Abundancy index landscape: $\sigma(n)/n$")
    ax.set_xlabel(r"$n$")
    ax.set_ylabel(r"$\sigma(n)/n$")
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
        experiment_id="e059",
        description="Abundancy index σ(n)/n and perfect-number threshold",
    )
    setup_logging(config=LoggingConfig(verbose=args.verbose))
    set_global_seed(args.seed)

    params = Params()
    paths = prepare_out_dir(out_dir=args.out_dir)

    sieve = build_factor_sieve(params.n_max)
    _tau, sigma = compute_tau_sigma(params.n_max, sieve=sieve)

    fig1 = _plot_sigma_over_n(params.n_max, sigma)
    save_figure(out_dir=paths.figures_dir, name="fig_01_sigma_over_n", fig=fig1)

    top: list[tuple[float, int]] = []
    for n in range(2, params.n_max + 1):
        top.append((sigma[n] / n, n))
    top.sort(reverse=True)
    top_k = top[: params.top_k]

    lines: list[str] = []
    lines.append("# E059 — Abundancy index σ(n)/n")
    lines.append("")
    lines.append(f"- n_max: {params.n_max}")
    lines.append("")
    lines.append(f"Top {params.top_k} values of σ(n)/n (value, n):")
    lines.append("")
    for v, n in top_k:
        lines.append(f"- {v:>8.5f} at n={n}")
    lines.append("")
    lines.append("Figure:")
    lines.append("- fig_01_sigma_over_n.png")
    lines.append("")

    write_json(paths.params_path, asdict(params))
    write_text(paths.report_path, "\n".join(lines), encoding="utf-8")
    return 0
