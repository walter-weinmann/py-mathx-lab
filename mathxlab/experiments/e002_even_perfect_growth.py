"""E002 — Even perfect numbers: generator and growth.

This experiment generates even perfect numbers from a curated list of known Mersenne
prime exponents and visualizes how fast they grow.

Mathematical background (Euclid-Euler):
    An even integer N is perfect iff
        N = 2^(p-1) (2^p - 1),
    where (2^p - 1) is prime (a Mersenne prime).

Usage (repository convention):
    make run EXP=e002

Artifacts:
    - figures/fig_01_digits_vs_p.png
    - figures/fig_02_bits_vs_p.png
    - figures/fig_03_log10_error_vs_p.png
    - params.json
    - report.md
"""

from __future__ import annotations

from dataclasses import asdict, dataclass
from math import log10
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
        exponents: Known Mersenne prime exponents p to use.
    """

    exponents: tuple[int, ...]


# ------------------------------------------------------------------------------
def _even_perfect(p: int) -> int:
    """Compute the even perfect number N(p) = 2^(p-1) (2^p - 1).

    Args:
        p: Mersenne exponent.

    Returns:
        The even perfect number as an exact Python integer.
    """
    m = (1 << p) - 1
    return (1 << (p - 1)) * m


# ------------------------------------------------------------------------------
def _digits(n: int) -> int:
    """Compute the number of base-10 digits of n.

    Args:
        n: Positive integer.

    Returns:
        The digit count.
    """
    if n <= 0:
        raise ValueError("n must be positive")
    # str() is exact and robust for the moderate p used in this experiment.
    return len(str(n))


# ------------------------------------------------------------------------------
def _write_report(*, report_path: Path, params: Params, seed: int) -> None:
    """Write a short Markdown report.

    Args:
        report_path: Path to report.md.
        params: Experiment parameters.
        seed: Run seed.
    """
    exp_str = ", ".join(str(p) for p in params.exponents)
    report_md = f"""\
# E002 — Even perfect numbers: generator and growth

**Reproduce:**

```bash
make run EXP=e002 ARGS="--seed {seed}"
```

**Seed:** `{seed}`

## Exponents

Mersenne prime exponents used in this run:

`{exp_str}`

## Outputs

- `figures/fig_01_digits_vs_p.png`
- `figures/fig_02_bits_vs_p.png`
- `figures/fig_03_log10_error_vs_p.png`
- `params.json`

## Notes

- Growth is extreme: both digits and bit length scale roughly linearly in `p`.
- The log-approximation error stays bounded and illustrates why `N(p)` behaves like `2^(2p)` up to a small correction.
"""
    report_path.write_text(report_md, encoding="utf-8")


# ------------------------------------------------------------------------------
def _plot_xy(*, x: np.ndarray, y: np.ndarray, title: str, xlabel: str, ylabel: str) -> fig.Figure:
    """Create a simple x-y line plot.

    Args:
        x: X values.
        y: Y values.
        title: Plot title.
        xlabel: X axis label.
        ylabel: Y axis label.

    Returns:
        Matplotlib figure.
    """
    fig_obj, ax = plt.subplots()
    ax.plot(x, y, marker="o")
    ax.set_title(title)
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    finalize_figure(fig_obj)
    return fig_obj


# ------------------------------------------------------------------------------
def main() -> int:
    """Run the experiment.

    Returns:
        Process exit code (0 for success).
    """
    args = parse_experiment_args(
        experiment_id="e002",
        description="Even perfect numbers: generator and growth",
    )
    setup_logging(config=LoggingConfig(verbose=args.verbose))
    set_global_seed(args.seed)

    params = Params(
        exponents=(2, 3, 5, 7, 13, 17, 19, 31),
    )

    out_paths = prepare_out_dir(out_dir=args.out_dir)

    p_vals = np.array(params.exponents, dtype=np.int64)
    logger.info("Computing even perfect numbers for %d exponents", p_vals.size)

    n_vals = [_even_perfect(int(p)) for p in p_vals]
    digits = np.array([_digits(n) for n in n_vals], dtype=np.int64)
    bits = np.array([int(n).bit_length() for n in n_vals], dtype=np.int64)

    # log10(N) and approximation 2p log10(2)
    log10_n = np.array([log10(n) for n in n_vals], dtype=np.float64)
    approx = 2.0 * p_vals.astype(np.float64) * log10(2.0)
    err = log10_n - approx

    fig1 = _plot_xy(
        x=p_vals,
        y=digits,
        title="Digits of even perfect numbers vs. exponent p",
        xlabel="p",
        ylabel="digits(N(p))",
    )
    save_figure(out_dir=out_paths.figures_dir, name="fig_01_digits_vs_p", fig=fig1)

    fig2 = _plot_xy(
        x=p_vals,
        y=bits,
        title="Bit length of even perfect numbers vs. exponent p",
        xlabel="p",
        ylabel="bit_length(N(p))",
    )
    save_figure(out_dir=out_paths.figures_dir, name="fig_02_bits_vs_p", fig=fig2)

    fig3 = _plot_xy(
        x=p_vals,
        y=err,
        title="Error of log10 approximation: log10(N(p)) - 2p log10(2)",
        xlabel="p",
        ylabel="error",
    )
    save_figure(out_dir=out_paths.figures_dir, name="fig_03_log10_error_vs_p", fig=fig3)

    write_json(out_paths.params_path, data=asdict(params))
    _write_report(report_path=out_paths.report_path, params=params, seed=args.seed)

    logger.info("Experiment E002 completed successfully. Artifacts saved to: %s", args.out_dir)
    return 0


# ------------------------------------------------------------------------------
if __name__ == "__main__":
    raise SystemExit(main())
