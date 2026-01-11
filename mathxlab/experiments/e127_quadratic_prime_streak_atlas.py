"""E127: Quadratic prime-run atlas for f(n)=n^2 + a n + b.

This experiment sweeps a small grid of integer parameters (a, b) for the
quadratic polynomial

    f(n) = n^2 + a n + b,

and measures the length of the **initial prime run** starting at n=0.

The goal is to make the "prime-rich" behavior of some quadratics (notably
Euler's n^2 + n + 41) visible as a 2D landscape.

Usage (repository convention):
    make run EXP=e127

Artifacts:
    - figures/fig_01_run_length_heatmap.png
    - figures/fig_02_run_length_histogram.png
    - params.json
    - report.md
"""

from __future__ import annotations

from dataclasses import asdict, dataclass
from pathlib import Path
from typing import cast

import matplotlib.figure as fig
import matplotlib.pyplot as plt
import numpy as np

from mathxlab.exp.cli import parse_experiment_args
from mathxlab.exp.io import prepare_out_dir, save_figure, write_json
from mathxlab.exp.logging import LoggingConfig, get_logger, setup_logging
from mathxlab.exp.random import set_global_seed
from mathxlab.exp.run_logging import infer_run_log_file
from mathxlab.experiments._prime_utils import prime_mask_up_to
from mathxlab.plots.helpers import finalize_figure

# ------------------------------------------------------------------------------
logger = get_logger(__name__)


# ------------------------------------------------------------------------------
@dataclass(frozen=True, slots=True)
class Params:
    """Experiment parameters.

    Args:
        seed: Random seed for reproducibility.
        a_min: Minimum a value in the sweep (inclusive).
        a_max: Maximum a value in the sweep (inclusive).
        b_min: Minimum b value in the sweep (inclusive).
        b_max: Maximum b value in the sweep (inclusive).
        n_run_max: Maximum n tested for the initial prime run (inclusive).
        top_k: Number of best (a, b) pairs included in the report.
    """

    seed: int
    a_min: int
    a_max: int
    b_min: int
    b_max: int
    n_run_max: int
    top_k: int


# ------------------------------------------------------------------------------
def _eval_quadratic(n: np.ndarray, *, a: int, b: int) -> np.ndarray:
    """Evaluate f(n)=n^2 + a n + b on an integer grid.

    Args:
        n: Integer grid.
        a: Linear coefficient.
        b: Constant term.

    Returns:
        Values f(n) as int64 array.
    """
    return cast(np.ndarray, (n * n + a * n + b).astype(np.int64))


# ------------------------------------------------------------------------------
def _initial_prime_run_length(values: np.ndarray, is_prime: np.ndarray) -> int:
    """Compute initial run length of prime values starting at index 0.

    A value is considered prime iff it is >= 2 and is_prime[value] is True.

    Args:
        values: Sequence of integer values.
        is_prime: Boolean primality mask indexed by value.

    Returns:
        The number of consecutive prime values from the start.
    """
    run = 0
    for v in values:
        v_i = int(v)
        if v_i < 2:
            break
        if v_i >= len(is_prime) or not bool(is_prime[v_i]):
            break
        run += 1
    return run


# ------------------------------------------------------------------------------
def _plot_heatmap(
    *,
    a_values: np.ndarray,
    b_values: np.ndarray,
    run_len: np.ndarray,
    highlight_a: int,
    highlight_b: int,
) -> fig.Figure:
    """Plot a heatmap of initial prime run lengths over (a, b).

    Args:
        a_values: Sorted list of a values.
        b_values: Sorted list of b values.
        run_len: 2D array run_len[b_index, a_index].
        highlight_a: a-value to highlight (Euler: 1).
        highlight_b: b-value to highlight (Euler: 41).

    Returns:
        Matplotlib figure.
    """
    fig_obj, ax = plt.subplots()

    im = ax.imshow(
        run_len,
        origin="lower",
        aspect="auto",
        extent=(
            float(a_values[0]) - 0.5,
            float(a_values[-1]) + 0.5,
            float(b_values[0]) - 0.5,
            float(b_values[-1]) + 0.5,
        ),
    )

    ax.set_title(r"Initial prime-run length for $f(n)=n^2 + a n + b$ (start at $n=0$)")
    ax.set_xlabel(r"$a$")
    ax.set_ylabel(r"$b$")

    cbar = fig_obj.colorbar(im, ax=ax)
    cbar.set_label("initial prime run length")

    if int(a_values[0]) <= highlight_a <= int(a_values[-1]) and int(
        b_values[0]
    ) <= highlight_b <= int(b_values[-1]):
        ax.scatter(
            [highlight_a],
            [highlight_b],
            marker="o",
            s=80,
            edgecolors="black",
            facecolors="none",
        )
        ax.annotate(
            "Euler (1,41)",
            (highlight_a, highlight_b),
            xytext=(6, 6),
            textcoords="offset points",
        )

    finalize_figure(fig_obj)
    return fig_obj


# ------------------------------------------------------------------------------
def _plot_histogram(*, run_len: np.ndarray) -> fig.Figure:
    """Plot a histogram of run lengths in the sweep.

    Args:
        run_len: 2D run length array.

    Returns:
        Matplotlib figure.
    """
    fig_obj, ax = plt.subplots()
    flat = run_len.ravel()
    bins = int(np.max(flat)) + 1 if flat.size else 1
    ax.hist(flat, bins=bins)
    ax.set_title("Distribution of initial prime-run lengths in the sweep")
    ax.set_xlabel("initial prime run length")
    ax.set_ylabel("count of (a,b) pairs")
    finalize_figure(fig_obj)
    return fig_obj


# ------------------------------------------------------------------------------
def _write_report(
    *,
    report_path: Path,
    params: Params,
    a_values: np.ndarray,
    b_values: np.ndarray,
    run_len: np.ndarray,
) -> None:
    """Write a short Markdown report.

    Args:
        report_path: Output report path.
        params: Experiment parameters.
        a_values: a-grid.
        b_values: b-grid.
        run_len: Run length grid.
    """
    entries: list[tuple[int, int, int]] = []
    for bi, b in enumerate(b_values):
        for ai, a in enumerate(a_values):
            entries.append((int(run_len[bi, ai]), int(a), int(b)))
    entries.sort(key=lambda t: (-t[0], t[1], t[2]))

    top = entries[: params.top_k]

    euler_run: int | None = None
    if params.a_min <= 1 <= params.a_max and params.b_min <= 41 <= params.b_max:
        ai = int(np.where(a_values == 1)[0][0])
        bi = int(np.where(b_values == 41)[0][0])
        euler_run = int(run_len[bi, ai])

    lines: list[str] = [
        "# E127: Quadratic prime-run atlas (n^2 + a n + b)",
        "",
        "**Reproduce:**",
        "",
        "```bash",
        "make run EXP=e127",
        "```",
        "",
        "### Parameters",
        f"- a range: `[{params.a_min}, {params.a_max}]`",
        f"- b range: `[{params.b_min}, {params.b_max}]`",
        f"- n_run_max: `{params.n_run_max}` (test n=0..n_run_max)",
        f"- top_k: `{params.top_k}`",
        "",
        "## Key observation",
        "Initial prime streaks vary sharply across (a,b). A few islands can look remarkably prime-rich on small ranges,",
        "which explains why Euler's famous polynomial stands out in short scans.",
        "",
    ]

    if euler_run is not None:
        lines.append(
            f"- Euler point (a=1,b=41) in this grid: run length **{euler_run}** (n=0..{euler_run - 1})."
        )
        lines.append("")

    lines += [
        "## Best run lengths in this sweep",
        "",
        "| run length | a | b | polynomial |",
        "|---:|---:|---:|:---|",
    ]
    for run, a, b in top:
        lines.append(f"| {run} | {a} | {b} | $n^2 + {a}n + {b}$ |")

    lines += [
        "",
        "## Outputs",
        "- `figures/fig_01_run_length_heatmap.png`",
        "- `figures/fig_02_run_length_histogram.png`",
        "- `params.json`",
        "- `report.md`",
        "",
    ]

    report_path.write_text("\n".join(lines), encoding="utf-8")


# ------------------------------------------------------------------------------
def main() -> int:
    """Run the experiment.

    Returns:
        Process exit code (0 for success).
    """
    args = parse_experiment_args(
        experiment_id="e127",
        description="Quadratic prime-run atlas (n^2 + a n + b)",
    )

    run_log = infer_run_log_file(out_dir=args.out_dir, experiment_slug="e127")
    setup_logging(config=LoggingConfig(verbose=args.verbose, log_file=run_log.log_file))
    set_global_seed(args.seed)
    logger.info("Starting experiment E127")

    params = Params(
        seed=args.seed,
        a_min=-50,
        a_max=50,
        b_min=-50,
        b_max=50,
        n_run_max=80,
        top_k=12,
    )

    out_paths = prepare_out_dir(out_dir=args.out_dir)

    a_values = np.arange(params.a_min, params.a_max + 1, dtype=np.int64)
    b_values = np.arange(params.b_min, params.b_max + 1, dtype=np.int64)
    n = np.arange(0, params.n_run_max + 1, dtype=np.int64)

    max_abs_a = max(abs(params.a_min), abs(params.a_max))
    max_abs_b = max(abs(params.b_min), abs(params.b_max))
    max_value = int(params.n_run_max * params.n_run_max + max_abs_a * params.n_run_max + max_abs_b)
    max_value = max(max_value, 2)

    is_prime = prime_mask_up_to(max_value)

    run_len = np.zeros((len(b_values), len(a_values)), dtype=np.int64)
    for bi, b in enumerate(b_values):
        for ai, a in enumerate(a_values):
            vals = _eval_quadratic(n, a=int(a), b=int(b))
            run_len[bi, ai] = _initial_prime_run_length(vals, is_prime)

    fig1 = _plot_heatmap(
        a_values=a_values,
        b_values=b_values,
        run_len=run_len,
        highlight_a=1,
        highlight_b=41,
    )
    save_figure(out_dir=out_paths.figures_dir, name="fig_01_run_length_heatmap", fig=fig1)

    fig2 = _plot_histogram(run_len=run_len)
    save_figure(out_dir=out_paths.figures_dir, name="fig_02_run_length_histogram", fig=fig2)

    write_json(out_paths.params_path, data=asdict(params))
    _write_report(
        report_path=out_paths.report_path,
        params=params,
        a_values=a_values,
        b_values=b_values,
        run_len=run_len,
    )

    logger.info("Experiment E127 completed successfully. Artifacts saved to: %s", args.out_dir)
    return 0


# ------------------------------------------------------------------------------
if __name__ == "__main__":
    raise SystemExit(main())
