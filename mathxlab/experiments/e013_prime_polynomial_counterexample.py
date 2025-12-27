"""E013 — Prime-polynomial counterexamples (Euler's n^2 + n + 41).

Euler's famous polynomial

    f(n) = n^2 + n + 41

produces primes for n = 0..39, but fails at n = 40:

    f(40) = 40^2 + 40 + 41 = 1681 = 41^2  (composite)

This experiment turns the "prime-generating polynomial" folklore into a clean,
visual counterexample and compares a few related quadratic polynomials.

Usage (repository convention):
    make run EXP=e013

Artifacts:
    - figures/fig_01_prime_indicator.png
    - figures/fig_02_initial_prime_run_lengths.png
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
        n_max: Maximum n value evaluated (inclusive).
        max_listed: Maximum number of examples shown in the report.
    """

    seed: int
    n_max: int
    max_listed: int


# ------------------------------------------------------------------------------
def prime_mask_up_to(n: int) -> np.ndarray:
    """Return a boolean primality mask is_prime[0..n].

    Args:
        n: Upper bound (inclusive).

    Returns:
        Boolean array of length n+1, where is_prime[k] is True iff k is prime.
    """
    if n < 0:
        raise ValueError("n must be >= 0")

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
def _format_factorization(factors: dict[int, int]) -> str:
    """Format a factorization dict as a compact product string.

    Args:
        factors: Dictionary {prime_factor: exponent}.

    Returns:
        Human-readable factorization string, e.g. "41^2 · 43".
    """
    parts: list[str] = []
    for p in sorted(factors.keys()):
        e = factors[p]
        if e == 1:
            parts.append(f"{p}")
        else:
            parts.append(f"{p}^{e}")
    return " · ".join(parts) if parts else "1"


# ------------------------------------------------------------------------------
def _polynomials() -> list[tuple[str, str]]:
    """Return the polynomials as Python expressions in variable n.

    The expressions are evaluated using `eval` with a restricted namespace.

    Returns:
        List of (label, expr) where expr uses only `n`.
    """
    return [
        ("n^2 + n + 41", "n*n + n + 41"),
        ("n^2 - n + 41", "n*n - n + 41"),
        ("n^2 + n + 17", "n*n + n + 17"),
    ]


# ------------------------------------------------------------------------------
def _eval_poly(expr: str, n: np.ndarray) -> np.ndarray:
    """Evaluate a polynomial expression on an integer vector.

    Args:
        expr: Expression string using variable `n` only.
        n: Integer numpy array.

    Returns:
        Integer numpy array of the same shape.
    """
    # Restricted eval: only 'n' is available.
    return np.array(eval(expr, {"__builtins__": {}}, {"n": n}), dtype=np.int64)


# ------------------------------------------------------------------------------
def _first_composite_index(values: np.ndarray, is_prime: np.ndarray) -> int | None:
    """Find the first index where values[i] is composite (>= 2) and not prime.

    Args:
        values: Evaluated polynomial values for n=0..n_max.
        is_prime: Prime mask up to max(values).

    Returns:
        Index i of the first composite value, or None if all are prime in range.
    """
    for i, v in enumerate(values):
        v_i = int(v)
        if v_i < 2:
            return i
        if not bool(is_prime[v_i]):
            return i
    return None


# ------------------------------------------------------------------------------
def _initial_prime_run_length(values: np.ndarray, is_prime: np.ndarray) -> int:
    """Compute the length of the initial consecutive-prime run from n=0.

    Args:
        values: Evaluated polynomial values for n=0..n_max.
        is_prime: Prime mask up to max(values).

    Returns:
        The count of consecutive n starting at 0 such that f(n) is prime.
    """
    run = 0
    for v in values:
        v_i = int(v)
        if v_i < 2:
            break
        if not bool(is_prime[v_i]):
            break
        run += 1
    return run


# ------------------------------------------------------------------------------
def _plot_prime_indicator(
    *,
    n: np.ndarray,
    series: list[tuple[str, np.ndarray]],
) -> fig.Figure:
    """Plot prime indicator (0/1) versus n for multiple polynomials.

    Args:
        n: n-grid.
        series: List of (label, prime_indicator) arrays.

    Returns:
        Matplotlib figure.
    """
    fig_obj, ax = plt.subplots()
    for label, indicator in series:
        ax.plot(n, indicator, label=label)
    ax.set_title("Prime indicator for quadratic polynomials")
    ax.set_xlabel("n")
    ax.set_ylabel("is_prime(f(n))")
    ax.set_yticks([0, 1])
    ax.legend(loc="best")
    finalize_figure(fig_obj)
    return fig_obj


# ------------------------------------------------------------------------------
def _plot_run_lengths(*, labels: list[str], run_lengths: np.ndarray) -> fig.Figure:
    """Plot initial prime-run lengths for each polynomial.

    Args:
        labels: Polynomial labels.
        run_lengths: Initial prime-run lengths.

    Returns:
        Matplotlib figure.
    """
    fig_obj, ax = plt.subplots()
    x = np.arange(len(labels), dtype=np.int64)
    ax.bar(x, run_lengths)
    ax.set_title("Initial consecutive-prime run length (starting at n=0)")
    ax.set_xlabel("polynomial")
    ax.set_ylabel("run length")
    ax.set_xticks(x)
    ax.set_xticklabels(labels, rotation=15, ha="right")
    finalize_figure(fig_obj)
    return fig_obj


# ------------------------------------------------------------------------------
def _write_report(
    *,
    report_path: Path,
    params: Params,
    results: list[dict[str, object]],
) -> None:
    """Write a short Markdown report.

    Args:
        report_path: Path to report.md.
        params: Parameters used for this run.
        results: Per-polynomial result dictionaries.
    """
    lines: list[str] = [
        "# E013 — Prime-polynomial counterexamples (Euler's n^2 + n + 41)",
        "",
        "**Reproduce:**",
        "",
        "```bash",
        "make run EXP=e013",
        "```",
        "",
        "## Parameters",
        f"- n_max: `{params.n_max}`",
        f"- max_listed: `{params.max_listed}`",
        "",
        "## Summary table",
        "",
        "| polynomial | initial prime run | first composite n | f(n) | factorization |",
        "|---|---:|---:|---:|---|",
    ]

    for r in results:
        poly = str(r["poly"])
        run_len = int(r["run_len"])  # type: ignore[call-overload]
        first_n = r["first_composite_n"]
        first_v = r["first_composite_value"]
        fac = r["first_composite_factorization"]

        if first_n is None:
            lines.append(f"| `{poly}` | {run_len} | _none_ | _none_ | _none_ |")
        else:
            lines.append(
                f"| `{poly}` | {run_len} | {int(first_n)} | {int(first_v)} | {fac} |"  # type: ignore[call-overload]
            )

    lines += [
        "",
        "## Notes",
        "- Euler's polynomial f(n)=n^2+n+41 is prime for n=0..39, but f(40)=41^2 is composite.",
        "- Quadratics can look 'prime-rich' on small ranges, which is a classic trap for intuition.",
        "- This experiment focuses on the *first* visible failure (counterexample) for each polynomial.",
        "",
        "## Outputs",
        "- `figures/fig_01_prime_indicator.png`",
        "- `figures/fig_02_initial_prime_run_lengths.png`",
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
        experiment_id="e013",
        description="Prime-polynomial counterexamples (Euler's n^2 + n + 41)",
    )

    setup_logging(config=LoggingConfig(verbose=args.verbose))
    set_global_seed(args.seed)
    logger.info("Starting experiment E013")

    params = Params(
        seed=args.seed,
        n_max=300,
        max_listed=10,
    )

    out_paths = prepare_out_dir(out_dir=args.out_dir)

    n = np.arange(0, params.n_max + 1, dtype=np.int64)

    polys = _polynomials()
    values_list: list[tuple[str, np.ndarray]] = [
        (label, _eval_poly(expr, n)) for label, expr in polys
    ]

    max_value = max(int(np.max(vals)) for _, vals in values_list)
    is_prime_val = prime_mask_up_to(max_value)

    # primes for factorization (only up to sqrt(max_value) needed)
    primes = primes_up_to(math.isqrt(max_value) + 1)

    indicator_series: list[tuple[str, np.ndarray]] = []
    run_lengths: list[int] = []
    results: list[dict[str, object]] = []

    for label, vals in values_list:
        indicator = np.array(
            [1 if (int(v) >= 2 and bool(is_prime_val[int(v)])) else 0 for v in vals], dtype=np.int64
        )
        indicator_series.append((label, indicator))

        run_len = _initial_prime_run_length(vals, is_prime_val)
        run_lengths.append(run_len)

        first_i = _first_composite_index(vals, is_prime_val)
        if first_i is None:
            results.append(
                {
                    "poly": label,
                    "run_len": run_len,
                    "first_composite_n": None,
                    "first_composite_value": None,
                    "first_composite_factorization": None,
                }
            )
            continue

        v_first = int(vals[first_i])
        if v_first < 2:
            fac_str = "not prime by definition"
        else:
            fac = factorize_trial_division(v_first, primes=primes)
            fac_str = _format_factorization(fac)

        results.append(
            {
                "poly": label,
                "run_len": run_len,
                "first_composite_n": int(first_i),
                "first_composite_value": v_first,
                "first_composite_factorization": fac_str,
            }
        )

    fig1 = _plot_prime_indicator(n=n, series=indicator_series)
    save_figure(out_dir=out_paths.figures_dir, name="fig_01_prime_indicator", fig=fig1)

    fig2 = _plot_run_lengths(
        labels=[lbl for lbl, _ in values_list], run_lengths=np.array(run_lengths, dtype=np.int64)
    )
    save_figure(out_dir=out_paths.figures_dir, name="fig_02_initial_prime_run_lengths", fig=fig2)

    write_json(out_paths.params_path, data=asdict(params))
    _write_report(report_path=out_paths.report_path, params=params, results=results)

    logger.info("Experiment E013 completed successfully. Artifacts saved to: %s", args.out_dir)
    return 0


# ------------------------------------------------------------------------------
if __name__ == "__main__":
    raise SystemExit(main())
