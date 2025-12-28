"""Dirichlet convolution helpers.

The Dirichlet convolution of arithmetic functions f and g is defined as:

    (f * g)(n) = ∑_{d | n} f(d) g(n/d)

This module provides a small helper to compute convolutions on a finite prefix
[1..N] for experiment purposes.

"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Callable


# ------------------------------------------------------------------------------
@dataclass(frozen=True)
class ConvolutionResult:
    """Result of a Dirichlet convolution computed on a prefix.

    Attributes:
        n_max: Maximum n (inclusive).
        values: List where values[n] = (f*g)(n) for 0..n_max.
    """

    n_max: int
    values: list[int]


# ------------------------------------------------------------------------------
def dirichlet_convolution(f: list[int], g: list[int], *, n_max: int) -> ConvolutionResult:
    """Compute the Dirichlet convolution (f*g)(n) for n <= n_max.

    The inputs are expected to be lists indexed by n with at least n_max+1 entries.

    Args:
        f: Function values f[n].
        g: Function values g[n].
        n_max: Maximum n.

    Returns:
        ConvolutionResult with values list.

    Raises:
        ValueError: If input lists are too short.
    """
    if len(f) <= n_max or len(g) <= n_max:
        raise ValueError("Input lists must have length >= n_max+1")

    h = [0] * (n_max + 1)
    for d in range(1, n_max + 1):
        fd = f[d]
        if fd == 0:
            continue
        for m in range(d, n_max + 1, d):
            h[m] += fd * g[m // d]
    return ConvolutionResult(n_max=n_max, values=h)


# ------------------------------------------------------------------------------
def epsilon(n_max: int) -> list[int]:
    """Return the identity element ε for Dirichlet convolution on [0..n_max].

    ε(1) = 1, ε(n)=0 for n != 1.

    Args:
        n_max: Maximum n.

    Returns:
        List eps with eps[1]=1.
    """
    eps = [0] * (n_max + 1)
    if n_max >= 1:
        eps[1] = 1
    return eps


# ------------------------------------------------------------------------------
def ones(n_max: int) -> list[int]:
    """Return the constant-one function 1(n)=1 for n>=1.

    Args:
        n_max: Maximum n.

    Returns:
        List one with one[n]=1 for n>=1.
    """
    one = [0] * (n_max + 1)
    for n in range(1, n_max + 1):
        one[n] = 1
    return one


# ------------------------------------------------------------------------------
def identity(n_max: int) -> list[int]:
    """Return the identity arithmetic function id(n)=n.

    Args:
        n_max: Maximum n.

    Returns:
        List id with id[n]=n.
    """
    out = [0] * (n_max + 1)
    for n in range(1, n_max + 1):
        out[n] = n
    return out
