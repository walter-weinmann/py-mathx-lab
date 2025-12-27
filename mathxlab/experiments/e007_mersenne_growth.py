"""E007 — Mersenne number growth.

This experiment visualizes how fast M_n = 2^n - 1 grows with n, using
cheap analytic formulas for bit-length and decimal digit count.

Usage (repository convention):
    make run EXP=e007

Artifacts:
    - figures/fig_01_digits_vs_n.png
    - figures/fig_02_bits_vs_n.png
    - params.json
    - report.md
"""

from __future__ import annotations

from dataclasses import asdict, dataclass
from pathlib import Path
from typing import TYPE_CHECKING

import matplotlib.figure as fig
import matplotlib.pyplot as plt
import numpy as np

if TYPE_CHECKING:
    from numpy.typing import NDArray

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
        n_max: Maximum exponent n (inclusive).
        stride: Downsampling stride for plots.
    """

    n_max: int
    stride: int


# ------------------------------------------------------------------------------
def _mersenne_digits(n: NDArray[np.int64]) -> NDArray[np.int64]:
    """Compute decimal digits of M_n = 2^n - 1 without constructing M_n.

    Args:
        n: Array of positive integers.

    Returns:
        Array of digit counts (base 10).
    """
    # digits(2^n - 1) = floor(n * log10(2)) + 1  for n >= 1
    res: NDArray[np.int64] = np.floor(n.astype(np.float64) * np.log10(2.0)).astype(np.int64) + 1
    return res


# ------------------------------------------------------------------------------
def _plot_digits(*, n: NDArray[np.int64], digits: NDArray[np.int64]) -> fig.Figure:
    """Plot digits(M_n) vs n."""
    fig_obj, ax = plt.subplots()
    ax.plot(n, digits)
    ax.set_title("Decimal digits of M_n = 2^n - 1")
    ax.set_xlabel("n")
    ax.set_ylabel("digits(M_n)")
    finalize_figure(fig_obj)
    return fig_obj


# ------------------------------------------------------------------------------
def _plot_bits(*, n: NDArray[np.int64], bits: NDArray[np.int64]) -> fig.Figure:
    """Plot bit-length of M_n vs n."""
    fig_obj, ax = plt.subplots()
    ax.plot(n, bits)
    ax.set_title("Bit-length of M_n = 2^n - 1")
    ax.set_xlabel("n")
    ax.set_ylabel("bits(M_n)")
    finalize_figure(fig_obj)
    return fig_obj


# ------------------------------------------------------------------------------
def _write_report(*, report_path: Path, params: Params) -> None:
    """Write a short Markdown report.

    Args:
        report_path: Path to report.md.
        params: Experiment parameters.
    """
    n = np.array([1, 2, 3, 5, 10, 100, 1_000, 10_000], dtype=np.int64)
    digits = _mersenne_digits(n)
    lines = [
        "# E007 — Mersenne number growth",
        "",
        "**Reproduce:**",
        "",
        "```bash",
        "make run EXP=e007",
        "```",
        "",
        "## Parameters",
        f"- n_max: `{params.n_max}`",
        f"- stride: `{params.stride}`",
        "",
        "## Quick reference table",
        "",
        "| n | digits(M_n) | bits(M_n) |",
        "|---:|---:|---:|",
    ]
    for nn, dd in zip(n.tolist(), digits.tolist(), strict=True):
        lines.append(f"| {nn} | {dd} | {nn} |")
    lines += [
        "",
        "## Notes",
        "- For n ≥ 1, the bit-length of M_n is exactly n.",
        "- digits(M_n) can be computed via floor(n·log10(2)) + 1 without building M_n.",
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
        experiment_id="e007",
        description="Mersenne number growth: digits and bits of 2^n - 1",
    )
    setup_logging(config=LoggingConfig(verbose=args.verbose))
    set_global_seed(args.seed)

    params = Params(
        n_max=500_000,
        stride=50,
    )

    out_paths = prepare_out_dir(out_dir=args.out_dir)

    n = np.arange(1, params.n_max + 1, dtype=np.int64)[:: params.stride]
    digits = _mersenne_digits(n)
    bits = n.copy()  # exact

    fig1 = _plot_digits(n=n, digits=digits)
    save_figure(out_dir=out_paths.figures_dir, name="fig_01_digits_vs_n", fig=fig1)

    fig2 = _plot_bits(n=n, bits=bits)
    save_figure(out_dir=out_paths.figures_dir, name="fig_02_bits_vs_n", fig=fig2)

    write_json(out_paths.params_path, data=asdict(params))
    _write_report(report_path=out_paths.report_path, params=params)

    logger.info("Experiment E007 completed successfully. Artifacts saved to: %s", args.out_dir)
    return 0


# ------------------------------------------------------------------------------
if __name__ == "__main__":
    raise SystemExit(main())
