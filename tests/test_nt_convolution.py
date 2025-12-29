"""Unit tests for Dirichlet convolution helpers."""

from __future__ import annotations

import pytest

from mathxlab.nt.arithmetic import build_factor_sieve, compute_mobius
from mathxlab.nt.convolution import dirichlet_convolution, epsilon


def test_dirichlet_convolution_identities() -> None:
    """Check a few standard identities on a small range.

    We work on arrays indexed by n with a dummy 0th entry.
    """
    n_max = 200
    sieve = build_factor_sieve(n_max)
    mu = compute_mobius(n_max, sieve=sieve)

    ones = [0] + [1] * n_max
    eps = [0] + [0] * (n_max - 1)
    eps[1] = 1

    # 1 * mu = eps.
    res = dirichlet_convolution(ones, mu, n_max=n_max)
    conv = res.values
    assert conv[1] == 1
    for n in range(2, n_max + 1):
        assert conv[n] == 0


def test_dirichlet_convolution_commutes() -> None:
    """Dirichlet convolution is commutative."""
    n_max = 120
    a = [0, *range(1, n_max + 1)]
    b = [0, *((-1) ** n for n in range(1, n_max + 1))]

    assert (
        dirichlet_convolution(a, b, n_max=n_max).values
        == dirichlet_convolution(b, a, n_max=n_max).values
    )


def test_epsilon_function_basic_values() -> None:
    """epsilon() should be the identity for Dirichlet convolution."""
    assert epsilon(0) == [0]
    assert epsilon(1) == [0, 1]
    assert epsilon(5) == [0, 1, 0, 0, 0, 0]


def test_dirichlet_convolution_rejects_short_inputs() -> None:
    """Input arrays must include indices up to n_max."""
    # Need length >= n_max + 1.
    with pytest.raises(ValueError, match=r"length >= n_max\+1"):
        _ = dirichlet_convolution([0, 1], [0, 1], n_max=2)


def test_dirichlet_convolution_skips_zero_f_values() -> None:
    """Zero f[d] should be skipped quickly (branch coverage)."""
    n_max = 12
    # f has zeros at many divisors.
    f = [0] * (n_max + 1)
    f[1] = 1
    f[4] = 2
    g = [0] + [1] * n_max

    res = dirichlet_convolution(f, g, n_max=n_max).values
    # (f*g)(n) = sum_{d|n} f(d) g(n/d). Since g(.) = 1, this is sum_{d|n} f(d).
    assert res[1] == 1.0
    assert res[2] == 1.0  # only d=1 contributes
    assert res[4] == 3.0  # d=1 and d=4 contribute
    assert res[8] == 3.0  # d=1 and d=4 contribute
