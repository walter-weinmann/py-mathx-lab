"""E060 — Jordan totients J_k(n): normalized landscapes for k=1..3.

Jordan's totient function generalizes Euler's totient:

    J_k(n) = n^k ∏_{p|n} (1 - 1/p^k)

For k=1, J_1 = φ.

This experiment computes J_k(n)/n^k for k=1..3 and plots them to show how the
normalization depends on k.

Usage (repository convention):
    make run EXP=e060

Artifacts:
    - figures/fig_01_jordan_normalized.png
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
from mathxlab.nt.arithmetic import FactorSieve, build_factor_sieve, jordan_totient


# ------------------------------------------------------------------------------
@dataclass(frozen=True)
class Params:
    """Experiment parameters.

    Attributes:
        n_max: Maximum n.
    """

    n_max: int = 80_000


# ------------------------------------------------------------------------------
def _plot_jordan_normalized(n_max: int, sieve: FactorSieve) -> fig.Figure:
    """Plot J_k(n)/n^k for k=1..3.

    Args:
        n_max: Maximum n.
        sieve: Factor sieve.

    Returns:
        Figure.
    """
    xs = list(range(1, n_max + 1))

    y1 = [jordan_totient(n, 1, sieve=sieve) / (n**1) for n in xs]
    y2 = [jordan_totient(n, 2, sieve=sieve) / (n**2) for n in xs]
    y3 = [jordan_totient(n, 3, sieve=sieve) / (n**3) for n in xs]

    f = plt.figure()
    ax = f.add_subplot(1, 1, 1)
    ax.plot(xs, y1, linewidth=0.8, label=r"$J_1(n)/n$")
    ax.plot(xs, y2, linewidth=0.8, label=r"$J_2(n)/n^2$")
    ax.plot(xs, y3, linewidth=0.8, label=r"$J_3(n)/n^3$")
    ax.set_title("Jordan totients (normalized)")
    ax.set_xlabel(r"$n$")
    ax.set_ylabel("Normalized value")
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
        experiment_id="e060",
        description="Jordan totients J_k(n): normalized landscapes for k=1..3",
    )
    setup_logging(config=LoggingConfig(verbose=args.verbose))
    set_global_seed(args.seed)

    params = Params()
    paths = prepare_out_dir(out_dir=args.out_dir)

    sieve = build_factor_sieve(params.n_max)
    fig1 = _plot_jordan_normalized(params.n_max, sieve)
    save_figure(out_dir=paths.figures_dir, name="fig_01_jordan_normalized", fig=fig1)

    lines = [
        "# E060 — Jordan totients",
        "",
        f"- n_max: {params.n_max}",
        "",
        "Figure:",
        "- fig_01_jordan_normalized.png",
        "",
    ]

    write_json(paths.params_path, asdict(params))
    write_text(paths.report_path, "\n".join(lines), encoding="utf-8")
    return 0
