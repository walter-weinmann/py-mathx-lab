"""E066: Character partial sums: cancellation profiles.

This experiment visualizes partial sums

    S(N) = sum_{n <= N} chi(n)

for Dirichlet characters chi modulo q, and summarizes maximal partial-sum
magnitudes across characters.

Notes:
    - Matplotlib's built-in mathtext parser is intentionally limited. To keep
      this experiment robust across platforms, we avoid LaTeX-heavy titles.
    - Character values are periodic modulo q, with chi(n)=0 when gcd(n,q)>1.
"""

from __future__ import annotations

import logging
from dataclasses import asdict, dataclass

import matplotlib.figure as fig
import matplotlib.pyplot as plt
import numpy as np

from mathxlab.exp.cli import parse_experiment_args
from mathxlab.exp.io import prepare_out_dir, save_figure, write_json, write_text
from mathxlab.exp.logging import LoggingConfig, setup_logging
from mathxlab.exp.run_logging import infer_run_log_file
from mathxlab.exp.seeding import set_global_seed
from mathxlab.nt.dirichlet import DirichletCharacter, all_characters

# ------------------------------------------------------------------------------
logger = logging.getLogger(__name__)


@dataclass(frozen=True)
class Params:
    """Experiment parameters."""

    q: int = 15
    n_max: int = 50_000
    include_principal: bool = False
    top_k: int = 8


def _compute_partial_sums(
    *, q: int, n_max: int, include_principal: bool
) -> tuple[list[DirichletCharacter], np.ndarray]:
    """Compute partial sums S(N)=sum_{n<=N} chi(n) for all characters mod q.

    Args:
        q: Modulus.
        n_max: Maximum N.
        include_principal: Whether to include the principal character.

    Returns:
        A pair (chars, sums) where:
            chars: List of DirichletCharacter objects.
            sums: Complex array of shape (m, n_max) with cumulative sums for each chi.
    """
    chars = all_characters(q)
    if not include_principal:
        chars = [c for c in chars if not getattr(c, "is_principal", False)]

    # Use periodicity: chi(n) = chi(n mod q).
    residues = (np.arange(1, n_max + 1, dtype=np.int64) % q).astype(np.int64)

    table = np.array([c.table() for c in chars], dtype=np.complex128)  # (m, q)
    vals = table[:, residues]  # (m, n_max)
    sums = np.cumsum(vals, axis=1)
    return chars, sums


def _plot_maxima(*, max_abs: np.ndarray, q: int, n_max: int) -> fig.Figure:
    """Plot maximal partial-sum magnitudes per character."""
    fig, ax = plt.subplots()
    order = np.argsort(max_abs)[::-1]
    ax.plot(np.arange(1, len(max_abs) + 1), max_abs[order], marker=".", linestyle="none")
    ax.set_title(f"Max |S(N)| across characters (q={q}, N_max={n_max})")
    ax.set_xlabel("Character rank (sorted by max |S|)")
    ax.set_ylabel("max_N |S(N)|")
    ax.set_yscale("log")
    return fig


def _plot_example(*, abs_s: np.ndarray, q: int, n_max: int) -> fig.Figure:
    """Plot |S(N)| for one representative character."""
    fig, ax = plt.subplots()
    ax.plot(np.arange(1, n_max + 1), abs_s)
    ax.set_title(f"Example trajectory: |S(N)| (q={q}, N_max={n_max})")
    ax.set_xlabel("N")
    ax.set_ylabel("|S(N)|")
    ax.set_yscale("log")
    return fig


def main() -> int:
    """Run the experiment.

    Returns:
        Process exit code (0 for success).
    """
    args = parse_experiment_args(
        experiment_id="e066",
        description="Character partial sums: cancellation profiles",
    )

    run_log = infer_run_log_file(out_dir=args.out_dir, experiment_slug="e066")
    setup_logging(config=LoggingConfig(verbose=args.verbose, log_file=run_log.log_file))
    set_global_seed(args.seed)

    logger.info("Starting experiment E066: Character partial sums: cancellation profiles.")

    params = Params()
    out_paths = prepare_out_dir(out_dir=args.out_dir)

    chars, sums = _compute_partial_sums(
        q=params.q, n_max=params.n_max, include_principal=params.include_principal
    )
    abs_sums = np.abs(sums)
    max_abs = abs_sums.max(axis=1)

    fig1 = _plot_maxima(max_abs=max_abs, q=params.q, n_max=params.n_max)
    save_figure(out_dir=out_paths.figures_dir, name="fig_01_max_partial_sums", fig=fig1)

    idx = int(np.argmax(max_abs))
    fig2 = _plot_example(abs_s=abs_sums[idx], q=params.q, n_max=params.n_max)
    save_figure(out_dir=out_paths.figures_dir, name="fig_02_example_partial_sum", fig=fig2)

    write_json(out_paths.params_path, data=asdict(params))

    top_k = min(params.top_k, len(chars))
    top_idx = np.argsort(max_abs)[::-1][:top_k]
    lines: list[str] = [
        "# E066: Character partial sums: cancellation profiles",
        "",
        "### Parameters",
        f"- q: {params.q}",
        f"- N_max: {params.n_max}",
        f"- include_principal: {params.include_principal}",
        "",
        "## Summary",
        f"Computed partial sums S(N)=sum_{{n<=N}} chi(n) for {len(chars)} Dirichlet characters modulo q.",
        "",
        "### Top characters by max |S(N)|",
        "",
        "| rank | index | max |S(N)| | conductor | principal |",
        "|---:|---:|---:|---:|:---:|",
    ]
    for r, i in enumerate(top_idx, start=1):
        chi = chars[int(i)]
        cond = getattr(chi, "conductor", None)
        cond_val = int(cond) if isinstance(cond, int) else (int(cond()) if callable(cond) else -1)
        is_pr = bool(getattr(chi, "is_principal", False))
        lines.append(f"| {r} | {int(i)} | {float(max_abs[int(i)]):.6g} | {cond_val} | {is_pr} |")

    write_text(out_paths.report_path, "\n".join(lines) + "\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
