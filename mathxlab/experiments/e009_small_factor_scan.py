"""E009 — Small-factor scan for Mersenne numbers.

Before running Lucas–Lehmer, many M_p are quickly ruled out by finding a
small prime factor q of M_p = 2^p - 1.

A necessary condition for q | (2^p - 1) is:
    2^p ≡ 1 (mod q)

Additionally, if p is an odd prime and q | (2^p - 1), then:
    q ≡ 1 (mod 2p)

This experiment searches q of the form q = 2*p*k + 1 up to a limit q_max.

Usage (repository convention):
    make run EXP=e009

Artifacts:
    - figures/fig_01_fraction_with_small_factor.png
    - figures/fig_02_found_factor_sizes.png
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
        p_max: Upper bound for prime exponents p (inclusive).
        max_tests: Cap on how many prime exponents to test.
        q_max: Upper bound for candidate factors q.
        require_q_prime: If True, sieve primes up to q_max and test only prime q.
    """

    p_max: int
    max_tests: int
    q_max: int
    require_q_prime: bool


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
def _prime_mask_up_to(n: int) -> np.ndarray:
    """Return boolean mask is_prime[0..n]."""
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
def find_small_factor_for_mp(
    p: int, *, q_max: int, require_q_prime: bool, is_prime_q: np.ndarray | None
) -> int | None:
    """Find a small factor q of M_p = 2^p - 1 up to q_max.

    Args:
        p: Prime exponent.
        q_max: Search limit for q.
        require_q_prime: Whether to restrict to prime q.
        is_prime_q: Boolean mask for primality up to q_max, required if require_q_prime is True.

    Returns:
        A factor q if found, otherwise None.
    """
    if p == 2:
        return None  # M_2 is prime; factor search not meaningful here
    step = 2 * p
    # q = 1 (mod 2p)
    k_max = (q_max - 1) // step
    for k in range(1, k_max + 1):
        q = step * k + 1
        if require_q_prime:
            if is_prime_q is None:
                raise ValueError("is_prime_q must be provided when require_q_prime=True")
            if not bool(is_prime_q[q]):
                continue
        # Check 2^p ≡ 1 (mod q)
        if pow(2, p, q) == 1:
            return q
    return None


# ------------------------------------------------------------------------------
def _plot_fraction(*, x: np.ndarray, frac: np.ndarray) -> fig.Figure:
    """Plot cumulative fraction of exponents with a small factor."""
    fig_obj, ax = plt.subplots()
    ax.plot(x, frac)
    ax.set_title("Fraction of tested M_p with a small factor ≤ q_max")
    ax.set_xlabel("test index")
    ax.set_ylabel("fraction")
    ax.set_ylim(0.0, 1.0)
    finalize_figure(fig_obj)
    return fig_obj


# ------------------------------------------------------------------------------
def _plot_factors(*, factors: np.ndarray) -> fig.Figure:
    """Plot distribution of found factor sizes."""
    fig_obj, ax = plt.subplots()
    ax.hist(factors, bins=40)
    ax.set_title("Sizes of first found factors q")
    ax.set_xlabel("q")
    ax.set_ylabel("count")
    ax.set_xscale("log")
    finalize_figure(fig_obj)
    return fig_obj


# ------------------------------------------------------------------------------
def _write_report(
    *, report_path: Path, params: Params, tested_p: list[int], factor_q: list[int | None]
) -> None:
    """Write a short Markdown report.

    Args:
        report_path: Path to report.md.
        params: Experiment parameters.
        tested_p: Prime exponents tested.
        factor_q: First found factor for each p (or None).
    """
    found = [(p, q) for p, q in zip(tested_p, factor_q, strict=True) if q is not None]
    lines = [
        "# E009 — Small-factor scan for Mersenne numbers",
        "",
        "**Reproduce:**",
        "",
        "```bash",
        "make run EXP=e009",
        "```",
        "",
        "## Parameters",
        f"- p_max: `{params.p_max}`",
        f"- max_tests: `{params.max_tests}`",
        f"- q_max: `{params.q_max}`",
        f"- require_q_prime: `{params.require_q_prime}`",
        "",
        "## Results",
        f"- tested exponents: `{len(tested_p)}`",
        f"- with small factor found: `{len(found)}`",
        "",
        "## Sample (first 20 with a found factor)",
        "",
        "| p | factor q |",
        "|---:|---:|",
    ]
    for p, q in found[:20]:
        lines.append(f"| {p} | {q} |")
    lines += [
        "",
        "## Notes",
        "- The congruence filter q ≡ 1 (mod 2p) is necessary but not sufficient.",
        "- A found q certifies M_p is composite; it does not factor M_p completely.",
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
        experiment_id="e009",
        description="Small-factor scan: search q | (2^p - 1) using q ≡ 1 (mod 2p)",
    )
    setup_logging(config=LoggingConfig(verbose=args.verbose))
    set_global_seed(args.seed)

    params = Params(
        p_max=10_000,
        max_tests=800,
        q_max=5_000_000,
        require_q_prime=True,
    )

    out_paths = prepare_out_dir(out_dir=args.out_dir)

    p_all = primes_up_to(params.p_max)[: params.max_tests]

    is_prime_q = _prime_mask_up_to(params.q_max) if params.require_q_prime else None

    tested_p: list[int] = []
    factor_q: list[int | None] = []

    for p in p_all:
        p_i = int(p)
        q = find_small_factor_for_mp(
            p_i,
            q_max=params.q_max,
            require_q_prime=params.require_q_prime,
            is_prime_q=is_prime_q,
        )
        tested_p.append(p_i)
        factor_q.append(q)

    found_mask = np.array([q is not None for q in factor_q], dtype=np.int64)
    cum_found = np.cumsum(found_mask)
    idx = np.arange(1, cum_found.size + 1, dtype=np.int64)
    frac = cum_found / idx.astype(np.float64)

    fig1 = _plot_fraction(x=idx, frac=frac)
    save_figure(out_dir=out_paths.figures_dir, name="fig_01_fraction_with_small_factor", fig=fig1)

    factors = np.array([q for q in factor_q if q is not None], dtype=np.int64)
    if factors.size > 0:
        fig2 = _plot_factors(factors=factors)
        save_figure(out_dir=out_paths.figures_dir, name="fig_02_found_factor_sizes", fig=fig2)
    else:
        logger.info("No factors found under q_max=%d; skipping factor histogram.", params.q_max)

    write_json(out_paths.params_path, data=asdict(params))
    _write_report(
        report_path=out_paths.report_path, params=params, tested_p=tested_p, factor_q=factor_q
    )

    logger.info("Experiment E009 completed successfully. Artifacts saved to: %s", args.out_dir)
    return 0


# ------------------------------------------------------------------------------
if __name__ == "__main__":
    raise SystemExit(main())
