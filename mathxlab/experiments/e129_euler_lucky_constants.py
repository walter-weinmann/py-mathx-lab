"""E129 — Euler's "lucky" quadratic constants in f(n)=n^2 + n + b.

Euler's famous polynomial

    f(n) = n^2 + n + 41

produces primes for n = 0..39, but it eventually fails (f(40)=41^2).
Historically, 41 is one of Euler's so-called "lucky" numbers: small constants b
for which n^2 + n + b yields an unusually long initial streak of primes.

This experiment compares a small set of classical b values by:
- plotting prime/composite indicators across n, and
- measuring the initial prime-run length for each b.

Usage (repository convention):
    make run EXP=e129

Artifacts:
    - figures/fig_01_prime_indicator_heatmap.png
    - figures/fig_02_initial_run_lengths.png
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
from mathxlab.experiments._prime_utils import (
    factorize_pollard_rho,
    format_factor_multiset,
    prime_mask_up_to,
)
from mathxlab.plots.helpers import finalize_figure

# ------------------------------------------------------------------------------
logger = get_logger(__name__)


# ------------------------------------------------------------------------------
@dataclass(frozen=True, slots=True)
class Params:
    """Experiment parameters.

    Args:
        seed: Random seed for reproducibility.
        b_values: Constant terms b to compare.
        n_max: Maximum n included in the scan (inclusive).
        max_listed: Maximum number of composites listed per polynomial in the report.
    """

    seed: int
    b_values: list[int]
    n_max: int
    max_listed: int


# ------------------------------------------------------------------------------
def _eval_poly(n: np.ndarray, *, b: int) -> np.ndarray:
    """Evaluate f(n)=n^2 + n + b on an integer grid.

    Args:
        n: Integer grid.
        b: Constant term.

    Returns:
        Values f(n) as int64 array.
    """
    return cast(np.ndarray, (n * n + n + b).astype(np.int64))


# ------------------------------------------------------------------------------
def _initial_prime_run_length(values: np.ndarray, is_prime: np.ndarray) -> int:
    """Compute the initial run length of primes starting at index 0.

    Args:
        values: Sequence of integer values.
        is_prime: Boolean primality mask indexed by value.

    Returns:
        Number of consecutive primes from the start.
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
def _first_composite_index(values: np.ndarray, is_prime: np.ndarray) -> int | None:
    """Return the first index i where values[i] is not prime.

    Args:
        values: Sequence of integer values.
        is_prime: Boolean primality mask indexed by value.

    Returns:
        Index of the first composite (or <2) value, or None if none found.
    """
    for i, v in enumerate(values):
        v_i = int(v)
        if v_i < 2:
            return i
        if v_i >= len(is_prime) or not bool(is_prime[v_i]):
            return i
    return None


# ------------------------------------------------------------------------------
def _plot_prime_indicator_heatmap(
    *,
    n: np.ndarray,
    b_values: list[int],
    indicator: np.ndarray,
) -> fig.Figure:
    """Plot a heatmap showing prime(1)/composite(0) across n and b.

    Args:
        n: n-grid (0..n_max).
        b_values: List of b values (one per heatmap row).
        indicator: Array shape (len(b_values), len(n)) with 1 for prime, 0 otherwise.

    Returns:
        Matplotlib figure.
    """
    fig_obj, ax = plt.subplots()
    im = ax.imshow(
        indicator,
        origin="lower",
        aspect="auto",
        extent=(int(n[0]) - 0.5, int(n[-1]) + 0.5, -0.5, len(b_values) - 0.5),
    )
    ax.set_title(r"Prime indicator for $f(n)=n^2+n+b$ (rows=b, columns=n)")
    ax.set_xlabel(r"$n$")
    ax.set_ylabel("b index")

    ax.set_yticks(np.arange(len(b_values), dtype=np.int64))
    ax.set_yticklabels([str(b) for b in b_values])

    cbar = fig_obj.colorbar(im, ax=ax)
    cbar.set_label("1 = prime, 0 = not prime")

    finalize_figure(fig_obj)
    return fig_obj


# ------------------------------------------------------------------------------
def _plot_run_lengths(*, b_values: list[int], run_lengths: np.ndarray) -> fig.Figure:
    """Plot initial prime-run lengths for each b.

    Args:
        b_values: List of b values.
        run_lengths: Run length per b.

    Returns:
        Matplotlib figure.
    """
    fig_obj, ax = plt.subplots()
    x = np.arange(len(b_values), dtype=np.int64)
    ax.bar(x, run_lengths)
    ax.set_title(r"Initial consecutive-prime run length for $f(n)=n^2+n+b$ (start at $n=0$)")
    ax.set_xlabel("b")
    ax.set_ylabel("run length")
    ax.set_xticks(x)
    ax.set_xticklabels([str(b) for b in b_values])
    finalize_figure(fig_obj)
    return fig_obj


# ------------------------------------------------------------------------------
def _write_report(
    *,
    report_path: Path,
    params: Params,
    run_lengths: dict[int, int],
    first_fail: dict[int, dict[str, object]],
) -> None:
    """Write a short Markdown report.

    Args:
        report_path: Path to report.md.
        params: Experiment parameters.
        run_lengths: Mapping b -> initial prime run length.
        first_fail: Mapping b -> witness data for first failure.
    """
    b_sorted = list(params.b_values)

    lines: list[str] = [
        "# E129 — Euler's prime-generating polynomial: lucky constants\n",
        "**Reproduce:**\n",
        "```bash\n",
        "make run EXP=e129\n",
        "```\n",
        "## Parameters\n",
        f"- n_max: `{params.n_max}`\n",
        f"- b_values: `{b_sorted}`\n",
        "\n",
        "## Summary\n",
        "| b | initial prime run | first non-prime n | f(n) | factorization |\n",
        "|---:|---:|---:|---:|---|\n",
    ]

    for b in b_sorted:
        run = int(run_lengths[b])
        ff = first_fail[b]
        n0 = ff["n"]
        v0 = ff["value"]
        fac = ff["factorization"]
        lines.append(f"| {b} | {run} | {n0} | {v0} | {fac} |\n")

    lines += [
        "\n",
        "## Notes\n",
        "- Many quadratics look prime-rich on small ranges; a short streak does not imply a deep theorem.\n",
        "- For any fixed b, there are always modular obstructions (e.g. the b-multiple subsequence for n=bk when b is prime).\n",
        "\n",
        "## Outputs\n",
        "- `figures/fig_01_prime_indicator_heatmap.png`\n",
        "- `figures/fig_02_initial_run_lengths.png`\n",
        "- `params.json`\n",
        "- `report.md`\n",
        "\n",
    ]

    report_path.write_text("".join(lines), encoding="utf-8")


# ------------------------------------------------------------------------------
def main() -> int:
    """Run the experiment.

    Returns:
        Process exit code (0 for success).
    """
    args = parse_experiment_args(
        experiment_id="e129",
        description="Euler's lucky constants for n^2 + n + b",
    )

    run_log = infer_run_log_file(out_dir=args.out_dir, experiment_slug="e129")
    setup_logging(config=LoggingConfig(verbose=args.verbose, log_file=run_log.log_file))
    set_global_seed(args.seed)
    logger.info("Starting experiment E129")

    params = Params(
        seed=args.seed,
        b_values=[2, 3, 5, 11, 17, 41],
        n_max=200,
        max_listed=10,
    )

    out_paths = prepare_out_dir(out_dir=args.out_dir)

    n = np.arange(0, params.n_max + 1, dtype=np.int64)
    max_b = max(params.b_values)
    max_value = int(params.n_max * params.n_max + params.n_max + max_b)
    max_value = max(max_value, 2)

    is_prime = prime_mask_up_to(max_value)

    indicator = np.zeros((len(params.b_values), len(n)), dtype=np.int64)
    run_lengths: dict[int, int] = {}
    first_fail: dict[int, dict[str, object]] = {}

    for row, b in enumerate(params.b_values):
        values = _eval_poly(n, b=b)
        indicator[row, :] = np.array(
            [1 if (int(v) >= 2 and bool(is_prime[int(v)])) else 0 for v in values],
            dtype=np.int64,
        )

        run = _initial_prime_run_length(values, is_prime)
        run_lengths[b] = run

        first_i = _first_composite_index(values, is_prime)
        if first_i is None:
            # within bounds, all prime
            first_fail[b] = {"n": "_none_", "value": "_none_", "factorization": "_none_"}
            continue

        v = int(values[first_i])
        if v < 2:
            fac = "not prime by definition"
        else:
            factors = factorize_pollard_rho(v, seed=params.seed)
            fac = format_factor_multiset(factors)

        first_fail[b] = {"n": int(first_i), "value": v, "factorization": fac}

    fig1 = _plot_prime_indicator_heatmap(n=n, b_values=params.b_values, indicator=indicator)
    save_figure(out_dir=out_paths.figures_dir, name="fig_01_prime_indicator_heatmap", fig=fig1)

    run_arr = np.array([run_lengths[b] for b in params.b_values], dtype=np.int64)
    fig2 = _plot_run_lengths(b_values=params.b_values, run_lengths=run_arr)
    save_figure(out_dir=out_paths.figures_dir, name="fig_02_initial_run_lengths", fig=fig2)

    write_json(out_paths.params_path, data=asdict(params))
    _write_report(
        report_path=out_paths.report_path,
        params=params,
        run_lengths=run_lengths,
        first_fail=first_fail,
    )

    logger.info("Experiment E129 completed successfully. Artifacts saved to: %s", args.out_dir)
    return 0


# ------------------------------------------------------------------------------
if __name__ == "__main__":
    raise SystemExit(main())
