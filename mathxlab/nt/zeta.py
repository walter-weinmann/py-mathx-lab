"""Numerical helpers for the Riemann zeta function and related quantities.

The implementations are intentionally simple and designed for educational /
exploratory experiments (not for high-precision research computations).

The module uses `mpmath` internally and exposes a small set of helpers for:

- partial Dirichlet/eta series
- truncated Euler products
- the Hardy Z-function
- the main-term zero counting approximation N(T)
"""

from __future__ import annotations

from collections.abc import Iterable, Iterator
from contextlib import contextmanager
from dataclasses import dataclass

import mpmath as mp

__all__ = [
    "ZetaEvalSettings",
    "chi_factor",
    "eta_series_partial",
    "euler_product_partial",
    "hardy_Z",
    "mp_workdps",
    "riemann_von_mangoldt_count",
    "zeta_series_partial",
    "zeta_via_eta",
]


@dataclass(frozen=True, slots=True)
class ZetaEvalSettings:
    """
    Settings for zeta-related numerical evaluations.

    Args:
        dps: Decimal digits of precision used by mpmath during the computation.

    Examples:
        >>> from mathxlab.nt.zeta import ZetaEvalSettings
        >>> ZetaEvalSettings  # doctest: +SKIP
    """

    dps: int = 50


@contextmanager
def mp_workdps(dps: int) -> Iterator[None]:
    """
    Temporarily set the mpmath precision (decimal digits).

    Args:
        dps: Decimal digits of precision.

    Yields:
        None. The previous precision is restored on exit.

    Examples:
        >>> from mathxlab.nt.zeta import mp_workdps
        >>> mp_workdps  # doctest: +SKIP
    """
    old = mp.mp.dps
    mp.mp.dps = int(dps)
    try:
        yield
    finally:
        mp.mp.dps = old


def zeta_series_partial(
    s: complex, n_max: int, *, settings: ZetaEvalSettings | None = None
) -> complex:
    """
    Compute the partial Dirichlet series for the Riemann zeta function.

    This computes:
        sum_{n=1..n_max} n^{-s}

    Args:
        s: Complex exponent.
        n_max: Number of terms.
        settings: Optional evaluation settings.

    Returns:
        Complex partial sum as a Python complex number.

    Examples:
        >>> from mathxlab.nt.zeta import zeta_series_partial
        >>> round(zeta_series_partial(2.0, 2000).real, 3)
        1.644
    """
    if n_max < 0:
        raise ValueError("n_max must be >= 0")
    if n_max == 0:
        return 0.0 + 0.0j

    cfg = settings or ZetaEvalSettings()
    with mp_workdps(cfg.dps):
        ss = mp.mpc(s)
        total = mp.mpc(0)
        for n in range(1, n_max + 1):
            total += mp.power(n, -ss)
        return complex(total)


def eta_series_partial(
    s: complex, n_max: int, *, settings: ZetaEvalSettings | None = None
) -> complex:
    """
    Compute the partial Dirichlet eta series.

    This computes:
        eta(s) = sum_{n=1..n_max} (-1)^{n-1} n^{-s}

    Args:
        s: Complex exponent.
        n_max: Number of terms.
        settings: Optional evaluation settings.

    Returns:
        Complex partial sum as a Python complex number.

    Examples:
        >>> from mathxlab.nt.zeta import eta_series_partial
        >>> eta_series_partial  # doctest: +SKIP
    """
    if n_max < 0:
        raise ValueError("n_max must be >= 0")
    if n_max == 0:
        return 0.0 + 0.0j

    cfg = settings or ZetaEvalSettings()
    with mp_workdps(cfg.dps):
        ss = mp.mpc(s)
        total = mp.mpc(0)
        sign = 1
        for n in range(1, n_max + 1):
            total += sign * mp.power(n, -ss)
            sign = -sign
        return complex(total)


def zeta_via_eta(s: complex, eta_value: complex) -> complex:
    """
    Recover zeta(s) from eta(s) via the identity.

    For s != 1:
        zeta(s) = eta(s) / (1 - 2^{1-s})

    Args:
        s: Complex argument.
        eta_value: Value of eta(s) (possibly a partial sum).

    Returns:
        Complex approximation of zeta(s).

    Examples:
        >>> from mathxlab.nt.zeta import zeta_via_eta
        >>> zeta_via_eta  # doctest: +SKIP
    """
    denom = 1.0 - complex(mp.power(2, 1 - mp.mpc(s)))
    if denom == 0:
        raise ZeroDivisionError("zeta_via_eta is singular at s=1")
    return eta_value / denom


def euler_product_partial(
    s: complex,
    primes: Iterable[int],
    *,
    settings: ZetaEvalSettings | None = None,
) -> complex:
    """
    Compute a partial Euler product approximation of zeta(s).

    This computes:
        prod_{p in primes} (1 - p^{-s})^{-1}

    Args:
        s: Complex argument.
        primes: Iterable of prime numbers.
        settings: Optional evaluation settings.

    Returns:
        Complex approximation as a Python complex.

    Examples:
        >>> from mathxlab.nt.zeta import euler_product_partial
        >>> euler_product_partial  # doctest: +SKIP
    """
    cfg = settings or ZetaEvalSettings()
    with mp_workdps(cfg.dps):
        ss = mp.mpc(s)
        prod = mp.mpc(1)
        for p in primes:
            pp = int(p)
            if pp <= 1:
                raise ValueError("primes must be integers >= 2")
            prod *= 1 / (1 - mp.power(pp, -ss))
        return complex(prod)


def chi_factor(s: complex, *, settings: ZetaEvalSettings | None = None) -> complex:
    """
    Compute the factor chi(s) in the functional equation of zeta.

    One convenient form is:
        zeta(s) = chi(s) * zeta(1 - s)

    where:
        chi(s) = 2^s * pi^{s-1} * sin(pi s / 2) * Gamma(1 - s)

    Args:
        s: Complex argument.
        settings: Optional evaluation settings.

    Returns:
        chi(s) as a Python complex.

    Examples:
        >>> from mathxlab.nt.zeta import chi_factor
        >>> chi_factor  # doctest: +SKIP
    """

    r"""Compute the factor chi(s) in the functional equation of zeta.

    One convenient form is:
        zeta(s) = chi(s) * zeta(1 - s)

    where:
        chi(s) = 2^s * pi^{s-1} * sin(pi s / 2) * Gamma(1 - s)

    Args:
        s: Complex argument.
        settings: Optional evaluation settings.

    Returns:
        chi(s) as a Python complex.
    """
    cfg = settings or ZetaEvalSettings()
    with mp_workdps(cfg.dps):
        ss = mp.mpc(s)
        return complex(
            mp.power(2, ss) * mp.power(mp.pi, ss - 1) * mp.sin(mp.pi * ss / 2) * mp.gamma(1 - ss)
        )


def hardy_Z(t: float, *, settings: ZetaEvalSettings | None = None) -> float:
    """Compute Hardy's Z-function at height t."""
    cfg = settings or ZetaEvalSettings()
    with mp_workdps(cfg.dps):
        return float(mp.siegelz(t))


def riemann_von_mangoldt_count(T: float) -> float:
    """Return the Riemann--von Mangoldt main term for N(T)."""
    if T <= 0:
        raise ValueError("T must be > 0")
    x = float(T) / (2.0 * float(mp.pi))
    return float(x * (mp.log(x) - 1.0) + 0.875)
