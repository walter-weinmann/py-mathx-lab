"""E053: Inverse totient: multiplicities of values φ(n)=m in a prefix.

The map n -> φ(n) is many-to-one. For a fixed bound N, we can count how many
n <= N share the same totient value.

This experiment:
- computes φ(n) for n<=N,
- counts multiplicities of m=φ(n),
- visualizes the multiplicity distribution and lists the top examples.

Usage (repository convention):
    make run EXP=e053

Artifacts:
    - figures/fig_01_multiplicity_hist.png
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
        hist_max: Histogram upper cap for multiplicity (bins beyond are grouped).
    """

    n_max: int = 200_000
    hist_max: int = 40


# ------------------------------------------------------------------------------
def _plot_multiplicity_hist(counts: list[int], hist_max: int) -> fig.Figure:
    """Plot histogram of multiplicities.

    Args:
        counts: Multiplicity counts for m in [0..max_phi].
        hist_max: Upper cap to show explicitly (tail grouped).

    Returns:
        Figure.
    """
    multiplicities = [c for c in counts if c > 0]

    capped: list[int] = []
    tail = 0
    for c in multiplicities:
        if c <= hist_max:
            capped.append(c)
        else:
            tail += 1

    f = plt.figure()
    ax = f.add_subplot(1, 1, 1)
    ax.hist(capped, bins=hist_max, range=(1, hist_max), edgecolor="black", linewidth=0.4)
    ax.set_title("Inverse totient: multiplicity distribution (capped)")
    ax.set_xlabel("Multiplicity (how many n share the same φ(n))")
    ax.set_ylabel("Count of totient values m")
    if tail:
        ax.text(
            0.98,
            0.98,
            f"tail (> {hist_max}): {tail} values",
            transform=ax.transAxes,
            ha="right",
            va="top",
        )
    return f


# ------------------------------------------------------------------------------
def main() -> int:
    """Run the experiment.

    Returns:
        Exit code.
    """
    args = parse_experiment_args(
        experiment_id="e053",
        description="Inverse totient: multiplicities of values φ(n)=m in a prefix",
    )

    run_log = infer_run_log_file(out_dir=args.out_dir, experiment_slug="e053")
    setup_logging(config=LoggingConfig(verbose=args.verbose, log_file=run_log.log_file))
    set_global_seed(args.seed)

    params = Params()
    paths = prepare_out_dir(out_dir=args.out_dir)

    sieve = build_factor_sieve(params.n_max)
    phi = compute_phi(params.n_max, sieve=sieve)

    max_phi = max(phi)
    counts = [0] * (max_phi + 1)
    for n in range(1, params.n_max + 1):
        counts[phi[n]] += 1

    fig1 = _plot_multiplicity_hist(counts, params.hist_max)
    save_figure(out_dir=paths.figures_dir, name="fig_01_multiplicity_hist", fig=fig1)

    # Top multiplicities
    top: list[tuple[int, int]] = []
    for m, c in enumerate(counts):
        if c > 0:
            top.append((c, m))
    top.sort(reverse=True)
    top10 = top[:10]

    lines: list[str] = []
    lines.append("# E053: Inverse totient multiplicities")
    lines.append("")
    lines.append(f"- n_max: {params.n_max}")
    lines.append("")
    lines.append("Top 10 totient values by multiplicity (count, m):")
    lines.append("")
    for c, m in top10:
        lines.append(f"- {c:>3} x : m = {m}")
    lines.append("")
    lines.append("Figure:")
    lines.append("- fig_01_multiplicity_hist.png")
    lines.append("")

    write_json(paths.params_path, asdict(params))
    write_text(paths.report_path, "\n".join(lines) + "\n", encoding="utf-8")
    return 0
