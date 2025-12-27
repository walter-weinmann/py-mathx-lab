"""Shared prime utilities for py-mathx-lab experiments.

This module is intentionally self-contained (stdlib + numpy only) so experiments
can rely on a stable toolkit:
- fast sieves (prime mask, prime list),
- Miller–Rabin (probabilistic + deterministic for 64-bit),
- Solovay–Strassen (probabilistic),
- simple factorization helpers (trial division + Pollard rho).

All functions are written for clarity and experiment use (not as a crypto library).
"""

from __future__ import annotations

import math
import random
from collections.abc import Iterable

import numpy as np


# ------------------------------------------------------------------------------
def prime_mask_up_to(n: int) -> np.ndarray:
    """Return a boolean primality mask is_prime[0..n].

    Args:
        n: Upper bound (inclusive).

    Returns:
        Boolean array of length n+1, where is_prime[k] is True iff k is prime.
    """
    if n < 0:
        raise ValueError("n must be >= 0")

    is_prime = np.ones(n + 1, dtype=bool)
    if n >= 0:
        is_prime[0] = False
    if n >= 1:
        is_prime[1] = False

    limit = int(n**0.5)
    for p in range(2, limit + 1):
        if is_prime[p]:
            is_prime[p * p : n + 1 : p] = False
    return is_prime


# ------------------------------------------------------------------------------
def primes_up_to(n: int) -> np.ndarray:
    """Compute all primes ≤ n via sieve.

    Args:
        n: Upper bound (inclusive).

    Returns:
        Sorted array of primes ≤ n.
    """
    if n < 2:
        return np.array([], dtype=np.int64)
    mask = prime_mask_up_to(n)
    return np.flatnonzero(mask).astype(np.int64)


# ------------------------------------------------------------------------------
def pi_array_from_mask(is_prime: np.ndarray) -> np.ndarray:
    """Compute pi(x) for x=0..n from a prime mask.

    Args:
        is_prime: Boolean array, where is_prime[k] indicates primality of k.

    Returns:
        Integer array pi where pi[x] = number of primes <= x.
    """
    return np.cumsum(is_prime.astype(np.int64))


# ------------------------------------------------------------------------------
def _decompose_n_minus_1(n: int) -> tuple[int, int]:
    """Decompose n-1 = d * 2^s with d odd.

    Args:
        n: Integer >= 3.

    Returns:
        (d, s) where d is odd and n-1 = d * 2^s.
    """
    d = n - 1
    s = 0
    while d % 2 == 0:
        d //= 2
        s += 1
    return d, s


# ------------------------------------------------------------------------------
def is_probable_prime_miller_rabin(n: int, bases: Iterable[int]) -> bool:
    """Miller–Rabin probable prime test.

    Args:
        n: Integer to test.
        bases: Bases to test.

    Returns:
        True if n is a strong probable prime to all given bases.
    """
    if n < 2:
        return False
    small_primes = (2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37)
    if n in small_primes:
        return True
    for p in small_primes:
        if n % p == 0:
            return False
    if n % 2 == 0:
        return False

    d, s = _decompose_n_minus_1(n)

    for a in bases:
        a_mod = a % n
        if a_mod in (0, 1):
            continue

        x = pow(a_mod, d, n)
        if x in (1, n - 1):
            continue

        witness = True
        for _ in range(s - 1):
            x = (x * x) % n
            if x == n - 1:
                witness = False
                break
        if witness:
            return False

    return True


# ------------------------------------------------------------------------------
MR_BASES_64BIT_12 = (2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37)


def is_prime_deterministic_64(n: int) -> bool:
    """Deterministic Miller–Rabin for 64-bit unsigned integers.

    This uses the well-known 12-base set that is deterministic for n < 2^64.

    Args:
        n: Integer to test.

    Returns:
        True iff n is prime (for n < 2^64); otherwise a very strong probable prime.
    """
    return is_probable_prime_miller_rabin(n, MR_BASES_64BIT_12)


# ------------------------------------------------------------------------------
def jacobi_symbol(a: int, n: int) -> int:
    """Compute the Jacobi symbol (a/n).

    Args:
        a: Integer.
        n: Odd positive integer.

    Returns:
        -1, 0, or +1.
    """
    if n <= 0 or n % 2 == 0:
        raise ValueError("n must be a positive odd integer")

    a = a % n
    result = 1
    while a != 0:
        while a % 2 == 0:
            a //= 2
            r = n % 8
            if r in (3, 5):
                result = -result

        a, n = n, a  # quadratic reciprocity
        if a % 4 == 3 and n % 4 == 3:
            result = -result
        a %= n

    return result if n == 1 else 0


# ------------------------------------------------------------------------------
def is_probable_prime_solovay_strassen(n: int, bases: Iterable[int]) -> bool:
    """Solovay–Strassen probable prime test.

    Args:
        n: Integer to test.
        bases: Bases to test.

    Returns:
        True if n passes all tests, False if composite is detected.
    """
    if n < 2:
        return False
    if n in (2, 3):
        return True
    if n % 2 == 0:
        return False

    for a in bases:
        a_mod = a % n
        if a_mod in (0, 1):
            continue

        x = jacobi_symbol(a_mod, n)
        if x == 0:
            return False
        # Euler criterion: a^((n-1)/2) ≡ (a/n) (mod n) for primes
        y = pow(a_mod, (n - 1) // 2, n)
        if y != (x % n):
            return False

    return True


# ------------------------------------------------------------------------------
def trial_division_factor(n: int, primes: np.ndarray) -> tuple[int, int] | None:
    """Find a non-trivial factor by trial division.

    Args:
        n: Number to factor (n >= 2).
        primes: Prime list for trial division.

    Returns:
        (p, e) with p^e | n, or None if no factor found in the given prime list.
    """
    if n < 2:
        raise ValueError("n must be >= 2")

    remaining = n
    for p in primes:
        p_i = int(p)
        if p_i * p_i > remaining:
            break
        if remaining % p_i == 0:
            e = 0
            while remaining % p_i == 0:
                remaining //= p_i
                e += 1
            return (p_i, e)
    return None


# ------------------------------------------------------------------------------
def pollard_rho(n: int, *, rng: random.Random) -> int:
    """Pollard's rho algorithm to find a non-trivial factor.

    Args:
        n: Composite odd integer.
        rng: Random generator.

    Returns:
        A non-trivial factor of n (not guaranteed to be prime).
    """
    if n % 2 == 0:
        return 2
    if n % 3 == 0:
        return 3

    while True:
        c = rng.randrange(1, n)
        x = rng.randrange(0, n)
        y = x
        d = 1

        def f(v: int, c_val: int) -> int:
            return (pow(v, 2, n) + c_val) % n

        while d == 1:
            x = f(x, c)
            y = f(f(y, c), c)
            d = math.gcd(abs(x - y), n)

        if d != n:
            return d


# ------------------------------------------------------------------------------
def factorize_pollard_rho(n: int, *, seed: int = 1) -> list[int]:
    """Factorize n using Pollard rho + Miller–Rabin.

    Args:
        n: Integer to factorize.
        seed: Random seed.

    Returns:
        List of (not necessarily sorted) prime factors.
    """
    if n < 2:
        return []

    rng = random.Random(seed)

    def _factor(m: int, out: list[int]) -> None:
        if m == 1:
            return
        if is_prime_deterministic_64(m):
            out.append(m)
            return
        d = pollard_rho(m, rng=rng)
        _factor(d, out)
        _factor(m // d, out)

    factors: list[int] = []
    _factor(n, factors)
    return factors


# ------------------------------------------------------------------------------
def format_factor_multiset(factors: list[int]) -> str:
    """Format prime factors as a multiplicative expression.

    Args:
        factors: List of prime factors.

    Returns:
        Compact string like "3^2 · 5 · 17".
    """
    if not factors:
        return "1"
    factors_sorted = sorted(factors)
    parts: list[str] = []
    i = 0
    while i < len(factors_sorted):
        p = factors_sorted[i]
        e = 1
        i += 1
        while i < len(factors_sorted) and factors_sorted[i] == p:
            e += 1
            i += 1
        parts.append(f"{p}" if e == 1 else f"{p}^{e}")
    return " · ".join(parts)
