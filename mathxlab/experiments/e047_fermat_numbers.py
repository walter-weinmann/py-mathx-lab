"""E047 — Fermat numbers: Pépin test and factor witnesses.

Fermat numbers are:

    F_n = 2^(2^n) + 1

This experiment demonstrates the classic counterexample story:
Fermat conjectured that all F_n are prime, but F_5 is composite.

We run:
- a Pépin test (primality certificate for Fermat numbers, for n >= 1),
- a bounded small-factor search to recover concrete factor witnesses,
- a lightweight visualization of growth and factor discovery.

Usage (repository convention):
    make run EXP=e047

Artifacts:
    - figures/fig_01_log10_Fn.png
    - figures/fig_02_smallest_factor.png
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
from mathxlab.experiments._prime_utils import primes_up_to

# ------------------------------------------------------------------------------
logger = get_logger(__name__)


# ------------------------------------------------------------------------------
@dataclass(frozen=True, slots=True)
class Params:
    """Experiment parameters.

    Args:
        n_max: Maximum Fermat index n to analyze (inclusive).
        factor_prime_bound: Upper bound for trial division primes when searching for a factor witness.
    """

    n_max: int
    factor_prime_bound: int


# ------------------------------------------------------------------------------
def fermat_number(n: int) -> int:
    """Compute the Fermat number F_n = 2^(2^n) + 1.

    Args:
        n: Fermat index.

    Returns:
        Fermat number F_n.
    """
    return (1 << (1 << n)) + 1


# ------------------------------------------------------------------------------
def pepin_is_prime(n: int, fn: int) -> bool:
    r"""Apply Pépin's test for Fermat numbers.

    Pépin's test: For n >= 1, F_n is prime iff
        3^((F_n - 1)/2) ≡ -1 (mod F_n)

    Notes:
        For Matplotlib mathtext in plots, avoid ``\pmod`` and use
        ``(\mathrm{mod}\ F_n)`` instead.

    Args:
        n: Fermat index.
        fn: The Fermat number F_n.

    Returns:
        True if fn passes Pépin's test, False otherwise.
    """
    if n < 1:
        raise ValueError("Pépin test is defined for n >= 1.")
    exp = (fn - 1) // 2
    return pow(3, exp, fn) == fn - 1  # -1 mod fn


# ------------------------------------------------------------------------------
def find_small_factor(fn: int, primes: np.ndarray) -> int | None:
    """Find a small prime factor of fn via trial division.

    Args:
        fn: Integer to factor.
        primes: Candidate primes to test.

    Returns:
        The smallest prime factor if found, otherwise None.
    """
    for p in primes.tolist():
        if p * p > fn:
            return None
        if fn % p == 0:
            return int(p)
    return None


# ------------------------------------------------------------------------------
def _plot_log10_growth(ns: list[int], log10_fn: list[float], is_prime: list[bool]) -> fig.Figure:
    """Plot log10(F_n) as a function of n and mark primality (via Pépin).

    Args:
        ns: Indices n.
        log10_fn: log10(F_n) values.
        is_prime: Flags from Pépin test (True for prime).

    Returns:
        Matplotlib figure.
    """
    fig1 = plt.figure(figsize=(9, 4.5))
    ax = fig1.add_subplot(1, 1, 1)
    ax.plot(ns, log10_fn, marker="o", linewidth=1.2)
    for n, y, ok in zip(ns, log10_fn, is_prime, strict=True):
        ax.annotate("prime" if ok else "comp.", (n, y), textcoords="offset points", xytext=(6, 6))
    ax.set_title(r"Fermat growth: $\log_{10}(F_n)$ with Pépin labels")
    ax.set_xlabel("n")
    ax.set_ylabel(r"$\log_{10}(F_n)$")
    ax.grid(True, alpha=0.25)
    return fig1


# ------------------------------------------------------------------------------
def _plot_smallest_factor(ns: list[int], factors: list[int | None]) -> fig.Figure:
    """Plot the smallest found factor (if any) vs n.

    Args:
        ns: Indices n.
        factors: Smallest found prime factor, or None.

    Returns:
        Matplotlib figure.
    """
    fig2 = plt.figure(figsize=(9, 4.5))
    ax = fig2.add_subplot(1, 1, 1)
    y = [float(f) if f is not None else np.nan for f in factors]
    ax.plot(ns, y, marker="o", linewidth=1.2)
    ax.set_yscale("log")
    ax.set_title(r"Smallest trial-division factor witness for $F_n$")
    ax.set_xlabel("n")
    ax.set_ylabel("smallest found factor (log scale)")
    ax.grid(True, alpha=0.25)
    return fig2


# ------------------------------------------------------------------------------
def _write_report(
    *, report_path: Path, params: Params, rows: list[tuple[int, int, bool, int | None]]
) -> None:
    """Write a short Markdown report.

    Args:
        report_path: Path to report.md.
        params: Parameters used.
        rows: (n, F_n, pepin_prime, smallest_factor).
    """
    lines: list[str] = []
    lines.append("# E047 — Fermat numbers: Pépin test and factor witnesses")
    lines.append("")
    lines.append("## Parameters")
    lines.append("")
    lines.append(f"- n_max: {params.n_max}")
    lines.append(f"- factor_prime_bound: {params.factor_prime_bound}")
    lines.append("")
    lines.append("## Results (bounded)")
    lines.append("")
    lines.append("| n | F_n | Pépin says prime? | smallest factor found |")
    lines.append("|---:|---:|:---:|---:|")
    for n, fn, ok, fac in rows:
        fac_s = str(fac) if fac is not None else "—"
        lines.append(f"| {n} | {fn} | {'✅' if ok else '❌'} | {fac_s} |")
    lines.append("")
    lines.append("### Notes")
    lines.append("")
    lines.append("- Pépin's test is definitive for Fermat numbers (n ≥ 1).")
    lines.append("- The factor search here is **bounded trial division**, meant to produce")
    lines.append("  small, explicit witnesses (e.g., for F_5 and F_6).")
    report_path.write_text("\n".join(lines) + "\n", encoding="utf-8")


# ------------------------------------------------------------------------------
def main() -> int:
    """Run the experiment.

    Returns:
        Process exit code (0 for success).
    """
    args = parse_experiment_args(
        experiment_id="e047",
        description="Fermat numbers: Pépin test + small factor witnesses",
    )
    setup_logging(config=LoggingConfig(verbose=args.verbose))
    set_global_seed(args.seed)

    params = Params(
        n_max=6,
        factor_prime_bound=1_000_000,
    )
    out_paths = prepare_out_dir(out_dir=args.out_dir)

    primes = primes_up_to(params.factor_prime_bound)

    rows: list[tuple[int, int, bool, int | None]] = []
    ns: list[int] = []
    log10_fn: list[float] = []
    is_prime: list[bool] = []
    factors: list[int | None] = []

    for n in range(0, params.n_max + 1):
        fn = fermat_number(n)
        ok = True if n == 0 else pepin_is_prime(n, fn)
        fac = find_small_factor(fn, primes) if not ok else None

        rows.append((n, fn, ok, fac))
        ns.append(n)
        log10_fn.append(math.log10(fn))
        is_prime.append(ok)
        factors.append(fac)

        logger.info("n=%s Fn=%s pepin_prime=%s factor=%s", n, fn, ok, fac)

    fig1 = _plot_log10_growth(ns=ns, log10_fn=log10_fn, is_prime=is_prime)
    save_figure(out_dir=out_paths.figures_dir, name="fig_01_log10_Fn", fig=fig1)

    fig2 = _plot_smallest_factor(ns=ns, factors=factors)
    save_figure(out_dir=out_paths.figures_dir, name="fig_02_smallest_factor", fig=fig2)

    write_json(out_paths.params_path, data=asdict(params))
    _write_report(report_path=out_paths.report_path, params=params, rows=rows)

    logger.info("Experiment E047 completed successfully. Artifacts saved to: %s", args.out_dir)
    return 0


# ------------------------------------------------------------------------------
if __name__ == "__main__":
    raise SystemExit(main())
