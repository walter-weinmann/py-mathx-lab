"""E012 — Fermat pseudoprimes and Carmichael numbers (counterexamples).

The Fermat primality test is based on:

    If p is prime and gcd(a, p) = 1, then a^(p-1) ≡ 1 (mod p).

A composite n can still satisfy the same congruence for a given base a. Such an
n is called a *Fermat pseudoprime to base a*.

Even worse, *Carmichael numbers* are composite n for which:

    a^(n-1) ≡ 1 (mod n)  for all a coprime to n.

This experiment scans n up to a limit, finds Fermat pseudoprimes to a chosen
base, and detects Carmichael numbers via Korselt's criterion.

Usage (repository convention):
    make run EXP=e012

Artifacts:
    - figures/fig_01_cumulative_counts.png
    - figures/fig_02_smallest_factor_hist.png
    - params.json
    - report.md
"""

from __future__ import annotations

import math
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
        seed: Random seed for reproducibility.
        n_max: Upper bound for n (inclusive).
        base: Fermat test base a.
        max_listed: Maximum number of examples shown in the report tables.
    """

    seed: int
    n_max: int
    base: int
    max_listed: int


# ------------------------------------------------------------------------------
def primes_up_to(n: int) -> np.ndarray:
    """Compute all primes ≤ n using the Sieve of Eratosthenes.

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
def prime_mask_up_to(n: int) -> np.ndarray:
    """Return a boolean primality mask is_prime[0..n].

    Args:
        n: Upper bound (inclusive).

    Returns:
        Boolean array of length n+1, where is_prime[k] is True iff k is prime.
    """
    is_prime = np.ones(n + 1, dtype=bool)
    if n >= 0:
        is_prime[0] = False
    if n >= 1:
        is_prime[1] = False

    limit = int(n**0.5)
    for p in range(2, limit + 1):
        if is_prime[p]:
            is_prime[p * p : n + 1 : p] = False

    return is_prime


# ------------------------------------------------------------------------------
def factorize_trial_division(n: int, *, primes: np.ndarray) -> dict[int, int]:
    """Factorize n by trial division using a provided prime list.

    Args:
        n: Integer to factorize (n >= 2).
        primes: Primes used for trial division (should cover up to sqrt(n)).

    Returns:
        Dictionary {prime_factor: exponent}.
    """
    if n < 2:
        raise ValueError("n must be >= 2")

    remaining = n
    factors: dict[int, int] = {}

    for p in primes:
        p_i = int(p)
        if p_i * p_i > remaining:
            break
        if remaining % p_i != 0:
            continue

        exp = 0
        while remaining % p_i == 0:
            remaining //= p_i
            exp += 1
        factors[p_i] = exp

    if remaining > 1:
        factors[int(remaining)] = factors.get(int(remaining), 0) + 1

    return factors


# ------------------------------------------------------------------------------
def is_carmichael(n: int, *, primes: np.ndarray) -> tuple[bool, int]:
    """Check whether n is a Carmichael number using Korselt's criterion.

    Korselt's criterion:
        A composite n is Carmichael iff:
          1) n is squarefree, and
          2) for every prime p dividing n: (p-1) divides (n-1).

    Args:
        n: Integer to test (n >= 3 recommended).
        primes: Primes for trial-division factorization.

    Returns:
        Tuple (is_carmichael, smallest_prime_factor).

    Raises:
        ValueError: If n < 3.
    """
    if n < 3:
        raise ValueError("n must be >= 3")

    fac = factorize_trial_division(n, primes=primes)

    # n is prime iff fac == {n: 1}
    if len(fac) == 1 and next(iter(fac.items())) == (n, 1):
        return (False, n)

    smallest_pf = min(fac.keys())

    # Must be squarefree
    if any(exp != 1 for exp in fac.values()):
        return (False, smallest_pf)

    nm1 = n - 1
    for p in fac:
        if nm1 % (p - 1) != 0:
            return (False, smallest_pf)

    return (True, smallest_pf)


# ------------------------------------------------------------------------------
def _plot_cumulative(*, x: np.ndarray, pseudo: np.ndarray, carm: np.ndarray) -> fig.Figure:
    """Plot cumulative counts of pseudoprimes and Carmichael numbers.

    Args:
        x: Integer x-axis values.
        pseudo: Cumulative pseudoprime counts at x.
        carm: Cumulative Carmichael counts at x.

    Returns:
        Matplotlib figure.
    """
    fig_obj, ax = plt.subplots()
    ax.plot(x, pseudo, label="Fermat pseudoprimes (base a)")
    ax.plot(x, carm, label="Carmichael numbers")
    ax.set_title("Cumulative counts up to n")
    ax.set_xlabel("n")
    ax.set_ylabel("count")
    ax.legend(loc="best")
    finalize_figure(fig_obj)
    return fig_obj


# ------------------------------------------------------------------------------
def _plot_smallest_factor_hist(*, smallest_factors: np.ndarray) -> fig.Figure:
    """Plot histogram of smallest prime factors among found pseudoprimes.

    Args:
        smallest_factors: Array of smallest prime factors.

    Returns:
        Matplotlib figure.
    """
    fig_obj, ax = plt.subplots()
    ax.hist(smallest_factors, bins=40)
    ax.set_title("Smallest prime factor of Fermat pseudoprimes (base a)")
    ax.set_xlabel("smallest prime factor")
    ax.set_ylabel("count")
    ax.set_xscale("log")
    finalize_figure(fig_obj)
    return fig_obj


# ------------------------------------------------------------------------------
def _write_report(
    *,
    report_path: Path,
    params: Params,
    pseudoprimes: list[int],
    carmichaels: list[int],
) -> None:
    """Write a short Markdown report.

    Args:
        report_path: Path to report.md.
        params: Parameters used for this run.
        pseudoprimes: Fermat pseudoprimes to base `params.base`.
        carmichaels: Carmichael numbers.
    """
    lines: list[str] = [
        "# E012 — Fermat pseudoprimes and Carmichael numbers",
        "",
        "**Reproduce:**",
        "",
        "```bash",
        f'make run EXP=e012 ARGS="--seed {params.seed}"',
        "```",
        "",
        "## Parameters",
        f"- seed: `{params.seed}`",
        f"- n_max: `{params.n_max}`",
        f"- base a: `{params.base}`",
        f"- max_listed: `{params.max_listed}`",
        "",
        "## Summary",
        f"- Fermat pseudoprimes to base {params.base}: `{len(pseudoprimes)}`",
        f"- Carmichael numbers: `{len(carmichaels)}`",
        "",
        "## First examples (Fermat pseudoprimes)",
        "",
        "| # | n |",
        "|---:|---:|",
    ]
    for i, n in enumerate(pseudoprimes[: params.max_listed], start=1):
        lines.append(f"| {i} | {n} |")

    lines += [
        "",
        "## First examples (Carmichael numbers)",
        "",
        "| # | n |",
        "|---:|---:|",
    ]
    for i, n in enumerate(carmichaels[: params.max_listed], start=1):
        lines.append(f"| {i} | {n} |")

    lines += [
        "",
        "## Notes",
        "- Fermat's test is one-way: primes pass, but some composites also pass.",
        "- Carmichael numbers are the strongest counterexamples: they pass for all coprime bases.",
        "- Detection here uses Korselt's criterion (squarefree + divisibility conditions).",
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
        experiment_id="e012",
        description="Fermat pseudoprimes and Carmichael numbers (counterexamples)",
    )

    setup_logging(config=LoggingConfig(verbose=args.verbose))
    logger.info("Starting experiment E012")

    params = Params(
        seed=args.seed,
        n_max=200_000,
        base=2,
        max_listed=25,
    )

    set_global_seed(params.seed)
    out_paths = prepare_out_dir(out_dir=args.out_dir)

    # Trial-division primes (enough to cover sqrt(n_max)).
    primes = primes_up_to(math.isqrt(params.n_max) + 1)
    is_prime = prime_mask_up_to(params.n_max)

    pseudoprimes: list[int] = []
    carmichaels: list[int] = []
    pseudo_smallest_pf: list[int] = []

    pseudo_cum = np.zeros(params.n_max + 1, dtype=np.int64)
    carm_cum = np.zeros(params.n_max + 1, dtype=np.int64)

    pseudo_count = 0
    carm_count = 0

    a = params.base

    for n in range(3, params.n_max + 1):
        if bool(is_prime[n]):
            pseudo_cum[n] = pseudo_count
            carm_cum[n] = carm_count
            continue

        if math.gcd(a, n) != 1:
            pseudo_cum[n] = pseudo_count
            carm_cum[n] = carm_count
            continue

        if pow(a, n - 1, n) == 1:
            pseudo_count += 1
            pseudoprimes.append(n)

            is_carm, smallest_pf = is_carmichael(n, primes=primes)
            pseudo_smallest_pf.append(smallest_pf)

            if is_carm:
                carm_count += 1
                carmichaels.append(n)

        pseudo_cum[n] = pseudo_count
        carm_cum[n] = carm_count

    x = np.arange(0, params.n_max + 1, dtype=np.int64)

    fig1 = _plot_cumulative(x=x, pseudo=pseudo_cum, carm=carm_cum)
    save_figure(out_dir=out_paths.figures_dir, name="fig_01_cumulative_counts", fig=fig1)

    smallest_arr = np.array(pseudo_smallest_pf, dtype=np.int64)
    if smallest_arr.size > 0:
        fig2 = _plot_smallest_factor_hist(smallest_factors=smallest_arr)
        save_figure(out_dir=out_paths.figures_dir, name="fig_02_smallest_factor_hist", fig=fig2)

    write_json(out_paths.params_path, data=asdict(params))
    _write_report(
        report_path=out_paths.report_path,
        params=params,
        pseudoprimes=pseudoprimes,
        carmichaels=carmichaels,
    )

    logger.info("Experiment E012 completed successfully. Artifacts saved to: %s", args.out_dir)
    return 0


# ------------------------------------------------------------------------------
if __name__ == "__main__":
    raise SystemExit(main())
