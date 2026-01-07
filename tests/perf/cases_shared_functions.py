"""Benchmark case definitions for shared mathxlab functions.

The cases are constructed to be deterministic:
- fixed seeds,
- fixed parameter sizes,
- all random inputs derived from local RNGs with fixed seeds.

Each case factory returns a zero-argument callable so the timing harness can
measure the *hot path* only (setup is outside the measurement loop).
"""

from __future__ import annotations

from collections.abc import Callable
from dataclasses import dataclass

import numpy as np


@dataclass(frozen=True, slots=True)
class PerfCase:
    """Definition of one microbenchmark case.

    Attributes:
        case_id: Stable case identifier.
        module: Module of the benchmarked function.
        function: Function name.
        description: Short human-readable description.
        make_callable: Factory returning the zero-arg callable to time.
        work_units: Optional work units per invocation (for throughput).
        unit_label: Label for work units.
    """

    case_id: str
    module: str
    function: str
    description: str
    make_callable: Callable[[], Callable[[], object]]
    work_units: int
    unit_label: str


def list_perf_cases() -> list[PerfCase]:
    """Return all performance cases for the requested shared functions.

    Returns:
        List of PerfCase instances.
    """
    cases: list[PerfCase] = []

    # ------------------------------------------------------------------
    # mathxlab.experiments._ap_utils
    # ------------------------------------------------------------------
    def _case_sample_grid_linear() -> Callable[[], object]:
        from mathxlab.experiments._ap_utils import sample_grid

        def run() -> object:
            return sample_grid(x_max=1_000_000, n=600, log=False)

        return run

    def _case_sample_grid_log() -> Callable[[], object]:
        from mathxlab.experiments._ap_utils import sample_grid

        def run() -> object:
            return sample_grid(x_max=1_000_000, n=600, log=True)

        return run

    def _case_counts_residue_q4() -> Callable[[], object]:
        from mathxlab.experiments._ap_utils import counts_in_residue_class
        from mathxlab.experiments._prime_utils import primes_up_to

        primes = primes_up_to(2_000_000).astype(np.int64)
        xs = np.linspace(2.0, 2_000_000.0, 800, dtype=np.float64)

        def run() -> object:
            return counts_in_residue_class(primes=primes, q=4, a=1, xs=xs)

        return run

    def _case_counts_residue_q101() -> Callable[[], object]:
        from mathxlab.experiments._ap_utils import counts_in_residue_class
        from mathxlab.experiments._prime_utils import primes_up_to

        primes = primes_up_to(2_000_000).astype(np.int64)
        xs = np.linspace(2.0, 2_000_000.0, 800, dtype=np.float64)

        def run() -> object:
            return counts_in_residue_class(primes=primes, q=101, a=1, xs=xs)

        return run

    cases.extend(
        [
            PerfCase(
                case_id="ap.sample_grid.linear.xmax_1e6.n_600",
                module="mathxlab.experiments._ap_utils",
                function="sample_grid",
                description="Linear grid for x in [2, 1e6], n=600.",
                make_callable=_case_sample_grid_linear,
                work_units=600,
                unit_label="points",
            ),
            PerfCase(
                case_id="ap.sample_grid.log.xmax_1e6.n_600",
                module="mathxlab.experiments._ap_utils",
                function="sample_grid",
                description="Log-spaced grid for x in [2, 1e6], n=600.",
                make_callable=_case_sample_grid_log,
                work_units=600,
                unit_label="points",
            ),
            PerfCase(
                case_id="ap.counts_in_residue_class.q4.xs_800.primes_2e6",
                module="mathxlab.experiments._ap_utils",
                function="counts_in_residue_class",
                description="pi(x; q=4, a=1) using primes<=2e6 and 800 queries.",
                make_callable=_case_counts_residue_q4,
                work_units=800,
                unit_label="queries",
            ),
            PerfCase(
                case_id="ap.counts_in_residue_class.q101.xs_800.primes_2e6",
                module="mathxlab.experiments._ap_utils",
                function="counts_in_residue_class",
                description="pi(x; q=101, a=1) using primes<=2e6 and 800 queries.",
                make_callable=_case_counts_residue_q101,
                work_units=800,
                unit_label="queries",
            ),
        ]
    )

    # ------------------------------------------------------------------
    # mathxlab.experiments._prime_utils
    # ------------------------------------------------------------------
    def _case_prime_mask_1e6() -> Callable[[], object]:
        from mathxlab.experiments._prime_utils import prime_mask_up_to

        def run() -> object:
            return prime_mask_up_to(1_000_000)

        return run

    def _case_primes_up_to_1e6() -> Callable[[], object]:
        from mathxlab.experiments._prime_utils import primes_up_to

        def run() -> object:
            return primes_up_to(1_000_000)

        return run

    def _case_is_probable_prime_miller_rabin_batch_1024() -> Callable[[], object]:
        import random

        from mathxlab.experiments._prime_utils import is_probable_prime_miller_rabin

        rng = random.Random(0)
        bases = (2, 3, 5, 7, 11, 13, 17)

        small_primes = (3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37)
        ns: list[int] = []
        while len(ns) < 1024:
            n = rng.getrandbits(63) | 1
            if n < 3:
                continue
            if any(n % p == 0 for p in small_primes):
                continue
            ns.append(n)

        def run() -> object:
            c = 0
            for n in ns:
                if is_probable_prime_miller_rabin(n, bases):
                    c += 1
            return c

        return run

    def _case_trial_division_semiprimes_256() -> Callable[[], object]:
        import random

        from mathxlab.experiments._prime_utils import primes_up_to, trial_division_factor

        primes = primes_up_to(100_000).astype(np.int64)
        rng = random.Random(0)

        candidates = [int(p) for p in primes if 50_000 <= int(p) <= 100_000]
        ns = [
            candidates[rng.randrange(len(candidates))] * candidates[rng.randrange(len(candidates))]
            for _ in range(256)
        ]

        def run() -> object:
            s = 0
            for n in ns:
                res = trial_division_factor(int(n), primes)
                if res is not None:
                    s += int(res[0])
            return s

        return run

    cases.extend(
        [
            PerfCase(
                case_id="prime.prime_mask_up_to.n_1e6",
                module="mathxlab.experiments._prime_utils",
                function="prime_mask_up_to",
                description="Sieve boolean prime mask up to n=1e6.",
                make_callable=_case_prime_mask_1e6,
                work_units=1_000_001,
                unit_label="values",
            ),
            PerfCase(
                case_id="prime.primes_up_to.n_1e6",
                module="mathxlab.experiments._prime_utils",
                function="primes_up_to",
                description="Prime list up to n=1e6.",
                make_callable=_case_primes_up_to_1e6,
                work_units=1_000_000,
                unit_label="n",
            ),
            PerfCase(
                case_id="prime.is_probable_prime_miller_rabin.batch_1024.bases_7",
                module="mathxlab.experiments._prime_utils",
                function="is_probable_prime_miller_rabin",
                description="Miller–Rabin on 1024 odd 63-bit candidates (bases 2..17).",
                make_callable=_case_is_probable_prime_miller_rabin_batch_1024,
                work_units=1024,
                unit_label="candidates",
            ),
            PerfCase(
                case_id="prime.trial_division_factor.semiprimes_256.primes_1e5",
                module="mathxlab.experiments._prime_utils",
                function="trial_division_factor",
                description="Trial division factorization of 256 semiprimes using primes<=1e5.",
                make_callable=_case_trial_division_semiprimes_256,
                work_units=256,
                unit_label="numbers",
            ),
        ]
    )

    # ------------------------------------------------------------------
    # mathxlab.nt.arithmetic
    # ------------------------------------------------------------------
    def _case_build_factor_sieve_500k() -> Callable[[], object]:
        from mathxlab.nt.arithmetic import build_factor_sieve

        def run() -> object:
            return build_factor_sieve(500_000)

        return run

    def _case_compute_phi_500k() -> Callable[[], object]:
        from mathxlab.nt.arithmetic import build_factor_sieve, compute_phi

        sieve = build_factor_sieve(500_000)

        def run() -> object:
            return compute_phi(500_000, sieve=sieve)

        return run

    def _case_compute_mobius_500k() -> Callable[[], object]:
        from mathxlab.nt.arithmetic import build_factor_sieve, compute_mobius

        sieve = build_factor_sieve(500_000)

        def run() -> object:
            return compute_mobius(500_000, sieve=sieve)

        return run

    def _case_compute_big_omega_500k() -> Callable[[], object]:
        from mathxlab.nt.arithmetic import build_factor_sieve, compute_big_omega

        sieve = build_factor_sieve(500_000)

        def run() -> object:
            return compute_big_omega(500_000, sieve=sieve)

        return run

    def _case_compute_tau_sigma_500k() -> Callable[[], object]:
        from mathxlab.nt.arithmetic import build_factor_sieve, compute_tau_sigma

        sieve = build_factor_sieve(500_000)

        def run() -> object:
            return compute_tau_sigma(500_000, sieve=sieve)

        return run

    cases.extend(
        [
            PerfCase(
                case_id="arith.build_factor_sieve.n_5e5",
                module="mathxlab.nt.arithmetic",
                function="build_factor_sieve",
                description="Build smallest-prime-factor sieve up to n=5e5.",
                make_callable=_case_build_factor_sieve_500k,
                work_units=500_000,
                unit_label="n",
            ),
            PerfCase(
                case_id="arith.compute_phi.n_5e5",
                module="mathxlab.nt.arithmetic",
                function="compute_phi",
                description="Compute φ(n) for 0..5e5 using a prebuilt SPF sieve.",
                make_callable=_case_compute_phi_500k,
                work_units=500_001,
                unit_label="values",
            ),
            PerfCase(
                case_id="arith.compute_mobius.n_5e5",
                module="mathxlab.nt.arithmetic",
                function="compute_mobius",
                description="Compute μ(n) for 0..5e5 using a prebuilt SPF sieve.",
                make_callable=_case_compute_mobius_500k,
                work_units=500_001,
                unit_label="values",
            ),
            PerfCase(
                case_id="arith.compute_big_omega.n_5e5",
                module="mathxlab.nt.arithmetic",
                function="compute_big_omega",
                description="Compute Ω(n) for 0..5e5 using a prebuilt SPF sieve.",
                make_callable=_case_compute_big_omega_500k,
                work_units=500_001,
                unit_label="values",
            ),
            PerfCase(
                case_id="arith.compute_tau_sigma.n_5e5",
                module="mathxlab.nt.arithmetic",
                function="compute_tau_sigma",
                description="Compute τ(n), σ(n) for 0..5e5 using a prebuilt SPF sieve.",
                make_callable=_case_compute_tau_sigma_500k,
                work_units=500_001,
                unit_label="values",
            ),
        ]
    )

    # ------------------------------------------------------------------
    # mathxlab.nt.dirichlet
    # ------------------------------------------------------------------
    def _case_all_characters_97() -> Callable[[], object]:
        from mathxlab.nt.dirichlet import all_characters

        def run() -> object:
            return all_characters(97)

        return run

    def _case_character_table_97() -> Callable[[], object]:
        from mathxlab.nt.dirichlet import character_table

        def run() -> object:
            return character_table(97)

        return run

    def _case_all_characters_420() -> Callable[[], object]:
        from mathxlab.nt.dirichlet import all_characters

        def run() -> object:
            return all_characters(420)

        return run

    def _case_character_table_420() -> Callable[[], object]:
        from mathxlab.nt.dirichlet import character_table

        def run() -> object:
            return character_table(420)

        return run

    def _case_euler_phi_semiprimes_256() -> Callable[[], object]:
        import random

        from mathxlab.experiments._prime_utils import primes_up_to
        from mathxlab.nt.dirichlet import euler_phi

        primes = [int(p) for p in primes_up_to(200_000) if 100_000 <= int(p) <= 200_000]
        rng = random.Random(0)
        ns = [
            primes[rng.randrange(len(primes))] * primes[rng.randrange(len(primes))]
            for _ in range(256)
        ]

        def run() -> object:
            s = 0
            for n in ns:
                s += euler_phi(int(n))
            return s

        return run

    cases.extend(
        [
            PerfCase(
                case_id="dirichlet.all_characters.q_97",
                module="mathxlab.nt.dirichlet",
                function="all_characters",
                description="Enumerate all Dirichlet characters modulo q=97 (prime).",
                make_callable=_case_all_characters_97,
                work_units=96,
                unit_label="characters",
            ),
            PerfCase(
                case_id="dirichlet.character_table.q_97",
                module="mathxlab.nt.dirichlet",
                function="character_table",
                description="Build full character table for q=97 (shape 96 x 97).",
                make_callable=_case_character_table_97,
                work_units=96 * 97,
                unit_label="cells",
            ),
            PerfCase(
                case_id="dirichlet.all_characters.q_420",
                module="mathxlab.nt.dirichlet",
                function="all_characters",
                description="Enumerate all Dirichlet characters modulo q=420 (phi=96).",
                make_callable=_case_all_characters_420,
                work_units=96,
                unit_label="characters",
            ),
            PerfCase(
                case_id="dirichlet.character_table.q_420",
                module="mathxlab.nt.dirichlet",
                function="character_table",
                description="Build full character table for q=420 (shape 96 x 420).",
                make_callable=_case_character_table_420,
                work_units=96 * 420,
                unit_label="cells",
            ),
            PerfCase(
                case_id="dirichlet.euler_phi.semiprimes_256.range_1e5_2e5",
                module="mathxlab.nt.dirichlet",
                function="euler_phi",
                description="Compute Euler φ for 256 semiprimes with factors in [1e5, 2e5].",
                make_callable=_case_euler_phi_semiprimes_256,
                work_units=256,
                unit_label="numbers",
            ),
        ]
    )

    # ------------------------------------------------------------------
    # mathxlab.nt.zeta
    # ------------------------------------------------------------------
    def _case_hardy_Z_batch_12() -> Callable[[], object]:
        from mathxlab.nt.zeta import ZetaEvalSettings, hardy_Z

        ts = np.linspace(10.0, 40.0, 12, dtype=np.float64)
        settings = ZetaEvalSettings(dps=30)

        def run() -> object:
            s = 0.0
            for t in ts:
                s += hardy_Z(float(t), settings=settings)
            return s

        return run

    cases.append(
        PerfCase(
            case_id="zeta.hardy_Z.batch_12.t_10_40.dps_30",
            module="mathxlab.nt.zeta",
            function="hardy_Z",
            description="Evaluate Hardy Z(t) for 12 t-values in [10, 40] with dps=30.",
            make_callable=_case_hardy_Z_batch_12,
            work_units=12,
            unit_label="t-evals",
        )
    )

    return cases
