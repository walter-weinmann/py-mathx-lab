"""E011 — Heuristic vs observed counts of Mersenne primes.

A common heuristic says that for prime exponents p, the probability that
M_p = 2^p - 1 is prime is about 1 / (p * ln 2).

This experiment compares:
    observed_count(p_max)
to:
    expected_count(p_max) = sum_{p prime ≤ p_max} 1 / (p * ln 2)

The observed count is computed via Lucas–Lehmer.

Usage (repository convention):
    make run EXP=e011

Artifacts:
    - figures/fig_01_observed_vs_expected.png
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
        p_max: Upper bound for prime exponents p (inclusive).
        max_tests: Cap on how many prime exponents to test.
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
        return True
    mp = (1 << p) - 1
    s = 4
    for _ in range(p - 2):
        s = (s * s - 2) % mp
    return s == 0


# ------------------------------------------------------------------------------
def _plot_observed_expected(
    *, p: np.ndarray, observed: np.ndarray, expected: np.ndarray
) -> fig.Figure:
    """Plot observed vs expected counts."""
    fig_obj, ax = plt.subplots()
    ax.plot(p, observed, label="observed")
    ax.plot(p, expected, label="expected (heuristic)")
    ax.set_title("Observed vs expected Mersenne prime counts")
    ax.set_xlabel("prime exponent p (running maximum)")
    ax.set_ylabel("count")
    ax.legend()
    finalize_figure(fig_obj)
    return fig_obj


# ------------------------------------------------------------------------------
def _write_report(
    *, report_path: Path, params: Params, last_p: int, obs: int, exp: float, found_p: list[int]
) -> None:
    """Write a short Markdown report.

    Args:
        report_path: Path to report.md.
        params: Experiment parameters.
        last_p: Largest tested exponent.
        obs: Observed count.
        exp: Expected count (heuristic).
        found_p: Exponents found where M_p is prime.
    """
    lines = [
        "# E011 — Heuristic vs observed counts of Mersenne primes",
        "",
        "**Reproduce:**",
        "",
        "```bash",
        "make run EXP=e011",
        "```",
        "",
        "## Parameters",
        f"- p_max: `{params.p_max}`",
        f"- max_tests: `{params.max_tests}`",
        "",
        "## Summary",
        f"- largest tested p: `{last_p}`",
        f"- observed count: `{obs}`",
        f"- expected (heuristic): `{exp:.6g}`",
        "",
        "## Found Mersenne prime exponents",
        "",
    ]
    if found_p:
        lines.append(", ".join(str(p) for p in found_p))
    else:
        lines.append("_none in this range (or max_tests too small)_")
    lines += [
        "",
        "## Notes",
        "- The heuristic probability is ~ 1/(p·ln 2) for prime p.",
        "- This is not a theorem; it is a back-of-the-envelope model for rarity.",
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
        experiment_id="e011",
        description="Compare observed vs heuristic expected Mersenne prime counts",
    )
    setup_logging(config=LoggingConfig(verbose=args.verbose))
    set_global_seed(args.seed)

    params = Params(
        p_max=20_000,
        max_tests=900,
    )

    out_paths = prepare_out_dir(out_dir=args.out_dir)

    p_all = primes_up_to(params.p_max)[: params.max_tests]

    found_p: list[int] = []
    observed: list[int] = []
    expected: list[float] = []
    p_running: list[int] = []

    obs = 0
    exp = 0.0
    ln2 = float(np.log(2.0))

    for p in p_all:
        p_i = int(p)
        ok = lucas_lehmer_is_prime(p_i)
        if ok:
            obs += 1
            found_p.append(p_i)

        exp += 1.0 / (p_i * ln2)

        p_running.append(p_i)
        observed.append(obs)
        expected.append(exp)

    p_arr = np.array(p_running, dtype=np.int64)
    obs_arr = np.array(observed, dtype=np.int64)
    exp_arr = np.array(expected, dtype=np.float64)

    fig1 = _plot_observed_expected(p=p_arr, observed=obs_arr, expected=exp_arr)
    save_figure(out_dir=out_paths.figures_dir, name="fig_01_observed_vs_expected", fig=fig1)

    write_json(out_paths.params_path, data=asdict(params))
    last_p = int(p_arr[-1]) if p_arr.size > 0 else 0
    _write_report(
        report_path=out_paths.report_path,
        params=params,
        last_p=last_p,
        obs=obs,
        exp=exp,
        found_p=found_p,
    )

    logger.info("Experiment E011 completed successfully. Artifacts saved to: %s", args.out_dir)
    return 0


# ------------------------------------------------------------------------------
if __name__ == "__main__":
    raise SystemExit(main())
