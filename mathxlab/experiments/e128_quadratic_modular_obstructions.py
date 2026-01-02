"""E128 — Modular obstructions for Euler-type quadratic prime polynomials.

Euler's polynomial

    f(n) = n^2 + n + 41

is prime for n=0..39, but it has a built-in divisibility pattern:

    f(41k) is divisible by 41  (for k >= 1).

This experiment makes such modular structure explicit by scanning small prime
moduli p, computing the set of residues n (mod p) for which

    f(n) ≡ 0 (mod p),

and writing a short report with concrete witnesses.

Usage (repository convention):
    make run EXP=e128

Artifacts:
    - figures/fig_01_root_counts_mod_p.png
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
from mathxlab.exp.run_logging import infer_run_log_file
from mathxlab.experiments._prime_utils import primes_up_to
from mathxlab.plots.helpers import finalize_figure

# ------------------------------------------------------------------------------
logger = get_logger(__name__)


# ------------------------------------------------------------------------------
@dataclass(frozen=True, slots=True)
class Params:
    """Experiment parameters.

    Args:
        seed: Random seed for reproducibility.
        a: Linear coefficient in f(n) = n^2 + a n + b.
        b: Constant term in f(n) = n^2 + a n + b.
        p_max: Largest prime modulus included in the scan.
        max_listed: Maximum number of primes listed in the report table.
        witness_k: Number of k-values shown for the special n = b*k witness.
    """

    seed: int
    a: int
    b: int
    p_max: int
    max_listed: int
    witness_k: int


# ------------------------------------------------------------------------------
def _eval_quadratic_mod(n: int, *, a: int, b: int, p: int) -> int:
    """Evaluate f(n)=n^2 + a n + b modulo p.

    Args:
        n: Integer residue.
        a: Linear coefficient.
        b: Constant term.
        p: Modulus.

    Returns:
        f(n) mod p in [0, p-1].
    """
    return (n * n + a * n + b) % p


# ------------------------------------------------------------------------------
def _roots_mod_p(*, a: int, b: int, p: int) -> list[int]:
    """Compute residues n (mod p) such that f(n) ≡ 0 (mod p).

    For the small p used here, brute force is simplest and fast.

    Args:
        a: Linear coefficient.
        b: Constant term.
        p: Prime modulus.

    Returns:
        Sorted list of residues n in {0,...,p-1} with f(n) ≡ 0 (mod p).
    """
    roots = [n for n in range(p) if _eval_quadratic_mod(n, a=a, b=b, p=p) == 0]
    roots.sort()
    return roots


# ------------------------------------------------------------------------------
def _plot_root_counts(*, primes: np.ndarray, root_counts: np.ndarray) -> fig.Figure:
    """Plot how many roots f(n) ≡ 0 (mod p) exist for each prime p.

    Args:
        primes: Array of primes.
        root_counts: Array of root counts per prime.

    Returns:
        Matplotlib figure.
    """
    fig_obj, ax = plt.subplots()
    ax.plot(primes, root_counts, marker="o", linestyle="none")
    ax.set_title(r"Number of roots of $f(n)\equiv 0\ (\mathrm{mod}\ p)$ for small primes $p$")
    ax.set_xlabel(r"$p$")
    ax.set_ylabel("root count in {0,...,p-1}")
    ax.set_yticks([0, 1, 2])
    finalize_figure(fig_obj)
    return fig_obj


# ------------------------------------------------------------------------------
def _write_report(
    *,
    report_path: Path,
    params: Params,
    primes: np.ndarray,
    roots_by_p: dict[int, list[int]],
) -> None:
    """Write a short Markdown report.

    Args:
        report_path: Output report path.
        params: Experiment parameters.
        primes: List of primes scanned.
        roots_by_p: Mapping p -> list of roots modulo p.
    """
    lines: list[str] = [
        "# E128 — Modular obstructions for quadratic prime polynomials",
        "",
        "**Reproduce:**",
        "",
        "```bash",
        "make run EXP=e128",
        "```",
        "",
        "## Parameters",
        f"- a: `{params.a}`",
        f"- b: `{params.b}`",
        f"- p_max: `{params.p_max}`",
        f"- max_listed: `{params.max_listed}`",
        f"- witness_k: `{params.witness_k}`",
        "",
        "## Key observation",
        "For any modulus p, the congruence f(n)≡0 (mod p) selects residue classes.",
        "Whenever n hits such a class, f(n) is divisible by p and therefore composite",
        "(unless f(n)=p).",
        "",
    ]

    a = params.a
    b = params.b

    if b != 0:
        lines += [
            "## A built-in infinite composite subsequence (Euler-style)",
            "For f(n)=n^2+an+b and n=bk:",
            r"$$f(bk) = (bk)^2 + a(bk) + b = b\,(b k^2 + a k + 1).$$",
            "So for k≥1, f(bk) is divisible by b (in absolute value).",
            "",
            "| k | n=bk | f(n) | divisible by |",
            "|---:|---:|---:|:---|",
        ]
        for k in range(1, params.witness_k + 1):
            n_val = b * k
            v = n_val * n_val + a * n_val + b
            lines.append(f"| {k} | {n_val} | {v} | {abs(b)} |")
        lines.append("")

    lines += [
        "## Roots modulo small primes",
        "The table below lists primes p for which f(n)≡0 (mod p) has solutions.",
        "",
        "| p | root count | roots n (mod p) |",
        "|---:|---:|:---|",
    ]

    listed = 0
    for p in primes:
        p_i = int(p)
        roots = roots_by_p.get(p_i, [])
        if not roots:
            continue
        listed += 1
        if listed > params.max_listed:
            break
        roots_str = ", ".join(str(r) for r in roots)
        lines.append(f"| {p_i} | {len(roots)} | {roots_str} |")

    if listed > params.max_listed:
        lines.append("")
        lines.append(f"*(truncated to first {params.max_listed} primes with roots)*")

    lines += [
        "",
        "## Outputs",
        "- `figures/fig_01_root_counts_mod_p.png`",
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
        experiment_id="e128",
        description="Modular obstructions for Euler-type quadratic prime polynomials",
    )

    run_log = infer_run_log_file(out_dir=args.out_dir, experiment_slug="e128")
    setup_logging(config=LoggingConfig(verbose=args.verbose, log_file=run_log.log_file))
    set_global_seed(args.seed)
    logger.info("Starting experiment E128")

    params = Params(
        seed=args.seed,
        a=1,
        b=41,
        p_max=199,
        max_listed=25,
        witness_k=6,
    )

    out_paths = prepare_out_dir(out_dir=args.out_dir)

    primes = primes_up_to(params.p_max)
    roots_by_p: dict[int, list[int]] = {}
    root_counts = np.zeros(len(primes), dtype=np.int64)

    for i, p in enumerate(primes):
        p_i = int(p)
        roots = _roots_mod_p(a=params.a, b=params.b, p=p_i)
        roots_by_p[p_i] = roots
        root_counts[i] = len(roots)

    fig1 = _plot_root_counts(primes=primes, root_counts=root_counts)
    save_figure(out_dir=out_paths.figures_dir, name="fig_01_root_counts_mod_p", fig=fig1)

    write_json(out_paths.params_path, data=asdict(params))
    _write_report(
        report_path=out_paths.report_path, params=params, primes=primes, roots_by_p=roots_by_p
    )

    logger.info("Experiment E128 completed successfully. Artifacts saved to: %s", args.out_dir)
    return 0


# ------------------------------------------------------------------------------
if __name__ == "__main__":
    raise SystemExit(main())
