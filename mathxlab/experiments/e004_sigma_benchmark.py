"""E004 — Benchmark σ(n) computation: sieve vs factorization.

This experiment benchmarks two equivalent strategies to compute the sum-of-divisors function σ(n):

A) Bulk divisor-sum sieve (compute σ(1..N) in one pass).
B) Per-number factorization (compute σ(n) from prime exponents).

The goal is not micro-optimizations, but a clear and reproducible comparison.

Usage (repository convention):
    make run EXP=e004

Artifacts:
    - figures/fig_01_runtime_vs_n.png
    - figures/fig_02_throughput_vs_n.png
    - params.json
    - report.md
"""

from __future__ import annotations

from dataclasses import asdict, dataclass
from math import isqrt
from pathlib import Path
from time import perf_counter
from typing import Any

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
        n_values: N values to benchmark (inclusive upper bound for 1..N).
        trials: Number of trials per method (median is reported).
        max_n_factor: Maximum N allowed for the factorization method (safety).
    """

    n_values: tuple[int, ...]
    trials: int
    max_n_factor: int


# ------------------------------------------------------------------------------
def sigma_sieve(n_max: int) -> np.ndarray:
    """Compute σ(0..N) via a divisor-sum sieve.

    Args:
        n_max: Upper bound N (inclusive).

    Returns:
        sigma array of length N+1.
    """
    sigma = np.zeros(n_max + 1, dtype=np.int64)
    for d in range(1, n_max + 1):
        sigma[d::d] += d
    return sigma


# ------------------------------------------------------------------------------
def primes_up_to(n: int) -> list[int]:
    """Return a list of primes <= n using a simple sieve.

    Args:
        n: Upper bound.

    Returns:
        List of primes in ascending order.
    """
    if n < 2:
        return []
    sieve = bytearray(b"\x01") * (n + 1)
    sieve[0:2] = b"\x00\x00"
    for p in range(2, isqrt(n) + 1):
        if sieve[p]:
            step = p
            start = p * p
            sieve[start : n + 1 : step] = b"\x00" * ((n - start) // step + 1)
    return [i for i in range(2, n + 1) if sieve[i]]


# ------------------------------------------------------------------------------
def sigma_from_factorization(n: int, primes: list[int]) -> int:
    """Compute σ(n) from prime factorization using a prime list.

    Args:
        n: Positive integer.
        primes: List of primes up to sqrt(max_n).

    Returns:
        σ(n).
    """
    if n < 1:
        raise ValueError("n must be >= 1")
    if n == 1:
        return 1

    x = n
    result = 1

    for p in primes:
        if p * p > x:
            break
        if x % p != 0:
            continue
        a = 0
        while x % p == 0:
            x //= p
            a += 1
        # σ(p^a) = (p^(a+1)-1)/(p-1)
        result *= (p ** (a + 1) - 1) // (p - 1)

    if x > 1:
        # Remaining prime factor
        result *= (x**2 - 1) // (x - 1)

    return result


# ------------------------------------------------------------------------------
def _median_time(fn: Any) -> float:
    """Measure median runtime over multiple trials."""
    times: list[float] = []
    for _ in range(fn.trials):
        t0 = perf_counter()
        fn()
        t1 = perf_counter()
        times.append(t1 - t0)
    return float(np.median(np.array(times, dtype=np.float64)))


# ------------------------------------------------------------------------------
def _plot_runtime(*, n_vals: np.ndarray, t_sieve: np.ndarray, t_fact: np.ndarray) -> fig.Figure:
    """Plot runtime curves."""
    fig_obj, ax = plt.subplots()
    ax.plot(n_vals, t_sieve, marker="o", label="sieve")
    ax.plot(n_vals, t_fact, marker="o", label="factorization")
    ax.set_title("Runtime vs N")
    ax.set_xlabel("N")
    ax.set_ylabel("seconds (median)")
    ax.legend(loc="best")
    finalize_figure(fig_obj)
    return fig_obj


# ------------------------------------------------------------------------------
def _plot_throughput(*, n_vals: np.ndarray, t_sieve: np.ndarray, t_fact: np.ndarray) -> fig.Figure:
    """Plot throughput curves (numbers per second)."""
    fig_obj, ax = plt.subplots()
    ax.plot(n_vals, n_vals / t_sieve, marker="o", label="sieve")
    ax.plot(n_vals, n_vals / t_fact, marker="o", label="factorization")
    ax.set_title("Throughput vs N")
    ax.set_xlabel("N")
    ax.set_ylabel("numbers / second")
    ax.legend(loc="best")
    finalize_figure(fig_obj)
    return fig_obj


# ------------------------------------------------------------------------------
def _write_report(
    *,
    report_path: Path,
    params: Params,
    n_vals: np.ndarray,
    t_sieve: np.ndarray,
    t_fact: np.ndarray,
) -> None:
    """Write a short Markdown report."""
    lines = [
        "# E004 — Benchmark σ(n) computation: sieve vs factorization",
        "",
        "**Reproduce:**",
        "",
        "```bash",
        "make run EXP=e004",
        "```",
        "",
        "## Parameters",
        f"- n_values: `{', '.join(str(int(x)) for x in n_vals)}`",
        f"- trials: `{params.trials}`",
        "",
        "## Results (median runtime)",
        "",
        "| N | sieve [s] | factorization [s] | speedup (sieve/fact) |",
        "|---:|---:|---:|---:|",
    ]
    for N, a, b in zip(n_vals, t_sieve, t_fact, strict=True):
        speed = a / b if b > 0 else float("nan")
        lines.append(f"| {int(N)} | {a:.4f} | {b:.4f} | {speed:.2f} |")
    lines.append("")
    lines.append("## Notes")
    lines.append(
        "- Sieve computes all σ(1..N) at once; factorization recomputes structure per number."
    )
    lines.append(
        "- Factorization is capped to moderate N to keep runtime reasonable in pure Python."
    )
    report_path.write_text("\n".join(lines) + "\n", encoding="utf-8")


# ------------------------------------------------------------------------------
def main() -> int:
    """Run the experiment.

    Returns:
        Process exit code (0 for success).
    """
    args = parse_experiment_args(
        experiment_id="e004",
        description="Benchmark σ(n): sieve vs factorization",
    )
    setup_logging(config=LoggingConfig(verbose=args.verbose))
    set_global_seed(args.seed)

    params = Params(
        n_values=(10_000, 30_000, 60_000, 100_000),
        trials=3,
        max_n_factor=100_000,
    )

    out_paths = prepare_out_dir(out_dir=args.out_dir)

    n_vals = np.array(params.n_values, dtype=np.int64)

    # Precompute primes once (for the largest N).
    primes = primes_up_to(isqrt(int(n_vals.max())))

    t_sieve = np.zeros(n_vals.size, dtype=np.float64)
    t_fact = np.zeros(n_vals.size, dtype=np.float64)

    for i, N in enumerate(n_vals):
        N_int = int(N)
        logger.info("Benchmarking N=%d", N_int)

        def run_sieve(N_int: int = N_int) -> None:
            _ = sigma_sieve(N_int)

        t_sieve[i] = _median_time(type("T", (), {"trials": params.trials, "__call__": run_sieve})())

        if N_int > params.max_n_factor:
            t_fact[i] = float("nan")
            continue

        def run_fact(N_int: int = N_int, primes: list[int] = primes) -> None:
            # Compute σ(n) for all n <= N using per-number factorization.
            # This is intentionally direct and readable.
            for n in range(1, N_int + 1):
                _ = sigma_from_factorization(n, primes)

        t_fact[i] = _median_time(type("T", (), {"trials": params.trials, "__call__": run_fact})())

    fig1 = _plot_runtime(n_vals=n_vals, t_sieve=t_sieve, t_fact=t_fact)
    save_figure(out_dir=out_paths.figures_dir, name="fig_01_runtime_vs_n", fig=fig1)

    fig2 = _plot_throughput(n_vals=n_vals, t_sieve=t_sieve, t_fact=t_fact)
    save_figure(out_dir=out_paths.figures_dir, name="fig_02_throughput_vs_n", fig=fig2)

    write_json(out_paths.params_path, data=asdict(params))
    _write_report(
        report_path=out_paths.report_path,
        params=params,
        n_vals=n_vals,
        t_sieve=t_sieve,
        t_fact=t_fact,
    )

    logger.info("Experiment E004 completed successfully. Artifacts saved to: %s", args.out_dir)
    return 0


# ------------------------------------------------------------------------------
if __name__ == "__main__":
    raise SystemExit(main())
