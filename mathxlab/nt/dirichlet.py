"""Dirichlet characters and small numerical helpers.

This module provides a compact, experiment-friendly implementation of Dirichlet
characters modulo ``q``:

- Enumeration of all characters modulo ``q`` using CRT factorization.
- Fast evaluation ``chi(n)`` for many ``n`` via precomputed discrete logs on
  each prime-power component.
- Simple conductor detection for small moduli (used to classify primitive vs.
  imprimitive characters).

The implementation targets small and medium moduli (typically ``q <= 200``) that
occur in educational and exploratory experiments. It is not meant to be a
high-performance algebra system.

References:
    - H. Davenport, *Multiplicative Number Theory*.
    - K. Ireland and M. Rosen, *A Classical Introduction to Modern Number Theory*.
"""

from __future__ import annotations

import itertools
from dataclasses import dataclass
from math import gcd
from typing import cast

import numpy as np

__all__ = [
    "DirichletCharacter",
    "all_characters",
    "character_table",
    "conductor",
    "euler_phi",
    "orthogonality_matrix",
    "reduced_residues",
]


# ------------------------------------------------------------------------------
def _factor_prime_powers(n: int) -> list[tuple[int, int, int]]:
    """Factor ``n`` into prime-power components.

    Args:
        n: Integer to factor (>= 1).

    Returns:
        List of tuples ``(p, k, p**k)`` for each prime factor.
    """
    if n < 1:
        raise ValueError("n must be >= 1")
    x = n
    out: list[tuple[int, int, int]] = []
    p = 2
    while p * p <= x:
        if x % p == 0:
            k = 0
            m = 1
            while x % p == 0:
                x //= p
                k += 1
                m *= p
            out.append((p, k, m))
        p += 1 if p == 2 else 2
    if x > 1:
        out.append((x, 1, x))
    return out


# ------------------------------------------------------------------------------
def euler_phi(n: int) -> int:
    """
    Compute Euler's totient φ(n) by prime factorization.

    Args:
        n: Positive integer.

    Returns:
        φ(n).

    Examples:
        >>> from mathxlab.nt.dirichlet import euler_phi
        >>> euler_phi  # doctest: +SKIP
    """
    if n < 1:
        raise ValueError("n must be >= 1")
    if n == 1:
        return 1
    phi = n
    for p, _, _ in _factor_prime_powers(n):
        phi = (phi // p) * (p - 1)
    return phi


# ------------------------------------------------------------------------------
def reduced_residues(q: int) -> list[int]:
    """
    Return the reduced residue system modulo ``q`` (sorted).

    Args:
        q: Modulus (>= 1).

    Returns:
        List of ``a`` in ``[1, q]`` with ``gcd(a, q) = 1``.

    Examples:
        >>> from mathxlab.nt.dirichlet import reduced_residues
        >>> reduced_residues  # doctest: +SKIP
    """
    if q < 1:
        raise ValueError("q must be >= 1")
    return [a for a in range(1, q + 1) if gcd(a, q) == 1]


# ------------------------------------------------------------------------------
def _primitive_root_prime_power(p: int, k: int) -> int:
    """Find a primitive root modulo ``p**k`` for odd prime ``p``.

    Args:
        p: Odd prime.
        k: Exponent (>= 1).

    Returns:
        A primitive root modulo ``p**k``.

    Raises:
        ValueError: If no primitive root is found (should not happen for odd p).
    """
    if p % 2 == 0:
        raise ValueError("p must be odd")
    if k < 1:
        raise ValueError("k must be >= 1")
    m = p**k
    order = euler_phi(m)
    # Factor order to test generator condition.
    factors = [pp for pp, _, _ in _factor_prime_powers(order)]
    for g in range(2, m):
        if gcd(g, m) != 1:
            continue
        ok = True
        for r in factors:
            if pow(g, order // r, m) == 1:
                ok = False
                break
        if ok:
            return g
    raise ValueError(f"no primitive root found for p^k = {p}^{k}")


# ------------------------------------------------------------------------------
@dataclass(frozen=True, slots=True)
class _Component:
    """Prime-power component for character evaluation.

    Attributes:
        modulus: Prime-power modulus m = p**k.
        params: Iterable of parameter tuples that enumerate all characters on this
            component.
    """

    modulus: int
    params: tuple[tuple[int, ...], ...]

    def value(self, *, n: int, param: tuple[int, ...]) -> complex:
        """Evaluate the component character at n (mod modulus)."""
        raise NotImplementedError


# ------------------------------------------------------------------------------
@dataclass(frozen=True, slots=True)
class _OddPrimePowerComponent(_Component):
    """Character component for odd prime powers (cyclic unit group)."""

    p: int
    k: int
    gen: int
    order: int
    log_map: dict[int, int]

    @staticmethod
    def build(*, p: int, k: int) -> _OddPrimePowerComponent:
        """Build component data for modulus p**k (odd prime)."""
        m = p**k
        order = euler_phi(m)
        gen = _primitive_root_prime_power(p, k)
        # Precompute discrete logs for all units: gen^t mod m.
        log_map: dict[int, int] = {}
        x = 1
        for t in range(order):
            log_map[x] = t
            x = (x * gen) % m
        params = tuple((a,) for a in range(order))  # χ(gen) = exp(2πi a / order)
        return _OddPrimePowerComponent(
            modulus=m,
            params=params,
            p=p,
            k=k,
            gen=gen,
            order=order,
            log_map=log_map,
        )

    def value(self, *, n: int, param: tuple[int, ...]) -> complex:
        a = param[0]
        r = n % self.modulus
        if gcd(r, self.modulus) != 1:
            return 0.0 + 0.0j
        t = self.log_map[r]
        angle = 2.0 * np.pi * (a * t % self.order) / self.order
        return complex(np.cos(angle), np.sin(angle))


# ------------------------------------------------------------------------------
@dataclass(frozen=True, slots=True)
class _TwoPowerComponent(_Component):
    """Character component for powers of two.

    For k >= 3, (Z/2^kZ)^* ~= C2 x C_{2^{k-2}} and can be generated by -1 and 5.
    """

    k: int
    order_cyc: int
    gen_cyc: int
    log_cyc: dict[int, int]

    @staticmethod
    def build(*, k: int) -> _TwoPowerComponent:
        """Build component data for modulus 2**k."""
        if k < 1:
            raise ValueError("k must be >= 1")
        m = 2**k
        if k == 1:
            # Units {1}: only the trivial character.
            return _TwoPowerComponent(
                modulus=m, params=((0,),), k=k, order_cyc=1, gen_cyc=1, log_cyc={1: 0}
            )
        if k == 2:
            # Units {1, 3} ≅ C2 generated by 3.
            gen = 3
            order = 2
            log_map = {1: 0, 3: 1}
            params = tuple((a,) for a in range(order))
            return _TwoPowerComponent(
                modulus=m, params=params, k=k, order_cyc=order, gen_cyc=gen, log_cyc=log_map
            )

        # k >= 3: use gen_cyc=5 (order 2^{k-2}) and sign generator -1 (order 2).
        order_cyc = 2 ** (k - 2)
        gen_cyc = 5 % m
        log_cyc: dict[int, int] = {}
        x = 1
        for t in range(order_cyc):
            log_cyc[x] = t
            x = (x * gen_cyc) % m

        params_list: list[tuple[int, int]] = []
        for a_sign in (0, 1):
            for b in range(order_cyc):
                params_list.append((a_sign, b))
        return _TwoPowerComponent(
            modulus=m,
            params=tuple(params_list),
            k=k,
            order_cyc=order_cyc,
            gen_cyc=gen_cyc,
            log_cyc=log_cyc,
        )

    def _exponents(self, r: int) -> tuple[int, int]:
        """Return (e, t) with r ≡ (-1)^e * gen_cyc^t (mod 2^k)."""
        m = self.modulus
        if self.k <= 2:
            # k=1 trivial, k=2 cyclic
            t = self.log_cyc[r]
            return 0, t

        if gcd(r, m) != 1:
            raise ValueError("r must be a unit")
        # Try e=0 then e=1.
        if r in self.log_cyc:
            return 0, self.log_cyc[r]
        r2 = (-r) % m
        if r2 in self.log_cyc:
            return 1, self.log_cyc[r2]
        raise ValueError("unit not representable via generators (should not happen)")

    def value(self, *, n: int, param: tuple[int, ...]) -> complex:
        r = n % self.modulus
        if gcd(r, self.modulus) != 1:
            return 0.0 + 0.0j

        if self.k == 1:
            return 1.0 + 0.0j

        if self.k == 2:
            a = param[0]
            t = self.log_cyc[r]
            angle = 2.0 * np.pi * (a * t % self.order_cyc) / self.order_cyc
            return complex(np.cos(angle), np.sin(angle))

        a_sign, b = param
        e, t = self._exponents(r)
        sign = -1.0 if (a_sign == 1 and e == 1) else 1.0
        angle = 2.0 * np.pi * (b * t % self.order_cyc) / self.order_cyc
        base = complex(np.cos(angle), np.sin(angle))
        return sign * base


# ------------------------------------------------------------------------------
def _build_components(q: int) -> list[_Component]:
    """Build prime-power components for modulus q."""
    comps: list[_Component] = []
    for p, k, _m in _factor_prime_powers(q):
        if p == 2:
            comps.append(_TwoPowerComponent.build(k=k))
        else:
            comps.append(_OddPrimePowerComponent.build(p=p, k=k))
    return comps


# ------------------------------------------------------------------------------
@dataclass(frozen=True, slots=True)
class DirichletCharacter:
    """
    Dirichlet character modulo q.

    The character is stored as a product of prime-power component characters.

    Attributes:
        modulus: Modulus q.
        params: Parameter tuples, one per prime-power component.

    Examples:
        >>> from mathxlab.nt.dirichlet import DirichletCharacter
        >>> DirichletCharacter  # doctest: +SKIP
    """

    modulus: int
    params: tuple[tuple[int, ...], ...]
    _components: tuple[_Component, ...]

    def __call__(self, n: int) -> complex:
        """Evaluate χ(n).

        Args:
            n: Integer input.

        Returns:
            Complex value of χ(n). Returns 0 if gcd(n, q) > 1.
        """
        q = self.modulus
        r = n % q
        if gcd(r, q) != 1:
            return 0.0 + 0.0j
        val = 1.0 + 0.0j
        for comp, par in zip(self._components, self.params, strict=True):
            val *= comp.value(n=r, param=par)
        return val

    @property
    def is_principal(self) -> bool:
        """Return True if χ is the principal character."""
        # Principal means all component parameters are 0.
        return all(all(x == 0 for x in par) for par in self.params)

    def table(self) -> np.ndarray:
        """Return the character table row for residues 0..q-1.

        Returns:
            A complex NumPy array of shape (q,) containing χ(0), χ(1), ..., χ(q-1).
        """
        q = self.modulus
        return np.array([self(n) for n in range(q)], dtype=np.complex128)

    @property
    def conductor(self) -> int:
        """Return the conductor of the character.

        Returns:
            The smallest f | q such that χ(n) depends only on n mod f.
        """
        return conductor(self)

    @property
    def is_primitive(self) -> bool:
        """Return True if the character is primitive.

        Returns:
            True iff conductor(χ) == q.
        """
        return self.conductor == self.modulus


# ------------------------------------------------------------------------------
def all_characters(q: int) -> list[DirichletCharacter]:
    """
    Enumerate all Dirichlet characters modulo q.

    Args:
        q: Modulus (>= 1).

    Returns:
        List of DirichletCharacter objects of length φ(q).

    Examples:
        >>> from mathxlab.nt.dirichlet import all_characters
        >>> chars = all_characters(5)
        >>> len(chars)
        4
    """
    if q < 1:
        raise ValueError("q must be >= 1")
    comps = _build_components(q)
    param_spaces = [comp.params for comp in comps]
    chars: list[DirichletCharacter] = []
    for params in itertools.product(*param_spaces):
        chars.append(DirichletCharacter(modulus=q, params=tuple(params), _components=tuple(comps)))
    # Stable order: principal first (optional)
    chars.sort(key=lambda c: 0 if c.is_principal else 1)
    return chars


# ------------------------------------------------------------------------------
def character_table(q: int) -> np.ndarray:
    """
    Return the full character table as a matrix.

    Args:
        q: Modulus.

    Returns:
        Complex matrix of shape (φ(q), q) where rows are characters and columns
        are residues 0..q-1.

    Examples:
        >>> from mathxlab.nt.dirichlet import character_table
        >>> character_table  # doctest: +SKIP
    """
    chars = all_characters(q)
    return np.vstack([c.table() for c in chars])


# ------------------------------------------------------------------------------
def conductor(chi: DirichletCharacter) -> int:
    """
    Compute the conductor of a character by brute-force divisor checks.

    The conductor is the smallest f | q such that χ(n) depends only on n mod f.

    This routine is intended for small q and experiment use.

    Args:
        chi: Character modulo q.

    Returns:
        The conductor f.

    Examples:
        >>> from mathxlab.nt.dirichlet import conductor
        >>> conductor  # doctest: +SKIP
    """
    q = chi.modulus
    # Enumerate divisors.
    divs = []
    for d in range(1, q + 1):
        if q % d == 0:
            divs.append(d)
    for f in divs:
        ok = True
        for a in range(q):
            if gcd(a, q) != 1:
                continue
            va = chi(a)
            for b in range(q):
                if a % f == b % f and gcd(b, q) == 1 and abs(va - chi(b)) > 1e-12:
                    ok = False
                    break
            if not ok:
                break
        if ok:
            return f
    return q


# ------------------------------------------------------------------------------
def orthogonality_matrix(q: int) -> np.ndarray:
    """
    Compute the character orthogonality matrix for modulus q.

    The matrix entries are:
        M[i,j] = (1/φ(q)) * ∑_{a mod q, gcd(a,q)=1} χ_i(a) conj(χ_j(a))

    For a correct implementation, M should be the identity.

    Args:
        q: Modulus.

    Returns:
        Complex matrix of shape (φ(q), φ(q)).

    Examples:
        >>> from mathxlab.nt.dirichlet import orthogonality_matrix
        >>> orthogonality_matrix  # doctest: +SKIP
    """
    chars = all_characters(q)
    rr = reduced_residues(q)
    phi_q = len(rr)
    vals = np.array([[c(a) for a in rr] for c in chars], dtype=np.complex128)
    res = (vals @ np.conjugate(vals).T) / float(phi_q)
    return cast(np.ndarray, res.astype(np.complex128))
