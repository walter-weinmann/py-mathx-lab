"""E051: Semiprimes: balanced vs unbalanced factorization timing.

A semiprime is n = p*q with p and q prime. RSA-style semiprimes tend to be
"balanced" (p and q have similar size), which typically makes factorization
harder than when one factor is much smaller.

This experiment generates small semiprimes and compares factorization time
between:
- balanced semiprimes (p and q with similar bit length),
- unbalanced semiprimes (one small factor, one larger factor).

We factor using Pollard's rho (with a small trial division front-end) and record
timings.

Usage (repository convention):
    make run EXP=e051

Artifacts:
    - figures/fig_01_factor_time_boxplot.png
    - figures/fig_02_factor_time_scatter.png
    - params.json
    - report.md
"""

from __future__ import annotations

import math
import random
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
from mathxlab.exp.run_logging import infer_run_log_file
from mathxlab.experiments._prime_utils import (
    is_prime_deterministic_64,
    is_probable_prime_miller_rabin,
    pollard_rho,
    primes_up_to,
    trial_division_factor,
)

# ------------------------------------------------------------------------------
logger = get_logger(__name__)


# ------------------------------------------------------------------------------
@dataclass(frozen=True, slots=True)
class Params:
    """Experiment parameters.

    Args:
        sample_count: Number of semiprimes to generate in each category.
        balanced_bits: Bit length for balanced semiprimes (approx).
        small_factor_bits: Bit length of small factor for unbalanced samples.
        mr_bases: Miller–Rabin bases for probable primality in prime generation.
        trial_division_bound: Prime bound for trial division pre-pass in factorization.
    """

    sample_count: int
    balanced_bits: int
    small_factor_bits: int
    mr_bases: tuple[int, ...]
    trial_division_bound: int


# ------------------------------------------------------------------------------
def _rand_odd(bits: int, rng: random.Random) -> int:
    """Generate a random odd integer with given bit length.

    Args:
        bits: Bit length (>= 2).
        rng: RNG.

    Returns:
        Random odd integer.
    """
    x = rng.getrandbits(bits)
    x |= 1 << (bits - 1)  # ensure top bit
    x |= 1  # odd
    return x


# ------------------------------------------------------------------------------
def generate_prime(bits: int, rng: random.Random, bases: tuple[int, ...]) -> int:
    """Generate a probable prime with the given bit length.

    Args:
        bits: Bit length.
        rng: RNG instance.
        bases: Miller–Rabin bases.

    Returns:
        Probable prime.
    """
    while True:
        n = _rand_odd(bits, rng)
        # Use deterministic 64-bit path when possible.
        if n < (1 << 63):
            if is_prime_deterministic_64(n):
                return n
        else:
            if is_probable_prime_miller_rabin(n, bases=bases):
                return n


# ------------------------------------------------------------------------------
def generate_semiprime_balanced(
    bits: int, rng: random.Random, bases: tuple[int, ...]
) -> tuple[int, int, int]:
    """Generate a balanced semiprime.

    Args:
        bits: Target bit length for n ≈ bits.
        rng: RNG.
        bases: MR bases.

    Returns:
        (n, p, q).
    """
    half = bits // 2
    p = generate_prime(half, rng, bases)
    q = generate_prime(bits - half, rng, bases)
    return p * q, p, q


# ------------------------------------------------------------------------------
def generate_semiprime_unbalanced(
    bits: int, small_bits: int, rng: random.Random, bases: tuple[int, ...]
) -> tuple[int, int, int]:
    """Generate an unbalanced semiprime.

    Args:
        bits: Approx target bit length for n.
        small_bits: Bit length for the small factor.
        rng: RNG.
        bases: MR bases.

    Returns:
        (n, p, q) where p is small.
    """
    p = generate_prime(small_bits, rng, bases)
    q = generate_prime(max(8, bits - small_bits), rng, bases)
    return p * q, p, q


# ------------------------------------------------------------------------------
def factor_semiprime(n: int, trial_bound: int) -> int:
    """Find a nontrivial factor of n.

    Args:
        n: Semiprime candidate.
        trial_bound: Bound for trial division pre-pass.

    Returns:
        A nontrivial factor.
    """
    primes = primes_up_to(trial_bound)
    res = trial_division_factor(n, primes)
    if res is not None:
        return res[0]
    rng = random.Random(1)
    f2 = pollard_rho(n, rng=rng)
    if f2 is None:
        # Very small sample sizes: fall back to brute step-up in rare failures.
        primes_full = primes_up_to(math.isqrt(n) + 1)
        res3 = trial_division_factor(n, primes_full)
        if res3 is None:
            raise RuntimeError("Factorization failed unexpectedly.")
        return res3[0]
    return f2


# ------------------------------------------------------------------------------
def _plot_boxplot(times_bal: np.ndarray, times_unbal: np.ndarray) -> fig.Figure:
    """Boxplot of factorization times.

    Args:
        times_bal: Times (seconds) for balanced samples.
        times_unbal: Times (seconds) for unbalanced samples.

    Returns:
        Figure.
    """
    fig1 = plt.figure(figsize=(8.5, 4.5))
    ax = fig1.add_subplot(1, 1, 1)
    ax.boxplot([times_bal, times_unbal], tick_labels=["balanced", "unbalanced"])
    ax.set_title("Factorization timing for semiprimes (Pollard rho)")
    ax.set_ylabel("seconds")
    ax.grid(True, alpha=0.25)
    return fig1


# ------------------------------------------------------------------------------
def _plot_scatter(ns: np.ndarray, times: np.ndarray, labels: list[str]) -> fig.Figure:
    """Scatter plot of log10(n) vs time.

    Args:
        ns: n values.
        times: timing values.
        labels: category labels aligned with ns.

    Returns:
        Figure.
    """
    fig2 = plt.figure(figsize=(9, 4.5))
    ax = fig2.add_subplot(1, 1, 1)
    x = np.log10(ns.astype(np.float64))
    ax.scatter(x, times, s=12)
    for xi, ti, lab in zip(x, times, labels, strict=True):
        ax.annotate(lab[0].upper(), (xi, ti), textcoords="offset points", xytext=(5, 5))
    ax.set_title(r"Semiprimes: $n=pq$ — factor time vs size")
    ax.set_xlabel(r"$\log_{10}(n)$")
    ax.set_ylabel("seconds")
    ax.grid(True, alpha=0.25)
    return fig2


# ------------------------------------------------------------------------------
def _write_report(
    *,
    report_path: Path,
    params: Params,
    items_bal: list[tuple[int, int, int, float]],
    items_unbal: list[tuple[int, int, int, float]],
) -> None:
    """Write report.

    Args:
        report_path: Path to report.md.
        params: Parameters.
        items_bal: (n,p,q,time).
        items_unbal: (n,p,q,time).
    """
    lines: list[str] = []
    lines.append("# E051: Semiprimes: balanced vs unbalanced factorization timing")
    lines.append("")
    lines.append("### Parameters")
    lines.append("")
    lines.append(f"- sample_count: {params.sample_count}")
    lines.append(f"- balanced_bits: {params.balanced_bits}")
    lines.append(f"- small_factor_bits: {params.small_factor_bits}")
    lines.append(f"- trial_division_bound: {params.trial_division_bound}")
    lines.append("")
    lines.append("## Summary")
    lines.append("")
    tb = np.array([t for _, _, _, t in items_bal], dtype=float)
    tu = np.array([t for _, _, _, t in items_unbal], dtype=float)
    lines.append(f"- balanced median time: {float(np.median(tb)):.6f}s")
    lines.append(f"- unbalanced median time: {float(np.median(tu)):.6f}s")
    lines.append("")
    lines.append("## Samples (first 10)")
    lines.append("")
    lines.append("| category | n | p | q | time (s) |")
    lines.append("|:--|---:|---:|---:|---:|")
    for n, p, q, t in items_bal[:10]:
        lines.append(f"| balanced | {n} | {p} | {q} | {t:.6f} |")
    for n, p, q, t in items_unbal[:10]:
        lines.append(f"| unbalanced | {n} | {p} | {q} | {t:.6f} |")
    report_path.write_text("\n".join(lines) + "\n", encoding="utf-8")


# ------------------------------------------------------------------------------
def main() -> int:
    """Run the experiment.

    Returns:
        Exit code.
    """
    args = parse_experiment_args(
        experiment_id="e051",
        description="Semiprimes: balanced vs unbalanced factorization timing",
    )

    run_log = infer_run_log_file(out_dir=args.out_dir, experiment_slug="e051")
    setup_logging(config=LoggingConfig(verbose=args.verbose, log_file=run_log.log_file))
    set_global_seed(args.seed)

    params = Params(
        sample_count=24,
        balanced_bits=44,
        small_factor_bits=16,
        mr_bases=(2, 3, 5, 7, 11, 13, 17),
        trial_division_bound=2000,
    )
    out_paths = prepare_out_dir(out_dir=args.out_dir)

    rng = random.Random(args.seed)

    items_bal: list[tuple[int, int, int, float]] = []
    items_unbal: list[tuple[int, int, int, float]] = []

    for _ in range(params.sample_count):
        n, p, q = generate_semiprime_balanced(params.balanced_bits, rng, params.mr_bases)
        t0 = perf_counter()
        f = factor_semiprime(n, params.trial_division_bound)
        t1 = perf_counter()
        # ensure factor is valid
        assert n % f == 0
        items_bal.append((n, p, q, t1 - t0))

    for _ in range(params.sample_count):
        n, p, q = generate_semiprime_unbalanced(
            params.balanced_bits, params.small_factor_bits, rng, params.mr_bases
        )
        t0 = perf_counter()
        f = factor_semiprime(n, params.trial_division_bound)
        t1 = perf_counter()
        assert n % f == 0
        items_unbal.append((n, p, q, t1 - t0))

    times_bal = np.array([t for _, _, _, t in items_bal], dtype=float)
    times_unbal = np.array([t for _, _, _, t in items_unbal], dtype=float)

    fig1 = _plot_boxplot(times_bal=times_bal, times_unbal=times_unbal)
    save_figure(out_dir=out_paths.figures_dir, name="fig_01_factor_time_boxplot", fig=fig1)

    ns_all = np.array([n for n, _, _, _ in items_bal + items_unbal], dtype=np.int64)
    ts_all = np.array([t for _, _, _, t in items_bal + items_unbal], dtype=float)
    labs = ["balanced"] * len(items_bal) + ["unbalanced"] * len(items_unbal)
    fig2 = _plot_scatter(ns=ns_all, times=ts_all, labels=labs)
    save_figure(out_dir=out_paths.figures_dir, name="fig_02_factor_time_scatter", fig=fig2)

    write_json(out_paths.params_path, data=asdict(params))
    _write_report(
        report_path=out_paths.report_path,
        params=params,
        items_bal=items_bal,
        items_unbal=items_unbal,
    )

    logger.info("Experiment E051 completed successfully. Artifacts saved to: %s", args.out_dir)
    return 0


# ------------------------------------------------------------------------------
if __name__ == "__main__":
    raise SystemExit(main())
