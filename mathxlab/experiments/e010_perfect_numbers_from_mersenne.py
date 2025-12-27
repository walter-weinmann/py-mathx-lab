"""E010 — Even perfect numbers from Mersenne primes.

Euclid–Euler theorem:
    If M_p = 2^p - 1 is prime, then
        N = 2^(p-1) * (2^p - 1)
    is an even perfect number.

This experiment finds small Mersenne primes (via Lucas–Lehmer) in a range
and constructs the corresponding perfect numbers, reporting their sizes.

Usage (repository convention):
    make run EXP=e010

Artifacts:
    - figures/fig_01_perfect_digits.png
    - params.json
    - report.md
"""

from __future__ import annotations

import math
from dataclasses import asdict, dataclass
from pathlib import Path
from time import perf_counter

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
        p_max: Upper bound for prime exponents p (inclusive).
        max_tests: Cap on how many prime exponents to test.
    """

    p_max: int
    max_tests: int


# ------------------------------------------------------------------------------
def primes_up_to(n: int) -> np.ndarray:
    """Sieve of Eratosthenes.

    Args:
        n: Upper bound (inclusive).

    Returns:
        Sorted array of primes ≤ n.
    """
    if n < 2:
        return np.array([], dtype=np.int64)
    sieve = np.ones(n + 1, dtype=bool)
    sieve[:2] = False
    limit = int(n**0.5)
    for p in range(2, limit + 1):
        if sieve[p]:
            sieve[p * p : n + 1 : p] = False
    return np.flatnonzero(sieve).astype(np.int64)


# ------------------------------------------------------------------------------
def lucas_lehmer_is_prime(p: int) -> bool:
    """Lucas–Lehmer test for M_p = 2^p - 1 (p prime).

    Args:
        p: Prime exponent.

    Returns:
        True iff M_p is prime.
    """
    if p == 2:
        return True
    mp = (1 << p) - 1
    s = 4
    for _ in range(p - 2):
        s = (s * s - 2) % mp
    return s == 0


# ------------------------------------------------------------------------------
def _perfect_from_p(p: int) -> int:
    """Construct even perfect number from a Mersenne prime exponent p."""
    # N = 2^(p-1) * (2^p - 1)
    return (1 << (p - 1)) * ((1 << p) - 1)


# ------------------------------------------------------------------------------
def _digits_base10_of_power2(k: int) -> int:
    """Digits of 2^k (base 10)."""
    return math.floor(k * math.log10(2.0)) + 1


# ------------------------------------------------------------------------------
def _digits_perfect(p: int) -> int:
    """Approximate digits of N = 2^(p-1) * (2^p - 1).

    For these sizes, exact digit count is:
        digits(N) = digits(2^(p-1) * (2^p - 1))
    We can compute it exactly by using logs; for modest p we can also build N.

    Args:
        p: Prime exponent.

    Returns:
        Decimal digits of the perfect number.
    """
    # log10(N) = log10(2^(p-1) * (2^p - 1))
    #          = (p-1)log10(2) + log10(2^p - 1)
    # For large p, 2^p - 1 is indistinguishable from 2^p for the purpose of
    # counting digits, except if 2^p is a power of 10 (which it never is).
    # Thus log10(N) ≈ (p-1)log10(2) + p*log10(2) = (2p-1)log10(2).
    log10n = (2 * p - 1) * math.log10(2.0)
    return math.floor(log10n) + 1


# ------------------------------------------------------------------------------
def _plot_digits(*, idx: np.ndarray, digits: np.ndarray) -> fig.Figure:
    """Plot digits of perfect numbers vs index."""
    fig_obj, ax = plt.subplots()
    ax.plot(idx, digits, marker="o")
    ax.set_title("Digits of even perfect numbers derived from Mersenne primes")
    ax.set_xlabel("k (1st, 2nd, ... found)")
    ax.set_ylabel("digits(N_k)")
    ax.set_yscale("log")
    finalize_figure(fig_obj)
    return fig_obj


# ------------------------------------------------------------------------------
def _write_report(
    *, report_path: Path, params: Params, found_p: list[int], runtimes_ms: list[float]
) -> None:
    """Write a short Markdown report.

    Args:
        report_path: Path to report.md.
        params: Experiment parameters.
        found_p: Exponents p where M_p is prime.
        runtimes_ms: LLT runtimes in milliseconds for each tested p.
    """
    lines = [
        "# E010 — Even perfect numbers from Mersenne primes",
        "",
        "**Reproduce:**",
        "",
        "```bash",
        "make run EXP=e010",
        "```",
        "",
        "## Parameters",
        f"- p_max: `{params.p_max}`",
        f"- max_tests: `{params.max_tests}`",
        "",
        "## Mersenne prime exponents found",
        "",
    ]
    if found_p:
        lines.append(", ".join(str(p) for p in found_p))
    else:
        lines.append("_none in this range (or max_tests too small)_")

    lines += [
        "",
        "## Derived even perfect numbers",
        "",
        "| p | digits(N) |",
        "|---:|---:|",
    ]
    for p in found_p:
        lines.append(f"| {p} | {_digits_perfect(p)} |")

    lines += [
        "",
        "## Notes",
        "- N = 2^(p-1)·(2^p-1) is perfect iff M_p is prime (Euclid–Euler).",
        "- For large p, we avoid constructing N explicitly and report its size (digits).",
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
        experiment_id="e010",
        description="Even perfect numbers from Mersenne primes (Euclid–Euler)",
    )
    setup_logging(config=LoggingConfig(verbose=args.verbose))
    set_global_seed(args.seed)

    params = Params(
        p_max=20_000,
        max_tests=800,
    )

    out_paths = prepare_out_dir(out_dir=args.out_dir)

    p_all = primes_up_to(params.p_max)[: params.max_tests]

    found_p: list[int] = []
    t_ms: list[float] = []

    for p in p_all:
        p_i = int(p)
        t0 = perf_counter()
        ok = lucas_lehmer_is_prime(p_i)
        dt = (perf_counter() - t0) * 1000.0
        t_ms.append(float(dt))
        if ok:
            found_p.append(p_i)

    digits = np.array([_digits_perfect(p) for p in found_p], dtype=np.int64)
    idx = np.arange(1, digits.size + 1, dtype=np.int64)

    if digits.size > 0:
        fig1 = _plot_digits(idx=idx, digits=digits)
        save_figure(out_dir=out_paths.figures_dir, name="fig_01_perfect_digits", fig=fig1)
    else:
        logger.info("No Mersenne primes found in this run; skipping plot.")

    write_json(out_paths.params_path, data=asdict(params))
    _write_report(
        report_path=out_paths.report_path, params=params, found_p=found_p, runtimes_ms=t_ms
    )

    logger.info("Experiment E010 completed successfully. Artifacts saved to: %s", args.out_dir)
    return 0


# ------------------------------------------------------------------------------
if __name__ == "__main__":
    raise SystemExit(main())
