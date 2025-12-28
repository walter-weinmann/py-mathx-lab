"""E048 — Carmichael numbers: Korselt scan + Fermat counterexamples.

Carmichael numbers are composite n such that for all a coprime to n:

    a^(n-1) ≡ 1 (mod n)

They are "absolute Fermat pseudoprimes" and are the canonical counterexamples to
the naive Fermat primality test.

This experiment:
- enumerates squarefree products of three primes <= N,
- checks Korselt's criterion to detect Carmichael numbers,
- verifies Fermat congruences for a small set of bases,
- visualizes the distribution of discovered Carmichael numbers.

Usage (repository convention):
    make run EXP=e048

Artifacts:
    - figures/fig_01_carmichael_growth.png
    - figures/fig_02_fermat_bases_pass.png
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
        n_max: Upper bound for Carmichael search.
        base_list: Bases to verify Fermat congruence a^(n-1) ≡ 1 (mod n).
        max_results: Maximum number of Carmichael numbers to keep (after sorting).
    """

    n_max: int
    base_list: tuple[int, ...]
    max_results: int


# ------------------------------------------------------------------------------
def is_carmichael_korselt(n: int, factors: tuple[int, int, int]) -> bool:
    """Check Korselt's criterion for a squarefree n with known prime factors.

    For squarefree n, Korselt says:
        n is Carmichael  <=>  for every prime p|n, (p-1) divides (n-1).

    Args:
        n: Candidate integer (composite).
        factors: Prime factors (p, q, r).

    Returns:
        True if Korselt's criterion holds, otherwise False.
    """
    n1 = n - 1
    return all(n1 % (p - 1) == 0 for p in factors)


# ------------------------------------------------------------------------------
def fermat_passes_for_bases(n: int, bases: tuple[int, ...]) -> int:
    """Count how many bases pass Fermat congruence for n.

    Args:
        n: Candidate integer (typically Carmichael).
        bases: Bases to test.

    Returns:
        Count of bases a with gcd(a, n)=1 and a^(n-1) ≡ 1 (mod n).
    """
    passed = 0
    for a in bases:
        if math.gcd(a, n) != 1:
            continue
        if pow(a, n - 1, n) == 1:
            passed += 1
    return passed


# ------------------------------------------------------------------------------
def enumerate_carmichael_three_prime(*, n_max: int) -> list[tuple[int, tuple[int, int, int]]]:
    """Enumerate Carmichael numbers n <= n_max with exactly three prime factors.

    Notes:
        Many small Carmichael numbers have exactly three prime factors, making
        this a good "step 0" experiment.

    Args:
        n_max: Upper bound.

    Returns:
        List of (n, (p,q,r)) sorted by n.
    """
    # Conservative prime limit for enumeration.
    # p*q*r <= n_max => p <= n_max^(1/3)
    p_max = round(n_max ** (1.0 / 3.0)) + 1
    primes = primes_up_to(max(p_max, 100))
    results: list[tuple[int, tuple[int, int, int]]] = []

    for _i, p in enumerate(primes.tolist()):
        # q can be larger; keep a safe upper bound
        q_max = math.isqrt(n_max // p) + 1
        qs = primes_up_to(q_max)
        for q in qs.tolist():
            if q <= p:
                continue
            pq = p * q
            if pq > n_max:
                break
            r_max = n_max // pq
            rs = primes_up_to(r_max)
            for r in rs.tolist():
                if r <= q:
                    continue
                n = pq * r
                if n > n_max:
                    break
                if is_carmichael_korselt(n, (p, q, r)):
                    results.append((n, (p, q, r)))
    results.sort(key=lambda x: x[0])
    return results


# ------------------------------------------------------------------------------
def _plot_growth(ns: np.ndarray) -> fig.Figure:
    """Plot the index of Carmichael numbers vs their value.

    Args:
        ns: Sorted Carmichael numbers.

    Returns:
        Matplotlib figure.
    """
    fig1 = plt.figure(figsize=(9, 4.5))
    ax = fig1.add_subplot(1, 1, 1)
    ax.plot(ns, np.arange(1, len(ns) + 1), marker=".", linestyle="none")
    ax.set_xscale("log")
    ax.set_title("Carmichael numbers (3 prime factors): index vs n")
    ax.set_xlabel("n (log scale)")
    ax.set_ylabel("index (count)")
    ax.grid(True, alpha=0.25)
    return fig1


# ------------------------------------------------------------------------------
def _plot_fermat_passes(ns: np.ndarray, pass_counts: np.ndarray, base_count: int) -> fig.Figure:
    """Plot how many Fermat bases pass for each Carmichael number.

    Args:
        ns: Carmichael numbers.
        pass_counts: Number of bases that pass.
        base_count: Number of bases in the test set.

    Returns:
        Matplotlib figure.
    """
    fig2 = plt.figure(figsize=(9, 4.5))
    ax = fig2.add_subplot(1, 1, 1)
    ax.scatter(ns, pass_counts, s=10)
    ax.set_xscale("log")
    ax.set_ylim(-0.5, base_count + 0.5)
    ax.set_title(r"Fermat passes for Carmichael n: $a^{n-1}\equiv 1\ (\mathrm{mod}\ n)$")
    ax.set_xlabel("n (log scale)")
    ax.set_ylabel("bases passed (coprime bases only)")
    ax.grid(True, alpha=0.25)
    return fig2


# ------------------------------------------------------------------------------
def _write_report(
    *,
    report_path: Path,
    params: Params,
    items: list[tuple[int, tuple[int, int, int]]],
    base_pass: dict[int, int],
) -> None:
    """Write a short Markdown report.

    Args:
        report_path: Path to report.md.
        params: Experiment parameters.
        items: List of (n, factors).
        base_pass: Mapping n -> number of bases passed.
    """
    lines: list[str] = []
    lines.append("# E048 — Carmichael numbers: Korselt scan + Fermat counterexamples")
    lines.append("")
    lines.append("## Parameters")
    lines.append("")
    lines.append(f"- n_max: {params.n_max}")
    lines.append(f"- bases: {', '.join(str(b) for b in params.base_list)}")
    lines.append("")
    lines.append("## Smallest Carmichael numbers found (3 prime factors)")
    lines.append("")
    lines.append("| n | factorization | Fermat bases passed |")
    lines.append("|---:|:--|---:|")
    for n, (p, q, r) in items[:20]:
        lines.append(f"| {n} | {p}·{q}·{r} | {base_pass[n]} |")
    lines.append("")
    lines.append("### Notes")
    lines.append("")
    lines.append("- These n are composite yet pass Fermat's congruence for **all** coprime bases.")
    lines.append(
        "- The scan here is restricted to squarefree products of **three** primes, which already"
    )
    lines.append("  recovers many classical examples (e.g., 561 = 3·11·17).")
    report_path.write_text("\n".join(lines) + "\n", encoding="utf-8")


# ------------------------------------------------------------------------------
def main() -> int:
    """Run the experiment.

    Returns:
        Process exit code (0 for success).
    """
    args = parse_experiment_args(
        experiment_id="e048",
        description="Carmichael numbers: Korselt scan + Fermat counterexamples",
    )
    setup_logging(config=LoggingConfig(verbose=args.verbose))
    set_global_seed(args.seed)

    params = Params(
        n_max=5_000_000,
        base_list=(2, 3, 5, 7, 11, 13),
        max_results=5000,
    )
    out_paths = prepare_out_dir(out_dir=args.out_dir)

    items = enumerate_carmichael_three_prime(n_max=params.n_max)
    if len(items) > params.max_results:
        items = items[: params.max_results]

    ns = np.array([n for n, _ in items], dtype=np.int64)
    base_pass: dict[int, int] = {}
    pass_counts = np.empty(len(items), dtype=np.int64)
    for i, (n, _) in enumerate(items):
        c = fermat_passes_for_bases(n, params.base_list)
        base_pass[n] = c
        pass_counts[i] = c

    fig1 = _plot_growth(ns=ns)
    save_figure(out_dir=out_paths.figures_dir, name="fig_01_carmichael_growth", fig=fig1)

    fig2 = _plot_fermat_passes(ns=ns, pass_counts=pass_counts, base_count=len(params.base_list))
    save_figure(out_dir=out_paths.figures_dir, name="fig_02_fermat_bases_pass", fig=fig2)

    write_json(out_paths.params_path, data=asdict(params))
    _write_report(
        report_path=out_paths.report_path, params=params, items=items, base_pass=base_pass
    )

    logger.info("Experiment E048 completed successfully. Artifacts saved to: %s", args.out_dir)
    return 0


# ------------------------------------------------------------------------------
if __name__ == "__main__":
    raise SystemExit(main())
