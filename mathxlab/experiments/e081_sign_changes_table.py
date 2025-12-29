"""E081 — Prime race sign changes: first crossings table.

A prime race difference D(x) only changes when x passes a prime. We can track
sign changes by iterating primes in order.

This experiment collects the first few sign changes for:
- mod 4: D4(x) = π(x;4,3) - π(x;4,1)
- mod 3: D3(x) = π(x;3,2) - π(x;3,1)

and writes them as a small table in the report. It also plots D4(x) against x
(on primes) up to a plot cutoff.

Usage:
    make run EXP=e081

Artifacts:
    - figures/fig_01_mod4_diff_on_primes.png
    - params.json
    - report.md
"""

from __future__ import annotations

from dataclasses import asdict, dataclass

import matplotlib.figure as fig
import matplotlib.pyplot as plt
import numpy as np

from mathxlab.exp.cli import parse_experiment_args
from mathxlab.exp.io import prepare_out_dir, save_figure, write_json, write_text
from mathxlab.exp.logging import LoggingConfig, get_logger, setup_logging
from mathxlab.exp.random import set_global_seed
from mathxlab.experiments._prime_utils import primes_up_to

# ------------------------------------------------------------------------------
logger = get_logger(__name__)


# ------------------------------------------------------------------------------
@dataclass(frozen=True)
class Params:
    """Parameters for E081."""

    x_max: int = 25_000_000
    max_changes: int = 20
    plot_max: int = 2_000_000


# ------------------------------------------------------------------------------
def _sign_changes(
    *, primes: np.ndarray, q: int, a_pos: int, a_neg: int, max_changes: int
) -> list[tuple[int, int]]:
    """Return [(prime, D_after)] at sign changes of D=pi(q,a_pos)-pi(q,a_neg)."""
    c_pos = 0
    c_neg = 0
    changes: list[tuple[int, int]] = []
    prev_sign = 0
    for p in primes:
        r = int(p % q)
        if r == (a_pos % q):
            c_pos += 1
        elif r == (a_neg % q):
            c_neg += 1
        D = c_pos - c_neg
        sign = 0 if D == 0 else (1 if D > 0 else -1)
        if prev_sign != 0 and sign != 0 and sign != prev_sign:
            changes.append((int(p), int(D)))
            if len(changes) >= max_changes:
                break
        if sign != 0:
            prev_sign = sign
    return changes


# ------------------------------------------------------------------------------
def _mod4_diff_on_primes(*, primes: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
    """Compute D4(p) on prime indices (for plotting)."""
    c1 = 0
    c3 = 0
    D: list[int] = []
    for p in primes:
        r = int(p % 4)
        if r == 1:
            c1 += 1
        elif r == 3:
            c3 += 1
        D.append(c3 - c1)
    return primes.astype(np.int64), np.array(D, dtype=np.int64)


# ------------------------------------------------------------------------------
def _plot_mod4(*, p: np.ndarray, D: np.ndarray) -> fig.Figure:
    fig_obj, ax = plt.subplots()
    ax.plot(p, D)
    ax.axhline(0.0, linestyle="--", linewidth=1.2)
    ax.set_title(r"Mod 4 race on primes: $D_4(p)=\pi(p;4,3)-\pi(p;4,1)$")
    ax.set_xlabel("prime p")
    ax.set_ylabel("D4(p)")
    return fig_obj


# ------------------------------------------------------------------------------
def _md_table(changes: list[tuple[int, int]]) -> list[str]:
    """Render sign changes as markdown table lines."""
    lines = ["| # | prime p | D after |", "|---:|---:|---:|"]
    for i, (p, D) in enumerate(changes, start=1):
        lines.append(f"| {i} | {p} | {D} |")
    return lines


# ------------------------------------------------------------------------------
def main(argv: list[str] | None = None) -> int:
    """Run E081."""
    args = parse_experiment_args(
        experiment_id="e081",
        description="Prime race sign changes: first crossings table.",
        argv=argv,
    )

    setup_logging(config=LoggingConfig(verbose=args.verbose))
    logger.info("Starting experiment E081: Prime race sign changes: first crossings table.")
    set_global_seed(args.seed)
    params = Params()
    paths = prepare_out_dir(out_dir=args.out_dir)

    primes = primes_up_to(params.x_max)

    ch4 = _sign_changes(primes=primes, q=4, a_pos=3, a_neg=1, max_changes=params.max_changes)
    ch3 = _sign_changes(primes=primes, q=3, a_pos=2, a_neg=1, max_changes=params.max_changes)

    # Plot D4(p) up to plot_max.
    primes_plot = primes[primes <= params.plot_max]
    p_plot, D_plot = _mod4_diff_on_primes(primes=primes_plot)
    fig1 = _plot_mod4(p=p_plot, D=D_plot)
    save_figure(out_dir=paths.figures_dir, name="fig_01_mod4_diff_on_primes", fig=fig1)

    lines = [
        "# E081 — Prime race sign changes",
        "",
        f"- x_max (search): {params.x_max}",
        f"- max_changes: {params.max_changes}",
        "",
        "## Mod 4: D4(x)=pi(x;4,3)-pi(x;4,1)",
        "",
        *(_md_table(ch4) if ch4 else ["(No sign change found in range.)"]),
        "",
        "## Mod 3: D3(x)=pi(x;3,2)-pi(x;3,1)",
        "",
        *(_md_table(ch3) if ch3 else ["(No sign change found in range.)"]),
        "",
        "Figure:",
        "- fig_01_mod4_diff_on_primes.png",
        "",
        "Notes:",
        "- Sign changes are detected at prime steps where D jumps.",
        "- If no sign change appears, increase x_max.",
        "",
    ]

    write_json(paths.params_path, asdict(params))
    write_text(paths.report_path, "\n".join(lines))
    return 0
