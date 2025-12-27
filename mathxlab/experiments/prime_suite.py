"""Prime Numbers experiment suite (E014–E046).

Each experiment has:
- deterministic outputs (seed),
- a short report.md,
- one or more figures.

The individual experiment modules (e014_*.py, e015_*.py, ...) are thin wrappers
that call into this suite.

Notes:
- Default ranges are intentionally moderate so "make run EXP=e0xx" stays fast.
- Most experiments are written as *counterexample-style* demonstrations:
  "this tempting rule/heuristic fails in this way".

"""

from __future__ import annotations

import math
from dataclasses import asdict, dataclass
from pathlib import Path
from time import perf_counter

import matplotlib.figure as fig
import matplotlib.pyplot as plt
import numpy as np

from mathxlab.exp.io import save_figure, write_json
from mathxlab.plots.helpers import finalize_figure

from ._prime_utils import (
    MR_BASES_64BIT_12,
    factorize_pollard_rho,
    format_factor_multiset,
    is_prime_deterministic_64,
    is_probable_prime_miller_rabin,
    is_probable_prime_solovay_strassen,
    pi_array_from_mask,
    prime_mask_up_to,
    primes_up_to,
)


# ------------------------------------------------------------------------------
@dataclass(frozen=True, slots=True)
class CommonParams:
    """Shared parameters.

    Args:
        seed: Random seed.
        n_max: Upper bound for sieve-based experiments (inclusive).
    """

    seed: int
    n_max: int


# ------------------------------------------------------------------------------
def _write_lines(report_path: Path, lines: list[str]) -> None:
    """Write a report as Markdown lines."""
    report_path.write_text("\n".join(lines), encoding="utf-8")


def _basic_report_header(eid: str, title: str, reproduce_exp: str) -> list[str]:
    """Return standard report header lines."""
    return [
        f"# {eid.upper()} — {title}",
        "",
        "**Reproduce:**",
        "",
        "```bash",
        f"make run EXP={reproduce_exp}",
        "```",
        "",
    ]


def _plot_series(
    *, x: np.ndarray, ys: list[tuple[str, np.ndarray]], title: str, xlab: str, ylab: str
) -> fig.Figure:
    """Simple multi-line plot helper."""
    fig_obj, ax = plt.subplots()
    for label, y in ys:
        ax.plot(x, y, label=label)
    ax.set_title(title)
    ax.set_xlabel(xlab)
    ax.set_ylabel(ylab)
    ax.legend(loc="best")
    finalize_figure(fig_obj)
    return fig_obj


def _plot_scatter(*, x: np.ndarray, y: np.ndarray, title: str, xlab: str, ylab: str) -> fig.Figure:
    """Simple scatter plot helper."""
    fig_obj, ax = plt.subplots()
    ax.scatter(x, y, s=8)
    ax.set_title(title)
    ax.set_xlabel(xlab)
    ax.set_ylabel(ylab)
    finalize_figure(fig_obj)
    return fig_obj


@dataclass(frozen=True, slots=True)
class ParamsE014:
    """Parameters for E014.

    Args:
        k_max: Number of primorial steps.
    """

    k_max: int


def run_e014(
    *, out_dir: Path, seed: int, figures_dir: Path, report_path: Path, params_path: Path
) -> None:
    """E014 — Primorial ± 1: "Euclid numbers are prime" fails quickly."""
    params = ParamsE014(k_max=30)
    primes = primes_up_to(200)
    prim = 1
    k_list: list[int] = []
    a_plus: list[int] = []
    a_minus: list[int] = []
    plus_is_prime: list[int] = []
    minus_is_prime: list[int] = []

    for k in range(1, params.k_max + 1):
        p = int(primes[k - 1])
        prim *= p
        n_plus = prim + 1
        n_minus = prim - 1
        k_list.append(k)
        a_plus.append(n_plus)
        a_minus.append(n_minus)
        plus_is_prime.append(1 if is_prime_deterministic_64(n_plus) else 0)
        minus_is_prime.append(1 if is_prime_deterministic_64(n_minus) else 0)

    x = np.array(k_list, dtype=np.int64)
    fig1 = _plot_series(
        x=x,
        ys=[
            ("primorial(k)+1 prime?", np.array(plus_is_prime, dtype=np.int64)),
            ("primorial(k)-1 prime?", np.array(minus_is_prime, dtype=np.int64)),
        ],
        title="Primorial ± 1 primality (counterexample to naive 'always prime')",
        xlab="k",
        ylab="is prime",
    )
    save_figure(out_dir=figures_dir, name="fig_01_primorial_pm1_prime_indicator", fig=fig1)

    # Find first composites and factor them (rho)
    first_plus = next((k for k, ok in zip(k_list, plus_is_prime, strict=True) if ok == 0), None)
    first_minus = next((k for k, ok in zip(k_list, minus_is_prime, strict=True) if ok == 0), None)

    lines = _basic_report_header("E014", "Primorial ± 1 counterexamples", "e014")
    lines += [
        "## Parameters",
        f"- k_max: `{params.k_max}`",
        "",
        "## First composite examples",
        "",
    ]
    if first_plus is not None:
        n = a_plus[first_plus - 1]
        fac = format_factor_multiset(factorize_pollard_rho(n, seed=seed))
        lines += [f"- first composite primorial(k)+1 at k={first_plus}: `{n}` = {fac}"]
    if first_minus is not None:
        n = a_minus[first_minus - 1]
        fac = format_factor_multiset(factorize_pollard_rho(n, seed=seed))
        lines += [f"- first composite primorial(k)-1 at k={first_minus}: `{n}` = {fac}"]
    lines += [
        "",
        "## Notes",
        "- Euclid's proof uses the idea `P+1` (where P is a product of primes) to show *some* new prime exists.",
        "- It does **not** imply `P±1` is itself prime; composites appear very early.",
        "",
        "## Outputs",
        "- `figures/fig_01_primorial_pm1_prime_indicator.png`",
        "- `params.json`",
        "- `report.md`",
    ]
    _write_lines(report_path, lines)
    write_json(params_path, data=asdict(params))


@dataclass(frozen=True, slots=True)
class ParamsE015:
    """Parameters for E015.

    Args:
        n_values: Values of n to benchmark for Wilson-style factorial mod.
    """

    n_values: list[int]


def _wilson_factorial_mod(n: int) -> int:
    """Compute (n-1)! mod n by iterative multiplication."""
    acc = 1
    for k in range(2, n):
        acc = (acc * k) % n
    return acc


def run_e015(
    *, out_dir: Path, seed: int, figures_dir: Path, report_path: Path, params_path: Path
) -> None:
    """E015 — Wilson's theorem is true, but the naive 'test' is unusable at scale."""
    params = ParamsE015(n_values=[200, 400, 800, 1200, 1600, 2000, 2400])

    t_ms: list[float] = []
    for n in params.n_values:
        t0 = perf_counter()
        _ = _wilson_factorial_mod(n)
        t_ms.append((perf_counter() - t0) * 1000.0)

    x = np.array(params.n_values, dtype=np.int64)
    y = np.array(t_ms, dtype=np.float64)
    fig1 = _plot_series(
        x=x,
        ys=[("time (ms)", y)],
        title="Wilson factorial-mod runtime grows ~O(n)",
        xlab="n",
        ylab="milliseconds",
    )
    save_figure(out_dir=figures_dir, name="fig_01_wilson_runtime", fig=fig1)

    lines = _basic_report_header(
        "E015", "Wilson test infeasibility (runtime counterexample)", "e015"
    )
    lines += [
        "## Parameters",
        f"- n_values: `{params.n_values}`",
        "",
        "## Notes",
        "- Wilson's theorem says (n-1)! ≡ -1 (mod n) iff n is prime.",
        "- This is a beautiful characterization, but computing (n-1)! mod n is linear-time in n and becomes impractical fast.",
        "",
        "## Outputs",
        "- `figures/fig_01_wilson_runtime.png`",
        "- `params.json`",
        "- `report.md`",
    ]
    _write_lines(report_path, lines)
    write_json(params_path, data=asdict(params))


@dataclass(frozen=True, slots=True)
class ParamsE016:
    """Parameters for E016.

    Args:
        bit_sizes: Bit sizes to benchmark.
        samples_per_size: Samples per bit size.
    """

    bit_sizes: list[int]
    samples_per_size: int


def _trial_division_is_prime(n: int, primes: np.ndarray) -> bool:
    """Trial division primality test using a prime table."""
    if n < 2:
        return False
    if n % 2 == 0:
        return n == 2
    r = math.isqrt(n)
    for p in primes:
        p_i = int(p)
        if p_i > r:
            break
        if n % p_i == 0:
            return n == p_i
    return True


def run_e016(
    *, out_dir: Path, seed: int, figures_dir: Path, report_path: Path, params_path: Path
) -> None:
    """E016 — Trial division collapses with size; MR stays fast (counterexample to 'simple is fine')."""
    rng = np.random.default_rng(seed)
    params = ParamsE016(bit_sizes=[20, 24, 28, 32, 36], samples_per_size=200)

    # primes for trial division up to sqrt(max n)
    max_n = (1 << max(params.bit_sizes)) - 1
    primes = primes_up_to(math.isqrt(max_n) + 1)

    t_trial: list[float] = []
    t_mr: list[float] = []

    for b in params.bit_sizes:
        nums = rng.integers(
            low=1 << (b - 1), high=(1 << b) - 1, size=params.samples_per_size, dtype=np.int64
        )
        nums |= 1  # odd
        # Trial division time
        t0 = perf_counter()
        _ = [_trial_division_is_prime(int(n), primes) for n in nums]
        t_trial.append((perf_counter() - t0) * 1000.0)
        # MR time
        t0 = perf_counter()
        _ = [is_probable_prime_miller_rabin(int(n), (2, 3, 5, 7, 11)) for n in nums]
        t_mr.append((perf_counter() - t0) * 1000.0)

    x = np.array(params.bit_sizes, dtype=np.int64)
    fig1 = _plot_series(
        x=x,
        ys=[
            ("trial division (ms)", np.array(t_trial, dtype=np.float64)),
            ("Miller–Rabin (ms)", np.array(t_mr, dtype=np.float64)),
        ],
        title="Primality testing runtime vs bit-size",
        xlab="bit size",
        ylab="total time (ms) for batch",
    )
    save_figure(out_dir=figures_dir, name="fig_01_trial_vs_mr_runtime", fig=fig1)

    lines = _basic_report_header("E016", "Trial division vs Miller–Rabin scaling", "e016")
    lines += [
        "## Parameters",
        f"- bit_sizes: `{params.bit_sizes}`",
        f"- samples_per_size: `{params.samples_per_size}`",
        "",
        "## Notes",
        "- Trial division is fine for small n, but runtime grows quickly with sqrt(n).",
        "- Miller–Rabin stays fast and is the practical default for big integers.",
        "",
    ]
    _write_lines(report_path, lines)
    write_json(params_path, data=asdict(params))


@dataclass(frozen=True, slots=True)
class ParamsE017:
    """Parameters for E017.

    Args:
        n_values: N values to estimate sieve memory for.
        segment_size: Segment size for segmented sieve.
    """

    n_values: list[int]
    segment_size: int


def run_e017(
    *, out_dir: Path, seed: int, figures_dir: Path, report_path: Path, params_path: Path
) -> None:
    """E017 — Full sieve memory vs segmented sieve (counterexample to 'O(N) is fine')."""
    params = ParamsE017(
        n_values=[10**6, 5 * 10**6, 10**7, 5 * 10**7, 10**8], segment_size=2_000_000
    )

    # Rough memory model: 1 byte per bool in numpy (often 1 byte)
    bytes_per_entry = 1
    mem_full = np.array([n * bytes_per_entry for n in params.n_values], dtype=np.float64) / (
        1024.0**2
    )
    mem_segment = np.array(
        [params.segment_size * bytes_per_entry for _ in params.n_values], dtype=np.float64
    ) / (1024.0**2)

    x = np.array(params.n_values, dtype=np.float64)
    fig1 = _plot_series(
        x=x,
        ys=[
            ("full sieve MB", mem_full),
            ("segmented sieve MB (window)", mem_segment),
        ],
        title="Memory cost: full sieve vs segmented window (rough estimate)",
        xlab="N",
        ylab="MB",
    )
    save_figure(out_dir=figures_dir, name="fig_01_sieve_memory_estimate", fig=fig1)

    lines = _basic_report_header("E017", "Sieve memory blow-up vs segmented sieve", "e017")
    lines += [
        "## Parameters",
        f"- n_values: `{params.n_values}`",
        f"- segment_size: `{params.segment_size}`",
        "",
        "## Notes",
        "- A full sieve uses O(N) memory and can become the limiting factor.",
        "- A segmented sieve keeps memory roughly constant by processing windows [L, R].",
        "",
    ]
    _write_lines(report_path, lines)
    write_json(params_path, data=asdict(params))


@dataclass(frozen=True, slots=True)
class ParamsE018:
    """Parameters for E018.

    Args:
        n_max: Search range for pseudoprimes.
    """

    n_max: int


def run_e018(
    *, out_dir: Path, seed: int, figures_dir: Path, report_path: Path, params_path: Path
) -> None:
    """E018 — Strong pseudoprimes: too few MR bases yields false positives (counterexample)."""
    params = ParamsE018(n_max=500_000)

    is_prime = prime_mask_up_to(params.n_max)
    # Define composites that pass MR for base sets
    xs = np.arange(3, params.n_max + 1, dtype=np.int64)
    xs = xs[xs % 2 == 1]
    composite_mask = ~is_prime[xs]

    bases_sets = [
        ("base {2}", (2,)),
        ("bases {2,3}", (2, 3)),
        ("bases {2,3,5}", (2, 3, 5)),
        ("bases {2,3,5,7,11}", (2, 3, 5, 7, 11)),
    ]

    counts: list[np.ndarray] = []
    for _, bases in bases_sets:
        liar = np.array([is_probable_prime_miller_rabin(int(n), bases) for n in xs], dtype=bool)
        liar_composites = liar & composite_mask
        counts.append(np.cumsum(liar_composites.astype(np.int64)))

    x = xs.astype(np.int64)
    ys = [(label, c.astype(np.int64)) for (label, _), c in zip(bases_sets, counts, strict=True)]
    fig1 = _plot_series(
        x=x,
        ys=ys,
        title="Cumulative strong pseudoprimes (composites that pass MR)",
        xlab="n (odd)",
        ylab="count of MR liars up to n",
    )
    save_figure(out_dir=figures_dir, name="fig_01_mr_pseudoprime_counts", fig=fig1)

    lines = _basic_report_header("E018", "Miller–Rabin base choice counterexamples", "e018")
    lines += [
        "## Parameters",
        f"- n_max: `{params.n_max}`",
        "",
        "## Notes",
        "- Miller–Rabin is reliable when you use enough bases (or a deterministic base set for bounded ranges).",
        "- Using too few bases creates rare-but-real false positives (strong pseudoprimes).",
        "",
    ]
    _write_lines(report_path, lines)
    write_json(params_path, data=asdict(params))


@dataclass(frozen=True, slots=True)
class ParamsE019:
    """Parameters for E019.

    Args:
        n_max: Max x for pi(x).
    """

    n_max: int


def run_e019(
    *, out_dir: Path, seed: int, figures_dir: Path, report_path: Path, params_path: Path
) -> None:
    """E019 — Prime density: pi(x) vs x/log x and error curve."""
    params = ParamsE019(n_max=2_000_000)

    is_prime = prime_mask_up_to(params.n_max)
    pi = pi_array_from_mask(is_prime)

    x = np.arange(2, params.n_max + 1, dtype=np.int64)
    approx = x / np.log(x.astype(np.float64))
    err = pi[x].astype(np.float64) - approx

    fig1 = _plot_series(
        x=x,
        ys=[
            ("pi(x)", pi[x].astype(np.float64)),
            ("x/log x", approx),
        ],
        title="Prime counting vs x/log x",
        xlab="x",
        ylab="value",
    )
    save_figure(out_dir=figures_dir, name="fig_01_pi_vs_x_logx", fig=fig1)

    fig2 = _plot_series(
        x=x,
        ys=[("pi(x) - x/log x", err)],
        title="Approximation error: pi(x) - x/log x",
        xlab="x",
        ylab="error",
    )
    save_figure(out_dir=figures_dir, name="fig_02_pi_minus_x_logx", fig=fig2)

    lines = _basic_report_header("E019", "Prime density and PNT visualization", "e019")
    lines += [
        "## Parameters",
        f"- n_max: `{params.n_max}`",
        "",
        "## Notes",
        "- The Prime Number Theorem suggests pi(x) ~ x/log x.",
        "- The error curve shows the approximation improves overall but wiggles persist.",
        "",
    ]
    _write_lines(report_path, lines)
    write_json(params_path, data=asdict(params))


@dataclass(frozen=True, slots=True)
class ParamsE020:
    """Parameters for E020.

    Args:
        n_max: Max x.
        step: Step size for numerical integration.
    """

    n_max: int
    step: int


def _li_approx(n_max: int, step: int) -> tuple[np.ndarray, np.ndarray]:
    """Approximate li(x) on a coarse grid using trapezoidal rule."""
    xs = np.arange(2, n_max + 1, step, dtype=np.float64)
    # integrate 1/log t from 2 to x
    f = 1.0 / np.log(xs)
    li = np.zeros_like(xs)
    for i in range(1, xs.size):
        li[i] = li[i - 1] + 0.5 * (f[i - 1] + f[i]) * (xs[i] - xs[i - 1])
    return xs, li


def run_e020(
    *, out_dir: Path, seed: int, figures_dir: Path, report_path: Path, params_path: Path
) -> None:
    """E020 — li(x) is often a better approximation than x/log x (visual counterexample)."""
    params = ParamsE020(n_max=3_000_000, step=2000)

    is_prime = prime_mask_up_to(params.n_max)
    pi = pi_array_from_mask(is_prime)

    xs, li = _li_approx(params.n_max, params.step)
    xi = xs.astype(np.int64)
    pi_x = pi[xi].astype(np.float64)
    xlogx = xs / np.log(xs)

    fig1 = _plot_series(
        x=xs,
        ys=[
            ("pi(x)", pi_x),
            ("x/log x", xlogx),
            ("li(x) (numeric)", li),
        ],
        title="pi(x) vs approximations",
        xlab="x",
        ylab="value",
    )
    save_figure(out_dir=figures_dir, name="fig_01_pi_vs_li", fig=fig1)

    fig2 = _plot_series(
        x=xs,
        ys=[
            ("pi(x)-x/log x", pi_x - xlogx),
            ("pi(x)-li(x)", pi_x - li),
        ],
        title="Error comparison on coarse grid",
        xlab="x",
        ylab="error",
    )
    save_figure(out_dir=figures_dir, name="fig_02_error_comparison", fig=fig2)

    lines = _basic_report_header("E020", "Compare pi(x) to li(x) numerically", "e020")
    lines += [
        "## Parameters",
        f"- n_max: `{params.n_max}`",
        f"- step: `{params.step}`",
        "",
        "## Notes",
        "- li(x) is defined by an integral of 1/log t and often tracks pi(x) more closely than x/log x.",
        "- Here we use a coarse trapezoidal approximation (good enough for a visual experiment).",
        "",
    ]
    _write_lines(report_path, lines)
    write_json(params_path, data=asdict(params))


@dataclass(frozen=True, slots=True)
class ParamsE021:
    """Parameters for E021.

    Args:
        n_max: Upper bound.
    """

    n_max: int


def run_e021(
    *, out_dir: Path, seed: int, figures_dir: Path, report_path: Path, params_path: Path
) -> None:
    """E021 — Explicit inequality sanity checks (conditions matter)."""
    params = ParamsE021(n_max=2_000_000)

    is_prime = prime_mask_up_to(params.n_max)
    pi = pi_array_from_mask(is_prime)

    x = np.arange(17, params.n_max + 1, 1000, dtype=np.int64).astype(np.float64)
    pix = pi[x.astype(np.int64)].astype(np.float64)
    xlogx = x / np.log(x)
    upper = 1.25506 * xlogx  # classic explicit constant (range-conditional)
    # lower = xlogx  # simple lower comparison

    fig1 = _plot_series(
        x=x,
        ys=[
            ("pi(x)", pix),
            ("x/log x", xlogx),
            ("1.25506 x/log x", upper),
        ],
        title="Explicit inequality sanity check (coarse grid)",
        xlab="x",
        ylab="value",
    )
    save_figure(out_dir=figures_dir, name="fig_01_explicit_bound_sanity", fig=fig1)

    lines = _basic_report_header("E021", "Explicit bounds sanity checks", "e021")
    lines += [
        "## Parameters",
        f"- n_max: `{params.n_max}`",
        "",
        "## Notes",
        "- Many explicit inequalities for pi(x) have *starting points* (valid only for x ≥ x0).",
        "- Experiments should always verify the assumptions before using a bound as a 'test oracle'.",
        "",
    ]
    _write_lines(report_path, lines)
    write_json(params_path, data=asdict(params))


@dataclass(frozen=True, slots=True)
class ParamsE022:
    """Parameters for E022.

    Args:
        n_max: Upper bound.
    """

    n_max: int


def run_e022(
    *, out_dir: Path, seed: int, figures_dir: Path, report_path: Path, params_path: Path
) -> None:
    """E022 — Prime race: pi(x;4,1) vs pi(x;4,3)."""
    params = ParamsE022(n_max=5_000_000)
    primes = primes_up_to(params.n_max)
    p = primes[primes >= 3]
    a = np.cumsum((p % 4 == 1).astype(np.int64))
    b = np.cumsum((p % 4 == 3).astype(np.int64))
    diff = a - b
    x = p.astype(np.int64)

    fig1 = _plot_series(
        x=x,
        ys=[("pi(x;4,1) - pi(x;4,3)", diff.astype(np.int64))],
        title="Prime race bias (mod 4) on growing x",
        xlab="prime p (as x)",
        ylab="difference",
    )
    save_figure(out_dir=figures_dir, name="fig_01_prime_race_mod4", fig=fig1)

    lines = _basic_report_header("E022", "Prime race modulo 4", "e022")
    lines += [
        "## Parameters",
        f"- n_max: `{params.n_max}`",
        "",
        "## Notes",
        "- Dirichlet's theorem implies each residue class (1 and 3 mod 4) gets infinitely many primes.",
        "- Yet finite ranges show biases (the 'prime race' phenomenon).",
        "",
    ]
    _write_lines(report_path, lines)
    write_json(params_path, data=asdict(params))


@dataclass(frozen=True, slots=True)
class ParamsE023:
    """Parameters for E023.

    Args:
        n_max: Upper bound.
        q: Modulus.
    """

    n_max: int
    q: int


def run_e023(
    *, out_dir: Path, seed: int, figures_dir: Path, report_path: Path, params_path: Path
) -> None:
    """E023 — Distribution of primes across residue classes mod q (finite-range bias)."""
    params = ParamsE023(n_max=3_000_000, q=10)
    primes = primes_up_to(params.n_max)
    p = primes[primes >= 3]
    residues = sorted({r for r in range(params.q) if math.gcd(r, params.q) == 1})
    counts = []
    for r in residues:
        counts.append(np.cumsum((p % params.q == r).astype(np.int64)))
    x = p.astype(np.int64)

    ys = [(f"r={r}", c.astype(np.int64)) for r, c in zip(residues, counts, strict=True)]
    fig1 = _plot_series(
        x=x,
        ys=ys,
        title=f"Counts of primes in residue classes mod {params.q}",
        xlab="prime p (as x)",
        ylab="count",
    )
    save_figure(out_dir=figures_dir, name="fig_01_residue_class_counts", fig=fig1)

    lines = _basic_report_header("E023", f"Residue class distribution mod {params.q}", "e023")
    lines += [
        "## Parameters",
        f"- n_max: `{params.n_max}`",
        f"- q: `{params.q}`",
        "",
        "## Notes",
        "- In the limit, reduced residue classes should balance, but finite ranges can show visible drift.",
        "",
    ]
    _write_lines(report_path, lines)
    write_json(params_path, data=asdict(params))


@dataclass(frozen=True, slots=True)
class ParamsE024:
    """Parameters for E024.

    Args:
        size: Odd grid size (size x size).
    """

    size: int


def run_e024(
    *, out_dir: Path, seed: int, figures_dir: Path, report_path: Path, params_path: Path
) -> None:
    """E024 — Ulam spiral: primes in a spiral show diagonal structure."""
    params = ParamsE024(size=301)
    if params.size % 2 == 0:
        raise ValueError("size must be odd")

    n_max = params.size * params.size
    is_prime = prime_mask_up_to(n_max)

    grid = np.zeros((params.size, params.size), dtype=np.int64)
    x = y = params.size // 2
    grid[y, x] = 1

    step = 1
    value = 1
    while value < n_max:
        # right, up, left, down
        for dx, dy, reps in [(1, 0, step), (0, -1, step), (-1, 0, step + 1), (0, 1, step + 1)]:
            for _ in range(reps):
                if value >= n_max:
                    break
                x += dx
                y += dy
                value += 1
                grid[y, x] = value
        step += 2

    prime_img = is_prime[grid]
    fig_obj, ax = plt.subplots()
    ax.imshow(prime_img, interpolation="nearest")
    ax.set_title("Ulam spiral (primes = True)")
    ax.set_xlabel("x")
    ax.set_ylabel("y")
    finalize_figure(fig_obj)
    save_figure(out_dir=figures_dir, name="fig_01_ulam_spiral", fig=fig_obj)

    lines = _basic_report_header("E024", "Ulam spiral structure", "e024")
    lines += [
        "## Parameters",
        f"- size: `{params.size}`",
        "",
        "## Notes",
        "- Diagonal streaks correspond to quadratic polynomials that produce many primes for small n.",
        "- This is a visual 'pattern trap': structure is real, but it does not imply a simple rule for primes.",
        "",
    ]
    _write_lines(report_path, lines)
    write_json(params_path, data=asdict(params))


@dataclass(frozen=True, slots=True)
class ParamsE025:
    """Parameters for E025.

    Args:
        n_max: Upper bound.
    """

    n_max: int


def run_e025(
    *, out_dir: Path, seed: int, figures_dir: Path, report_path: Path, params_path: Path
) -> None:
    """E025 — Prime gaps are not monotone (counterexample to naive 'gaps always grow')."""
    params = ParamsE025(n_max=2_000_000)
    primes = primes_up_to(params.n_max)
    gaps = primes[1:] - primes[:-1]
    idx = np.arange(1, gaps.size + 1, dtype=np.int64)

    fig1 = _plot_series(
        x=idx,
        ys=[("gap", gaps.astype(np.int64))],
        title="Prime gaps vs index (shows strong non-monotonicity)",
        xlab="n (gap index)",
        ylab="p_{n+1}-p_n",
    )
    save_figure(out_dir=figures_dir, name="fig_01_prime_gaps", fig=fig1)

    lines = _basic_report_header("E025", "Prime gaps are not monotone", "e025")
    lines += [
        "## Parameters",
        f"- n_max: `{params.n_max}`",
        "",
        "## Notes",
        "- Even though the *typical* gap near x is about log x, gaps fluctuate wildly.",
        "- This plot is a quick antidote to monotonic thinking.",
        "",
    ]
    _write_lines(report_path, lines)
    write_json(params_path, data=asdict(params))


@dataclass(frozen=True, slots=True)
class ParamsE026:
    """Parameters for E026.

    Args:
        n_max: Upper bound.
        bins: Histogram bins.
    """

    n_max: int
    bins: int


def run_e026(
    *, out_dir: Path, seed: int, figures_dir: Path, report_path: Path, params_path: Path
) -> None:
    """E026 — Gap normalization: g/log p helps compare scales."""
    params = ParamsE026(n_max=5_000_000, bins=60)
    primes = primes_up_to(params.n_max)
    gaps = primes[1:] - primes[:-1]
    denom = np.log(primes[:-1].astype(np.float64))
    gnorm = gaps.astype(np.float64) / denom

    fig_obj, ax = plt.subplots()
    ax.hist(gnorm, bins=params.bins)
    ax.set_title("Histogram of normalized prime gaps g/log p")
    ax.set_xlabel("g / log p")
    ax.set_ylabel("count")
    finalize_figure(fig_obj)
    save_figure(out_dir=figures_dir, name="fig_01_gap_normalized_hist", fig=fig_obj)

    lines = _basic_report_header("E026", "Normalized prime gaps", "e026")
    lines += [
        "## Parameters",
        f"- n_max: `{params.n_max}`",
        f"- bins: `{params.bins}`",
        "",
        "## Notes",
        "- Normalization lets you compare gap statistics across different magnitudes of p.",
        "",
    ]
    _write_lines(report_path, lines)
    write_json(params_path, data=asdict(params))


@dataclass(frozen=True, slots=True)
class ParamsE027:
    """Parameters for E027.

    Args:
        n_max: Upper bound.
    """

    n_max: int


def run_e027(
    *, out_dir: Path, seed: int, figures_dir: Path, report_path: Path, params_path: Path
) -> None:
    """E027 — Record prime gaps vs log^2 heuristic (Cramér-style scaling)."""
    params = ParamsE027(n_max=20_000_000)
    primes = primes_up_to(params.n_max)
    gaps = primes[1:] - primes[:-1]

    record_gap: list[int] = []
    record_p: list[int] = []
    best = 0
    for p, g in zip(primes[:-1], gaps, strict=True):
        gi = int(g)
        if gi > best:
            best = gi
            record_gap.append(best)
            record_p.append(int(p))

    p_arr = np.array(record_p, dtype=np.float64)
    g_arr = np.array(record_gap, dtype=np.float64)
    heuristic = np.log(p_arr) ** 2

    fig1 = _plot_series(
        x=p_arr,
        ys=[("record gap", g_arr), ("log(p)^2", heuristic)],
        title="Record gaps vs log^2(p) heuristic",
        xlab="p (where record occurs)",
        ylab="gap size",
    )
    save_figure(out_dir=figures_dir, name="fig_01_record_gaps_vs_log2", fig=fig1)

    lines = _basic_report_header("E027", "Record prime gaps vs log^2 heuristic", "e027")
    lines += [
        "## Parameters",
        f"- n_max: `{params.n_max}`",
        "",
        "## Notes",
        "- Cramér-style heuristics suggest maximal gaps around x scale like O(log^2 x).",
        "- This experiment is empirical: we compare record gaps to log^2(p) on a finite range.",
        "",
    ]
    _write_lines(report_path, lines)
    write_json(params_path, data=asdict(params))


@dataclass(frozen=True, slots=True)
class ParamsE028:
    """Parameters for E028.

    Args:
        n_max: Upper bound.
        window: Number of consecutive gaps per window.
        step: Window step.
    """

    n_max: int
    window: int
    step: int


def run_e028(
    *, out_dir: Path, seed: int, figures_dir: Path, report_path: Path, params_path: Path
) -> None:
    """E028 — Jumping champions: most frequent gap in sliding windows."""
    params = ParamsE028(n_max=10_000_000, window=200_000, step=100_000)
    primes = primes_up_to(params.n_max)
    gaps = (primes[1:] - primes[:-1]).astype(np.int64)

    champions: list[int] = []
    positions: list[int] = []

    for start in range(0, max(1, gaps.size - params.window), params.step):
        chunk = gaps[start : start + params.window]
        if chunk.size == 0:
            break
        vals, counts = np.unique(chunk, return_counts=True)
        champ = int(vals[int(np.argmax(counts))])
        champions.append(champ)
        positions.append(int(primes[min(start + params.window, primes.size - 1)]))

    x = np.array(positions, dtype=np.int64)
    y = np.array(champions, dtype=np.int64)
    fig1 = _plot_series(
        x=x,
        ys=[("jumping champion gap", y)],
        title="Jumping champion (most frequent gap) vs x (windowed)",
        xlab="x (approx window end prime)",
        ylab="gap",
    )
    save_figure(out_dir=figures_dir, name="fig_01_jumping_champion", fig=fig1)

    lines = _basic_report_header("E028", "Jumping champions (most frequent gaps)", "e028")
    lines += [
        "## Parameters",
        f"- n_max: `{params.n_max}`",
        f"- window: `{params.window}` gaps",
        f"- step: `{params.step}` gaps",
        "",
        "## Notes",
        "- The most frequent gap tends to be a small primorial-related number (often 6 for quite a while).",
        "- This is a fun example of 'typical behavior' that changes slowly with scale.",
        "",
    ]
    _write_lines(report_path, lines)
    write_json(params_path, data=asdict(params))


@dataclass(frozen=True, slots=True)
class ParamsE029:
    """Parameters for E029.

    Args:
        n_max: Upper bound.
    """

    n_max: int


def run_e029(
    *, out_dir: Path, seed: int, figures_dir: Path, report_path: Path, params_path: Path
) -> None:
    """E029 — Twin prime counts vs simple Hardy–Littlewood-style heuristic."""
    params = ParamsE029(n_max=10_000_000)
    primes = primes_up_to(params.n_max)
    # prime_set = {int(p) for p in primes.tolist()}

    xs = np.arange(100_000, params.n_max + 1, 200_000, dtype=np.int64)
    counts: list[int] = []
    heur: list[float] = []

    C2 = 0.6601618158468696  # twin prime constant (approx)
    for x in xs:
        # Count twin primes with p <= x, p+2 prime
        # Use primes list prefix for speed
        ps = primes[primes <= x]
        c = int(np.sum(np.isin(ps + 2, ps)))
        counts.append(c)
        heur.append(float(2.0 * C2 * x / (math.log(float(x)) ** 2)))

    fig1 = _plot_series(
        x=xs.astype(np.float64),
        ys=[
            ("observed twins", np.array(counts, dtype=np.float64)),
            ("heuristic ~ 2C2 x/log^2 x", np.array(heur)),
        ],
        title="Twin prime counts vs heuristic",
        xlab="x",
        ylab="count",
    )
    save_figure(out_dir=figures_dir, name="fig_01_twin_count_vs_heuristic", fig=fig1)

    lines = _basic_report_header("E029", "Twin primes: observed vs heuristic", "e029")
    lines += [
        "## Parameters",
        f"- n_max: `{params.n_max}`",
        "",
        "## Notes",
        "- The heuristic curve is not a theorem; it's an asymptotic guess from prime k-tuple heuristics.",
        "- The point is to compare shapes and scaling, not to expect perfect agreement at small x.",
        "",
    ]
    _write_lines(report_path, lines)
    write_json(params_path, data=asdict(params))


@dataclass(frozen=True, slots=True)
class ParamsE030:
    """Parameters for E030.

    Args:
        n_max: Upper bound.
        d_values: Differences to count (e.g., 4 and 6).
    """

    n_max: int
    d_values: list[int]


def run_e030(
    *, out_dir: Path, seed: int, figures_dir: Path, report_path: Path, params_path: Path
) -> None:
    """E030 — Cousin and sexy primes: compare counts of prime pairs."""
    params = ParamsE030(n_max=10_000_000, d_values=[4, 6])
    primes = primes_up_to(params.n_max)
    ps = primes.astype(np.int64)

    xs = np.arange(200_000, params.n_max + 1, 200_000, dtype=np.int64)
    curves: list[tuple[str, np.ndarray]] = []

    for d in params.d_values:
        counts: list[int] = []
        for x in xs:
            pfx = ps[ps <= x]
            counts.append(int(np.sum(np.isin(pfx + d, pfx))))
        curves.append((f"pairs with d={d}", np.array(counts, dtype=np.int64)))

    fig1 = _plot_series(
        x=xs.astype(np.float64),
        ys=[(label, y.astype(np.float64)) for label, y in curves],
        title="Counts of prime pairs (cousin d=4, sexy d=6)",
        xlab="x",
        ylab="count",
    )
    save_figure(out_dir=figures_dir, name="fig_01_cousin_sexy_counts", fig=fig1)

    lines = _basic_report_header("E030", "Cousin and sexy prime pairs", "e030")
    lines += [
        "## Parameters",
        f"- n_max: `{params.n_max}`",
        f"- d_values: `{params.d_values}`",
        "",
        "## Notes",
        "- Prime pairs with fixed even gap d are all instances of prime constellations.",
        "- Different d values have different 'local obstructions' (mod constraints) and different constants.",
        "",
    ]
    _write_lines(report_path, lines)
    write_json(params_path, data=asdict(params))


@dataclass(frozen=True, slots=True)
class ParamsE031:
    """Parameters for E031.

    Args:
        max_mod: Check admissibility against primes up to this modulus.
    """

    max_mod: int


def _is_admissible(offsets: list[int], primes_small: list[int]) -> bool:
    """Check admissibility by ensuring no modulus p is fully covered."""
    for p in primes_small:
        residues = {(o % p) for o in offsets}
        if len(residues) == p:
            return False
    return True


def run_e031(
    *, out_dir: Path, seed: int, figures_dir: Path, report_path: Path, params_path: Path
) -> None:
    """E031 — Prime k-tuple admissibility: mod obstructions are real counterexamples."""
    params = ParamsE031(max_mod=29)
    primes_small = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29]

    patterns = [
        ("twin {0,2}", [0, 2]),
        ("cousin {0,4}", [0, 4]),
        ("sexy {0,6}", [0, 6]),
        ("bad triple {0,2,4}", [0, 2, 4]),  # covers mod 3
        ("prime triplet {0,2,6}", [0, 2, 6]),
        ("prime quadruplet {0,2,6,8}", [0, 2, 6, 8]),
    ]

    admissible = [1 if _is_admissible(offs, primes_small) else 0 for _, offs in patterns]
    x = np.arange(len(patterns), dtype=np.int64)

    fig_obj, ax = plt.subplots()
    ax.bar(x, np.array(admissible, dtype=np.int64))
    ax.set_title("Admissibility of small prime constellations")
    ax.set_xlabel("pattern index")
    ax.set_ylabel("admissible? (1=yes, 0=no)")
    ax.set_xticks(x)
    ax.set_xticklabels([name for name, _ in patterns], rotation=15, ha="right")
    finalize_figure(fig_obj)
    save_figure(out_dir=figures_dir, name="fig_01_admissibility", fig=fig_obj)

    lines = _basic_report_header("E031", "Admissibility and modular obstructions", "e031")
    lines += [
        "## Parameters",
        f"- max_mod: `{params.max_mod}`",
        "",
        "## Results",
    ]
    for (name, _offs), ok in zip(patterns, admissible, strict=True):
        lines.append(f"- {name}: {'admissible' if ok else 'NOT admissible'}")
    lines += [
        "",
        "## Notes",
        "- A pattern must be admissible (no modulus p blocks it completely) to have any chance of occurring infinitely often.",
        "- This is a crisp 'counterexample filter' for naive prime-pattern claims.",
        "",
    ]
    _write_lines(report_path, lines)
    write_json(params_path, data=asdict(params))


@dataclass(frozen=True, slots=True)
class ParamsE032:
    """Parameters for E032.

    Args:
        n_max: Upper bound.
    """

    n_max: int


def run_e032(
    *, out_dir: Path, seed: int, figures_dir: Path, report_path: Path, params_path: Path
) -> None:
    """E032 — Count small prime constellations (triplets/quadruplets) up to N."""
    params = ParamsE032(n_max=10_000_000)
    primes = primes_up_to(params.n_max)
    p = primes.astype(np.int64)
    prime_set = {int(v) for v in p.tolist()}

    patterns = {
        "triplet {0,2,6}": [0, 2, 6],
        "triplet {0,4,6}": [0, 4, 6],
        "quadruplet {0,2,6,8}": [0, 2, 6, 8],
    }

    xs = np.arange(500_000, params.n_max + 1, 500_000, dtype=np.int64)
    ys: list[tuple[str, np.ndarray]] = []
    for name, offs in patterns.items():
        counts: list[int] = []
        for x in xs:
            ps = p[p <= x]
            c = 0
            for pp in ps:
                ok = True
                for o in offs:
                    if int(pp + o) not in prime_set:
                        ok = False
                        break
                if ok:
                    c += 1
            counts.append(c)
        ys.append((name, np.array(counts, dtype=np.int64)))

    fig1 = _plot_series(
        x=xs.astype(np.float64),
        ys=[(name, arr.astype(np.float64)) for name, arr in ys],
        title="Counts of small prime constellations (finite range)",
        xlab="x",
        ylab="count",
    )
    save_figure(out_dir=figures_dir, name="fig_01_constellation_counts", fig=fig1)

    lines = _basic_report_header("E032", "Prime triplets and quadruplets", "e032")
    lines += [
        "## Parameters",
        f"- n_max: `{params.n_max}`",
        "",
        "## Notes",
        "- These patterns are rare; counts grow slowly.",
        "- The plot helps compare how quickly different constellations appear in the same range.",
        "",
    ]
    _write_lines(report_path, lines)
    write_json(params_path, data=asdict(params))


@dataclass(frozen=True, slots=True)
class ParamsE033:
    """Parameters for E033.

    Args:
        n_max: Upper bound.
        threshold: Gap threshold.
    """

    n_max: int
    threshold: int


def run_e033(
    *, out_dir: Path, seed: int, figures_dir: Path, report_path: Path, params_path: Path
) -> None:
    """E033 — Small gaps exist often, but that doesn't make them twins (data-only counterexample)."""
    params = ParamsE033(n_max=10_000_000, threshold=100)
    primes = primes_up_to(params.n_max)
    gaps = (primes[1:] - primes[:-1]).astype(np.int64)

    idx = np.arange(1, gaps.size + 1, dtype=np.int64)
    small = np.cumsum((gaps <= params.threshold).astype(np.int64))
    twins = np.cumsum((gaps == 2).astype(np.int64))

    fig1 = _plot_series(
        x=idx,
        ys=[
            (f"gaps <= {params.threshold}", small.astype(np.int64)),
            ("twin gaps (==2)", twins.astype(np.int64)),
        ],
        title="Cumulative counts: 'bounded gaps' vs twins",
        xlab="gap index",
        ylab="cumulative count",
    )
    save_figure(out_dir=figures_dir, name="fig_01_bounded_vs_twins", fig=fig1)

    lines = _basic_report_header("E033", "Bounded gaps vs twin primes (not the same)", "e033")
    lines += [
        "## Parameters",
        f"- n_max: `{params.n_max}`",
        f"- threshold: `{params.threshold}`",
        "",
        "## Notes",
        "- Seeing many small gaps does not imply the smallest gap (2) occurs infinitely often.",
        "- This is not a proof statement, just a numerical 'intuition guardrail'.",
        "",
    ]
    _write_lines(report_path, lines)
    write_json(params_path, data=asdict(params))


@dataclass(frozen=True, slots=True)
class ParamsE034:
    """Parameters for E034.

    Args:
        n_max: Upper bound.
        window: Window length.
        step: Step.
    """

    n_max: int
    window: int
    step: int


def run_e034(
    *, out_dir: Path, seed: int, figures_dir: Path, report_path: Path, params_path: Path
) -> None:
    """E034 — Twin prime counts vary strongly across windows (variance counterexample)."""
    params = ParamsE034(n_max=10_000_000, window=500_000, step=200_000)
    primes = primes_up_to(params.n_max).astype(np.int64)
    # prime_set = {int(p) for p in primes.tolist()}

    xs: list[int] = []
    ys: list[int] = []
    for L in range(2, params.n_max - params.window, params.step):
        R = L + params.window
        ps = primes[(primes >= L) & (primes <= R)]
        c = int(np.sum(np.isin(ps + 2, ps)))
        xs.append(R)
        ys.append(c)

    fig1 = _plot_series(
        x=np.array(xs, dtype=np.int64),
        ys=[("twin count in window", np.array(ys, dtype=np.int64))],
        title="Twin primes in sliding windows (shows variance)",
        xlab="window end R",
        ylab="count",
    )
    save_figure(out_dir=figures_dir, name="fig_01_twin_window_variance", fig=fig1)

    lines = _basic_report_header("E034", "Twin primes in sliding windows", "e034")
    lines += [
        "## Parameters",
        f"- n_max: `{params.n_max}`",
        f"- window: `{params.window}`",
        f"- step: `{params.step}`",
        "",
        "## Notes",
        "- Even if a heuristic gives an average density, local counts in windows vary a lot.",
        "- This is a counterexample to 'smoothness' assumptions when eyeballing primes.",
        "",
    ]
    _write_lines(report_path, lines)
    write_json(params_path, data=asdict(params))


@dataclass(frozen=True, slots=True)
class ParamsE035:
    """Parameters for E035.

    Args:
        n_max: Upper bound.
        q: Modulus.
    """

    n_max: int
    q: int


def run_e035(
    *, out_dir: Path, seed: int, figures_dir: Path, report_path: Path, params_path: Path
) -> None:
    """E035 — Primes in arithmetic progressions: empirical counts in reduced residues."""
    params = ParamsE035(n_max=10_000_000, q=12)
    primes = primes_up_to(params.n_max).astype(np.int64)
    p = primes[primes >= 5]
    residues = [r for r in range(params.q) if math.gcd(r, params.q) == 1]

    xs = np.arange(200_000, params.n_max + 1, 200_000, dtype=np.int64)
    ys: list[tuple[str, np.ndarray]] = []

    for r in residues:
        counts: list[int] = []
        for x in xs:
            ps = p[p <= x]
            counts.append(int(np.sum(ps % params.q == r)))
        ys.append((f"r={r}", np.array(counts, dtype=np.int64)))

    fig1 = _plot_series(
        x=xs.astype(np.float64),
        ys=[(label, arr.astype(np.float64)) for label, arr in ys],
        title=f"Prime counts in residue classes mod {params.q}",
        xlab="x",
        ylab="count",
    )
    save_figure(out_dir=figures_dir, name="fig_01_primes_in_ap_counts", fig=fig1)

    lines = _basic_report_header(
        "E035", f"Primes in arithmetic progressions mod {params.q}", "e035"
    )
    lines += [
        "## Parameters",
        f"- n_max: `{params.n_max}`",
        f"- q: `{params.q}`",
        "",
        "## Notes",
        "- Dirichlet's theorem guarantees infinitely many primes in each reduced residue class.",
        "- Finite ranges show biases and slow convergence to equal proportions.",
        "",
    ]
    _write_lines(report_path, lines)
    write_json(params_path, data=asdict(params))


@dataclass(frozen=True, slots=True)
class ParamsE036:
    """Parameters for E036.

    Args:
        n_max: Upper bound.
        max_d: Max step d to search.
    """

    n_max: int
    max_d: int


def run_e036(
    *, out_dir: Path, seed: int, figures_dir: Path, report_path: Path, params_path: Path
) -> None:
    """E036 — Small arithmetic progressions of primes (3-term and 4-term) in ranges."""
    params = ParamsE036(n_max=2_000_000, max_d=5_000)
    primes = primes_up_to(params.n_max).astype(np.int64)
    prime_set = {int(p) for p in primes.tolist()}

    found3: list[tuple[int, int, int]] = []
    found4: list[tuple[int, int, int, int]] = []

    # Search over starting prime p and steps d (small)
    for p in primes:
        p_i = int(p)
        for d in range(2, params.max_d + 1, 2):
            if p_i + 2 * d > params.n_max:
                break
            if (p_i + d) in prime_set and (p_i + 2 * d) in prime_set:
                found3.append((p_i, p_i + d, p_i + 2 * d))
                if (p_i + 3 * d) in prime_set:
                    found4.append((p_i, p_i + d, p_i + 2 * d, p_i + 3 * d))
        if len(found3) > 5000 and len(found4) > 2000:
            break

    # Plot counts of found progressions by maximum term
    ends3 = np.array([t[2] for t in found3], dtype=np.int64)
    ends4 = np.array([t[3] for t in found4], dtype=np.int64)

    xs = np.arange(50_000, params.n_max + 1, 50_000, dtype=np.int64)
    c3 = np.array([int(np.sum(ends3 <= x)) for x in xs], dtype=np.int64)
    c4 = np.array([int(np.sum(ends4 <= x)) for x in xs], dtype=np.int64)

    fig1 = _plot_series(
        x=xs.astype(np.float64),
        ys=[
            ("3-term APs found", c3.astype(np.float64)),
            ("4-term APs found", c4.astype(np.float64)),
        ],
        title="Cumulative count of small prime arithmetic progressions found",
        xlab="max term",
        ylab="count",
    )
    save_figure(out_dir=figures_dir, name="fig_01_prime_ap_counts", fig=fig1)

    lines = _basic_report_header("E036", "Prime arithmetic progressions (small search)", "e036")
    lines += [
        "## Parameters",
        f"- n_max: `{params.n_max}`",
        f"- max_d: `{params.max_d}`",
        "",
        "## Notes",
        "- This is a finite search for short APs, not a proof of existence for arbitrary lengths.",
        "- Even small ranges contain many 3-term APs; 4-term APs are rarer but still appear.",
        "",
        "## Sample progressions",
        "",
        f"- 3-term examples: `{found3[:5]}`",
        f"- 4-term examples: `{found4[:5]}`",
        "",
    ]
    _write_lines(report_path, lines)
    write_json(params_path, data=asdict(params))


@dataclass(frozen=True, slots=True)
class ParamsE037:
    """Parameters for E037.

    Args:
        n_values: Values of n to demonstrate prime-free runs of length n-1.
    """

    n_values: list[int]


def run_e037(
    *, out_dir: Path, seed: int, figures_dir: Path, report_path: Path, params_path: Path
) -> None:
    """E037 — Prime-free intervals exist: n!+2,...,n!+n are all composite."""
    params = ParamsE037(n_values=[10, 20, 30, 40, 50, 60, 80])

    lengths: list[int] = []
    for n in params.n_values:
        base = math.factorial(n)
        ok = True
        for k in range(2, n + 1):
            if is_prime_deterministic_64(base + k):
                ok = False
                break
        lengths.append((n - 1) if ok else 0)

    x = np.array(params.n_values, dtype=np.int64)
    y = np.array(lengths, dtype=np.int64)
    fig1 = _plot_series(
        x=x,
        ys=[("verified prime-free length", y)],
        title="Constructed prime-free intervals from factorial trick",
        xlab="n",
        ylab="length (n-1)",
    )
    save_figure(out_dir=figures_dir, name="fig_01_prime_free_factorial", fig=fig1)

    lines = _basic_report_header("E037", "Prime-free intervals via factorial construction", "e037")
    lines += [
        "## Parameters",
        f"- n_values: `{params.n_values}`",
        "",
        "## Notes",
        "- For each n, the numbers n!+2, n!+3, ..., n!+n are divisible by 2,3,...,n respectively.",
        "- This provides explicit long runs of composites (a counterexample to 'primes appear regularly').",
        "",
    ]
    _write_lines(report_path, lines)
    write_json(params_path, data=asdict(params))


@dataclass(frozen=True, slots=True)
class ParamsE038:
    """Parameters for E038.

    Args:
        n_max: Check Bertrand postulate for n up to n_max.
    """

    n_max: int


def run_e038(
    *, out_dir: Path, seed: int, figures_dir: Path, report_path: Path, params_path: Path
) -> None:
    """E038 — Bertrand's postulate: for n>1 there is a prime in (n, 2n)."""
    params = ParamsE038(n_max=500_000)
    is_prime = prime_mask_up_to(2 * params.n_max + 10)
    pi = pi_array_from_mask(is_prime)

    ns = np.arange(2, params.n_max + 1, 1000, dtype=np.int64)
    has_prime = np.array([(pi[2 * n] - pi[n]) > 0 for n in ns], dtype=np.int64)

    fig1 = _plot_series(
        x=ns,
        ys=[("indicator", has_prime)],
        title="Bertrand postulate indicator on a coarse grid (should be all 1s)",
        xlab="n",
        ylab="exists prime in (n,2n)?",
    )
    save_figure(out_dir=figures_dir, name="fig_01_bertrand_indicator", fig=fig1)

    lines = _basic_report_header(
        "E038", "Bertrand's postulate (computational verification)", "e038"
    )
    lines += [
        "## Parameters",
        f"- n_max: `{params.n_max}`",
        "",
        "## Notes",
        "- Bertrand's postulate is a theorem; this experiment is a quick computational sanity check.",
        "- It's also a useful 'prime existence oracle' for constructing examples.",
        "",
    ]
    _write_lines(report_path, lines)
    write_json(params_path, data=asdict(params))


@dataclass(frozen=True, slots=True)
class ParamsE039:
    """Parameters for E039.

    Args:
        n_max: Upper bound for p.
    """

    n_max: int


def run_e039(
    *, out_dir: Path, seed: int, figures_dir: Path, report_path: Path, params_path: Path
) -> None:
    """E039 — Sophie Germain primes and safe primes (counts in range)."""
    params = ParamsE039(n_max=5_000_000)
    primes = primes_up_to(params.n_max).astype(np.int64)
    prime_set = {int(p) for p in primes.tolist()}

    xs = np.arange(200_000, params.n_max + 1, 200_000, dtype=np.int64)
    sg_counts: list[int] = []
    safe_counts: list[int] = []

    for x in xs:
        ps = primes[primes <= x]
        sg = 0
        safe = 0
        for p in ps:
            q = int(2 * p + 1)
            if q <= 2 * params.n_max and is_prime_deterministic_64(q):
                sg += 1
        # safe primes q where (q-1)/2 is prime: count q in [..] by scanning ps as q
        for q in ps:
            if ((q - 1) // 2) in prime_set:
                safe += 1
        sg_counts.append(sg)
        safe_counts.append(safe)

    fig1 = _plot_series(
        x=xs.astype(np.float64),
        ys=[
            ("Sophie Germain primes p (2p+1 prime)", np.array(sg_counts, dtype=np.float64)),
            ("safe primes q ((q-1)/2 prime)", np.array(safe_counts, dtype=np.float64)),
        ],
        title="Counts of related prime families",
        xlab="x",
        ylab="count up to x",
    )
    save_figure(out_dir=figures_dir, name="fig_01_sg_safe_counts", fig=fig1)

    lines = _basic_report_header("E039", "Sophie Germain and safe primes", "e039")
    lines += [
        "## Parameters",
        f"- n_max: `{params.n_max}`",
        "",
        "## Notes",
        "- These prime families matter in cryptography and in prime pattern heuristics.",
        "- Counts grow slowly; local fluctuations are visible at moderate x.",
        "",
    ]
    _write_lines(report_path, lines)
    write_json(params_path, data=asdict(params))


@dataclass(frozen=True, slots=True)
class ParamsE040:
    """Parameters for E040.

    Args:
        digits_max: Max digits to scan palindromes.
        limit: Stop scanning after this many palindromes.
    """

    digits_max: int
    limit: int


def _make_palindrome(x: int, even: bool) -> int:
    """Create a palindrome from x."""
    s = str(x)
    t = s + (s[::-1] if even else s[-2::-1])
    return int(t)


def run_e040(
    *, out_dir: Path, seed: int, figures_dir: Path, report_path: Path, params_path: Path
) -> None:
    """E040 — Palindromic primes: even-length palindromes are divisible by 11 (counterexample)."""
    params = ParamsE040(digits_max=10, limit=50_000)

    even_len_pal: list[int] = []
    even_len_prime: list[int] = []

    odd_len_pal: list[int] = []
    odd_len_prime: list[int] = []

    count = 0
    x = 1
    while count < params.limit:
        pal_even = _make_palindrome(x, even=True)
        pal_odd = _make_palindrome(x, even=False)
        even_len_pal.append(pal_even)
        odd_len_pal.append(pal_odd)
        even_len_prime.append(1 if is_prime_deterministic_64(pal_even) else 0)
        odd_len_prime.append(1 if is_prime_deterministic_64(pal_odd) else 0)
        x += 1
        count += 1

    idx = np.arange(1, len(even_len_pal) + 1, dtype=np.int64)
    fig1 = _plot_series(
        x=idx,
        ys=[
            ("even-length pal prime?", np.array(even_len_prime, dtype=np.int64)),
            ("odd-length pal prime?", np.array(odd_len_prime, dtype=np.int64)),
        ],
        title="Palindrome primality indicator (even-length are almost never prime)",
        xlab="index",
        ylab="is prime",
    )
    save_figure(out_dir=figures_dir, name="fig_01_palindrome_prime_indicator", fig=fig1)

    # Find the only common even-length palindromic prime (should be 11)
    candidates = [p for p, ok in zip(even_len_pal, even_len_prime, strict=True) if ok == 1]
    lines = _basic_report_header("E040", "Palindromic primes and the '11 trap'", "e040")
    lines += [
        "## Parameters",
        f"- digits_max: `{params.digits_max}`",
        f"- limit: `{params.limit}`",
        "",
        "## Notes",
        "- Every even-length base-10 palindrome is divisible by 11, hence composite (except 11 itself).",
        f"- Even-length palindromic primes found in this scan: `{candidates[:10]}`",
        "",
    ]
    _write_lines(report_path, lines)
    write_json(params_path, data=asdict(params))


@dataclass(frozen=True, slots=True)
class ParamsE041:
    """Parameters for E041.

    Args:
        m_max: Max Fermat index m to test.
    """

    m_max: int


def run_e041(
    *, out_dir: Path, seed: int, figures_dir: Path, report_path: Path, params_path: Path
) -> None:
    """E041 — Fermat numbers: not all are prime (counterexample at F5)."""
    params = ParamsE041(m_max=8)

    ms: list[int] = []
    prime_flag: list[int] = []
    values: list[int] = []
    factors: list[str] = []

    for m in range(params.m_max + 1):
        Fm = (1 << (1 << m)) + 1
        ms.append(m)
        values.append(Fm)
        ok = 1 if is_prime_deterministic_64(Fm) else 0
        prime_flag.append(ok)
        if ok:
            factors.append("prime (in 64-bit test)")
        else:
            fac = format_factor_multiset(factorize_pollard_rho(Fm, seed=seed))
            factors.append(fac)

    x = np.array(ms, dtype=np.int64)
    fig1 = _plot_series(
        x=x,
        ys=[("is prime?", np.array(prime_flag, dtype=np.int64))],
        title="Fermat numbers primality indicator (small m)",
        xlab="m",
        ylab="is prime",
    )
    save_figure(out_dir=figures_dir, name="fig_01_fermat_primality", fig=fig1)

    lines = _basic_report_header(
        "E041", "Fermat numbers: prime for m<=4, composite afterwards", "e041"
    )
    lines += [
        "## Parameters",
        f"- m_max: `{params.m_max}`",
        "",
        "## Table",
        "",
        "| m | F_m | prime? | factorization (if composite) |",
        "|---:|---:|---:|---|",
    ]
    for m, v, ok, fac in zip(ms, values, prime_flag, factors, strict=True):
        lines.append(f"| {m} | {v} | {ok} | {fac} |")
    lines += [
        "",
        "## Notes",
        "- Fermat conjectured all F_m are prime; F5 is famously composite.",
        "- This experiment provides a clean counterexample table and factors (via rho).",
        "",
    ]
    _write_lines(report_path, lines)
    write_json(params_path, data=asdict(params))


@dataclass(frozen=True, slots=True)
class ParamsE042:
    """Parameters for E042.

    Args:
        k_max: Max repunit length k.
    """

    k_max: int


def _repunit(k: int) -> int:
    """Return R_k = (10^k - 1) / 9."""
    return int((10**k - 1) // 9)


def run_e042(
    *, out_dir: Path, seed: int, figures_dir: Path, report_path: Path, params_path: Path
) -> None:
    """E042 — Repunit primes: many k are forced composite (counterexamples)."""
    params = ParamsE042(k_max=30)

    ks = np.arange(1, params.k_max + 1, dtype=np.int64)
    flags: list[int] = []
    for k in ks.tolist():
        n = _repunit(int(k))
        # Quick composite filters: if k has factor 2 or 5, R_k is divisible by 11? (not exactly)
        flags.append(1 if is_probable_prime_miller_rabin(n, MR_BASES_64BIT_12) else 0)

    fig1 = _plot_series(
        x=ks,
        ys=[("MR-prime indicator", np.array(flags, dtype=np.int64))],
        title="Repunit R_k primality indicator (probable primes)",
        xlab="k",
        ylab="probable prime?",
    )
    save_figure(out_dir=figures_dir, name="fig_01_repunit_indicator", fig=fig1)

    lines = _basic_report_header("E042", "Repunit primes (small k scan)", "e042")
    lines += [
        "## Parameters",
        f"- k_max: `{params.k_max}`",
        "",
        "## Notes",
        "- Repunit numbers grow fast; this experiment uses Miller–Rabin for a probable-prime indicator.",
        "- Many k values produce composites; prime k is necessary (but not sufficient) for R_k to be prime.",
        "",
    ]
    _write_lines(report_path, lines)
    write_json(params_path, data=asdict(params))


@dataclass(frozen=True, slots=True)
class ParamsE043:
    """Parameters for E043.

    Args:
        samples: Number of semiprimes to factor.
        bits: Bit-size for factors.
    """

    samples: int
    bits: int


def run_e043(
    *, out_dir: Path, seed: int, figures_dir: Path, report_path: Path, params_path: Path
) -> None:
    """E043 — Pollard rho runtime varies wildly (counterexample to 'same size => same effort')."""
    rng = np.random.default_rng(seed)
    params = ParamsE043(samples=80, bits=28)

    times_ms: list[float] = []
    nums: list[int] = []

    # Pre-sieve primes for selecting random primes in a band
    p_list = primes_up_to(1 << params.bits).astype(np.int64)
    p_list = p_list[p_list > (1 << (params.bits - 1))]

    for _ in range(params.samples):
        p = int(rng.choice(p_list))
        q = int(rng.choice(p_list))
        n = p * q
        nums.append(n)
        t0 = perf_counter()
        fac = factorize_pollard_rho(n, seed=seed)
        _ = fac
        times_ms.append((perf_counter() - t0) * 1000.0)

    x = np.arange(1, params.samples + 1, dtype=np.int64)
    fig1 = _plot_series(
        x=x,
        ys=[("factor time (ms)", np.array(times_ms, dtype=np.float64))],
        title="Pollard rho factorization time for similar-size semiprimes",
        xlab="sample index",
        ylab="ms",
    )
    save_figure(out_dir=figures_dir, name="fig_01_pollard_rho_runtime_variance", fig=fig1)

    lines = _basic_report_header("E043", "Pollard rho runtime variability", "e043")
    lines += [
        "## Parameters",
        f"- samples: `{params.samples}`",
        f"- bits: `{params.bits}`",
        "",
        "## Notes",
        "- Factoring difficulty depends on structure (e.g., closeness of factors), not just bit size.",
        "- Rho is stochastic; variance is expected and is a useful experimental feature.",
        "",
    ]
    _write_lines(report_path, lines)
    write_json(params_path, data=asdict(params))


@dataclass(frozen=True, slots=True)
class ParamsE044:
    """Parameters for E044.

    Args:
        samples: Random odd integers to test.
        bits: Bit size.
        bases: Bases per test.
    """

    samples: int
    bits: int
    bases: list[int]


def run_e044(
    *, out_dir: Path, seed: int, figures_dir: Path, report_path: Path, params_path: Path
) -> None:
    """E044 — Solovay–Strassen vs Miller–Rabin (liar rates on random composites)."""
    rng = np.random.default_rng(seed)
    params = ParamsE044(samples=4000, bits=32, bases=[2, 3, 5, 7, 11])

    # generate random odds, filter composites using deterministic MR 64 (good enough here)
    low = 1 << (params.bits - 1)
    high = (1 << params.bits) - 1
    nums = rng.integers(low=low, high=high, size=params.samples, dtype=np.int64)
    nums |= 1
    nums_i = [int(n) for n in nums.tolist()]
    composites = [n for n in nums_i if not is_prime_deterministic_64(n)]

    ss_pass = [is_probable_prime_solovay_strassen(n, params.bases) for n in composites]
    mr_pass = [is_probable_prime_miller_rabin(n, tuple(params.bases)) for n in composites]

    # liar indicators (passing though composite)
    ss_liars = np.cumsum(np.array(ss_pass, dtype=np.int64))
    mr_liars = np.cumsum(np.array(mr_pass, dtype=np.int64))
    x = np.arange(1, len(composites) + 1, dtype=np.int64)

    fig1 = _plot_series(
        x=x,
        ys=[
            ("SS liars (cum)", ss_liars.astype(np.int64)),
            ("MR liars (cum)", mr_liars.astype(np.int64)),
        ],
        title="Cumulative liar counts on random composites",
        xlab="composite sample index",
        ylab="liars seen",
    )
    save_figure(out_dir=figures_dir, name="fig_01_ss_vs_mr_liars", fig=fig1)

    lines = _basic_report_header("E044", "Solovay–Strassen vs Miller–Rabin (liars)", "e044")
    lines += [
        "## Parameters",
        f"- samples: `{params.samples}`",
        f"- bits: `{params.bits}`",
        f"- bases: `{params.bases}`",
        "",
        "## Notes",
        "- Both tests are probabilistic; liar rates depend on bases and on the composite distribution.",
        "- In practice, Miller–Rabin with strong base sets is often preferred.",
        "",
    ]
    _write_lines(report_path, lines)
    write_json(params_path, data=asdict(params))


@dataclass(frozen=True, slots=True)
class ParamsE045:
    """Parameters for E045.

    Args:
        samples: Random odd integers to test.
        bits: Bit size.
    """

    samples: int
    bits: int


def run_e045(
    *, out_dir: Path, seed: int, figures_dir: Path, report_path: Path, params_path: Path
) -> None:
    """E045 — Deterministic 64-bit MR: 12 bases vs small subsets (counterexample)."""
    rng = np.random.default_rng(seed)
    params = ParamsE045(samples=20000, bits=64)

    # Random 64-bit odds (within Python int)
    nums = rng.integers(low=0, high=np.iinfo(np.uint64).max, size=params.samples, dtype=np.uint64)
    nums |= 1
    nums_i = [int(n) for n in nums.tolist()]

    bases_small = [
        ("{2,3,5}", (2, 3, 5)),
        ("{2,3,5,7,11}", (2, 3, 5, 7, 11)),
        ("12 primes (det 64-bit)", MR_BASES_64BIT_12),
    ]

    # Compare pass rates (not "prime rates") to illustrate that small base sets accept more composites
    passes: list[np.ndarray] = []
    for _, bases in bases_small:
        passes.append(
            np.array(
                [1 if is_probable_prime_miller_rabin(n, bases) else 0 for n in nums_i],
                dtype=np.int64,
            )
        )

    x = np.arange(1, params.samples + 1, dtype=np.int64)
    cum = [np.cumsum(p) for p in passes]
    fig1 = _plot_series(
        x=x,
        ys=[(label, c.astype(np.int64)) for (label, _), c in zip(bases_small, cum, strict=True)],
        title="Cumulative count of 'passes' for random 64-bit odds",
        xlab="sample index",
        ylab="pass count",
    )
    save_figure(out_dir=figures_dir, name="fig_01_mr_base_set_pass_counts", fig=fig1)

    lines = _basic_report_header("E045", "Deterministic 64-bit MR base sets", "e045")
    lines += [
        "## Parameters",
        f"- samples: `{params.samples}`",
        f"- bits: `{params.bits}`",
        "",
        "## Notes",
        "- For n < 2^64, the 12-base set (2..37 primes) is deterministic.",
        "- Smaller base sets are faster but allow some composites through (rare, but real).",
        "",
    ]
    _write_lines(report_path, lines)
    write_json(params_path, data=asdict(params))


@dataclass(frozen=True, slots=True)
class ParamsE046:
    """Parameters for E046.

    Args:
        n_max: Range end.
        mr_bases: Base set for fast MR stage.
    """

    n_max: int
    mr_bases: list[int]


def run_e046(
    *, out_dir: Path, seed: int, figures_dir: Path, report_path: Path, params_path: Path
) -> None:
    """E046 — A practical prime-testing pipeline (and how it can fail if tuned badly)."""
    params = ParamsE046(n_max=2_000_000, mr_bases=[2, 3, 5])

    is_prime = prime_mask_up_to(params.n_max)
    # primes = np.flatnonzero(is_prime).astype(np.int64).tolist()
    # primes_small = primes_up_to(math.isqrt(params.n_max) + 1)

    # pipeline classification on odd numbers:
    # stage 1: quick MR (limited bases)
    # stage 2: accept as prime (but compare to true sieve ground truth to detect misclassifications)
    odds = np.arange(3, params.n_max + 1, 2, dtype=np.int64)
    mr_pass = np.array(
        [is_probable_prime_miller_rabin(int(n), tuple(params.mr_bases)) for n in odds], dtype=bool
    )
    truth = is_prime[odds]
    false_pos = mr_pass & (~truth)
    false_neg = (~mr_pass) & truth

    # Plot cumulative counts
    x = odds.astype(np.int64)
    fp_cum = np.cumsum(false_pos.astype(np.int64))
    fn_cum = np.cumsum(false_neg.astype(np.int64))

    fig1 = _plot_series(
        x=x,
        ys=[
            ("false positives", fp_cum.astype(np.int64)),
            ("false negatives", fn_cum.astype(np.int64)),
        ],
        title="Pipeline errors vs odd n (MR base set too small)",
        xlab="n (odd)",
        ylab="cumulative errors",
    )
    save_figure(out_dir=figures_dir, name="fig_01_pipeline_error_counts", fig=fig1)

    # Show first few false positives
    fp_vals = [int(v) for v in x[false_pos][:10].tolist()]
    fp_fac = [format_factor_multiset(factorize_pollard_rho(v, seed=seed)) for v in fp_vals]

    lines = _basic_report_header("E046", "Prime-testing pipeline and tuning pitfalls", "e046")
    lines += [
        "## Parameters",
        f"- n_max: `{params.n_max}`",
        f"- mr_bases: `{params.mr_bases}`",
        "",
        "## First false positives (composites that passed MR stage)",
        "",
    ]
    if fp_vals:
        lines += ["| n | factorization |", "|---:|---|"]
        for v, fac in zip(fp_vals, fp_fac, strict=True):
            lines.append(f"| {v} | {fac} |")
    else:
        lines.append("_none in this range_")
    lines += [
        "",
        "## Notes",
        "- Pipelines are great for speed, but correctness depends on parameters.",
        "- This experiment intentionally uses too few MR bases to produce counterexamples.",
        "",
    ]
    _write_lines(report_path, lines)
    write_json(params_path, data=asdict(params))
