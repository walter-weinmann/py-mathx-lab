"""E052: Totient ratio landscape: φ(n) / n and primorial structure.

Euler's totient function φ(n) counts integers 1<=k<=n that are coprime to n.
The ratio φ(n)/n equals:

    φ(n)/n = ∏_{p|n} (1 - 1/p)

This ratio becomes small when n has many small prime factors; record-low values
occur at primorial-like n.

Usage (repository convention):
    make run EXP=e052

Artifacts:
    - figures/fig_01_phi_over_n.png
    - figures/fig_02_record_lows.png
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
from mathxlab.nt.arithmetic import build_factor_sieve, compute_phi


# ------------------------------------------------------------------------------
@dataclass(frozen=True)
class Params:
    """Experiment parameters.

    Attributes:
        n_max: Maximum n to compute.
    """

    n_max: int = 200_000


# ------------------------------------------------------------------------------
def _plot_phi_over_n(n_max: int, phi: list[int]) -> fig.Figure:
    """Plot φ(n)/n for n=1..n_max.

    Args:
        n_max: Maximum n.
        phi: Totient values.

    Returns:
        Figure.
    """
    xs = list(range(1, n_max + 1))
    ys = [phi[n] / n for n in xs]

    f = plt.figure()
    ax = f.add_subplot(1, 1, 1)
    ax.plot(xs, ys, linewidth=0.8)
    ax.set_title(r"Totient ratio landscape: $\varphi(n)/n$")
    ax.set_xlabel(r"$n$")
    ax.set_ylabel(r"$\varphi(n)/n$")
    ax.set_xlim(1, n_max)
    return f


# ------------------------------------------------------------------------------
def _plot_record_lows(n_max: int, phi: list[int]) -> fig.Figure:
    """Plot record-low values of φ(n)/n.

    Args:
        n_max: Maximum n.
        phi: Totient values.

    Returns:
        Figure.
    """
    record_x: list[int] = []
    record_y: list[float] = []

    best = float("inf")
    for n in range(2, n_max + 1):
        r = phi[n] / n
        if r < best:
            best = r
            record_x.append(n)
            record_y.append(r)

    f = plt.figure()
    ax = f.add_subplot(1, 1, 1)
    ax.plot(record_x, record_y, marker="o", linewidth=1.0, markersize=3)
    ax.set_title(r"Record lows of $\varphi(n)/n$ (primorial-like structure)")
    ax.set_xlabel(r"$n$")
    ax.set_ylabel(r"$\varphi(n)/n$")
    ax.set_xscale("log")
    ax.set_ylim(0, max(record_y) * 1.05)
    return f


# ------------------------------------------------------------------------------
def main() -> int:
    """Run the experiment.

    Returns:
        Exit code.
    """
    args = parse_experiment_args(
        experiment_id="e052",
        description="Totient ratio landscape: φ(n)/n and primorial structure",
    )

    run_log = infer_run_log_file(out_dir=args.out_dir, experiment_slug="e052")
    setup_logging(config=LoggingConfig(verbose=args.verbose, log_file=run_log.log_file))
    set_global_seed(args.seed)

    params = Params()
    paths = prepare_out_dir(out_dir=args.out_dir)

    sieve = build_factor_sieve(params.n_max)
    phi = compute_phi(params.n_max, sieve=sieve)

    fig1 = _plot_phi_over_n(params.n_max, phi)
    fig2 = _plot_record_lows(params.n_max, phi)

    save_figure(out_dir=paths.figures_dir, name="fig_01_phi_over_n", fig=fig1)
    save_figure(out_dir=paths.figures_dir, name="fig_02_record_lows", fig=fig2)

    # Report
    ratios = [phi[n] / n for n in range(2, params.n_max + 1)]
    min_ratio = min(ratios)
    min_n = 2 + ratios.index(min_ratio)

    lines: list[str] = []
    lines.append("# E052: Totient ratio landscape")
    lines.append("")
    lines.append(f"- n_max: {params.n_max}")
    lines.append(f"- min φ(n)/n in range: {min_ratio:.6f} at n={min_n}")
    lines.append("")
    lines.append("Figures:")
    lines.append("- fig_01_phi_over_n.png")
    lines.append("- fig_02_record_lows.png")
    lines.append("")

    write_json(paths.params_path, asdict(params))
    write_text(paths.report_path, "\n".join(lines) + "\n", encoding="utf-8")
    return 0
