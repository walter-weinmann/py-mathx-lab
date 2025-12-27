"""E008 — Lucas–Lehmer scan for Mersenne primes.

This experiment applies the Lucas–Lehmer test (LLT) to M_p = 2^p - 1
for prime exponents p up to a chosen bound.

Usage (repository convention):
    make run EXP=e008

Artifacts:
    - figures/fig_01_time_vs_p.png
    - figures/fig_02_cumulative_primes.png
    - params.json
    - report.md
"""

from __future__ import annotations

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
        max_tests: Optional cap on how many prime exponents to test (for speed).
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
        return True  # M_2 = 3
    mp = (1 << p) - 1
    s = 4
    for _ in range(p - 2):
        s = (s * s - 2) % mp
    return s == 0


# ------------------------------------------------------------------------------
def _plot_time(*, p: np.ndarray, t_ms: np.ndarray) -> fig.Figure:
    """Plot LLT runtime vs p."""
    fig_obj, ax = plt.subplots()
    ax.plot(p, t_ms, marker="o", linestyle="none")
    ax.set_title("Lucas–Lehmer runtime per exponent")
    ax.set_xlabel("prime exponent p")
    ax.set_ylabel("time (ms)")
    ax.set_yscale("log")
    finalize_figure(fig_obj)
    return fig_obj


# ------------------------------------------------------------------------------
def _plot_cumulative(*, idx: np.ndarray, cum: np.ndarray) -> fig.Figure:
    """Plot cumulative count of Mersenne primes found."""
    fig_obj, ax = plt.subplots()
    ax.plot(idx, cum)
    ax.set_title("Cumulative Mersenne primes found")
    ax.set_xlabel("test index (prime exponents in increasing order)")
    ax.set_ylabel("count")
    finalize_figure(fig_obj)
    return fig_obj


# ------------------------------------------------------------------------------
def _write_report(
    *, report_path: Path, params: Params, tested_p: list[int], is_mp_prime: list[bool]
) -> None:
    """Write a short Markdown report.

    Args:
        report_path: Path to report.md.
        params: Experiment parameters.
        tested_p: Prime exponents tested.
        is_mp_prime: Corresponding primality outcomes.
    """
    found = [p for p, ok in zip(tested_p, is_mp_prime, strict=True) if ok]
    lines = [
        "# E008 — Lucas–Lehmer scan for Mersenne primes",
        "",
        "**Reproduce:**",
        "",
        "```bash",
        "make run EXP=e008",
        "```",
        "",
        "## Parameters",
        f"- p_max: `{params.p_max}`",
        f"- max_tests: `{params.max_tests}`",
        "",
        "## Results",
        f"- tested exponents: `{len(tested_p)}`",
        f"- Mersenne primes found: `{len(found)}`",
        "",
        "### Prime exponents p where M_p is prime",
        "",
    ]
    if found:
        lines.append(", ".join(str(p) for p in found))
    else:
        lines.append("_none in this range (or max_tests too small)_")
    lines += [
        "",
        "## Notes",
        "- LLT is a deterministic primality test specialized to M_p = 2^p - 1.",
        "- Only prime exponents p need to be tested: if 2^n-1 is prime, then n must be prime.",
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
        experiment_id="e008",
        description="Lucas–Lehmer scan: test M_p = 2^p - 1 for prime exponents p",
    )
    setup_logging(config=LoggingConfig(verbose=args.verbose))
    set_global_seed(args.seed)

    params = Params(
        p_max=10_000,
        max_tests=600,
    )

    out_paths = prepare_out_dir(out_dir=args.out_dir)

    p_all = primes_up_to(params.p_max)
    tested_p: list[int] = []
    is_mp_prime: list[bool] = []
    t_ms: list[float] = []

    for p in p_all[: params.max_tests]:
        p_i = int(p)
        t0 = perf_counter()
        ok = lucas_lehmer_is_prime(p_i)
        dt = (perf_counter() - t0) * 1000.0

        tested_p.append(p_i)
        is_mp_prime.append(bool(ok))
        t_ms.append(float(dt))

    p_arr = np.array(tested_p, dtype=np.int64)
    t_arr = np.array(t_ms, dtype=np.float64)

    cum = np.cumsum(np.array(is_mp_prime, dtype=np.int64))
    idx = np.arange(1, cum.size + 1, dtype=np.int64)

    fig1 = _plot_time(p=p_arr, t_ms=t_arr)
    save_figure(out_dir=out_paths.figures_dir, name="fig_01_time_vs_p", fig=fig1)

    fig2 = _plot_cumulative(idx=idx, cum=cum)
    save_figure(out_dir=out_paths.figures_dir, name="fig_02_cumulative_primes", fig=fig2)

    write_json(out_paths.params_path, data=asdict(params))
    _write_report(
        report_path=out_paths.report_path, params=params, tested_p=tested_p, is_mp_prime=is_mp_prime
    )

    logger.info("Experiment E008 completed successfully. Artifacts saved to: %s", args.out_dir)
    return 0


# ------------------------------------------------------------------------------
if __name__ == "__main__":
    raise SystemExit(main())
