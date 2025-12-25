"""E006 — Near misses to perfection.

This experiment searches for integers n ≤ N where the perfect condition σ(n) = 2n is
almost satisfied, but not exactly.

It uses a divisor-sum sieve to compute σ(1..N), then ranks candidates by deviation
from perfection.

Usage (repository convention):
    make run EXP=e006

Artifacts:
    - figures/fig_01_near_miss_scatter.png
    - figures/fig_02_topk_deviation.png
    - params.json
    - report.md
"""

from __future__ import annotations

from dataclasses import asdict, dataclass
from pathlib import Path

import matplotlib.figure as fig
import matplotlib.pyplot as plt
import numpy as np

from mathxlab.exp.cli import parse_experiment_args
from mathxlab.exp.io import prepare_out_dir, save_figure, write_json
from mathxlab.exp.logging import LoggingConfig, get_logger, setup_logging
from mathxlab.exp.random import set_global_seed
from mathxlab.plots.helpers import finalize_figure

# ------------------------------------------------------------------------------
logger = get_logger(__name__)


# ------------------------------------------------------------------------------
@dataclass(frozen=True, slots=True)
class Params:
    """Experiment parameters.

    Args:
        n_max: Upper bound N (inclusive).
        top_k: Number of best near-misses to keep.
        stride_scatter: Downsampling stride for scatter plot.
    """

    n_max: int
    top_k: int
    stride_scatter: int


# ------------------------------------------------------------------------------
def sigma_sieve(n_max: int) -> np.ndarray:
    """Compute σ(0..N) via a divisor-sum sieve.

    Args:
        n_max: Upper bound N (inclusive).

    Returns:
        sigma array with sigma[n] = σ(n).
    """
    sigma = np.zeros(n_max + 1, dtype=np.int64)
    for d in range(1, n_max + 1):
        sigma[d::d] += d
    return sigma


# ------------------------------------------------------------------------------
def _write_report(
    *, report_path: Path, params: Params, top: list[tuple[int, int, int, float]]
) -> None:
    """Write a short Markdown report.

    Args:
        report_path: Path to report.md.
        params: Experiment parameters.
        top: List of tuples (n, sigma, abs_dev, rel_dev).
    """
    lines = [
        "# E006 — Near misses to perfection",
        "",
        "**Reproduce:**",
        "",
        "```bash",
        "make run EXP=e006",
        "```",
        "",
        "## Parameters",
        f"- N: `{params.n_max}`",
        f"- top_k: `{params.top_k}`",
        "",
        "## Top near misses (excluding perfect numbers)",
        "",
        "| n | σ(n) | |σ(n)-2n| | |σ(n)/n - 2| |",
        "|---:|---:|---:|---:|",
    ]
    for n, s, d1, d2 in top:
        lines.append(f"| {n} | {s} | {d1} | {d2:.6g} |")
    lines.append("")
    lines.append("## Notes")
    lines.append(
        "- Ranking is primarily by absolute deviation |σ(n)-2n|, with relative deviation reported for context."
    )
    report_path.write_text("\n".join(lines) + "\n", encoding="utf-8")


# ------------------------------------------------------------------------------
def _plot_scatter(*, n: np.ndarray, rel_dev: np.ndarray) -> fig.Figure:
    """Scatter plot of relative deviation vs n."""
    fig_obj, ax = plt.subplots()
    ax.scatter(n, rel_dev, s=3)
    ax.set_title("Relative deviation from perfection")
    ax.set_xlabel("n")
    ax.set_ylabel("|σ(n)/n - 2|")
    ax.set_yscale("log")
    finalize_figure(fig_obj)
    return fig_obj


# ------------------------------------------------------------------------------
def _plot_topk(*, idx: np.ndarray, d1: np.ndarray) -> fig.Figure:
    """Plot absolute deviation for the top-k near misses."""
    fig_obj, ax = plt.subplots()
    ax.plot(np.arange(idx.size), d1, marker="o")
    ax.set_title("Top-k near misses by |σ(n)-2n|")
    ax.set_xlabel("rank")
    ax.set_ylabel("|σ(n)-2n|")
    finalize_figure(fig_obj)
    return fig_obj


# ------------------------------------------------------------------------------
def main() -> int:
    """Run the experiment.

    Returns:
        Process exit code (0 for success).
    """
    args = parse_experiment_args(
        experiment_id="e006",
        description="Near misses to perfection: σ(n) close to 2n",
    )
    setup_logging(config=LoggingConfig(verbose=args.verbose))
    set_global_seed(args.seed)

    params = Params(
        n_max=300_000,
        top_k=50,
        stride_scatter=10,
    )

    out_paths = prepare_out_dir(out_dir=args.out_dir)

    logger.info("Computing sigma sieve up to N=%d", params.n_max)
    sigma = sigma_sieve(params.n_max)

    n = np.arange(1, params.n_max + 1, dtype=np.int64)
    s = sigma[1:]

    # Identify perfect numbers exactly
    perfect_mask = s == (2 * n)
    # Deviation measures
    d1 = np.abs(s - 2 * n).astype(np.int64)
    rel = np.abs((s / n.astype(np.float64)) - 2.0)

    # Exclude perfect numbers from ranking
    d1_rank = d1.copy()
    d1_rank[perfect_mask] = np.iinfo(np.int64).max

    # Top-k indices (smallest deviations)
    idx = np.argpartition(d1_rank, params.top_k)[: params.top_k]
    idx = idx[np.argsort(d1_rank[idx])]

    top: list[tuple[int, int, int, float]] = []
    for i in idx:
        nn = int(n[i])
        ss = int(s[i])
        dd1 = int(d1[i])
        dd2 = float(rel[i])
        top.append((nn, ss, dd1, dd2))

    # Scatter plot (downsample for readability)
    n_s = n[:: params.stride_scatter]
    rel_s = rel[:: params.stride_scatter]
    fig1 = _plot_scatter(n=n_s, rel_dev=rel_s)
    save_figure(out_dir=out_paths.figures_dir, name="fig_01_near_miss_scatter", fig=fig1)

    fig2 = _plot_topk(idx=idx, d1=np.array([d1[i] for i in idx], dtype=np.int64))
    save_figure(out_dir=out_paths.figures_dir, name="fig_02_topk_deviation", fig=fig2)

    write_json(out_paths.params_path, data=asdict(params))
    _write_report(report_path=out_paths.report_path, params=params, top=top)

    logger.info("Experiment E006 completed successfully. Artifacts saved to: %s", args.out_dir)
    return 0


# ------------------------------------------------------------------------------
if __name__ == "__main__":
    raise SystemExit(main())
