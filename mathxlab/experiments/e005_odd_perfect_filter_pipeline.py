"""E005 — Odd perfect numbers: constraint filter pipeline.

Odd perfect numbers are an open problem: it is unknown whether any exist.

This experiment does NOT attempt to discover an odd perfect number. Instead, it
makes well-known *necessary conditions* tangible by applying them as staged filters
to the set of odd integers up to N and plotting a survival curve.

Implemented necessary conditions (conservative set):
    1) Touchard congruence:
        n ≡ 1 (mod 12)  OR  n ≡ 9 (mod 36)
    2) Euler form constraint:
        n = q^a * m^2 with q prime, gcd(q,m)=1, and q ≡ a ≡ 1 (mod 4)

Usage (repository convention):
    make run EXP=e005

Artifacts:
    - figures/fig_01_survival_curve.png
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
        n_max: Upper bound N (inclusive).
        stride_plot: Plotting stride for scatter/curve (visual only).
    """

    n_max: int
    stride_plot: int


# ------------------------------------------------------------------------------
def spf_sieve(n_max: int) -> np.ndarray:
    """Compute smallest-prime-factor (SPF) array for 2..N.

    Args:
        n_max: Upper bound N (inclusive).

    Returns:
        Array spf where spf[n] is the smallest prime dividing n (spf[0]=spf[1]=0).
    """
    spf = np.zeros(n_max + 1, dtype=np.int32)
    for i in range(2, n_max + 1):
        if spf[i] == 0:
            spf[i] = i
            if i <= n_max // i:
                spf[i * i :: i] = np.where(spf[i * i :: i] == 0, i, spf[i * i :: i])
    return spf


# ------------------------------------------------------------------------------
def factorize_with_spf(n: int, spf: np.ndarray) -> dict[int, int]:
    """Factorize n using the SPF table.

    Args:
        n: Integer to factorize (n >= 1).
        spf: Smallest-prime-factor table.

    Returns:
        Dictionary {prime: exponent}.
    """
    if n < 1:
        raise ValueError("n must be >= 1")
    if n == 1:
        return {}
    x = n
    factors: dict[int, int] = {}
    while x > 1:
        p = int(spf[x]) if x < spf.size else 0
        if p == 0:
            # Fallback: x is prime or outside table.
            factors[x] = factors.get(x, 0) + 1
            break
        factors[p] = factors.get(p, 0) + 1
        x //= p
    return factors


# ------------------------------------------------------------------------------
def touchard_congruence(n: int) -> bool:
    """Check the Touchard congruence condition for odd perfect numbers.

    Args:
        n: Odd integer.

    Returns:
        True if n satisfies n ≡ 1 (mod 12) or n ≡ 9 (mod 36).
    """
    return (n % 12 == 1) or (n % 36 == 9)


# ------------------------------------------------------------------------------
def euler_form_possible(n: int, spf: np.ndarray) -> bool:
    """Check the Euler form necessary condition for odd perfect numbers.

    Any odd perfect number must be representable as:
        n = q^a * m^2,
    where q is prime, gcd(q,m)=1, and q ≡ a ≡ 1 (mod 4).

    Args:
        n: Odd integer.
        spf: SPF sieve for factorization.

    Returns:
        True if n matches the Euler form constraints, False otherwise.
    """
    factors = factorize_with_spf(n, spf)
    odd_exp = [(p, a) for p, a in factors.items() if a % 2 == 1]
    if len(odd_exp) != 1:
        return False

    q, a = odd_exp[0]
    if q % 4 != 1:
        return False
    return a % 4 == 1


# ------------------------------------------------------------------------------
def _plot_survival(*, stages: list[str], counts: np.ndarray) -> fig.Figure:
    """Plot survival curve after each stage.

    Args:
        stages: Stage names.
        counts: Remaining candidates after each stage.

    Returns:
        Matplotlib figure.
    """
    fig_obj, ax = plt.subplots()
    x = np.arange(len(stages), dtype=np.int64)
    ax.plot(x, counts, marker="o")
    ax.set_xticks(x, stages, rotation=15, ha="right")
    ax.set_title("Odd perfect number constraints: survival curve")
    ax.set_xlabel("constraint stage")
    ax.set_ylabel("remaining candidates (count)")
    finalize_figure(fig_obj)
    return fig_obj


# ------------------------------------------------------------------------------
def _write_report(
    *, report_path: Path, params: Params, stages: list[str], counts: np.ndarray
) -> None:
    """Write a short Markdown report."""
    lines = [
        "# E005 — Odd perfect numbers: constraint filter pipeline",
        "",
        "**Reproduce:**",
        "",
        "```bash",
        "make run EXP=e005",
        "```",
        "",
        "## Parameters",
        f"- N: `{params.n_max}`",
        "",
        "## Survival table",
        "",
        "| Stage | Remaining |",
        "|---|---:|",
    ]
    for s, c in zip(stages, counts, strict=True):
        lines.append(f"| {s} | {int(c)} |")
    lines.append("")
    lines.append("## Notes")
    lines.append(
        "- These are necessary conditions only; surviving candidates are *not* perfect by implication."
    )
    lines.append(
        "- Euler-form testing requires factorization; SPF makes it feasible for moderate N."
    )
    report_path.write_text("\n".join(lines) + "\n", encoding="utf-8")


# ------------------------------------------------------------------------------
def main() -> int:
    """Run the experiment.

    Returns:
        Process exit code (0 for success).
    """
    args = parse_experiment_args(
        experiment_id="e005",
        description="Odd perfect numbers: constraint filter pipeline",
    )
    setup_logging(config=LoggingConfig(verbose=args.verbose))
    set_global_seed(args.seed)

    params = Params(
        n_max=300_000,
        stride_plot=1,
    )

    out_paths = prepare_out_dir(out_dir=args.out_dir)

    logger.info("Building SPF sieve up to N=%d", params.n_max)
    spf = spf_sieve(params.n_max)

    # Candidate set: odd integers > 1
    candidates = np.arange(3, params.n_max + 1, 2, dtype=np.int64)

    stages: list[str] = []
    counts: list[int] = []

    stages.append("odd integers")
    counts.append(int(candidates.size))

    # Stage 1: Touchard congruence
    mask1 = np.array([touchard_congruence(int(n)) for n in candidates], dtype=bool)
    candidates = candidates[mask1]
    stages.append("Touchard congruence")
    counts.append(int(candidates.size))
    logger.info("After Touchard congruence: %d", candidates.size)

    # Stage 2: Euler form possible
    mask2 = np.array([euler_form_possible(int(n), spf) for n in candidates], dtype=bool)
    candidates = candidates[mask2]
    stages.append("Euler form (q^a*m^2)")
    counts.append(int(candidates.size))
    logger.info("After Euler form filter: %d", candidates.size)

    counts_arr = np.array(counts, dtype=np.int64)
    fig1 = _plot_survival(stages=stages, counts=counts_arr)
    save_figure(out_dir=out_paths.figures_dir, name="fig_01_survival_curve", fig=fig1)

    write_json(out_paths.params_path, data=asdict(params))
    _write_report(
        report_path=out_paths.report_path, params=params, stages=stages, counts=counts_arr
    )

    logger.info("Experiment E005 completed successfully. Artifacts saved to: %s", args.out_dir)
    return 0


# ------------------------------------------------------------------------------
if __name__ == "__main__":
    raise SystemExit(main())
