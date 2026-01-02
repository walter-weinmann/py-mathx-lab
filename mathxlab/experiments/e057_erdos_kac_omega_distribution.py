"""E057 — Erdős–Kac in practice: Ω(n) looks Gaussian after normalization.

The Erdős–Kac theorem states that the number of prime factors (with multiplicity)
of a random integer behaves like a normal random variable after suitable
normalization.

This experiment:
- computes Ω(n) for n<=N,
- normalizes using log log N,
- shows a histogram and overlays the standard normal density.

Usage (repository convention):
    make run EXP=e057

Artifacts:
    - figures/fig_01_erdos_kac_hist.png
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
from mathxlab.nt.arithmetic import build_factor_sieve, compute_big_omega


# ------------------------------------------------------------------------------
@dataclass(frozen=True)
class Params:
    """Experiment parameters.

    Attributes:
        n_max: Maximum n.
        bins: Histogram bins.
    """

    n_max: int = 400_000
    bins: int = 60


# ------------------------------------------------------------------------------
def _std_normal_pdf(x: float) -> float:
    """Standard normal PDF.

    Args:
        x: Point.

    Returns:
        Density value.
    """
    return math.exp(-0.5 * x * x) / math.sqrt(2.0 * math.pi)


# ------------------------------------------------------------------------------
def _plot_erdos_kac(n_max: int, big_omega: list[int], bins: int) -> fig.Figure:
    """Plot normalized Ω(n) histogram and overlay standard normal density.

    Args:
        n_max: Maximum n.
        big_omega: Ω(n) values.
        bins: Histogram bins.

    Returns:
        Figure.
    """
    mu = math.log(math.log(n_max))
    sigma = math.sqrt(mu)

    samples: list[float] = []
    for n in range(3, n_max + 1):
        z = (big_omega[n] - mu) / sigma
        samples.append(z)

    f = plt.figure()
    ax = f.add_subplot(1, 1, 1)
    ax.hist(samples, bins=bins, density=True, edgecolor="black", linewidth=0.3)
    xs = [(-4.0 + 8.0 * i / 400.0) for i in range(401)]
    ax.plot(xs, [_std_normal_pdf(x) for x in xs], linewidth=1.2, label="standard normal")
    ax.set_title(r"Erdős–Kac: histogram of $(\Omega(n)-\log\log N)/\sqrt{\log\log N}$")
    ax.set_xlabel("Normalized value")
    ax.set_ylabel("Density")
    ax.legend()
    return f


# ------------------------------------------------------------------------------
def main() -> int:
    """Run the experiment.

    Returns:
        Exit code.
    """
    args = parse_experiment_args(
        experiment_id="e057",
        description="Erdős–Kac in practice: normalized Ω(n) looks Gaussian",
    )

    run_log = infer_run_log_file(out_dir=args.out_dir, experiment_slug="e057")
    setup_logging(config=LoggingConfig(verbose=args.verbose, log_file=run_log.log_file))
    set_global_seed(args.seed)

    params = Params()
    paths = prepare_out_dir(out_dir=args.out_dir)

    sieve = build_factor_sieve(params.n_max)
    big_omega = compute_big_omega(params.n_max, sieve=sieve)

    fig1 = _plot_erdos_kac(params.n_max, big_omega, params.bins)
    save_figure(out_dir=paths.figures_dir, name="fig_01_erdos_kac_hist", fig=fig1)

    lines = [
        "# E057 — Erdős–Kac histogram",
        "",
        f"- n_max: {params.n_max}",
        f"- bins: {params.bins}",
        "",
        "Figure:",
        "- fig_01_erdos_kac_hist.png",
        "",
    ]

    write_json(paths.params_path, asdict(params))
    write_text(paths.report_path, "\n".join(lines), encoding="utf-8")
    return 0
