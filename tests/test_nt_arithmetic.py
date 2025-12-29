"""Unit tests for core arithmetic helpers.

These tests are intentionally small and deterministic so they run fast while
still providing meaningful coverage for the sieve-driven implementations.
"""

from __future__ import annotations

import math

import pytest

from mathxlab.nt.arithmetic import (
    build_factor_sieve,
    carmichael_lambda,
    carmichael_lambda_for_prime_power,
    chebyshev_psi,
    compute_mobius,
    compute_phi,
    compute_tau_sigma,
    compute_von_mangoldt,
    factorize,
    jordan_totient,
    lcm,
    von_mangoldt,
)


def test_factorize_and_lcm() -> None:
    """Factorization via SPF sieve matches expected prime powers."""
    sieve = build_factor_sieve(200)
    assert factorize(1, sieve=sieve) == []
    assert factorize(2, sieve=sieve) == [(2, 1)]
    assert factorize(12, sieve=sieve) == [(2, 2), (3, 1)]
    assert factorize(180, sieve=sieve) == [(2, 2), (3, 2), (5, 1)]

    assert lcm(12, 18) == 36
    assert lcm(21, 6) == 42


def test_phi_mobius_tau_sigma_small_values() -> None:
    """Check classic arithmetic functions against known small values."""
    n_max = 60
    sieve = build_factor_sieve(n_max)

    phi = compute_phi(n_max, sieve=sieve)
    mu = compute_mobius(n_max, sieve=sieve)
    tau, sigma = compute_tau_sigma(n_max, sieve=sieve)

    # Euler phi.
    assert phi[1] == 1
    assert phi[2] == 1
    assert phi[12] == 4
    assert phi[36] == 12

    # Möbius.
    assert mu[1] == 1
    assert mu[2] == -1
    assert mu[4] == 0
    assert mu[30] == (-1) ** 3

    # Divisor count and sum of divisors.
    assert tau[1] == 1
    assert tau[12] == 6  # 1,2,3,4,6,12
    assert sigma[12] == 28

    # Sanity: multiplicativity of phi for coprime inputs.
    assert math.gcd(3, 5) == 1
    assert phi[3 * 5] == phi[3] * phi[5]


def test_carmichael_and_jordan_totient() -> None:
    """Carmichael's lambda and Jordan totient J_k match easy cases."""
    sieve = build_factor_sieve(200)

    # Carmichael lambda:
    # - for odd prime powers p^e, it's phi(p^e)
    # - for 2^e with e>=3, it's 2^{e-2}
    assert carmichael_lambda(9, sieve=sieve) == 6
    assert carmichael_lambda(8, sieve=sieve) == 2
    assert carmichael_lambda(16, sieve=sieve) == 4
    assert carmichael_lambda(15, sieve=sieve) == 4  # lcm(lambda(3), lambda(5))

    # Jordan totient: J_1(n) == phi(n)
    assert jordan_totient(36, 1, sieve=sieve) == 12

    # J_2(p) = p^2 - 1 for prime p.
    assert jordan_totient(7, 2, sieve=sieve) == 48


def test_von_mangoldt() -> None:
    """von Mangoldt is log(p) on prime powers, 0 otherwise."""
    sieve = build_factor_sieve(200)
    assert abs(von_mangoldt(1, sieve=sieve)) < 1e-12

    # Prime.
    assert abs(von_mangoldt(13, sieve=sieve) - math.log(13)) < 1e-12

    # Prime powers.
    assert abs(von_mangoldt(27, sieve=sieve) - math.log(3)) < 1e-12
    assert abs(von_mangoldt(16, sieve=sieve) - math.log(2)) < 1e-12

    # Not a prime power.
    assert abs(von_mangoldt(12, sieve=sieve)) < 1e-12


def test_build_factor_sieve_rejects_too_small_nmax() -> None:
    """Sieve construction should reject n_max < 2."""
    with pytest.raises(ValueError):
        build_factor_sieve(0)
    with pytest.raises(ValueError):
        build_factor_sieve(1)


def test_factorize_and_squarefree_input_validation() -> None:
    """Validate that factorization helpers reject unsupported inputs."""
    sieve = build_factor_sieve(50)

    with pytest.raises(ValueError):
        factorize(0, sieve=sieve)

    with pytest.raises(ValueError):
        factorize(51, sieve=sieve)


def test_carmichael_lambda_for_prime_power_edge_cases() -> None:
    """Cover special cases for Carmichael lambda on prime powers."""
    # 2^1, 2^2 are special.
    assert carmichael_lambda_for_prime_power(2, 1) == 1
    assert carmichael_lambda_for_prime_power(2, 2) == 2
    assert carmichael_lambda_for_prime_power(2, 3) == 2

    # For odd prime p^e it's phi(p^e).
    assert carmichael_lambda_for_prime_power(3, 2) == (3 - 1) * 3

    with pytest.raises(ValueError):
        carmichael_lambda_for_prime_power(2, 0)


def test_compute_von_mangoldt_and_chebyshev_psi_sanity() -> None:
    """Compute arrays for Λ(n) and ψ(x) and test simple monotonicity."""
    sieve = build_factor_sieve(100)
    lam = compute_von_mangoldt(30, sieve=sieve)

    # Λ(p) = log(p)
    assert abs(lam[13] - math.log(13)) < 1e-12
    # Λ(n)=0 for non-prime-powers.
    assert abs(lam[12]) < 1e-12

    psi = chebyshev_psi(30, sieve=sieve)
    # ψ(x) is non-decreasing.
    assert all(psi[i] <= psi[i + 1] + 1e-12 for i in range(30))
    # ψ(p) - ψ(p-1) = log(p) for prime p.
    assert abs(psi[13] - psi[12] - math.log(13)) < 1e-12

    # Bounds check.
    with pytest.raises(ValueError):
        compute_von_mangoldt(200, sieve=sieve)
    with pytest.raises(ValueError):
        chebyshev_psi(200, sieve=sieve)


def test_jordan_totient_rejects_invalid_k() -> None:
    """Jordan totient should reject k < 1."""
    sieve = build_factor_sieve(50)
    with pytest.raises(ValueError):
        jordan_totient(10, 0, sieve=sieve)
