"""E049: Wieferich primes (base 2): rare congruence hits.

A Wieferich prime (base 2) is a prime p such that:

    2^(p-1) ≡ 1 (mod p^2)

This is a rare strengthening of Fermat's congruence. Only two base-2 Wieferich
primes are known: 1093 and 3511.

This experiment:
- scans primes up to a bound,
- detects Wieferich hits,
- visualizes the "Wieferich quotient" distribution.

Usage (repository convention):
    make run EXP=e049

Artifacts:
    - figures/fig_01_wieferich_hits.png
    - figures/fig_02_quotient_scatter.png
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

# ------------------------------------------------------------------------------
logger = get_logger(__name__)


# ------------------------------------------------------------------------------
@dataclass(frozen=True, slots=True)
class Params:
    """Experiment parameters.

    Args:
        p_max: Upper bound (inclusive) for prime scan.
        base: Base a (default 2) for Wieferich condition.
    """

    p_max: int
    base: int


# ------------------------------------------------------------------------------
def wieferich_hits(*, p_max: int, base: int) -> tuple[np.ndarray, np.ndarray]:
    """Compute Wieferich hits and the Wieferich quotient-like value for primes ≤ p_max.

    For each prime p, compute:
        r = base^(p-1) mod p^2
        q = (r - 1) / p  (mod p)

    For Wieferich primes, r == 1 (mod p^2), i.e. q == 0.

    Args:
        p_max: Upper bound for primes.
        base: Base.

    Returns:
        (primes, q_values) where q_values are in [0, p-1].
    """
    ps = primes_up_to(p_max)
    # Drop p=2 for base=2, because p^2=4 makes the quotient definition degenerate.
    ps = ps[ps >= 3]
    q = np.empty(len(ps), dtype=np.int64)
    for i, p in enumerate(ps.tolist()):
        mod = int(p) * int(p)
        r = pow(base, int(p) - 1, mod)
        delta = (r - 1) % mod
        # delta is divisible by p (by Fermat), so integer division is safe.
        q[i] = (delta // int(p)) % int(p)
    return ps, q


# ------------------------------------------------------------------------------
def _plot_hits(ps: np.ndarray, q: np.ndarray) -> fig.Figure:
    """Plot Wieferich hits as vertical markers.

    Args:
        ps: Primes scanned.
        q: q-values.

    Returns:
        Figure.
    """
    hits = ps[q == 0]
    fig1 = plt.figure(figsize=(9, 3.8))
    ax = fig1.add_subplot(1, 1, 1)
    if len(hits) > 0:
        ax.vlines(hits, 0, 1, linewidth=1.5)
    ax.set_title(r"Wieferich primes (base 2): $2^{p-1}\equiv 1\ (\mathrm{mod}\ p^2)$")
    ax.set_xlabel("p")
    ax.set_yticks([])
    ax.grid(True, alpha=0.25)
    ax.set_xlim(0, ps.max() * 1.02)
    return fig1


# ------------------------------------------------------------------------------
def _plot_quotient(ps: np.ndarray, q: np.ndarray) -> fig.Figure:
    """Scatter plot of the quotient-like value q.

    Args:
        ps: Primes.
        q: q-values.

    Returns:
        Figure.
    """
    fig2 = plt.figure(figsize=(9, 4.5))
    ax = fig2.add_subplot(1, 1, 1)
    ax.scatter(ps, q, s=6)
    ax.set_title("Wieferich quotient-like value q for primes up to bound")
    ax.set_xlabel("p")
    ax.set_ylabel("q = (a^(p-1) mod p^2 - 1) / p  (mod p)")
    ax.grid(True, alpha=0.25)
    return fig2


# ------------------------------------------------------------------------------
def _write_report(*, report_path: Path, params: Params, hits: list[int]) -> None:
    """Write a short Markdown report.

    Args:
        report_path: Path to report.md.
        params: Parameters used.
        hits: Wieferich primes found.
    """
    lines: list[str] = []
    lines.append("# E049: Wieferich primes (base 2)")
    lines.append("")
    lines.append("### Parameters")
    lines.append("")
    lines.append(f"- p_max: {params.p_max}")
    lines.append(f"- base: {params.base}")
    lines.append("")
    lines.append("### Hits")
    lines.append("")
    if hits:
        lines.append("Wieferich primes found within the scan bound:")
        lines.append("")
        lines.append(", ".join(str(h) for h in hits))
    else:
        lines.append("No Wieferich primes were found within the scan bound.")
    lines.append("")
    lines.append("### Notes")
    lines.append("")
    lines.append("- For base 2, the smallest known Wieferich primes are 1093 and 3511.")
    lines.append("- The scan here is purely computational and bounded.")
    report_path.write_text("\n".join(lines) + "\n", encoding="utf-8")


# ------------------------------------------------------------------------------
def main() -> int:
    """Run the experiment.

    Returns:
        Process exit code (0 for success).
    """
    args = parse_experiment_args(
        experiment_id="e049",
        description="Wieferich primes (base 2): scan + quotient visualization",
    )

    run_log = infer_run_log_file(out_dir=args.out_dir, experiment_slug="e049")
    setup_logging(config=LoggingConfig(verbose=args.verbose, log_file=run_log.log_file))
    set_global_seed(args.seed)

    params = Params(
        p_max=200_000,
        base=2,
    )
    out_paths = prepare_out_dir(out_dir=args.out_dir)

    ps, q = wieferich_hits(p_max=params.p_max, base=params.base)
    hits = ps[q == 0].tolist()

    fig1 = _plot_hits(ps=ps, q=q)
    save_figure(out_dir=out_paths.figures_dir, name="fig_01_wieferich_hits", fig=fig1)

    fig2 = _plot_quotient(ps=ps, q=q)
    save_figure(out_dir=out_paths.figures_dir, name="fig_02_quotient_scatter", fig=fig2)

    write_json(out_paths.params_path, data=asdict(params))
    _write_report(report_path=out_paths.report_path, params=params, hits=[int(h) for h in hits])

    logger.info("Experiment E049 completed successfully. Artifacts saved to: %s", args.out_dir)
    return 0


# ------------------------------------------------------------------------------
if __name__ == "__main__":
    raise SystemExit(main())
