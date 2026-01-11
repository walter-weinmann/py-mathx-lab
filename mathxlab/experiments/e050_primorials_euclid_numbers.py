"""E050: Primorials and Euclid numbers: p# ± 1 are usually composite.

The primorial of the k-th prime is:

    p_k# = ∏_{i=1..k} p_i

Euclid-style numbers p_k# ± 1 are coprime to all primes ≤ p_k, but they are
*not* typically prime. This experiment demonstrates that behavior and produces
small factor witnesses for early k.

Usage (repository convention):
    make run EXP=e050

Artifacts:
    - figures/fig_01_log10_euclid.png
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
from mathxlab.exp.run_logging import infer_run_log_file
from mathxlab.experiments._prime_utils import (
    is_probable_prime_miller_rabin,
    primes_up_to,
    trial_division_factor,
)

# ------------------------------------------------------------------------------
logger = get_logger(__name__)


# ------------------------------------------------------------------------------
@dataclass(frozen=True, slots=True)
class Params:
    """Experiment parameters.

    Args:
        k_max: Maximum primorial index k to analyze (inclusive).
        factor_prime_bound: Upper bound for trial division primes for finding a factor witness.
        mr_bases: Bases for Miller–Rabin probable prime test (used for large integers).
    """

    k_max: int
    factor_prime_bound: int
    mr_bases: tuple[int, ...]


# ------------------------------------------------------------------------------
def primorial(primes: list[int]) -> int:
    """Compute the primorial (product) for a list of primes.

    Args:
        primes: Prime list (e.g., first k primes).

    Returns:
        Product of primes.
    """
    p = 1
    for q in primes:
        p *= q
    return p


# ------------------------------------------------------------------------------
def find_small_factor(n: int, bound: int) -> int | None:
    """Try to find a small factor of n by trial division.

    Args:
        n: Integer to factor.
        bound: Prime bound for trial division.

    Returns:
        Smallest factor if found, otherwise None.
    """
    if n < 2:
        return None
    primes = primes_up_to(bound)
    res = trial_division_factor(n, primes)
    return res[0] if res is not None else None


# ------------------------------------------------------------------------------
def _plot_log10(
    ks: list[int], logp: list[float], logm: list[float], pp: list[bool], pm: list[bool]
) -> fig.Figure:
    """Plot log10(p_k# ± 1) vs k, marking probable prime flags.

    Args:
        ks: k indices.
        logp: log10(p_k# + 1).
        logm: log10(p_k# - 1).
        pp: probable prime flags for +1.
        pm: probable prime flags for -1.

    Returns:
        Figure.
    """
    fig1 = plt.figure(figsize=(9, 4.5))
    ax = fig1.add_subplot(1, 1, 1)
    ax.plot(ks, logp, marker="o", label=r"$\log_{10}(p_k\# + 1)$")
    ax.plot(ks, logm, marker="o", label=r"$\log_{10}(p_k\# - 1)$")
    for k, y, ok in zip(ks, logp, pp, strict=True):
        if ok:
            ax.annotate("pp", (k, y), textcoords="offset points", xytext=(5, 5))
    for k, y, ok in zip(ks, logm, pm, strict=True):
        if ok:
            ax.annotate("pp", (k, y), textcoords="offset points", xytext=(5, -12))
    ax.set_title("Primorial ± 1 growth (pp = probable prime under MR bases)")
    ax.set_xlabel("k (index of prime p_k)")
    ax.set_ylabel(r"$\log_{10}(n)$")
    ax.grid(True, alpha=0.25)
    ax.legend()
    return fig1


# ------------------------------------------------------------------------------
def _plot_factors(ks: list[int], f_plus: list[int | None], f_minus: list[int | None]) -> fig.Figure:
    """Plot smallest found factor witness for p_k# ± 1.

    Args:
        ks: k indices.
        f_plus: factors for +1.
        f_minus: factors for -1.

    Returns:
        Figure.
    """
    fig2 = plt.figure(figsize=(9, 4.5))
    ax = fig2.add_subplot(1, 1, 1)
    yp = [float(v) if v is not None else np.nan for v in f_plus]
    ym = [float(v) if v is not None else np.nan for v in f_minus]
    ax.plot(ks, yp, marker="o", label="smallest factor of p# + 1")
    ax.plot(ks, ym, marker="o", label="smallest factor of p# - 1")
    ax.set_yscale("log")
    ax.set_title("Small factor witnesses (bounded trial division)")
    ax.set_xlabel("k")
    ax.set_ylabel("smallest found factor (log scale)")
    ax.grid(True, alpha=0.25)
    ax.legend()
    return fig2


# ------------------------------------------------------------------------------
def _write_report(
    *,
    report_path: Path,
    params: Params,
    rows: list[tuple[int, int, bool, int | None, int, bool, int | None]],
) -> None:
    """Write report.

    Args:
        report_path: Path to report.md.
        params: Parameters.
        rows: (k, n_plus, pp_plus, fac_plus, n_minus, pp_minus, fac_minus).
    """
    lines: list[str] = []
    lines.append("# E050: Primorials and Euclid numbers (p# ± 1)")
    lines.append("")
    lines.append("### Parameters")
    lines.append("")
    lines.append(f"- k_max: {params.k_max}")
    lines.append(f"- factor_prime_bound: {params.factor_prime_bound}")
    lines.append(f"- mr_bases: {', '.join(str(b) for b in params.mr_bases)}")
    lines.append("")
    lines.append("### Results")
    lines.append("")
    lines.append("| k | p_k# + 1 | pp? | factor | p_k# - 1 | pp? | factor |")
    lines.append("|---:|---:|:---:|---:|---:|:---:|---:|")
    for k, n_p, pp_p, f_p, n_m, pp_m, f_m in rows:
        lines.append(
            f"| {k} | {n_p} | {'✅' if pp_p else '❌'} | {f_p if f_p is not None else '—'}"
            f" | {n_m} | {'✅' if pp_m else '❌'} | {f_m if f_m is not None else '—'} |"
        )
    lines.append("")
    lines.append("### Notes")
    lines.append("")
    lines.append("- `pp?` is *probable prime* under the chosen Miller–Rabin bases.")
    lines.append("- Factor witnesses are from bounded trial division (not a full factorization).")
    report_path.write_text("\n".join(lines) + "\n", encoding="utf-8")


# ------------------------------------------------------------------------------
def main() -> int:
    """Run the experiment.

    Returns:
        Exit code.
    """
    args = parse_experiment_args(
        experiment_id="e050",
        description="Primorials: Euclid numbers p# ± 1 are usually composite",
    )

    run_log = infer_run_log_file(out_dir=args.out_dir, experiment_slug="e050")
    setup_logging(config=LoggingConfig(verbose=args.verbose, log_file=run_log.log_file))
    set_global_seed(args.seed)

    params = Params(
        k_max=16,
        factor_prime_bound=1_000_000,
        mr_bases=(2, 3, 5, 7, 11, 13, 17),
    )
    out_paths = prepare_out_dir(out_dir=args.out_dir)

    primes = primes_up_to(200)  # enough for k<=46
    rows: list[tuple[int, int, bool, int | None, int, bool, int | None]] = []

    ks: list[int] = []
    logp: list[float] = []
    logm: list[float] = []
    pp_plus: list[bool] = []
    pp_minus: list[bool] = []
    f_plus: list[int | None] = []
    f_minus: list[int | None] = []

    for k in range(1, params.k_max + 1):
        first = primes[:k].tolist()
        pk = int(first[-1])
        psharp = primorial(first)

        n_p = psharp + 1
        n_m = psharp - 1

        pp_p = is_probable_prime_miller_rabin(n_p, bases=params.mr_bases)
        pp_m = is_probable_prime_miller_rabin(n_m, bases=params.mr_bases)

        fac_p = None if pp_p else find_small_factor(n_p, bound=params.factor_prime_bound)
        fac_m = None if pp_m else find_small_factor(n_m, bound=params.factor_prime_bound)

        rows.append((k, n_p, pp_p, fac_p, n_m, pp_m, fac_m))

        ks.append(k)
        logp.append(math.log10(n_p))
        logm.append(math.log10(n_m))
        pp_plus.append(pp_p)
        pp_minus.append(pp_m)
        f_plus.append(fac_p)
        f_minus.append(fac_m)

        logger.info(
            "k=%s p_k=%s p#=%s  +1=%s pp=%s f=%s  -1=%s pp=%s f=%s",
            k,
            pk,
            psharp,
            n_p,
            pp_p,
            fac_p,
            n_m,
            pp_m,
            fac_m,
        )

    fig1 = _plot_log10(ks=ks, logp=logp, logm=logm, pp=pp_plus, pm=pp_minus)
    save_figure(out_dir=out_paths.figures_dir, name="fig_01_log10_euclid", fig=fig1)

    fig2 = _plot_factors(ks=ks, f_plus=f_plus, f_minus=f_minus)
    save_figure(out_dir=out_paths.figures_dir, name="fig_02_smallest_factor", fig=fig2)

    write_json(out_paths.params_path, data=asdict(params))
    _write_report(report_path=out_paths.report_path, params=params, rows=rows)

    logger.info("Experiment E050 completed successfully. Artifacts saved to: %s", args.out_dir)
    return 0


# ------------------------------------------------------------------------------
if __name__ == "__main__":
    raise SystemExit(main())
