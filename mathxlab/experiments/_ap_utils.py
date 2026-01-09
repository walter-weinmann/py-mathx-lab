"""Utilities for arithmetic progression prime counting experiments.

This helper module provides small, dependency-light building blocks used in
E070+ experiments:

- prime counting in residue classes via numpy searchsorted,
- a simple logarithmic integral approximation Li(x) via trapezoidal rule.

The goal is to keep the experiments readable and consistent rather than to
provide the most accurate numerical methods.
"""

from __future__ import annotations

from typing import cast

import numpy as np


# ------------------------------------------------------------------------------
def counts_in_residue_class(*, primes: np.ndarray, q: int, a: int, xs: np.ndarray) -> np.ndarray:
    """Compute pi(x; q, a) for all x in xs.

    Args:
        primes: Sorted primes array.
        q: Modulus.
        a: Residue class.
        xs: Query points (increasing).

    Returns:
        Integer array pi where pi[i] = #{p <= xs[i] : p ≡ a (mod q)}.
    """
    if q < 1:
        raise ValueError("q must be >= 1")
    if xs.ndim != 1:
        raise ValueError("xs must be 1D")
    mask = (primes % q) == (a % q)
    p_a = primes[mask]
    return np.searchsorted(p_a, xs, side="right").astype(np.int64)


# ------------------------------------------------------------------------------
def li_trap(*, xs: np.ndarray, step: int = 200) -> np.ndarray:
    """Approximate Li(x) for x in xs via trapezoidal integration of 1/log t.

    This is a coarse approximation, sufficient for visual comparisons in the
    experiment ranges (typically <= a few million).

    Args:
        xs: Query points (1D increasing).
        step: Integration step size (in the same units as x).

    Returns:
        Float array Li(xs).
    """
    if xs.ndim != 1:
        raise ValueError("xs must be 1D")
    x_max = float(xs[-1])
    if x_max < 2.0:
        return np.zeros_like(xs, dtype=np.float64)

    # Integrate on a uniform grid.
    grid = np.arange(2.0, x_max + step, float(step), dtype=np.float64)
    f = 1.0 / np.log(grid)
    # trapezoid cumulative integral
    cum = np.zeros_like(grid)
    cum[1:] = np.cumsum(0.5 * (f[1:] + f[:-1]) * (grid[1:] - grid[:-1]))
    # interpolate to requested points
    return cast(np.ndarray, np.interp(xs, grid, cum).astype(np.float64))


# ------------------------------------------------------------------------------
def normalized_race_statistic(*, xs: np.ndarray, diff: np.ndarray) -> np.ndarray:
    """Compute a simple normalized race statistic.

    The normalization is a common heuristic:
        diff(x) * log(x) / sqrt(x)

    Args:
        xs: Sample points (x).
        diff: Difference array at those points.

    Returns:
        Normalized statistic.
    """
    x = np.maximum(xs, 2.0)
    res = diff.astype(np.float64) * np.log(x) / np.sqrt(x)
    return cast(np.ndarray, res.astype(np.float64))


# ------------------------------------------------------------------------------
def sample_grid(*, x_max: int, n: int = 600, log: bool = False) -> np.ndarray:
    """Create a sampling grid for x in [2, x_max].

    Args:
        x_max: Upper bound.
        n: Number of sample points.
        log: If True, use a log-spaced grid (geometric progression).

    Returns:
        Array of sample points (float64).
    """
    if x_max < 2:
        raise ValueError("x_max must be >= 2")
    if n < 2:
        raise ValueError("n must be >= 2")
    if log:
        xs = np.geomspace(2.0, float(x_max), n, dtype=np.float64)
    else:
        xs = np.linspace(2.0, float(x_max), n, dtype=np.float64)
    return xs
