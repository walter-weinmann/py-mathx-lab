"""E062: Carmichael's λ(n) vs Euler's φ(n): exponent vs group size.

Carmichael's lambda function λ(n) is the exponent of the multiplicative group
(Z/nZ)^* . It satisfies λ(n) | φ(n), and can be much smaller than φ(n).

This experiment computes λ(n) and φ(n) for n<=N and plots:
- the ratio λ(n)/φ(n),
- a histogram of log10 λ(n).

Usage (repository convention):
    make run EXP=e062

Artifacts:
    - figures/fig_01_ratio_lambda_over_phi.png
    - figures/fig_02_log10_lambda_hist.png
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
from mathxlab.nt.arithmetic import build_factor_sieve, carmichael_lambda, compute_phi


# ------------------------------------------------------------------------------
@dataclass(frozen=True)
class Params:
    """Experiment parameters.

    Attributes:
        n_max: Maximum n.
        hist_bins: Histogram bins for log10 λ(n).
    """

    n_max: int = 120_000
    hist_bins: int = 60


# ------------------------------------------------------------------------------
def _plot_ratio(n_max: int, ratios: list[float]) -> fig.Figure:
    """Plot λ(n)/φ(n).

    Args:
        n_max: Maximum n.
        ratios: Ratio values for n=0..n_max.

    Returns:
        Figure.
    """
    xs = list(range(2, n_max + 1))
    ys = [ratios[n] for n in xs]

    f = plt.figure()
    ax = f.add_subplot(1, 1, 1)
    ax.plot(xs, ys, linewidth=0.7)
    ax.set_title(r"Ratio landscape: $\lambda(n)/\varphi(n)$")
    ax.set_xlabel(r"$n$")
    ax.set_ylabel(r"$\lambda(n)/\varphi(n)$")
    ax.set_xlim(2, n_max)
    return f


# ------------------------------------------------------------------------------
def _plot_log10_hist(n_max: int, lam_values: list[int], bins: int) -> fig.Figure:
    """Plot histogram of log10 λ(n).

    Args:
        n_max: Maximum n.
        lam_values: λ(n) for n=0..n_max.
        bins: Histogram bins.

    Returns:
        Figure.
    """
    samples = [math.log10(lam_values[n]) for n in range(2, n_max + 1) if lam_values[n] > 0]

    f = plt.figure()
    ax = f.add_subplot(1, 1, 1)
    ax.hist(samples, bins=bins, edgecolor="black", linewidth=0.3)
    ax.set_title(r"Histogram of $\log_{10} \lambda(n)$")
    ax.set_xlabel(r"$\log_{10}\lambda(n)$")
    ax.set_ylabel("Count")
    return f


# ------------------------------------------------------------------------------
def main() -> int:
    """Run the experiment.

    Returns:
        Exit code.
    """
    args = parse_experiment_args(
        experiment_id="e062",
        description="Carmichael λ(n) vs Euler φ(n)",
    )

    run_log = infer_run_log_file(out_dir=args.out_dir, experiment_slug="e062")
    setup_logging(config=LoggingConfig(verbose=args.verbose, log_file=run_log.log_file))
    set_global_seed(args.seed)

    params = Params()
    paths = prepare_out_dir(out_dir=args.out_dir)

    sieve = build_factor_sieve(params.n_max)
    phi = compute_phi(params.n_max, sieve=sieve)

    lam_values = [0] * (params.n_max + 1)
    ratios = [0.0] * (params.n_max + 1)
    for n in range(1, params.n_max + 1):
        lam_values[n] = carmichael_lambda(n, sieve=sieve)
        if n >= 2 and phi[n] > 0:
            ratios[n] = lam_values[n] / phi[n]

    fig1 = _plot_ratio(params.n_max, ratios)
    fig2 = _plot_log10_hist(params.n_max, lam_values, params.hist_bins)

    save_figure(out_dir=paths.figures_dir, name="fig_01_ratio_lambda_over_phi", fig=fig1)
    save_figure(out_dir=paths.figures_dir, name="fig_02_log10_lambda_hist", fig=fig2)

    min_ratio = min(ratios[2:])
    max_ratio = max(ratios[2:])

    lines = [
        "# E062: Carmichael λ(n) vs φ(n)",
        "",
        f"- n_max: {params.n_max}",
        f"- min λ/φ: {min_ratio:.6f}",
        f"- max λ/φ: {max_ratio:.6f}",
        "",
        "Figures:",
        "- fig_01_ratio_lambda_over_phi.png",
        "- fig_02_log10_lambda_hist.png",
        "",
    ]

    write_json(paths.params_path, asdict(params))
    write_text(paths.report_path, "\n".join(lines), encoding="utf-8")
    return 0
