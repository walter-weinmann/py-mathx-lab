"""Experiment package.

Experiments are organized as importable modules, e.g.:

    uv run python -m mathxlab.experiments.e001

This package also exposes a small, stable registry so other tooling (CLI / docs
builders) can enumerate available experiments without importing every module.
"""

from __future__ import annotations

from collections.abc import Iterable
from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class ExperimentSpec:
    """Lightweight metadata about an experiment.

    Args:
        experiment_id: The experiment id, e.g. "e001".
        title: Human-readable title (used in listings).
        module: Import path of the experiment entry point module.
    """

    experiment_id: str
    title: str
    module: str


# Keep this list in sync with files under `mathxlab/experiments/`.
_EXPERIMENTS: tuple[ExperimentSpec, ...] = (
    ExperimentSpec(
        experiment_id="e001",
        title="Taylor error landscapes for sin(x)",
        module="mathxlab.experiments.e001",
    ),
    ExperimentSpec(
        experiment_id="e002",
        title="Even perfect numbers: generator and growth",
        module="mathxlab.experiments.e002",
    ),
    ExperimentSpec(
        experiment_id="e003",
        title="Abundancy index landscape",
        module="mathxlab.experiments.e003",
    ),
    ExperimentSpec(
        experiment_id="e004",
        title="Benchmark σ(n) computation: sieve vs factorization",
        module="mathxlab.experiments.e004",
    ),
    ExperimentSpec(
        experiment_id="e005",
        title="Odd perfect numbers: constraint filter pipeline",
        module="mathxlab.experiments.e005",
    ),
    ExperimentSpec(
        experiment_id="e006",
        title="Near misses to perfection",
        module="mathxlab.experiments.e006",
    ),
    ExperimentSpec(
        experiment_id="e007",
        title="Mersenne number growth",
        module="mathxlab.experiments.e007",
    ),
    ExperimentSpec(
        experiment_id="e008",
        title="Lucas–Lehmer scan for Mersenne primes",
        module="mathxlab.experiments.e008",
    ),
    ExperimentSpec(
        experiment_id="e009",
        title="Small-factor scan for Mersenne numbers",
        module="mathxlab.experiments.e009",
    ),
    ExperimentSpec(
        experiment_id="e010",
        title="Even perfect numbers from Mersenne primes",
        module="mathxlab.experiments.e010",
    ),
    ExperimentSpec(
        experiment_id="e011",
        title="Heuristic vs observed counts of Mersenne primes",
        module="mathxlab.experiments.e011",
    ),
    ExperimentSpec(
        experiment_id="e012",
        title="Fermat pseudoprimes and Carmichael numbers (counterexamples)",
        module="mathxlab.experiments.e012",
    ),
    ExperimentSpec(
        experiment_id="e013",
        title="Prime-polynomial counterexamples (Euler's n^2 + n + 41)",
        module="mathxlab.experiments.e013",
    ),
    ExperimentSpec(
        experiment_id="e014",
        title="Primorial ± 1 counterexamples",
        module="mathxlab.experiments.e014",
    ),
    ExperimentSpec(
        experiment_id="e015",
        title="Wilson test infeasibility",
        module="mathxlab.experiments.e015",
    ),
    ExperimentSpec(
        experiment_id="e016",
        title="Trial division vs Miller–Rabin scaling",
        module="mathxlab.experiments.e016",
    ),
    ExperimentSpec(
        experiment_id="e017",
        title="Sieve memory blow-up vs segmented sieve",
        module="mathxlab.experiments.e017",
    ),
    ExperimentSpec(
        experiment_id="e018",
        title="Miller–Rabin base choice counterexamples",
        module="mathxlab.experiments.e018",
    ),
    ExperimentSpec(
        experiment_id="e019",
        title="Prime density and PNT visualization",
        module="mathxlab.experiments.e019",
    ),
    ExperimentSpec(
        experiment_id="e020",
        title="Compare pi(x) to li(x) numerically",
        module="mathxlab.experiments.e020",
    ),
    ExperimentSpec(
        experiment_id="e021",
        title="Explicit bounds sanity checks",
        module="mathxlab.experiments.e021",
    ),
    ExperimentSpec(
        experiment_id="e022",
        title="Prime race modulo 4",
        module="mathxlab.experiments.e022",
    ),
    ExperimentSpec(
        experiment_id="e023",
        title="Residue class distribution mod q",
        module="mathxlab.experiments.e023",
    ),
    ExperimentSpec(
        experiment_id="e024",
        title="Ulam spiral structure",
        module="mathxlab.experiments.e024",
    ),
    ExperimentSpec(
        experiment_id="e025",
        title="Prime gaps are not monotone",
        module="mathxlab.experiments.e025",
    ),
    ExperimentSpec(
        experiment_id="e026",
        title="Normalized prime gaps",
        module="mathxlab.experiments.e026",
    ),
    ExperimentSpec(
        experiment_id="e027",
        title="Record prime gaps vs log^2 heuristic",
        module="mathxlab.experiments.e027",
    ),
    ExperimentSpec(
        experiment_id="e028",
        title="Jumping champions (most frequent gaps)",
        module="mathxlab.experiments.e028",
    ),
    ExperimentSpec(
        experiment_id="e029",
        title="Twin primes: observed vs heuristic",
        module="mathxlab.experiments.e029",
    ),
    ExperimentSpec(
        experiment_id="e030",
        title="Cousin and sexy prime pairs",
        module="mathxlab.experiments.e030",
    ),
    ExperimentSpec(
        experiment_id="e031",
        title="Admissibility and modular obstructions",
        module="mathxlab.experiments.e031",
    ),
    ExperimentSpec(
        experiment_id="e032",
        title="Prime triplets and quadruplets",
        module="mathxlab.experiments.e032",
    ),
    ExperimentSpec(
        experiment_id="e033",
        title="Bounded gaps vs twin primes (not the same)",
        module="mathxlab.experiments.e033",
    ),
    ExperimentSpec(
        experiment_id="e034",
        title="Twin primes in sliding windows",
        module="mathxlab.experiments.e034",
    ),
    ExperimentSpec(
        experiment_id="e035",
        title="Primes in arithmetic progressions mod q",
        module="mathxlab.experiments.e035",
    ),
    ExperimentSpec(
        experiment_id="e036",
        title="Prime arithmetic progressions (small search)",
        module="mathxlab.experiments.e036",
    ),
    ExperimentSpec(
        experiment_id="e037",
        title="Prime-free intervals via factorial construction",
        module="mathxlab.experiments.e037",
    ),
    ExperimentSpec(
        experiment_id="e038",
        title="Bertrand's postulate (computational verification)",
        module="mathxlab.experiments.e038",
    ),
    ExperimentSpec(
        experiment_id="e039",
        title="Sophie Germain and safe primes",
        module="mathxlab.experiments.e039",
    ),
    ExperimentSpec(
        experiment_id="e040",
        title="Palindromic primes and the '11 trap'",
        module="mathxlab.experiments.e040",
    ),
    ExperimentSpec(
        experiment_id="e041",
        title="Fermat numbers: not all prime",
        module="mathxlab.experiments.e041",
    ),
    ExperimentSpec(
        experiment_id="e042",
        title="Repunit primes (small k scan)",
        module="mathxlab.experiments.e042",
    ),
    ExperimentSpec(
        experiment_id="e043",
        title="Pollard rho runtime variability",
        module="mathxlab.experiments.e043",
    ),
    ExperimentSpec(
        experiment_id="e044",
        title="Solovay–Strassen vs Miller–Rabin (liars)",
        module="mathxlab.experiments.e044",
    ),
    ExperimentSpec(
        experiment_id="e045",
        title="Deterministic 64-bit MR base sets",
        module="mathxlab.experiments.e045",
    ),
    ExperimentSpec(
        experiment_id="e046",
        title="Prime-testing pipeline and tuning pitfalls",
        module="mathxlab.experiments.e046",
    ),
    ExperimentSpec(
        experiment_id="e047",
        title="Fermat numbers: Pépin test and factor witnesses",
        module="mathxlab.experiments.e047",
    ),
    ExperimentSpec(
        experiment_id="e048",
        title="Carmichael numbers: Korselt scan + Fermat counterexamples",
        module="mathxlab.experiments.e048",
    ),
    ExperimentSpec(
        experiment_id="e049",
        title="Wieferich primes (base 2): rare congruence hits",
        module="mathxlab.experiments.e049",
    ),
    ExperimentSpec(
        experiment_id="e050",
        title="Primorials and Euclid numbers: p# ± 1 are usually composite",
        module="mathxlab.experiments.e050",
    ),
    ExperimentSpec(
        experiment_id="e051",
        title="Semiprimes: balanced vs unbalanced factorization timing",
        module="mathxlab.experiments.e051",
    ),
    ExperimentSpec(
        experiment_id="e052",
        title="Totient ratio landscape: φ(n) / n and primorial structure",
        module="mathxlab.experiments.e052",
    ),
    ExperimentSpec(
        experiment_id="e053",
        title="Inverse totient: multiplicities of values φ(n)=m in a prefix",
        module="mathxlab.experiments.e053",
    ),
    ExperimentSpec(
        experiment_id="e054",
        title="Möbius μ(n) and squarefree density via μ(n)^2",
        module="mathxlab.experiments.e054",
    ),
    ExperimentSpec(
        experiment_id="e055",
        title="Mertens function walk: M(x)=∑_{n≤x} μ(n)",
        module="mathxlab.experiments.e055",
    ),
    ExperimentSpec(
        experiment_id="e056",
        title="Liouville vs Möbius: two ±1 walks built from prime factors",
        module="mathxlab.experiments.e056",
    ),
    ExperimentSpec(
        experiment_id="e057",
        title="Erdős–Kac in practice: Ω(n) looks Gaussian after normalization",
        module="mathxlab.experiments.e057",
    ),
    ExperimentSpec(
        experiment_id="e058",
        title="Divisor count τ(n): record values and highly composite behavior",
        module="mathxlab.experiments.e058",
    ),
    ExperimentSpec(
        experiment_id="e059",
        title="Abundancy index: σ(n)/n and the perfect-number threshold",
        module="mathxlab.experiments.e059",
    ),
    ExperimentSpec(
        experiment_id="e060",
        title="Jordan totients J_k(n): normalized landscapes for k=1..3",
        module="mathxlab.experiments.e060",
    ),
    ExperimentSpec(
        experiment_id="e061",
        title="von Mangoldt Λ(n) and Chebyshev ψ(x): jumps at prime powers",
        module="mathxlab.experiments.e061",
    ),
    ExperimentSpec(
        experiment_id="e062",
        title="Carmichael's λ(n) vs Euler's φ(n): exponent vs group size",
        module="mathxlab.experiments.e062",
    ),
    ExperimentSpec(
        experiment_id="e063",
        title="Dirichlet convolution identities (computational checks)",
        module="mathxlab.experiments.e063",
    ),
    ExperimentSpec(
        experiment_id="e064",
        title="Dirichlet characters: tables and phases",
        module="mathxlab.experiments.e064",
    ),
    ExperimentSpec(
        experiment_id="e065",
        title="Dirichlet characters: orthogonality matrix",
        module="mathxlab.experiments.e065",
    ),
    ExperimentSpec(
        experiment_id="e066",
        title="Character partial sums: cancellation profiles",
        module="mathxlab.experiments.e066",
    ),
    ExperimentSpec(
        experiment_id="e067",
        title="Gauss sums: magnitude vs sqrt(q)",
        module="mathxlab.experiments.e067",
    ),
    ExperimentSpec(
        experiment_id="e068",
        title="Dirichlet L(s,χ): series vs Euler product",
        module="mathxlab.experiments.e068",
    ),
    ExperimentSpec(
        experiment_id="e069",
        title="L(1,χ): slow convergence and smoothing",
        module="mathxlab.experiments.e069",
    ),
    ExperimentSpec(
        experiment_id="e070",
        title="Primes in residue classes: pi(x;q,a)",
        module="mathxlab.experiments.e070",
    ),
    ExperimentSpec(
        experiment_id="e071",
        title="PNT(AP) numerics: pi(x;q,a) - Li(x)/phi(q)",
        module="mathxlab.experiments.e071",
    ),
    ExperimentSpec(
        experiment_id="e072",
        title="Prime race mod 4: pi(x;4,3) vs pi(x;4,1)",
        module="mathxlab.experiments.e072",
    ),
    ExperimentSpec(
        experiment_id="e073",
        title="Prime race mod 3: pi(x;3,2) vs pi(x;3,1)",
        module="mathxlab.experiments.e073",
    ),
    ExperimentSpec(
        experiment_id="e074",
        title="Prime race mod 8: leaderboard among 1,3,5,7",
        module="mathxlab.experiments.e074",
    ),
    ExperimentSpec(
        experiment_id="e075",
        title="Prime race statistic: distribution on log-grid",
        module="mathxlab.experiments.e075",
    ),
    ExperimentSpec(
        experiment_id="e076",
        title="Chebyshev θ(x;q,a): weighted prime counts",
        module="mathxlab.experiments.e076",
    ),
    ExperimentSpec(
        experiment_id="e077",
        title="Indicator via character orthogonality (sanity check)",
        module="mathxlab.experiments.e077",
    ),
    ExperimentSpec(
        experiment_id="e078",
        title="Max |sum_{n<=N} χ(n)| across characters",
        module="mathxlab.experiments.e078",
    ),
    ExperimentSpec(
        experiment_id="e079",
        title="Primitive vs imprimitive characters: conductors",
        module="mathxlab.experiments.e079",
    ),
    ExperimentSpec(
        experiment_id="e080",
        title="Chebyshev bias: leader fraction vs x",
        module="mathxlab.experiments.e080",
    ),
    ExperimentSpec(
        experiment_id="e081",
        title="Prime race: first sign changes and crossings",
        module="mathxlab.experiments.e081",
    ),
    ExperimentSpec(
        experiment_id="e082",
        title="Zeta(s) Dirichlet series convergence",
        module="mathxlab.experiments.e082",
    ),
    ExperimentSpec(
        experiment_id="e083",
        title="Zeta(s) series vs Euler product",
        module="mathxlab.experiments.e083",
    ),
    ExperimentSpec(
        experiment_id="e084",
        title="Zeta on the critical line: magnitude sampling",
        module="mathxlab.experiments.e084",
    ),
    ExperimentSpec(
        experiment_id="e085",
        title="Eta-series acceleration near s=1",
        module="mathxlab.experiments.e085",
    ),
    ExperimentSpec(
        experiment_id="e086",
        title="Hardy Z(t) near the first zeros",
        module="mathxlab.experiments.e086",
    ),
    ExperimentSpec(
        experiment_id="e087",
        title="Gram points and Hardy Z",
        module="mathxlab.experiments.e087",
    ),
    ExperimentSpec(
        experiment_id="e088",
        title="Zero counting vs Riemann--von Mangoldt main term",
        module="mathxlab.experiments.e088",
    ),
    ExperimentSpec(
        experiment_id="e089",
        title="Heatmap of log|zeta(s)| on a coarse grid",
        module="mathxlab.experiments.e089",
    ),
    ExperimentSpec(
        experiment_id="e090",
        title="Functional equation residual heatmap",
        module="mathxlab.experiments.e090",
    ),
    ExperimentSpec(
        experiment_id="e091",
        title="Partial Euler products on the critical line",
        module="mathxlab.experiments.e091",
    ),
    ExperimentSpec(
        experiment_id="e092",
        title="1/zeta(s) via the Möbius Dirichlet series",
        module="mathxlab.experiments.e092",
    ),
    ExperimentSpec(
        experiment_id="e093",
        title="-zeta'(s)/zeta(s) via the von Mangoldt series",
        module="mathxlab.experiments.e093",
    ),
    ExperimentSpec(
        experiment_id="e094",
        title="ω(n) vs Ω(n): Erdős–Kac side-by-side",
        module="mathxlab.experiments.e094",
    ),
    ExperimentSpec(
        experiment_id="e095",
        title="Squarefree filter: ω(n)=Ω(n) when μ(n)≠0",
        module="mathxlab.experiments.e095",
    ),
    ExperimentSpec(
        experiment_id="e096",
        title="Record-holders for τ(n)",
        module="mathxlab.experiments.e096",
    ),
    ExperimentSpec(
        experiment_id="e097",
        title="σ(n)/n landscape: deficient, perfect, abundant",
        module="mathxlab.experiments.e097",
    ),
    ExperimentSpec(
        experiment_id="e098",
        title="Extremals of sigma(n)/n^a across a",
        module="mathxlab.experiments.e098",
    ),
    ExperimentSpec(
        experiment_id="e099",
        title="Jordan totients J_k: atlas and identities",
        module="mathxlab.experiments.e099",
    ),
    ExperimentSpec(
        experiment_id="e100",
        title="Carmichael λ(n) vs Euler φ(n)",
        module="mathxlab.experiments.e100",
    ),
    ExperimentSpec(
        experiment_id="e101",
        title="Reduced residues: (Z/qZ)^x as a concrete set",
        module="mathxlab.experiments.e101",
    ),
    ExperimentSpec(
        experiment_id="e102",
        title="Dirichlet convolution identity zoo",
        module="mathxlab.experiments.e102",
    ),
    ExperimentSpec(
        experiment_id="e103",
        title="Chebyshev ψ(x): prime powers drive the jumps",
        module="mathxlab.experiments.e103",
    ),
    ExperimentSpec(
        experiment_id="e104",
        title="Von Mangoldt Λ: support and statistics",
        module="mathxlab.experiments.e104",
    ),
    ExperimentSpec(
        experiment_id="e105",
        title="Mertens function M(x): scaling views",
        module="mathxlab.experiments.e105",
    ),
    ExperimentSpec(
        experiment_id="e106",
        title="Real vs complex Dirichlet characters (small moduli)",
        module="mathxlab.experiments.e106",
    ),
    ExperimentSpec(
        experiment_id="e107",
        title="Conductor distribution for characters",
        module="mathxlab.experiments.e107",
    ),
    ExperimentSpec(
        experiment_id="e108",
        title="Character orthogonality matrix heatmap",
        module="mathxlab.experiments.e108",
    ),
    ExperimentSpec(
        experiment_id="e109",
        title="Gauss sums τ(χ) for prime modulus",
        module="mathxlab.experiments.e109",
    ),
    ExperimentSpec(
        experiment_id="e110",
        title="Dirichlet L-series partial sums (toy)",
        module="mathxlab.experiments.e110",
    ),
    ExperimentSpec(
        experiment_id="e111",
        title="Euler product vs Dirichlet series for L(s,χ)",
        module="mathxlab.experiments.e111",
    ),
    ExperimentSpec(
        experiment_id="e112",
        title="Prime race pi(x;q,a) - pi(x;q,b)",
        module="mathxlab.experiments.e112",
    ),
    ExperimentSpec(
        experiment_id="e113",
        title="First prime in each reduced residue class",
        module="mathxlab.experiments.e113",
    ),
    ExperimentSpec(
        experiment_id="e114",
        title="ζ(1/2+it) via η-series: truncation error curves",
        module="mathxlab.experiments.e114",
    ),
    ExperimentSpec(
        experiment_id="e115",
        title="Hardy Z(t): sign-change scan near low zeros",
        module="mathxlab.experiments.e115",
    ),
    ExperimentSpec(
        experiment_id="e116",
        title="Zero-count proxy vs Riemann–von Mangoldt main term",
        module="mathxlab.experiments.e116",
    ),
    ExperimentSpec(
        experiment_id="e117",
        title="Functional equation check: zeta(s) approx chi(s) zeta(1-s)",
        module="mathxlab.experiments.e117",
    ),
    ExperimentSpec(
        experiment_id="e118",
        title="Euler product approximation vs ζ(s): where it degrades",
        module="mathxlab.experiments.e118",
    ),
    ExperimentSpec(
        experiment_id="e119",
        title="psi(x)-x with simple smoothing",
        module="mathxlab.experiments.e119",
    ),
    ExperimentSpec(
        experiment_id="e120",
        title="Pretentious distance toy: sum_{p<=x} (1-Re chi(p))/p",
        module="mathxlab.experiments.e120",
    ),
    ExperimentSpec(
        experiment_id="e121",
        title="Multiplicativity stress tests (random coprime pairs)",
        module="mathxlab.experiments.e121",
    ),
    ExperimentSpec(
        experiment_id="e122",
        title="Arithmetic function atlas: μ(n), ω(n), φ(n)/n heatmaps",
        module="mathxlab.experiments.e122",
    ),
    ExperimentSpec(
        experiment_id="e123",
        title="Correlation matrix: arithmetic functions on 1..N",
        module="mathxlab.experiments.e123",
    ),
    ExperimentSpec(
        experiment_id="e124",
        title="Klauber triangle",
        module="mathxlab.experiments.e124",
    ),
    ExperimentSpec(
        experiment_id="e125",
        title="Sacks spiral",
        module="mathxlab.experiments.e125",
    ),
    ExperimentSpec(
        experiment_id="e126",
        title="Hexagonal number spiral",
        module="mathxlab.experiments.e126",
    ),
    ExperimentSpec(
        experiment_id="e127",
        title="Quadratic prime-run atlas (n^2 + a n + b)",
        module="mathxlab.experiments.e127",
    ),
    ExperimentSpec(
        experiment_id="e128",
        title="Quadratic modular obstructions (Euler-type)",
        module="mathxlab.experiments.e128",
    ),
    ExperimentSpec(
        experiment_id="e129",
        title="Euler lucky constants for n^2 + n + b",
        module="mathxlab.experiments.e129",
    ),
)


def iter_experiments() -> Iterable[ExperimentSpec]:
    """Iterate over known experiments.

    Returns:
        An iterable of ExperimentSpec items in ascending experiment id order.
    """
    return _EXPERIMENTS


def list_experiment_ids() -> tuple[str, ...]:
    """Return all known experiment ids.

    Returns:
        Tuple of ids like ("e001", "e002", ...).
    """
    return tuple(e.experiment_id for e in _EXPERIMENTS)


def get_experiment_module(experiment_id: str) -> str:
    """Return the module import path for a given experiment id.

    Args:
        experiment_id: The experiment id, e.g. "e003".

    Returns:
        The module import path, e.g. "mathxlab.experiments.e003".

    Raises:
        KeyError: If the experiment id is unknown.
    """
    for e in _EXPERIMENTS:
        if e.experiment_id == experiment_id:
            return e.module
    raise KeyError(f"Unknown experiment id: {experiment_id!r}")


__all__ = [
    "ExperimentSpec",
    "get_experiment_module",
    "iter_experiments",
    "list_experiment_ids",
]
