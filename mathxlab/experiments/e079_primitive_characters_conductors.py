"""E079 — Primitive vs imprimitive characters: conductors.

A character modulo q may factor through a smaller modulus f | q. The smallest
such modulus is the **conductor** of the character.

This experiment computes conductors for all characters modulo q (small q) and
visualizes how many characters have each conductor.

Usage:
    make run EXP=e079

Artifacts:
    - figures/fig_01_conductor_counts.png
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
from mathxlab.exp.logging import LoggingConfig, get_logger, setup_logging
from mathxlab.exp.random import set_global_seed
from mathxlab.exp.io import prepare_out_dir, save_figure, write_json, write_text
from mathxlab.nt.dirichlet import all_characters, conductor, euler_phi

# ------------------------------------------------------------------------------
logger = get_logger(__name__)



# ------------------------------------------------------------------------------
@dataclass(frozen=True)
class Params:
    """Parameters for E079."""

    q: int = 12


# ------------------------------------------------------------------------------
def _plot_counts(*, conductors: list[int], counts: list[int], q: int) -> fig.Figure:
    fig_obj, ax = plt.subplots()
    x = np.arange(len(conductors))
    ax.bar(x, counts)
    ax.set_xticks(x, [str(c) for c in conductors])
    ax.set_title(rf"Conductor counts for characters mod q={q}")
    ax.set_xlabel("conductor f")
    ax.set_ylabel("number of characters")
    return fig_obj


# ------------------------------------------------------------------------------
def main(argv: list[str] | None = None) -> int:
    """Run E079."""
    args = parse_experiment_args(
        experiment_id="e079",
        description="Primitive vs imprimitive characters: conductors.",
        argv=argv,
    )

    setup_logging(config=LoggingConfig(verbose=args.verbose))
    logger.info("Starting experiment E079: Primitive vs imprimitive characters: conductors.")
    set_global_seed(args.seed)
    params = Params()
    paths = prepare_out_dir(out_dir=args.out_dir)

    chars = all_characters(params.q)
    conds = [conductor(c) for c in chars]

    # Count occurrences.
    uniq = sorted(set(conds))
    counts = [conds.count(u) for u in uniq]

    fig1 = _plot_counts(conductors=uniq, counts=counts, q=params.q)
    save_figure(out_dir=paths.figures_dir, name="fig_01_conductor_counts", fig=fig1)

    n_primitive = sum(1 for c in conds if c == params.q)
    lines = [
        "# E079 — Conductors of Dirichlet characters",
        "",
        f"- q: {params.q}",
        f"- phi(q): {euler_phi(params.q)}",
        f"- number of primitive characters (conductor = q): {n_primitive}",
        "",
        "Conductor breakdown:",
    ]
    for u, c in zip(uniq, counts, strict=True):
        lines.append(f"- f={u}: {c}")
    lines += [
        "",
        "Figure:",
        "- fig_01_conductor_counts.png",
        "",
        "Notes:",
        "- Conductor computation here is a brute-force check intended for small q.",
        "",
    ]

    write_json(paths.params_path, asdict(params))
    write_text(paths.report_path, "\n".join(lines))
    return 0