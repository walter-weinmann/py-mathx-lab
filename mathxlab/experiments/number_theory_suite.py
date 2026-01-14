"""Number theory experiment suite (E094–E123).
This module groups a block of number-theoretic experiments that share
common utilities (factor sieves, prime lists, Dirichlet characters, zeta helpers).

Each experiment has a small `run_e###(...)` function that writes:
- figures under `figures_dir`
- `params.json`
- `report.md`

Notes:
- Default workloads are intentionally small so the full experiment smoke test
  remains fast in CI.
"""

from __future__ import annotations

import math
from dataclasses import asdict, dataclass
from pathlib import Path

import mpmath as mp
import numpy as np
from matplotlib import pyplot as plt

from mathxlab.exp.io import save_figure, write_json
from mathxlab.experiments._prime_utils import primes_up_to
from mathxlab.nt.arithmetic import (
    FactorSieve,
    build_factor_sieve,
    carmichael_lambda,
    chebyshev_psi,
    compute_big_omega,
    compute_mobius,
    compute_omega,
    compute_phi,
    compute_tau_sigma,
    compute_von_mangoldt,
    jordan_totient,
)
from mathxlab.nt.convolution import dirichlet_convolution, epsilon, identity, ones
from mathxlab.nt.dirichlet import (
    DirichletCharacter,
    all_characters,
    conductor,
    euler_phi,
    orthogonality_matrix,
    reduced_residues,
)
from mathxlab.nt.zeta import (
    ZetaEvalSettings,
    chi_factor,
    eta_series_partial,
    euler_product_partial,
    hardy_Z,
    riemann_von_mangoldt_count,
    zeta_via_eta,
)
from mathxlab.plots.helpers import finalize_figure


# ------------------------------------------------------------------------------
def _write_report(*, report_path: Path, lines: list[str]) -> None:
    """Write a small Markdown report.

    Args:
        report_path: Destination path.
        lines: Report lines without trailing newline.
    """
    report_path.write_text("\n".join(lines) + "\n", encoding="utf-8")


# ------------------------------------------------------------------------------
def _factor_sieve(n_max: int) -> FactorSieve:
    """Build and return a factor sieve for [0..n_max]."""
    return build_factor_sieve(n_max)


def _as_np(values: list[int], n_max: int) -> np.ndarray:
    """Convert a prefix list[0..n_max] into an ndarray[1..n_max]."""
    return np.asarray(values[1 : n_max + 1], dtype=np.int64)


@dataclass(frozen=True, slots=True)
class ParamsE094:
    """Parameters for E094.

    Args:
        n_max: Upper bound N (inclusive).
        max_k: Maximum factor-count bin to display.
    """

    n_max: int = 200_000
    max_k: int = 12


def run_e094(
    *, out_dir: Path, seed: int, figures_dir: Path, report_path: Path, params_path: Path
) -> None:
    """E094: ω(n) vs Ω(n): Erdős–Kac side-by-side."""
    params = ParamsE094()
    write_json(params_path, asdict(params))

    sieve = _factor_sieve(params.n_max)
    omega = _as_np(compute_omega(params.n_max, sieve=sieve), params.n_max)
    bigomega = _as_np(compute_big_omega(params.n_max, sieve=sieve), params.n_max)
    k_max = params.max_k
    c1 = np.bincount(np.clip(omega, 0, k_max), minlength=k_max + 1)
    c2 = np.bincount(np.clip(bigomega, 0, k_max), minlength=k_max + 1)
    x = np.arange(0, k_max + 1)
    fig, ax = plt.subplots()
    ax.bar(x - 0.2, c1, width=0.4, label="omega")
    ax.bar(x + 0.2, c2, width=0.4, label="Omega")
    ax.set_title("Histogram of ω(n) and Ω(n) for n=1..N")
    ax.set_xlabel("k")
    ax.set_ylabel("count (clipped at max_k)")
    ax.legend()
    finalize_figure(fig)
    save_figure(out_dir=figures_dir, name="fig_01_omega_vs_bigomega_hist", fig=fig)
    plt.close(fig)
    mu1 = float(np.mean(omega))
    mu2 = float(np.mean(bigomega))
    v1 = float(np.var(omega))
    v2 = float(np.var(bigomega))
    ll = math.log(math.log(params.n_max)) if params.n_max > 2 else float("nan")

    lines: list[str] = []
    lines.append("# E094: ω(n) vs Ω(n): Erdős–Kac side-by-side")
    lines.append("")
    lines.append("## Artifacts")
    lines.append("- figures/fig_01_omega_vs_bigomega_hist.png")
    lines.append("- params.json")
    lines.append("- report.md")
    lines.append("")
    lines.append("### Notes")
    lines.append(f"- Mean ω(n) ≈ {mu1:.3f}, Var ω(n) ≈ {v1:.3f}")
    lines.append(f"- Mean Ω(n) ≈ {mu2:.3f}, Var Ω(n) ≈ {v2:.3f}")
    lines.append(f"- log log N ≈ {ll:.3f} (Erdős–Kac heuristic scale)")
    _write_report(report_path=report_path, lines=lines)


@dataclass(frozen=True, slots=True)
class ParamsE095:
    """Parameters for E095.

    Args:
        n_max: Upper bound N (inclusive).
        max_k: Maximum factor-count bin to display.
    """

    n_max: int = 200_000
    max_k: int = 12


def run_e095(
    *, out_dir: Path, seed: int, figures_dir: Path, report_path: Path, params_path: Path
) -> None:
    """E095: Squarefree filter: ω(n)=Ω(n) when μ(n)≠0."""
    params = ParamsE095()
    write_json(params_path, asdict(params))

    sieve = _factor_sieve(params.n_max)
    mu = compute_mobius(params.n_max, sieve=sieve)
    omega = _as_np(compute_omega(params.n_max, sieve=sieve), params.n_max)
    bigomega = _as_np(compute_big_omega(params.n_max, sieve=sieve), params.n_max)
    mask_sqfree = np.asarray(mu[1 : params.n_max + 1], dtype=np.int64) != 0
    diff = bigomega - omega
    diff_sqfree = diff[mask_sqfree]
    frac_eq_all = float(np.mean(diff == 0))
    frac_eq_sqfree = float(np.mean(diff_sqfree == 0)) if diff_sqfree.size else 1.0
    k_max = params.max_k
    c_all = np.bincount(np.clip(diff, 0, k_max), minlength=k_max + 1)
    c_sf = np.bincount(np.clip(diff_sqfree, 0, k_max), minlength=k_max + 1)
    x = np.arange(0, k_max + 1)
    fig, ax = plt.subplots()
    ax.bar(x - 0.2, c_all, width=0.4, label="all n")
    ax.bar(x + 0.2, c_sf, width=0.4, label="squarefree")
    ax.set_title("Histogram of Ω(n)-ω(n)")
    ax.set_xlabel("k (clipped)")
    ax.set_ylabel("count")
    ax.legend()
    finalize_figure(fig)
    save_figure(out_dir=figures_dir, name="fig_01_bigomega_minus_omega", fig=fig)
    plt.close(fig)

    lines: list[str] = []
    lines.append("# E095: Squarefree filter: ω(n)=Ω(n) when μ(n)≠0")
    lines.append("")
    lines.append("## Artifacts")
    lines.append("- figures/fig_01_bigomega_minus_omega.png")
    lines.append("- params.json")
    lines.append("- report.md")
    lines.append("")
    lines.append("### Notes")
    lines.append(f"- Fraction with Ω(n)=ω(n) on all integers: {frac_eq_all:.4f}")
    lines.append(
        f"- Fraction with Ω(n)=ω(n) on squarefree integers: {frac_eq_sqfree:.4f} (should be 1.0)"
    )
    lines.append("- Ω(n)-ω(n) counts repeated prime powers (p^k with k≥2).")
    _write_report(report_path=report_path, lines=lines)


@dataclass(frozen=True, slots=True)
class ParamsE096:
    """Parameters for E096.

    Args:
        n_max: Upper bound N (inclusive).
        max_points: Maximum number of record points to include in the plot.
    """

    n_max: int = 300_000
    max_points: int = 150


def run_e096(
    *, out_dir: Path, seed: int, figures_dir: Path, report_path: Path, params_path: Path
) -> None:
    """E096: Record-holders for τ(n)."""
    params = ParamsE096()
    write_json(params_path, asdict(params))

    sieve = _factor_sieve(params.n_max)
    tau, _sigma = compute_tau_sigma(params.n_max, sieve=sieve)
    tau_np = _as_np(tau, params.n_max)
    record_ns: list[int] = []
    record_vals: list[int] = []
    best = 0
    for i, v in enumerate(tau_np, start=1):
        if int(v) > best:
            best = int(v)
            record_ns.append(i)
            record_vals.append(best)
    if len(record_ns) > params.max_points:
        record_ns = record_ns[: params.max_points]
        record_vals = record_vals[: params.max_points]
    fig, ax = plt.subplots()
    ax.step(record_ns, record_vals, where="post")
    ax.set_title("Record values of τ(n) up to N")
    ax.set_xlabel("n (record-holders)")
    ax.set_ylabel("max τ(n) so far")
    ax.set_xscale("log")
    finalize_figure(fig)
    save_figure(out_dir=figures_dir, name="fig_01_tau_records", fig=fig)
    plt.close(fig)
    top = list(zip(record_ns[-10:], record_vals[-10:], strict=False))

    lines: list[str] = []
    lines.append("# E096: Record-holders for τ(n)")
    lines.append("")
    lines.append("## Artifacts")
    lines.append("- figures/fig_01_tau_records.png")
    lines.append("- params.json")
    lines.append("- report.md")
    lines.append("")
    lines.append("### Notes")
    lines.append(f"- Number of record-holders found: {len(record_ns)}")
    lines.append(f"- Last 10 record-holders (n, τ(n)): {top}")
    lines.append(
        "- Record-holders are built from small primes with nonincreasing exponents (highly composite flavor)."
    )
    _write_report(report_path=report_path, lines=lines)


@dataclass(frozen=True, slots=True)
class ParamsE097:
    """Parameters for E097.

    Args:
        n_max: Upper bound N (inclusive).
        stride: Downsampling stride for scatter plotting.
    """

    n_max: int = 200_000
    stride: int = 20


def run_e097(
    *, out_dir: Path, seed: int, figures_dir: Path, report_path: Path, params_path: Path
) -> None:
    """E097: σ(n)/n landscape: deficient, perfect, abundant."""
    params = ParamsE097()
    write_json(params_path, asdict(params))

    sieve = _factor_sieve(params.n_max)
    _tau, sigma = compute_tau_sigma(params.n_max, sieve=sieve)
    sigma_np = np.asarray(sigma[1 : params.n_max + 1], dtype=np.float64)
    n = np.arange(1, params.n_max + 1, dtype=np.float64)
    ratio = sigma_np / n
    abundant = ratio > 2.0
    perfect = np.isclose(ratio, 2.0)
    frac_abundant = float(np.mean(abundant))
    count_perfect = int(np.sum(perfect))
    idx = np.arange(0, params.n_max, params.stride)
    fig, ax = plt.subplots()
    ax.scatter((idx + 1), ratio[idx], s=3)
    ax.axhline(2.0, linestyle="--")
    ax.set_title("σ(n)/n for n=1..N (downsampled)")
    ax.set_xlabel("n")
    ax.set_ylabel("σ(n)/n")
    ax.set_xscale("log")
    finalize_figure(fig)
    save_figure(out_dir=figures_dir, name="fig_01_sigma_over_n_scatter", fig=fig)
    plt.close(fig)
    perfect_ns = np.where(perfect)[0] + 1
    perfect_list = perfect_ns[:20].tolist()

    lines: list[str] = []
    lines.append("# E097: σ(n)/n landscape: deficient, perfect, abundant")
    lines.append("")
    lines.append("## Artifacts")
    lines.append("- figures/fig_01_sigma_over_n_scatter.png")
    lines.append("- params.json")
    lines.append("- report.md")
    lines.append("")
    lines.append("### Notes")
    lines.append(f"- Fraction abundant (σ(n)>2n) up to N: {frac_abundant:.4f}")
    lines.append(f"- Number of perfect numbers detected up to N: {count_perfect}")
    lines.append(f"- First perfect numbers in range (if any): {perfect_list}")
    _write_report(report_path=report_path, lines=lines)


@dataclass(frozen=True, slots=True)
class ParamsE098:
    """Parameters for E098.

    Args:
        n_max: Upper bound N (inclusive).
        alpha_min: Minimum alpha value.
        alpha_max: Maximum alpha value.
        alpha_steps: Number of alpha grid points.
    """

    n_max: int = 60_000
    alpha_min: float = 0.5
    alpha_max: float = 2.0
    alpha_steps: int = 40


def run_e098(
    *, out_dir: Path, seed: int, figures_dir: Path, report_path: Path, params_path: Path
) -> None:
    """E098: Extremals of σ(n)/n^α across α."""
    params = ParamsE098()
    write_json(params_path, asdict(params))

    sieve = _factor_sieve(params.n_max)
    _tau, sigma = compute_tau_sigma(params.n_max, sieve=sieve)
    sigma_np = np.asarray(sigma[1 : params.n_max + 1], dtype=np.float64)
    n = np.arange(1, params.n_max + 1, dtype=np.float64)
    alphas = np.linspace(params.alpha_min, params.alpha_max, params.alpha_steps)
    argmax: list[int] = []
    best_vals: list[float] = []
    for a in alphas:
        score = sigma_np / (n**a)
        i = int(np.argmax(score))
        argmax.append(i + 1)
        best_vals.append(float(score[i]))
    fig, ax = plt.subplots()
    ax.plot(alphas, argmax)
    ax.set_title("Argmax of σ(n)/n^α (n≤N)")
    ax.set_xlabel("α")
    ax.set_ylabel("argmax n")
    finalize_figure(fig)
    save_figure(out_dir=figures_dir, name="fig_01_argmax_vs_alpha", fig=fig)
    plt.close(fig)
    # summarize transitions
    transitions: list[tuple[float, int]] = []
    last = None
    for a, n_star in zip(alphas, argmax, strict=False):
        if last is None or n_star != last:
            transitions.append((float(a), int(n_star)))
            last = n_star

    lines: list[str] = []
    lines.append("# E098: Extremals of σ(n)/n^α across α")
    lines.append("")
    lines.append("## Artifacts")
    lines.append("- figures/fig_01_argmax_vs_alpha.png")
    lines.append("- params.json")
    lines.append("- report.md")
    lines.append("")
    lines.append("### Notes")
    lines.append(f"- Unique maximizers encountered: {len(set(argmax))}")
    lines.append(f"- First transitions (alpha, argmax n): {transitions[:10]}")
    lines.append("- This is a small-N proxy for highly/colossally abundant phenomena.")
    _write_report(report_path=report_path, lines=lines)


@dataclass(frozen=True, slots=True)
class ParamsE099:
    """Parameters for E099.

    Args:
        n_max: Upper bound N (inclusive).
        k_max: Maximum k for J_k.
        stride: Downsampling stride for scatter plotting.
    """

    n_max: int = 30_000
    k_max: int = 4
    stride: int = 10


def run_e099(
    *, out_dir: Path, seed: int, figures_dir: Path, report_path: Path, params_path: Path
) -> None:
    """E099: Jordan totients J_k: atlas and identities."""
    params = ParamsE099()
    write_json(params_path, asdict(params))

    sieve = _factor_sieve(params.n_max)
    phi = compute_phi(params.n_max, sieve=sieve)
    # n = np.arange(1, params.n_max + 1, dtype=np.float64)
    idx = np.arange(1, params.n_max + 1, params.stride, dtype=int)
    fig, ax = plt.subplots()
    means: list[float] = []
    max_abs_phi_err = 0
    for k in range(1, params.k_max + 1):
        vals = np.array([jordan_totient(int(i), k, sieve=sieve) for i in idx], dtype=np.float64)
        ratio = vals / ((idx.astype(np.float64)) ** k)
        ax.plot(idx, ratio, label=f"k={k}")
        means.append(float(np.mean(ratio)))
    # verify J1==phi on a small sample
    sample = np.linspace(1, params.n_max, 100, dtype=int)
    for s in sample:
        j1 = jordan_totient(int(s), 1, sieve=sieve)
        max_abs_phi_err = max(max_abs_phi_err, abs(int(phi[s]) - int(j1)))
    ax.set_title("Ratios J_k(n)/n^k (downsampled)")
    ax.set_xlabel("n")
    ax.set_ylabel("ratio")
    ax.set_xscale("log")
    ax.legend()
    finalize_figure(fig)
    save_figure(out_dir=figures_dir, name="fig_01_jordan_ratios", fig=fig)
    plt.close(fig)

    lines: list[str] = []
    lines.append("# E099: Jordan totients J_k: atlas and identities")
    lines.append("")
    lines.append("## Artifacts")
    lines.append("- figures/fig_01_jordan_ratios.png")
    lines.append("- params.json")
    lines.append("- report.md")
    lines.append("")
    lines.append("### Notes")
    lines.append(f"- Mean ratios (downsampled) for k=1..k_max: {[round(x, 6) for x in means]}")
    lines.append(f"- Max |J_1(n)-phi(n)| on a 100-point sample: {max_abs_phi_err}")
    lines.append("- J_k(n) = n^k ∏_{p|n}(1-1/p^k) (multiplicative).")
    _write_report(report_path=report_path, lines=lines)


@dataclass(frozen=True, slots=True)
class ParamsE100:
    """Parameters for E100.

    Args:
        n_max: Upper bound N (inclusive).
        max_ratio: Max ratio bin for histogram (values clipped).
        bins: Number of histogram bins.
    """

    n_max: int = 25_000
    max_ratio: float = 1.0
    bins: int = 40


def run_e100(
    *, out_dir: Path, seed: int, figures_dir: Path, report_path: Path, params_path: Path
) -> None:
    """E100: Carmichael λ(n) vs Euler φ(n)."""
    params = ParamsE100()
    write_json(params_path, asdict(params))

    sieve = _factor_sieve(params.n_max)
    phi = compute_phi(params.n_max, sieve=sieve)
    lam = np.array(
        [carmichael_lambda(n, sieve=sieve) for n in range(1, params.n_max + 1)], dtype=np.float64
    )
    phi_np = np.asarray(phi[1 : params.n_max + 1], dtype=np.float64)
    ratio = np.divide(lam, phi_np, out=np.zeros_like(lam), where=phi_np != 0)
    ratio_clip = np.clip(ratio, 0.0, params.max_ratio)
    fig, ax = plt.subplots()
    ax.hist(ratio_clip, bins=params.bins)
    ax.set_title("Histogram of λ(n)/φ(n) (clipped)")
    ax.set_xlabel("λ(n)/φ(n)")
    ax.set_ylabel("count")
    finalize_figure(fig)
    save_figure(out_dir=figures_dir, name="fig_01_lambda_over_phi_hist", fig=fig)
    plt.close(fig)
    min_ratio = float(np.min(ratio))
    max_ratio = float(np.max(ratio))

    lines: list[str] = []
    lines.append("# E100: Carmichael λ(n) vs Euler φ(n)")
    lines.append("")
    lines.append("## Artifacts")
    lines.append("- figures/fig_01_lambda_over_phi_hist.png")
    lines.append("- params.json")
    lines.append("- report.md")
    lines.append("")
    lines.append("### Notes")
    lines.append(f"- min λ(n)/φ(n): {min_ratio:.6f}")
    lines.append(f"- max λ(n)/φ(n): {max_ratio:.6f}")
    lines.append("- λ(n) is the exponent of (Z/nZ)^× and often much smaller than φ(n).")
    _write_report(report_path=report_path, lines=lines)


@dataclass(frozen=True, slots=True)
class ParamsE101:
    """Parameters for E101.

    Args:
        q_values: Moduli to inspect.
    """

    q_values: tuple[int, ...] = (10, 12, 15, 21, 30)


def run_e101(
    *, out_dir: Path, seed: int, figures_dir: Path, report_path: Path, params_path: Path
) -> None:
    """E101: Reduced residues: (Z/qZ)^× as a concrete set."""
    params = ParamsE101()
    write_json(params_path, asdict(params))

    q_vals = list(params.q_values)
    sizes = []
    phis = []
    for q in q_vals:
        rr = reduced_residues(int(q))
        sizes.append(len(rr))
        phis.append(euler_phi(int(q)))
    x = np.arange(len(q_vals))
    fig, ax = plt.subplots()
    ax.bar(x - 0.2, sizes, width=0.4, label="|RR(q)|")
    ax.bar(x + 0.2, phis, width=0.4, label="phi(q)")
    ax.set_title("Reduced residue system size vs phi(q)")
    ax.set_xlabel("q index")
    ax.set_ylabel("count")
    ax.set_xticks(x, [str(q) for q in q_vals])
    ax.legend()
    finalize_figure(fig)
    save_figure(out_dir=figures_dir, name="fig_01_reduced_residues_sizes", fig=fig)
    plt.close(fig)
    examples = {int(q): reduced_residues(int(q))[:15] for q in q_vals}

    lines: list[str] = []
    lines.append("# E101: Reduced residues: (Z/qZ)^× as a concrete set")
    lines.append("")
    lines.append("## Artifacts")
    lines.append("- figures/fig_01_reduced_residues_sizes.png")
    lines.append("- params.json")
    lines.append("- report.md")
    lines.append("")
    lines.append("### Notes")
    lines.append(f"- Checked q values: {list(params.q_values)}")
    lines.append(
        f"- sizes match phi(q): {all(int(a) == int(b) for a, b in zip(sizes, phis, strict=False))}"
    )
    lines.append(f"- Example prefixes of RR(q): {examples}")
    _write_report(report_path=report_path, lines=lines)


@dataclass(frozen=True, slots=True)
class ParamsE102:
    """Parameters for E102.

    Args:
        n_max: Maximum n for convolution checks.
    """

    n_max: int = 20_000


def run_e102(
    *, out_dir: Path, seed: int, figures_dir: Path, report_path: Path, params_path: Path
) -> None:
    """E102: Dirichlet convolution identity zoo."""
    params = ParamsE102()
    write_json(params_path, asdict(params))

    sieve = _factor_sieve(params.n_max)
    mu = compute_mobius(params.n_max, sieve=sieve)
    phi = compute_phi(params.n_max, sieve=sieve)
    one = ones(params.n_max)
    eps = epsilon(params.n_max)
    idf = identity(params.n_max)
    tau, sigma = compute_tau_sigma(params.n_max, sieve=sieve)
    # μ * 1 = ε
    conv_mu_one = dirichlet_convolution(mu, one, n_max=params.n_max).values
    err_mu = max(abs(conv_mu_one[i] - eps[i]) for i in range(0, params.n_max + 1))
    # φ * 1 = id
    conv_phi_one = dirichlet_convolution(phi, one, n_max=params.n_max).values
    err_phi = max(abs(conv_phi_one[i] - idf[i]) for i in range(0, params.n_max + 1))
    # 1 * 1 = τ
    conv_one_one = dirichlet_convolution(one, one, n_max=params.n_max).values
    err_tau = max(abs(conv_one_one[i] - tau[i]) for i in range(0, params.n_max + 1))
    # id * 1 = σ
    conv_id_one = dirichlet_convolution(idf, one, n_max=params.n_max).values
    err_sigma = max(abs(conv_id_one[i] - sigma[i]) for i in range(0, params.n_max + 1))
    labels = ["mu*1-eps", "phi*1-id", "1*1-tau", "id*1-sigma"]
    errs = [err_mu, err_phi, err_tau, err_sigma]
    fig, ax = plt.subplots()
    ax.bar(np.arange(len(errs)), errs)
    ax.set_title("Max absolute error for classic convolution identities")
    ax.set_xlabel("identity")
    ax.set_ylabel("max |lhs-rhs|")
    ax.set_xticks(np.arange(len(errs)), labels, rotation=20, ha="right")
    finalize_figure(fig)
    save_figure(out_dir=figures_dir, name="fig_01_convolution_identity_errors", fig=fig)
    plt.close(fig)

    lines: list[str] = []
    lines.append("# E102: Dirichlet convolution identity zoo")
    lines.append("")
    lines.append("## Artifacts")
    lines.append("- figures/fig_01_convolution_identity_errors.png")
    lines.append("- params.json")
    lines.append("- report.md")
    lines.append("")
    lines.append("### Notes")
    lines.append(f"- Max errors: {dict(zip(labels, errs, strict=False))}")
    lines.append("- All should be exactly 0 for these sieve-based implementations.")
    _write_report(report_path=report_path, lines=lines)


@dataclass(frozen=True, slots=True)
class ParamsE103:
    """Parameters for E103.

    Args:
        n_max: Upper bound N (inclusive).
        stride: Downsampling stride for plotting.
    """

    n_max: int = 200_000
    stride: int = 5


def run_e103(
    *, out_dir: Path, seed: int, figures_dir: Path, report_path: Path, params_path: Path
) -> None:
    """E103: Chebyshev ψ(x): prime powers drive the jumps."""
    params = ParamsE103()
    write_json(params_path, asdict(params))

    sieve = _factor_sieve(params.n_max)
    psi = chebyshev_psi(params.n_max, sieve=sieve)
    lam = compute_von_mangoldt(params.n_max, sieve=sieve)
    psi_np = np.asarray(psi[1 : params.n_max + 1], dtype=np.float64)
    n = np.arange(1, params.n_max + 1, dtype=np.float64)
    diff = psi_np - n
    idx = np.arange(0, params.n_max, params.stride)
    fig, ax = plt.subplots()
    ax.plot((idx + 1), diff[idx])
    ax.set_title("ψ(x) - x (downsampled)")
    ax.set_xlabel("x")
    ax.set_ylabel("ψ(x)-x")
    ax.set_xscale("log")
    finalize_figure(fig)
    save_figure(out_dir=figures_dir, name="fig_01_psi_minus_x", fig=fig)
    plt.close(fig)
    nonzero = int(sum(1 for v in lam[1 : params.n_max + 1] if v != 0.0))

    lines: list[str] = []
    lines.append("# E103: Chebyshev ψ(x): prime powers drive the jumps")
    lines.append("")
    lines.append("## Artifacts")
    lines.append("- figures/fig_01_psi_minus_x.png")
    lines.append("- params.json")
    lines.append("- report.md")
    lines.append("")
    lines.append("### Notes")
    lines.append(f"- Nonzero Λ(n) terms up to N (prime powers): {nonzero}")
    lines.append("- ψ(x) is the summatory von Mangoldt function and jumps at prime powers.")
    _write_report(report_path=report_path, lines=lines)


@dataclass(frozen=True, slots=True)
class ParamsE104:
    """Parameters for E104.

    Args:
        n_max: Upper bound N (inclusive).
        bins: Histogram bins.
    """

    n_max: int = 200_000
    bins: int = 30


def run_e104(
    *, out_dir: Path, seed: int, figures_dir: Path, report_path: Path, params_path: Path
) -> None:
    """E104: Von Mangoldt Λ: support and statistics."""
    params = ParamsE104()
    write_json(params_path, asdict(params))

    sieve = _factor_sieve(params.n_max)
    lam = compute_von_mangoldt(params.n_max, sieve=sieve)
    vals = np.asarray([v for v in lam[1 : params.n_max + 1] if v != 0.0], dtype=np.float64)
    density = float(vals.size) / float(params.n_max)
    fig, ax = plt.subplots()
    ax.hist(vals, bins=params.bins)
    ax.set_title("Histogram of nonzero Λ(n) values (log primes)")
    ax.set_xlabel("Λ(n)")
    ax.set_ylabel("count")
    finalize_figure(fig)
    save_figure(out_dir=figures_dir, name="fig_01_lambda_hist", fig=fig)
    plt.close(fig)
    unique = sorted({round(float(x), 8) for x in vals})

    lines: list[str] = []
    lines.append("# E104: Von Mangoldt Λ: support and statistics")
    lines.append("")
    lines.append("## Artifacts")
    lines.append("- figures/fig_01_lambda_hist.png")
    lines.append("- params.json")
    lines.append("- report.md")
    lines.append("")
    lines.append("### Notes")
    lines.append(f"- Nonzero density: {density:.6f}")
    lines.append(f"- Unique Λ(n) values are logs of primes; sample: {unique[:10]}")
    _write_report(report_path=report_path, lines=lines)


@dataclass(frozen=True, slots=True)
class ParamsE105:
    """Parameters for E105.

    Args:
        n_max: Upper bound N (inclusive).
        stride: Downsampling stride for plotting.
    """

    n_max: int = 200_000
    stride: int = 5


def run_e105(
    *, out_dir: Path, seed: int, figures_dir: Path, report_path: Path, params_path: Path
) -> None:
    """E105: Mertens function M(x): scaling views."""
    params = ParamsE105()
    write_json(params_path, asdict(params))

    sieve = _factor_sieve(params.n_max)
    mu = compute_mobius(params.n_max, sieve=sieve)
    mu_np = np.asarray(mu[1 : params.n_max + 1], dtype=np.int64)
    M = np.cumsum(mu_np).astype(np.float64)
    n = np.arange(1, params.n_max + 1, dtype=np.float64)
    rescaled = M / np.sqrt(n)
    idx = np.arange(0, params.n_max, params.stride)
    fig, ax = plt.subplots()
    ax.plot((idx + 1), M[idx])
    ax.set_title("Mertens function M(x) (downsampled)")
    ax.set_xlabel("x")
    ax.set_ylabel("M(x)")
    ax.set_xscale("log")
    finalize_figure(fig)
    save_figure(out_dir=figures_dir, name="fig_01_mertens_M", fig=fig)
    plt.close(fig)
    fig, ax = plt.subplots()
    ax.plot((idx + 1), rescaled[idx])
    ax.set_title("Rescaled M(x)/sqrt(x) (downsampled)")
    ax.set_xlabel("x")
    ax.set_ylabel("M(x)/sqrt(x)")
    ax.set_xscale("log")
    finalize_figure(fig)
    save_figure(out_dir=figures_dir, name="fig_02_mertens_rescaled", fig=fig)
    plt.close(fig)
    max_abs = float(np.max(np.abs(M)))

    lines: list[str] = []
    lines.append("# E105: Mertens function M(x): scaling views")
    lines.append("")
    lines.append("## Artifacts")
    lines.append("- figures/fig_01_mertens_M.png")
    lines.append("- figures/fig_02_mertens_rescaled.png")
    lines.append("- params.json")
    lines.append("- report.md")
    lines.append("")
    lines.append("### Notes")
    lines.append(f"- max |M(x)| on 1..N: {max_abs:.1f}")
    lines.append("- Random-walk-like oscillations appear across scales (visual heuristic).")
    _write_report(report_path=report_path, lines=lines)


@dataclass(frozen=True, slots=True)
class ParamsE106:
    """Parameters for E106.

    Args:
        q_values: Moduli to inspect.
    """

    q_values: tuple[int, ...] = (5, 8, 10, 12, 15)


def run_e106(
    *, out_dir: Path, seed: int, figures_dir: Path, report_path: Path, params_path: Path
) -> None:
    """E106: Real vs complex Dirichlet characters (small moduli)."""
    params = ParamsE106()
    write_json(params_path, asdict(params))

    q_vals = list(params.q_values)
    real_counts: list[int] = []
    total_counts: list[int] = []
    for q in q_vals:
        chars = all_characters(int(q))
        total_counts.append(len(chars))
        cnt = 0
        for chi in chars:
            # A character is 'real' if values are in {-1,0,1} up to numerical noise.
            vals = [chi(a) for a in range(q)]
            if all(abs(v.imag) < 1e-12 for v in vals):
                cnt += 1
        real_counts.append(cnt)
    x = np.arange(len(q_vals))
    fig, ax = plt.subplots()
    ax.bar(x - 0.2, real_counts, width=0.4, label="real")
    ax.bar(x + 0.2, total_counts, width=0.4, label="total")
    ax.set_title("Real Dirichlet characters among all characters")
    ax.set_xlabel("q")
    ax.set_ylabel("count")
    ax.set_xticks(x, [str(q) for q in q_vals])
    ax.legend()
    finalize_figure(fig)
    save_figure(out_dir=figures_dir, name="fig_01_real_character_counts", fig=fig)
    plt.close(fig)

    lines: list[str] = []
    lines.append("# E106: Real vs complex Dirichlet characters (small moduli)")
    lines.append("")
    lines.append("## Artifacts")
    lines.append("- figures/fig_01_real_character_counts.png")
    lines.append("- params.json")
    lines.append("- report.md")
    lines.append("")
    lines.append("### Notes")
    lines.append(f"- q values: {q_vals}")
    lines.append(f"- real/total: {list(zip(q_vals, real_counts, total_counts, strict=False))}")
    lines.append("- Real characters correspond to quadratic characters and products thereof.")
    _write_report(report_path=report_path, lines=lines)


@dataclass(frozen=True, slots=True)
class ParamsE107:
    """Parameters for E107.

    Args:
        q: Composite modulus to inspect.
    """

    q: int = 60


def run_e107(
    *, out_dir: Path, seed: int, figures_dir: Path, report_path: Path, params_path: Path
) -> None:
    """E107: Conductor distribution for characters."""
    params = ParamsE107()
    write_json(params_path, asdict(params))

    q = int(params.q)
    chars = all_characters(q)
    conds = [conductor(chi) for chi in chars]
    values, counts = np.unique(np.asarray(conds, dtype=np.int64), return_counts=True)
    fig, ax = plt.subplots()
    ax.bar(values, counts)
    ax.set_title(f"Conductor counts for characters mod {q}")
    ax.set_xlabel("conductor")
    ax.set_ylabel("count")
    finalize_figure(fig)
    save_figure(out_dir=figures_dir, name="fig_01_conductor_hist", fig=fig)
    plt.close(fig)
    nontrivial = int(sum(1 for chi in chars if not chi.is_principal))

    lines: list[str] = []
    lines.append("# E107: Conductor distribution for characters")
    lines.append("")
    lines.append("## Artifacts")
    lines.append("- figures/fig_01_conductor_hist.png")
    lines.append("- params.json")
    lines.append("- report.md")
    lines.append("")
    lines.append("### Notes")
    lines.append(f"- Total characters: {len(chars)}")
    lines.append(f"- Non-principal characters: {nontrivial}")
    lines.append(f"- Conductors observed: {values.tolist()}")
    _write_report(report_path=report_path, lines=lines)


@dataclass(frozen=True, slots=True)
class ParamsE108:
    """Parameters for E108.

    Args:
        q: Modulus (small, to keep the matrix readable).
    """

    q: int = 15


def run_e108(
    *, out_dir: Path, seed: int, figures_dir: Path, report_path: Path, params_path: Path
) -> None:
    """E108: Character orthogonality matrix heatmap."""
    params = ParamsE108()
    write_json(params_path, asdict(params))

    q = int(params.q)
    mat = orthogonality_matrix(q)
    abs_mat = np.abs(mat)
    fig, ax = plt.subplots()
    im = ax.imshow(abs_mat, aspect="auto")
    fig.colorbar(im, ax=ax)
    ax.set_title(f"|<chi_i, chi_j>| for characters mod {q}")
    ax.set_xlabel("j")
    ax.set_ylabel("i")
    finalize_figure(fig)
    save_figure(out_dir=figures_dir, name="fig_01_orthogonality_abs", fig=fig)
    plt.close(fig)
    diag_mean = float(np.mean(np.diag(abs_mat)))
    off_mean = float(np.mean(abs_mat - np.diag(np.diag(abs_mat)))) / (
        abs_mat.size - abs_mat.shape[0]
    )

    lines: list[str] = []
    lines.append("# E108: Character orthogonality matrix heatmap")
    lines.append("")
    lines.append("## Artifacts")
    lines.append("- figures/fig_01_orthogonality_abs.png")
    lines.append("- params.json")
    lines.append("- report.md")
    lines.append("")
    lines.append("### Notes")
    lines.append(f"- Mean diagonal magnitude: {diag_mean:.6f}")
    lines.append(f"- Mean off-diagonal magnitude: {off_mean:.6f}")
    lines.append(
        "- For a correctly normalized inner product, diagonal entries dominate and off-diagonals are ~0."
    )
    _write_report(report_path=report_path, lines=lines)


@dataclass(frozen=True, slots=True)
class ParamsE109:
    """Parameters for E109.

    Args:
        q: Prime modulus.
    """

    q: int = 11


def run_e109(
    *, out_dir: Path, seed: int, figures_dir: Path, report_path: Path, params_path: Path
) -> None:
    """E109: Gauss sums τ(χ) for prime modulus."""
    params = ParamsE109()
    write_json(params_path, asdict(params))

    q = int(params.q)
    chars = [chi for chi in all_characters(q) if not chi.is_principal]
    w = np.exp(2j * np.pi / q)
    mags: list[float] = []
    for chi in chars:
        s = 0j
        for a in range(q):
            s += chi(a) * (w**a)
        mags.append(abs(s))
    mags_np = np.asarray(mags, dtype=np.float64)
    fig, ax = plt.subplots()
    ax.bar(np.arange(len(mags_np)), mags_np)
    ax.axhline(math.sqrt(q), linestyle="--")
    ax.set_title(f"Gauss sum magnitudes |τ(χ)| (mod {q})")
    ax.set_xlabel("nonprincipal character index")
    ax.set_ylabel("|τ(χ)|")
    finalize_figure(fig)
    save_figure(out_dir=figures_dir, name="fig_01_gauss_sum_magnitudes", fig=fig)
    plt.close(fig)
    rel_err = float(np.max(np.abs(mags_np - math.sqrt(q))))

    lines: list[str] = []
    lines.append("# E109: Gauss sums τ(χ) for prime modulus")
    lines.append("")
    lines.append("## Artifacts")
    lines.append("- figures/fig_01_gauss_sum_magnitudes.png")
    lines.append("- params.json")
    lines.append("- report.md")
    lines.append("")
    lines.append("### Notes")
    lines.append(f"- Nonprincipal characters: {len(chars)}")
    lines.append(f"- max | |τ(χ)| - sqrt(q) |: {rel_err:.6f}")
    lines.append(
        "- For prime q, nonprincipal characters are primitive and |τ(χ)| = sqrt(q) (classic theorem)."
    )
    _write_report(report_path=report_path, lines=lines)


@dataclass(frozen=True, slots=True)
class ParamsE110:
    """Parameters for E110.

    Args:
        q: Modulus.
        n_max: Truncation for the Dirichlet series.
        s_re: Real part of s for convergent evaluation.
    """

    q: int = 5
    n_max: int = 5_000
    s_re: float = 1.0


def run_e110(
    *, out_dir: Path, seed: int, figures_dir: Path, report_path: Path, params_path: Path
) -> None:
    """E110: Dirichlet L-series partial sums (toy)."""
    params = ParamsE110()
    write_json(params_path, asdict(params))

    q = int(params.q)
    chars = [chi for chi in all_characters(q) if not chi.is_principal]
    if not chars:
        _write_report(report_path=report_path, lines=["# E110: no nonprincipal characters found"])
        return
    chi = chars[0]
    s = complex(params.s_re, 0.0)
    partial: list[complex] = []
    acc = 0j
    for n in range(1, params.n_max + 1):
        acc += chi(n) / (n**s)
        partial.append(acc)
    partial_np = np.asarray(partial, dtype=np.complex128)
    fig, ax = plt.subplots()
    ax.plot(np.arange(1, params.n_max + 1), np.abs(partial_np))
    ax.set_title(f"|sum_{{n <= N}} chi(n)/n^s| for s={s} (mod {q})")
    ax.set_xlabel("N")
    ax.set_ylabel("magnitude")
    finalize_figure(fig)
    save_figure(out_dir=figures_dir, name="fig_01_L_partial_magnitude", fig=fig)
    plt.close(fig)
    final_val = partial_np[-1]

    lines: list[str] = []
    lines.append("# E110: Dirichlet L-series partial sums (toy)")
    lines.append("")
    lines.append("## Artifacts")
    lines.append("- figures/fig_01_L_partial_magnitude.png")
    lines.append("- params.json")
    lines.append("- report.md")
    lines.append("")
    lines.append("### Notes")
    lines.append("- Using first nonprincipal character mod q.")
    lines.append(f"- Final partial sum at N=n_max: {final_val}.")
    lines.append("- For nonprincipal χ and Re(s)=1, the series converges (slowly).")
    _write_report(report_path=report_path, lines=lines)


@dataclass(frozen=True, slots=True)
class ParamsE111:
    """Parameters for E111.

    Args:
        q: Modulus.
        s_re: Real part of s (>1).
        n_series: Truncation for Dirichlet series.
        p_max: Max prime for Euler product.
        p_steps: Number of prime cutoffs to test.
    """

    q: int = 5
    s_re: float = 1.5
    n_series: int = 8_000
    p_max: int = 2_000
    p_steps: int = 30


def run_e111(
    *, out_dir: Path, seed: int, figures_dir: Path, report_path: Path, params_path: Path
) -> None:
    """E111: Euler product vs Dirichlet series for L(s,χ)."""
    params = ParamsE111()
    write_json(params_path, asdict(params))

    q = int(params.q)
    chars = [chi for chi in all_characters(q) if not chi.is_principal]
    if not chars:
        _write_report(report_path=report_path, lines=["# E111: no nonprincipal characters found"])
        return
    chi = chars[0]
    s = complex(params.s_re, 0.0)
    # reference via long series
    ref = 0j
    for n in range(1, params.n_series + 1):
        ref += chi(n) / (n**s)
    primes = primes_up_to(params.p_max).astype(int).tolist()
    cutoffs = np.linspace(10, len(primes), params.p_steps, dtype=int)
    errs: list[float] = []
    ps: list[int] = []
    for c in cutoffs:
        pp = primes[: int(c)]
        prod = 1.0 + 0j
        for p in pp:
            prod *= 1.0 / (1.0 - chi(p) / (p**s))
        err = abs(prod - ref)
        errs.append(float(err))
        ps.append(pp[-1] if pp else 2)
    fig, ax = plt.subplots()
    ax.plot(ps, errs)
    ax.set_title(f"|Euler product - series| for L(s,chi), s={s}")
    ax.set_xlabel("prime cutoff P")
    ax.set_ylabel("absolute error")
    ax.set_xscale("log")
    ax.set_yscale("log")
    finalize_figure(fig)
    save_figure(out_dir=figures_dir, name="fig_01_euler_product_error", fig=fig)
    plt.close(fig)
    best = float(min(errs)) if errs else float("nan")

    lines: list[str] = []
    lines.append("# E111: Euler product vs Dirichlet series for L(s,χ)")
    lines.append("")
    lines.append("## Artifacts")
    lines.append("- figures/fig_01_euler_product_error.png")
    lines.append("- params.json")
    lines.append("- report.md")
    lines.append("")
    lines.append("### Notes")
    lines.append(f"- Reference computed by series up to N={params.n_series}")
    lines.append(f"- Best (min) absolute error across P cutoffs: {best:.3e}")
    lines.append("- For Re(s)>1, Euler product and series converge to the same L(s,χ).")
    _write_report(report_path=report_path, lines=lines)


@dataclass(frozen=True, slots=True)
class ParamsE112:
    """Parameters for E112.

    Args:
        q: Modulus.
        a: First residue (must be coprime to q).
        b: Second residue (must be coprime to q).
        p_max: Max prime to include.
    """

    q: int = 8
    a: int = 1
    b: int = 3
    p_max: int = 800_000


def run_e112(
    *, out_dir: Path, seed: int, figures_dir: Path, report_path: Path, params_path: Path
) -> None:
    """E112: Prime race π(x;q,a) − π(x;q,b)."""
    params = ParamsE112()
    write_json(params_path, asdict(params))

    primes = primes_up_to(params.p_max)
    p = primes[primes >= 3]
    a = np.cumsum((p % params.q == params.a).astype(np.int64))
    b = np.cumsum((p % params.q == params.b).astype(np.int64))
    diff = a - b
    fig, ax = plt.subplots()
    ax.plot(p, diff)
    ax.set_title(
        f"Prime race diff up to {params.p_max}: a={params.a}, b={params.b} (mod {params.q})"
    )
    ax.set_xlabel("prime p")
    ax.set_ylabel("π(p;q,a)-π(p;q,b)")
    ax.set_xscale("log")
    finalize_figure(fig)
    save_figure(out_dir=figures_dir, name="fig_01_prime_race_diff", fig=fig)
    plt.close(fig)
    lead = int(diff[-1]) if diff.size else 0

    lines: list[str] = []
    lines.append("# E112: Prime race π(x;q,a) − π(x;q,b)")
    lines.append("")
    lines.append("## Artifacts")
    lines.append("- figures/fig_01_prime_race_diff.png")
    lines.append("- params.json")
    lines.append("- report.md")
    lines.append("")
    lines.append("### Notes")
    lines.append(f"- Final lead at p_max: {lead}")
    lines.append("- The diff changes sign; persistent bias is subtle and depends on q,a,b.")
    _write_report(report_path=report_path, lines=lines)


@dataclass(frozen=True, slots=True)
class ParamsE113:
    """Parameters for E113.

    Args:
        q: Modulus.
        p_max: Search primes up to this bound.
    """

    q: int = 30
    p_max: int = 200_000


def run_e113(
    *, out_dir: Path, seed: int, figures_dir: Path, report_path: Path, params_path: Path
) -> None:
    """E113: First prime in each reduced residue class."""
    params = ParamsE113()
    write_json(params_path, asdict(params))

    q = int(params.q)
    rr = reduced_residues(q)
    primes = primes_up_to(params.p_max).astype(int).tolist()
    first: dict[int, int] = dict.fromkeys(rr, 0)
    for p in primes:
        if p < 2:
            continue
        r = p % q
        if r in first and first[r] == 0:
            first[r] = p
        if all(v != 0 for v in first.values()):
            break
    vals = [first[a] for a in rr]
    fig, ax = plt.subplots()
    ax.bar(np.arange(len(rr)), vals)
    ax.set_title(f"First prime for each a in RR({q})")
    ax.set_xlabel("residue index")
    ax.set_ylabel("first prime")
    ax.set_xticks(np.arange(len(rr)), [str(a) for a in rr], rotation=30, ha="right")
    finalize_figure(fig)
    save_figure(out_dir=figures_dir, name="fig_01_first_prime_per_residue", fig=fig)
    plt.close(fig)
    missing = [a for a, v in first.items() if v == 0]

    lines: list[str] = []
    lines.append("# E113: First prime in each reduced residue class")
    lines.append("")
    lines.append("## Artifacts")
    lines.append("- figures/fig_01_first_prime_per_residue.png")
    lines.append("- params.json")
    lines.append("- report.md")
    lines.append("")
    lines.append("### Notes")
    lines.append(f"- RR(q) size: {len(rr)}")
    lines.append(f"- Missing residues within search bound: {missing}")
    lines.append("- This is a small-N version of the Linnik / least prime in AP story.")
    _write_report(report_path=report_path, lines=lines)


@dataclass(frozen=True, slots=True)
class ParamsE114:
    """Parameters for E114.

    Args:
        t_max: Max height t.
        t_steps: Number of t samples.
        n_terms_values: Eta truncation sizes.
        ref_dps: mpmath precision for reference zeta.
        eval_dps: mpmath precision for eta evaluation.
    """

    t_max: float = 30.0
    t_steps: int = 61
    n_terms_values: tuple[int, ...] = (100, 200, 400)
    ref_dps: int = 70
    eval_dps: int = 50


def run_e114(
    *, out_dir: Path, seed: int, figures_dir: Path, report_path: Path, params_path: Path
) -> None:
    """E114: ζ(1/2+it) via η-series: truncation error curves."""
    params = ParamsE114()
    write_json(params_path, asdict(params))

    ts = np.linspace(0.0, float(params.t_max), int(params.t_steps))
    n_terms_list = list(params.n_terms_values)
    settings = ZetaEvalSettings(dps=int(params.eval_dps))
    # reference
    ref: list[complex] = []
    with mp.workdps(int(params.ref_dps)):
        for t in ts:
            ref.append(complex(mp.zeta(0.5 + 1j * float(t))))
    errors: dict[int, np.ndarray] = {}
    for n_terms in n_terms_list:
        approx: list[complex] = []
        for t in ts:
            s = 0.5 + 1j * float(t)
            eta = eta_series_partial(s, int(n_terms), settings=settings)
            approx.append(zeta_via_eta(s, eta))
        a = np.asarray(approx, dtype=np.complex128)
        r = np.asarray(ref, dtype=np.complex128)
        errors[int(n_terms)] = np.abs(a - r)
    fig, ax = plt.subplots()
    for n_terms in n_terms_list:
        ax.plot(ts, errors[int(n_terms)], label=f"N={n_terms}")
    ax.set_title("Absolute error |zeta_eta - zeta_ref| along critical line")
    ax.set_xlabel("t")
    ax.set_ylabel("absolute error")
    ax.set_yscale("log")
    ax.legend()
    finalize_figure(fig)
    save_figure(out_dir=figures_dir, name="fig_01_eta_truncation_errors", fig=fig)
    plt.close(fig)
    max_err = {n: float(np.max(err)) for n, err in errors.items()}

    lines: list[str] = []
    lines.append("# E114: ζ(1/2+it) via η-series: truncation error curves")
    lines.append("")
    lines.append("## Artifacts")
    lines.append("- figures/fig_01_eta_truncation_errors.png")
    lines.append("- params.json")
    lines.append("- report.md")
    lines.append("")
    lines.append("### Notes")
    lines.append("- n_terms -> max error: {}".format({k: f"{v:.2e}" for k, v in max_err.items()}))
    lines.append(
        "- η-series converges for Re(s)>0, but near Re(s)=1/2 the truncation error is still visible."
    )
    _write_report(report_path=report_path, lines=lines)


@dataclass(frozen=True, slots=True)
class ParamsE115:
    """Parameters for E115.

    Args:
        t_max: Max t to scan.
        dt: Step size in t.
        dps: mpmath precision used by hardy_Z.
    """

    t_max: float = 40.0
    dt: float = 0.1
    dps: int = 40


def run_e115(
    *, out_dir: Path, seed: int, figures_dir: Path, report_path: Path, params_path: Path
) -> None:
    """E115: Hardy Z(t): sign-change scan near low zeros."""
    params = ParamsE115()
    write_json(params_path, asdict(params))

    settings = ZetaEvalSettings(dps=int(params.dps))
    ts = np.arange(0.0, float(params.t_max) + 1e-12, float(params.dt))
    Z = np.array([hardy_Z(float(t), settings=settings) for t in ts], dtype=np.float64)
    signs = np.sign(Z)
    changes = np.where(np.diff(signs) != 0)[0]
    intervals = [(float(ts[i]), float(ts[i + 1])) for i in changes[:12]]
    fig, ax = plt.subplots()
    ax.plot(ts, Z)
    ax.set_title("Hardy Z(t) (coarse scan)")
    ax.set_xlabel("t")
    ax.set_ylabel("Z(t)")
    finalize_figure(fig)
    save_figure(out_dir=figures_dir, name="fig_01_hardy_Z_scan", fig=fig)
    plt.close(fig)

    lines: list[str] = []
    lines.append("# E115: Hardy Z(t): sign-change scan near low zeros")
    lines.append("")
    lines.append("## Artifacts")
    lines.append("- figures/fig_01_hardy_Z_scan.png")
    lines.append("- params.json")
    lines.append("- report.md")
    lines.append("")
    lines.append("### Notes")
    lines.append(f"- Sign-change intervals (first 12): {intervals}")
    lines.append("- Each sign change suggests a zero of ζ(1/2+it) in that interval.")
    _write_report(report_path=report_path, lines=lines)


@dataclass(frozen=True, slots=True)
class ParamsE116:
    """Parameters for E116.

    Args:
        t_max: Max t to scan.
        dt: Step size in t.
        dps: mpmath precision used by hardy_Z.
    """

    t_max: float = 120.0
    dt: float = 0.2
    dps: int = 40


def run_e116(
    *, out_dir: Path, seed: int, figures_dir: Path, report_path: Path, params_path: Path
) -> None:
    """E116: Zero-count proxy vs Riemann–von Mangoldt main term."""
    params = ParamsE116()
    write_json(params_path, asdict(params))

    settings = ZetaEvalSettings(dps=int(params.dps))
    ts = np.arange(0.0, float(params.t_max) + 1e-12, float(params.dt))
    Z = np.array([hardy_Z(float(t), settings=settings) for t in ts], dtype=np.float64)
    sgn = np.sign(Z)
    changes = np.where(np.diff(sgn) != 0)[0]
    # crude count: each sign change => >=1 zero
    zero_ts = ts[changes]
    obs_counts = np.arange(1, len(zero_ts) + 1, dtype=np.float64)
    rvm = np.array([riemann_von_mangoldt_count(float(t)) for t in zero_ts], dtype=np.float64)
    fig, ax = plt.subplots()
    ax.plot(zero_ts, obs_counts, label="observed (sign changes)")
    ax.plot(zero_ts, rvm, label="RVM main term")
    ax.set_title("Zero-count proxy vs RVM main term")
    ax.set_xlabel("T")
    ax.set_ylabel("count")
    ax.legend()
    finalize_figure(fig)
    save_figure(out_dir=figures_dir, name="fig_01_zero_count_vs_rvm", fig=fig)
    plt.close(fig)
    final_obs = int(obs_counts[-1]) if obs_counts.size else 0
    final_rvm = float(rvm[-1]) if rvm.size else 0.0

    lines: list[str] = []
    lines.append("# E116: Zero-count proxy vs Riemann–von Mangoldt main term")
    lines.append("")
    lines.append("## Artifacts")
    lines.append("- figures/fig_01_zero_count_vs_rvm.png")
    lines.append("- params.json")
    lines.append("- report.md")
    lines.append("")
    lines.append("### Notes")
    lines.append(f"- Observed sign changes up to T: {final_obs}")
    lines.append(f"- RVM main term at last observed T: {final_rvm:.3f}")
    lines.append(
        "- Coarse scan undercounts (missed multiple zeros within a single dt bin) but tracks the growth trend."
    )
    _write_report(report_path=report_path, lines=lines)


@dataclass(frozen=True, slots=True)
class ParamsE117:
    """Parameters for E117.

    Args:
        t_max: Max imaginary part t.
        t_steps: Number of t samples.
        sigma: Real part σ for s=σ+it.
        dps: mpmath precision for evaluation.
    """

    t_max: float = 25.0
    t_steps: int = 60
    sigma: float = 0.2
    dps: int = 70


def run_e117(
    *, out_dir: Path, seed: int, figures_dir: Path, report_path: Path, params_path: Path
) -> None:
    """E117: Functional equation check: ζ(s) ≈ χ(s) ζ(1−s)."""
    params = ParamsE117()
    write_json(params_path, asdict(params))

    ts = np.linspace(0.0, float(params.t_max), int(params.t_steps))
    rel_err: list[float] = []
    settings = ZetaEvalSettings(dps=int(params.dps))
    with mp.workdps(int(params.dps)):
        for t in ts:
            s = complex(float(params.sigma), float(t))
            z1 = complex(mp.zeta(s))
            z2 = complex(mp.zeta(1.0 - s))
            chi = chi_factor(s, settings=settings)
            denom = abs(z1) if abs(z1) > 0 else 1.0
            rel_err.append(abs(z1 - chi * z2) / denom)
    rel = np.asarray(rel_err, dtype=np.float64)
    fig, ax = plt.subplots()
    ax.plot(ts, rel)
    ax.set_title("Relative functional-equation residual")
    ax.set_xlabel("t")
    ax.set_ylabel("rel error")
    ax.set_yscale("log")
    finalize_figure(fig)
    save_figure(out_dir=figures_dir, name="fig_01_functional_equation_residual", fig=fig)
    plt.close(fig)
    max_rel = float(np.max(rel)) if rel.size else float("nan")

    lines: list[str] = []
    lines.append("# E117: Functional equation check: ζ(s) ≈ χ(s) ζ(1−s)")
    lines.append("")
    lines.append("## Artifacts")
    lines.append("- figures/fig_01_functional_equation_residual.png")
    lines.append("- params.json")
    lines.append("- report.md")
    lines.append("")
    lines.append("### Notes")
    lines.append(f"- max relative residual on grid: {max_rel:.2e}")
    lines.append(
        "- This checks numerical consistency of chi_factor and mpmath zeta implementation on a small grid."
    )
    _write_report(report_path=report_path, lines=lines)


@dataclass(frozen=True, slots=True)
class ParamsE118:
    """Parameters for E118.

    Args:
        p_max: Max prime for Euler product.
        p_steps: Number of prime cutoffs.
        dps: mpmath precision.
        s_values: s values to compare.
    """

    p_max: int = 50_000
    p_steps: int = 40
    dps: int = 60
    s_values: tuple[complex, ...] = ((1.2 + 0j), (1.05 + 0j), (0.9 + 0j))


def run_e118(
    *, out_dir: Path, seed: int, figures_dir: Path, report_path: Path, params_path: Path
) -> None:
    """E118: Euler product approximation vs ζ(s): where it degrades."""
    params = ParamsE118()
    write_json(params_path, asdict(params))

    primes = primes_up_to(int(params.p_max)).astype(int).tolist()
    cut_idxs = np.linspace(10, len(primes), int(params.p_steps), dtype=int)
    P_vals = [primes[i - 1] for i in cut_idxs]
    settings = ZetaEvalSettings(dps=int(params.dps))
    errs_by_s: dict[str, list[float]] = {}
    with mp.workdps(int(params.dps)):
        for s in params.s_values:
            z_ref = complex(mp.zeta(s))
            errs: list[float] = []
            for idx in cut_idxs:
                prod = euler_product_partial(s, primes[: int(idx)], settings=settings)
                errs.append(float(abs(prod - z_ref)))
            errs_by_s[str(s)] = errs
    fig, ax = plt.subplots()
    for s_str, errs in errs_by_s.items():
        ax.plot(P_vals, errs, label=s_str)
    ax.set_title("Euler product error |prod_p<=P - zeta(s)|")
    ax.set_xlabel("P")
    ax.set_ylabel("absolute error")
    ax.set_xscale("log")
    ax.set_yscale("log")
    ax.legend()
    finalize_figure(fig)
    save_figure(out_dir=figures_dir, name="fig_01_euler_product_breakdown", fig=fig)
    plt.close(fig)
    best = {k: float(min(v)) for k, v in errs_by_s.items()}

    lines: list[str] = []
    lines.append("# E118: Euler product approximation vs ζ(s): where it degrades")
    lines.append("")
    lines.append("## Artifacts")
    lines.append("- figures/fig_01_euler_product_breakdown.png")
    lines.append("- params.json")
    lines.append("- report.md")
    lines.append("")
    lines.append("### Notes")
    lines.append(
        "- Best (min) abs error per s: {}".format({k: f"{v:.2e}" for k, v in best.items()})
    )
    lines.append(
        "- As Re(s) approaches 1 from the right, convergence slows; for Re(s)<=1 the Euler product no longer converges."
    )
    _write_report(report_path=report_path, lines=lines)


@dataclass(frozen=True, slots=True)
class ParamsE119:
    """Parameters for E119.

    Args:
        n_max: Upper bound N (inclusive).
        stride: Downsampling stride for plotting.
        window: Smoothing window (moving average) for ψ(x)−x.
    """

    n_max: int = 300_000
    stride: int = 10
    window: int = 500


def run_e119(
    *, out_dir: Path, seed: int, figures_dir: Path, report_path: Path, params_path: Path
) -> None:
    """E119: ψ(x)−x with simple smoothing."""
    params = ParamsE119()
    write_json(params_path, asdict(params))

    sieve = _factor_sieve(params.n_max)
    psi = chebyshev_psi(params.n_max, sieve=sieve)
    psi_np = np.asarray(psi[1 : params.n_max + 1], dtype=np.float64)
    n = np.arange(1, params.n_max + 1, dtype=np.float64)
    diff = psi_np - n
    w = int(params.window)
    kernel = np.ones(w, dtype=np.float64) / float(w)
    smooth = np.convolve(diff, kernel, mode="same")
    idx = np.arange(0, params.n_max, int(params.stride))
    fig, ax = plt.subplots()
    ax.plot((idx + 1), diff[idx], label="raw")
    ax.plot((idx + 1), smooth[idx], label="smoothed")
    ax.set_title("ψ(x)−x (raw and smoothed)")
    ax.set_xlabel("x")
    ax.set_ylabel("value")
    ax.set_xscale("log")
    ax.legend()
    finalize_figure(fig)
    save_figure(out_dir=figures_dir, name="fig_01_psi_minus_x_smoothed", fig=fig)
    plt.close(fig)
    max_raw = float(np.max(np.abs(diff)))
    max_smooth = float(np.max(np.abs(smooth)))

    lines: list[str] = []
    lines.append("# E119: ψ(x)−x with simple smoothing")
    lines.append("")
    lines.append("## Artifacts")
    lines.append("- figures/fig_01_psi_minus_x_smoothed.png")
    lines.append("- params.json")
    lines.append("- report.md")
    lines.append("")
    lines.append("### Notes")
    lines.append(f"- max |ψ(x)−x| (raw): {max_raw:.1f}")
    lines.append(f"- max |ψ(x)−x| (smoothed): {max_smooth:.1f}")
    lines.append("- Smoothing suppresses prime-power spikes and reveals slower oscillations.")
    _write_report(report_path=report_path, lines=lines)


@dataclass(frozen=True, slots=True)
class ParamsE120:
    """Parameters for E120.

    Args:
        q: Modulus.
        p_max: Max prime to include.
    """

    q: int = 8
    p_max: int = 400_000


def run_e120(
    *, out_dir: Path, seed: int, figures_dir: Path, report_path: Path, params_path: Path
) -> None:
    """E120: Pretentious distance toy: sum_{p<=x} (1−Re χ(p))/p."""
    params = ParamsE120()
    write_json(params_path, asdict(params))

    q = int(params.q)
    chars = all_characters(q)
    chi0 = next((c for c in chars if c.is_principal), None)
    chi1 = next((c for c in chars if not c.is_principal), None)
    if chi0 is None or chi1 is None:
        _write_report(report_path=report_path, lines=["# E120: insufficient characters"])
        return
    primes = primes_up_to(int(params.p_max)).astype(int)
    # ignore p=2 when q even to avoid chi(p)=0 spikes dominating
    primes = primes[primes > 2]

    def _dist(chi: DirichletCharacter) -> np.ndarray:
        vals = np.array([1.0 - float(np.real(chi(int(p)))) for p in primes], dtype=np.float64)
        return np.cumsum(vals / primes.astype(np.float64))

    d0 = _dist(chi0)
    d1 = _dist(chi1)
    fig, ax = plt.subplots()
    ax.plot(primes, d0, label="principal")
    ax.plot(primes, d1, label="nonprincipal")
    ax.set_title(f"Pretentious distance proxy (mod {q})")
    ax.set_xlabel("prime p")
    ax.set_ylabel("cumulative sum")
    ax.set_xscale("log")
    ax.legend()
    finalize_figure(fig)
    save_figure(out_dir=figures_dir, name="fig_01_pretentious_distance_proxy", fig=fig)
    plt.close(fig)
    end0 = float(d0[-1]) if d0.size else 0.0
    end1 = float(d1[-1]) if d1.size else 0.0

    lines: list[str] = []
    lines.append("# E120: Pretentious distance toy: sum_{p <= x} (1−Re χ(p))/p")
    lines.append("")
    lines.append("## Artifacts")
    lines.append("- figures/fig_01_pretentious_distance_proxy.png")
    lines.append("- params.json")
    lines.append("- report.md")
    lines.append("")
    lines.append("### Notes")
    lines.append(f"- Final value (principal): {end0:.6f}")
    lines.append(f"- Final value (nonprincipal): {end1:.6f}")
    lines.append(
        "- This is a toy version of the pretentious distance framework (Granville–Soundararajan)."
    )
    _write_report(report_path=report_path, lines=lines)


@dataclass(frozen=True, slots=True)
class ParamsE121:
    """Parameters for E121.

    Args:
        n_max: Max n for function tables.
        pairs: Number of random coprime pairs to test.
    """

    n_max: int = 100_000
    pairs: int = 3_000


def run_e121(
    *, out_dir: Path, seed: int, figures_dir: Path, report_path: Path, params_path: Path
) -> None:
    """E121: Multiplicativity stress tests (random coprime pairs)."""
    params = ParamsE121()
    write_json(params_path, asdict(params))

    rng = np.random.default_rng(int(seed))
    sieve = _factor_sieve(params.n_max)
    mu = compute_mobius(params.n_max, sieve=sieve)
    phi = compute_phi(params.n_max, sieve=sieve)
    tau, sigma = compute_tau_sigma(params.n_max, sieve=sieve)
    omega = compute_omega(params.n_max, sieve=sieve)
    bigomega = compute_big_omega(params.n_max, sieve=sieve)

    def _gcd(a: int, b: int) -> int:
        while b:
            a, b = b, a % b
        return abs(a)

    failures: dict[str, int] = {
        "mu": 0,
        "phi": 0,
        "tau": 0,
        "sigma": 0,
        "omega_add": 0,
        "bigomega_add": 0,
    }
    tested = 0
    while tested < int(params.pairs):
        a = int(rng.integers(1, params.n_max + 1))
        b = int(rng.integers(1, params.n_max + 1))
        if _gcd(a, b) != 1:
            continue
        tested += 1
        ab = a * b
        if ab > params.n_max:
            continue
        # multiplicative: f(ab)=f(a)f(b) (or additive for omega counts)
        if mu[ab] != mu[a] * mu[b]:
            failures["mu"] += 1
        if phi[ab] != phi[a] * phi[b]:
            failures["phi"] += 1
        if tau[ab] != tau[a] * tau[b]:
            failures["tau"] += 1
        if sigma[ab] != sigma[a] * sigma[b]:
            failures["sigma"] += 1
        if omega[ab] != omega[a] + omega[b]:
            failures["omega_add"] += 1
        if bigomega[ab] != bigomega[a] + bigomega[b]:
            failures["bigomega_add"] += 1
    fig, ax = plt.subplots()
    keys = list(failures.keys())
    vals = [failures[k] for k in keys]
    ax.bar(np.arange(len(keys)), vals)
    ax.set_title("Multiplicativity failures on random coprime pairs")
    ax.set_xlabel("function")
    ax.set_ylabel("failure count")
    ax.set_xticks(np.arange(len(keys)), keys, rotation=25, ha="right")
    finalize_figure(fig)
    save_figure(out_dir=figures_dir, name="fig_01_multiplicativity_failures", fig=fig)
    plt.close(fig)

    lines: list[str] = []
    lines.append("# E121: Multiplicativity stress tests (random coprime pairs)")
    lines.append("")
    lines.append("## Artifacts")
    lines.append("- figures/fig_01_multiplicativity_failures.png")
    lines.append("- params.json")
    lines.append("- report.md")
    lines.append("")
    lines.append("### Notes")
    lines.append(f"- Tested coprime pairs (attempted): {int(params.pairs)}")
    lines.append(f"- Failure counts: {failures}")
    lines.append("- These should be 0 (within the sampled range and for coprime pairs).")
    _write_report(report_path=report_path, lines=lines)


@dataclass(frozen=True, slots=True)
class ParamsE122:
    """Parameters for E122.

    Args:
        side: Side length for the atlas grid (side^2 numbers).
    """

    side: int = 256


def run_e122(
    *, out_dir: Path, seed: int, figures_dir: Path, report_path: Path, params_path: Path
) -> None:
    """E122: Arithmetic function atlas: μ(n), ω(n), φ(n)/n heatmaps."""
    params = ParamsE122()
    write_json(params_path, asdict(params))

    side = int(params.side)
    n_max = side * side
    sieve = _factor_sieve(n_max)
    mu = np.asarray(compute_mobius(n_max, sieve=sieve)[1:], dtype=np.float64)
    omega = np.asarray(compute_omega(n_max, sieve=sieve)[1:], dtype=np.float64)
    phi = np.asarray(compute_phi(n_max, sieve=sieve)[1:], dtype=np.float64)
    n = np.arange(1, n_max + 1, dtype=np.float64)
    phi_ratio = phi / n
    mu_img = mu.reshape((side, side))
    omega_img = omega.reshape((side, side))
    phi_img = phi_ratio.reshape((side, side))
    fig, ax = plt.subplots()
    im = ax.imshow(mu_img, aspect="auto")
    fig.colorbar(im, ax=ax)
    ax.set_title("μ(n) atlas (row-major n)")
    ax.set_xlabel("col")
    ax.set_ylabel("row")
    finalize_figure(fig)
    save_figure(out_dir=figures_dir, name="fig_01_mu_atlas", fig=fig)
    plt.close(fig)
    fig, ax = plt.subplots()
    im = ax.imshow(omega_img, aspect="auto")
    fig.colorbar(im, ax=ax)
    ax.set_title("ω(n) atlas (row-major n)")
    ax.set_xlabel("col")
    ax.set_ylabel("row")
    finalize_figure(fig)
    save_figure(out_dir=figures_dir, name="fig_02_omega_atlas", fig=fig)
    plt.close(fig)
    fig, ax = plt.subplots()
    im = ax.imshow(phi_img, aspect="auto")
    fig.colorbar(im, ax=ax)
    ax.set_title("φ(n)/n atlas (row-major n)")
    ax.set_xlabel("col")
    ax.set_ylabel("row")
    finalize_figure(fig)
    save_figure(out_dir=figures_dir, name="fig_03_phi_ratio_atlas", fig=fig)
    plt.close(fig)

    lines: list[str] = []
    lines.append("# E122: Arithmetic function atlas: μ(n), ω(n), φ(n)/n heatmaps")
    lines.append("")
    lines.append("## Artifacts")
    lines.append("- figures/fig_01_mu_atlas.png")
    lines.append("- figures/fig_02_omega_atlas.png")
    lines.append("- figures/fig_03_phi_ratio_atlas.png")
    lines.append("- params.json")
    lines.append("- report.md")
    lines.append("")
    lines.append("### Notes")
    lines.append(
        f"- Atlas size: side={int(params.side)} => N={int(params.side) * int(params.side)}"
    )
    lines.append("- Visual textures encode multiplicativity and prime-power structure.")
    _write_report(report_path=report_path, lines=lines)


@dataclass(frozen=True, slots=True)
class ParamsE123:
    """Parameters for E123.

    Args:
        n_max: Upper bound N (inclusive).
        stride: Stride for sampling (increase to speed up).
    """

    n_max: int = 80_000
    stride: int = 1


def run_e123(
    *, out_dir: Path, seed: int, figures_dir: Path, report_path: Path, params_path: Path
) -> None:
    """E123: Correlation matrix: arithmetic functions on 1..N."""
    params = ParamsE123()
    write_json(params_path, asdict(params))

    sieve = _factor_sieve(params.n_max)
    n = np.arange(1, params.n_max + 1, int(params.stride), dtype=np.float64)
    n_int = n.astype(int)
    mu_full = compute_mobius(params.n_max, sieve=sieve)
    phi_full = compute_phi(params.n_max, sieve=sieve)
    tau_full, sigma_full = compute_tau_sigma(params.n_max, sieve=sieve)
    omega_full = compute_omega(params.n_max, sieve=sieve)
    bigomega_full = compute_big_omega(params.n_max, sieve=sieve)
    mu = np.asarray([mu_full[i] for i in n_int], dtype=np.float64)
    phi = np.asarray([phi_full[i] for i in n_int], dtype=np.float64) / n
    tau = np.asarray([tau_full[i] for i in n_int], dtype=np.float64)
    sigma = np.asarray([sigma_full[i] for i in n_int], dtype=np.float64) / n
    omega = np.asarray([omega_full[i] for i in n_int], dtype=np.float64)
    bigomega = np.asarray([bigomega_full[i] for i in n_int], dtype=np.float64)
    logn = np.log(n)
    data = np.vstack([logn, mu, phi, tau, sigma, omega, bigomega])
    names = ["log n", "mu", "phi/n", "tau", "sigma/n", "omega", "Omega"]
    corr = np.corrcoef(data)
    fig, ax = plt.subplots()
    im = ax.imshow(corr, vmin=-1.0, vmax=1.0)
    fig.colorbar(im, ax=ax)
    ax.set_xticks(np.arange(len(names)), names, rotation=30, ha="right")
    ax.set_yticks(np.arange(len(names)), names)
    ax.set_title("Correlation matrix (sampled)")
    finalize_figure(fig)
    save_figure(out_dir=figures_dir, name="fig_01_correlation_matrix", fig=fig)
    plt.close(fig)
    # list strongest correlations off-diagonal
    pairs: list[tuple[float, str, str]] = []
    for i in range(len(names)):
        for j in range(i + 1, len(names)):
            pairs.append((abs(float(corr[i, j])), names[i], names[j]))
    pairs.sort(reverse=True)
    top_pairs = [(a, b, round(v, 4)) for v, a, b in pairs[:8]]

    lines: list[str] = []
    lines.append("# E123: Correlation matrix: arithmetic functions on 1..N")
    lines.append("")
    lines.append("## Artifacts")
    lines.append("- figures/fig_01_correlation_matrix.png")
    lines.append("- params.json")
    lines.append("- report.md")
    lines.append("")
    lines.append("### Notes")
    lines.append(f"- Variables: {names}")
    lines.append(f"- Strongest |corr| pairs (name1, name2, |corr|): {top_pairs}")
    lines.append(
        "- Interpret cautiously: many variables are highly non-Gaussian and arithmetic in nature."
    )
    _write_report(report_path=report_path, lines=lines)
