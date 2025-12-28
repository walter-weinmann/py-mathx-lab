"""Arithmetic functions and factor-sieve helpers.

This module provides simple, fast utilities for experiments involving classic
arithmetic functions such as:

- Euler's totient function φ(n)
- Möbius function μ(n)
- Divisor functions τ(n) and σ(n)
- Prime-factor counting functions ω(n) and Ω(n)
- Liouville function λ(n) = (-1)^{Ω(n)}
- Carmichael function λ(n) (Carmichael's lambda)
- Jordan totient functions J_k(n)
- von Mangoldt function Λ(n) and Chebyshev ψ(x)

All functions are implemented without external dependencies and are designed
for ranges up to a few million in typical experiment settings.

"""

from __future__ import annotations

import math
from dataclasses import dataclass


# ------------------------------------------------------------------------------
@dataclass(frozen=True)
class FactorSieve:
    """Factor-sieve data for fast integer arithmetic.

    Attributes:
        n_max: Maximum integer covered by the sieve.
        spf: Smallest prime factor for every n in [0..n_max]. For n < 2, the
            value is 0.
        primes: List of primes up to n_max.
    """

    n_max: int
    spf: list[int]
    primes: list[int]


# ------------------------------------------------------------------------------
def build_factor_sieve(n_max: int) -> FactorSieve:
    """Build a linear-time smallest-prime-factor sieve.

    Args:
        n_max: Maximum integer to cover (inclusive). Must be >= 2.

    Returns:
        FactorSieve instance.

    Raises:
        ValueError: If n_max < 2.
    """
    if n_max < 2:
        raise ValueError("n_max must be >= 2")

    spf: list[int] = [0] * (n_max + 1)
    primes: list[int] = []

    for n in range(2, n_max + 1):
        if spf[n] == 0:
            spf[n] = n
            primes.append(n)

        for p in primes:
            nn = n * p
            if nn > n_max:
                break
            spf[nn] = p
            if p == spf[n]:
                break

    return FactorSieve(n_max=n_max, spf=spf, primes=primes)


# ------------------------------------------------------------------------------
def factorize(n: int, *, sieve: FactorSieve) -> list[tuple[int, int]]:
    """Factorize n into prime powers using the SPF sieve.

    Args:
        n: Integer to factorize (>= 1).
        sieve: Factor sieve.

    Returns:
        List of (prime, exponent) pairs. For n == 1 the list is empty.

    Raises:
        ValueError: If n is out of bounds for the sieve or n < 1.
    """
    if n < 1:
        raise ValueError("n must be >= 1")
    if n > sieve.n_max:
        raise ValueError(f"n={n} exceeds sieve.n_max={sieve.n_max}")

    out: list[tuple[int, int]] = []
    x = n
    while x > 1:
        p = sieve.spf[x]
        e = 0
        while x % p == 0:
            x //= p
            e += 1
        out.append((p, e))
    return out


# ------------------------------------------------------------------------------
def lcm(a: int, b: int) -> int:
    """Compute the least common multiple.

    Args:
        a: First integer.
        b: Second integer.

    Returns:
        lcm(a, b) with lcm(0, b) == 0.
    """
    if a == 0 or b == 0:
        return 0
    return abs(a // math.gcd(a, b) * b)


# ------------------------------------------------------------------------------
def compute_phi(n_max: int, *, sieve: FactorSieve) -> list[int]:
    """Compute φ(n) for 0..n_max via dynamic SPF recurrence.

    Args:
        n_max: Maximum n to compute (<= sieve.n_max).
        sieve: Factor sieve.

    Returns:
        List phi where phi[n] = φ(n). phi[0] = 0, phi[1] = 1.
    """
    if n_max > sieve.n_max:
        raise ValueError("n_max exceeds sieve")
    phi = [0] * (n_max + 1)
    phi[1] = 1
    for n in range(2, n_max + 1):
        p = sieve.spf[n]
        m = n // p
        if m % p == 0:
            phi[n] = phi[m] * p
        else:
            phi[n] = phi[m] * (p - 1)
    return phi


# ------------------------------------------------------------------------------
def compute_mobius(n_max: int, *, sieve: FactorSieve) -> list[int]:
    """Compute μ(n) for 0..n_max using SPF recurrence.

    Args:
        n_max: Maximum n to compute (<= sieve.n_max).
        sieve: Factor sieve.

    Returns:
        List mu where mu[n] = μ(n). mu[0]=0, mu[1]=1.
    """
    if n_max > sieve.n_max:
        raise ValueError("n_max exceeds sieve")
    mu = [0] * (n_max + 1)
    mu[1] = 1
    for n in range(2, n_max + 1):
        p = sieve.spf[n]
        m = n // p
        if m % p == 0:
            mu[n] = 0
        else:
            mu[n] = -mu[m]
    return mu


# ------------------------------------------------------------------------------
def compute_omega(n_max: int, *, sieve: FactorSieve) -> list[int]:
    """Compute ω(n): number of distinct prime factors of n.

    Args:
        n_max: Maximum n to compute (<= sieve.n_max).
        sieve: Factor sieve.

    Returns:
        List omega with omega[0]=0, omega[1]=0.
    """
    if n_max > sieve.n_max:
        raise ValueError("n_max exceeds sieve")
    omega = [0] * (n_max + 1)
    for n in range(2, n_max + 1):
        p = sieve.spf[n]
        m = n // p
        omega[n] = omega[m] + (1 if m % p != 0 else 0)
    return omega


# ------------------------------------------------------------------------------
def compute_big_omega(n_max: int, *, sieve: FactorSieve) -> list[int]:
    """Compute Ω(n): number of prime factors of n with multiplicity.

    Args:
        n_max: Maximum n to compute (<= sieve.n_max).
        sieve: Factor sieve.

    Returns:
        List big_omega with big_omega[0]=0, big_omega[1]=0.
    """
    if n_max > sieve.n_max:
        raise ValueError("n_max exceeds sieve")
    big_omega = [0] * (n_max + 1)
    for n in range(2, n_max + 1):
        p = sieve.spf[n]
        big_omega[n] = big_omega[n // p] + 1
    return big_omega


# ------------------------------------------------------------------------------
def compute_tau_sigma(n_max: int, *, sieve: FactorSieve) -> tuple[list[int], list[int]]:
    """Compute τ(n) and σ(n) for 0..n_max using SPF recurrences.

    Args:
        n_max: Maximum n to compute (<= sieve.n_max).
        sieve: Factor sieve.

    Returns:
        (tau, sigma) where:
            tau[n] = number of divisors of n (τ(n)),
            sigma[n] = sum of divisors of n (σ(n)).
    """
    if n_max > sieve.n_max:
        raise ValueError("n_max exceeds sieve")

    tau = [0] * (n_max + 1)
    sigma = [0] * (n_max + 1)

    tau[1] = 1
    sigma[1] = 1

    # For each n>1, we represent n = p^e * core, where p is the smallest prime factor
    # and core is not divisible by p. We cache:
    # - exp[n] = e
    # - p_pow[n] = p^e
    # - p_sum[n] = 1 + p + ... + p^e
    # This yields:
    #   τ(n) = τ(core) * (e+1)
    #   σ(n) = σ(core) * (1 + p + ... + p^e)
    exp = [0] * (n_max + 1)
    p_pow = [0] * (n_max + 1)
    p_sum = [0] * (n_max + 1)
    core = [0] * (n_max + 1)

    for n in range(2, n_max + 1):
        p = sieve.spf[n]
        m = n // p
        if sieve.spf[m] == p:
            exp[n] = exp[m] + 1
            p_pow[n] = p_pow[m] * p
            p_sum[n] = p_sum[m] + p_pow[n]
            core[n] = core[m]
        else:
            exp[n] = 1
            p_pow[n] = p
            p_sum[n] = 1 + p
            core[n] = m

        tau[n] = tau[core[n]] * (exp[n] + 1)
        sigma[n] = sigma[core[n]] * p_sum[n]

    return tau, sigma


# ------------------------------------------------------------------------------
def liouville(big_omega_n: int) -> int:
    """Compute Liouville function λ(n) from Ω(n).

    Args:
        big_omega_n: Ω(n).

    Returns:
        λ(n) = (-1)^{Ω(n)} as +1 or -1.
    """
    return -1 if (big_omega_n % 2 == 1) else 1


# ------------------------------------------------------------------------------
def carmichael_lambda_for_prime_power(p: int, e: int) -> int:
    """Compute Carmichael's λ(p^e).

    Args:
        p: Prime.
        e: Exponent (>= 1).

    Returns:
        λ(p^e) as integer.
    """
    if e < 1:
        raise ValueError("e must be >= 1")

    if p == 2:
        if e == 1:
            return 1
        if e == 2:
            return 2
        return int(2 ** (e - 2))

    # For odd primes, λ(p^e) = φ(p^e)
    return int((p - 1) * (p ** (e - 1)))


# ------------------------------------------------------------------------------
def carmichael_lambda(n: int, *, sieve: FactorSieve) -> int:
    """Compute Carmichael's lambda function λ(n).

    Args:
        n: Integer to evaluate (>= 1).
        sieve: Factor sieve.

    Returns:
        λ(n).

    Raises:
        ValueError: If n out of range.
    """
    factors = factorize(n, sieve=sieve)
    lam = 1
    for p, e in factors:
        lam = lcm(lam, carmichael_lambda_for_prime_power(p, e))
    return lam


# ------------------------------------------------------------------------------
def jordan_totient(n: int, k: int, *, sieve: FactorSieve) -> int:
    """Compute Jordan's totient function J_k(n).

    J_k(n) = n^k ∏_{p|n} (1 - 1/p^k)

    Args:
        n: Integer to evaluate (>= 1).
        k: Parameter k (>= 1).
        sieve: Factor sieve.

    Returns:
        J_k(n).
    """
    if k < 1:
        raise ValueError("k must be >= 1")
    factors = factorize(n, sieve=sieve)

    # Compute with integer arithmetic: start with n^k, then multiply by (p^k - 1)/p^k.
    out: int = n**k
    for p, _e in factors:
        pk = p**k
        out = out // pk * (pk - 1)
    return out


# ------------------------------------------------------------------------------
def compute_von_mangoldt(n_max: int, *, sieve: FactorSieve) -> list[float]:
    """Compute Λ(n) for n=0..n_max.

    Λ(n) = log p if n is a prime power p^k (k>=1), else 0.

    Args:
        n_max: Maximum n.
        sieve: Factor sieve.

    Returns:
        List lam where lam[n] = Λ(n) as float.
    """
    if n_max > sieve.n_max:
        raise ValueError("n_max exceeds sieve")

    lam = [0.0] * (n_max + 1)
    for p in sieve.primes:
        pk = p
        logp = math.log(p)
        while pk <= n_max:
            lam[pk] = logp
            # Guard against overflow in pk *= p for large p and n_max.
            if pk > n_max // p:
                break
            pk *= p
    return lam


# ------------------------------------------------------------------------------
def von_mangoldt(n: int, *, sieve: FactorSieve) -> float:
    """Compute the von Mangoldt function Λ(n).

    Λ(n) = log p if n is a prime power p^k (k>=1), else 0.

    Args:
        n: Integer to evaluate (>= 1).
        sieve: Factor sieve.

    Returns:
        Λ(n) as float (natural logarithm).
    """
    if n <= 1:
        return 0.0
    factors = factorize(n, sieve=sieve)
    if len(factors) != 1:
        return 0.0
    p, _e = factors[0]
    return math.log(p)


# ------------------------------------------------------------------------------
def chebyshev_psi(n_max: int, *, sieve: FactorSieve) -> list[float]:
    """Compute Chebyshev's ψ(x) for x=0..n_max.

    ψ(x) = ∑_{n<=x} Λ(n)

    Args:
        n_max: Maximum x.
        sieve: Factor sieve.

    Returns:
        List psi where psi[x] = ψ(x).
    """
    lam = compute_von_mangoldt(n_max, sieve=sieve)
    psi = [0.0] * (n_max + 1)
    running = 0.0
    for n in range(1, n_max + 1):
        running += lam[n]
        psi[n] = running
    return psi
