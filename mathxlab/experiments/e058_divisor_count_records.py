"""E058: Divisor count τ(n): record values and highly composite behavior.

The divisor-counting function τ(n) counts the number of divisors of n.
Record values of τ(n) are attained at "highly composite"-like integers with many
small prime factors.

This experiment computes τ(n) up to N and plots:
- τ(n) for n<=N (thin), and
- record highs of τ(n) (highlighted).

Usage (repository convention):
    make run EXP=e058

Artifacts:
    - figures/fig_01_tau_records.png
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
from mathxlab.nt.arithmetic import build_factor_sieve, compute_tau_sigma


# ------------------------------------------------------------------------------
@dataclass(frozen=True)
class Params:
    """Experiment parameters.

    Attributes:
        n_max: Maximum n.
    """

    n_max: int = 300_000


# ------------------------------------------------------------------------------
def _plot_tau_records(n_max: int, tau: list[int]) -> fig.Figure:
    """Plot τ(n) and record highs.

    Args:
        n_max: Maximum n.
        tau: τ values.

    Returns:
        Figure.
    """
    xs = list(range(1, n_max + 1))

    record_x: list[int] = []
    record_y: list[int] = []
    best = 0
    for n in range(1, n_max + 1):
        if tau[n] > best:
            best = tau[n]
            record_x.append(n)
            record_y.append(tau[n])

    f = plt.figure()
    ax = f.add_subplot(1, 1, 1)
    ax.plot(xs, [tau[n] for n in xs], linewidth=0.5, label=r"$\tau(n)$")
    ax.plot(record_x, record_y, marker="o", linewidth=1.0, markersize=3, label="record highs")
    ax.set_title(r"Divisor count records: $\tau(n)$ up to N")
    ax.set_xlabel(r"$n$")
    ax.set_ylabel(r"$\tau(n)$")
    ax.set_xscale("log")
    ax.legend()
    return f


# ------------------------------------------------------------------------------
def main() -> int:
    """Run the experiment.

    Returns:
        Exit code.
    """
    args = parse_experiment_args(
        experiment_id="e058",
        description="Divisor count τ(n): record values and highly composite behavior",
    )

    run_log = infer_run_log_file(out_dir=args.out_dir, experiment_slug="e058")
    setup_logging(config=LoggingConfig(verbose=args.verbose, log_file=run_log.log_file))
    set_global_seed(args.seed)

    params = Params()
    paths = prepare_out_dir(out_dir=args.out_dir)

    sieve = build_factor_sieve(params.n_max)
    tau, _sigma = compute_tau_sigma(params.n_max, sieve=sieve)

    fig1 = _plot_tau_records(params.n_max, tau)
    save_figure(out_dir=paths.figures_dir, name="fig_01_tau_records", fig=fig1)

    best = max(tau[1:])
    n_best = tau[1:].index(best) + 1

    lines = [
        "# E058: Divisor count records",
        "",
        f"- n_max: {params.n_max}",
        f"- max τ(n) in range: {best} at n={n_best}",
        "",
        "Figure:",
        "- fig_01_tau_records.png",
        "",
    ]
    write_json(paths.params_path, asdict(params))
    write_text(paths.report_path, "\n".join(lines), encoding="utf-8")
    return 0
