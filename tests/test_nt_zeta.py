"""Unit tests for mathxlab.nt.zeta."""

from __future__ import annotations

import mpmath as mp
import pytest

from mathxlab.experiments._prime_utils import primes_up_to
from mathxlab.nt.zeta import (
    chi_factor,
    eta_series_partial,
    euler_product_partial,
    hardy_Z,
    riemann_von_mangoldt_count,
    zeta_series_partial,
    zeta_via_eta,
)


def test_zeta_series_partial_error_decreases() -> None:
    """Partial sums for s=2 should improve with larger N."""
    s = 2.0
    with mp.workdps(60):
        z_true = complex(mp.zeta(s))

    err_100 = abs(zeta_series_partial(s, 100) - z_true)
    err_2000 = abs(zeta_series_partial(s, 2000) - z_true)

    assert err_2000 < err_100


def test_eta_acceleration_reconstructs_zeta() -> None:
    """zeta(s) recovered from eta(s) should be reasonably accurate."""
    s = 1.1
    with mp.workdps(80):
        z_true = complex(mp.zeta(s))

    eta_5000 = eta_series_partial(s, 5000)
    z_eta = zeta_via_eta(s, eta_5000)

    assert abs(z_eta - z_true) < 1e-3


def test_chi_factor_functional_equation_residual_small() -> None:
    """Functional equation should hold to numerical precision."""
    s = 0.3 + 7.0j
    with mp.workdps(80):
        lhs = mp.zeta(mp.mpc(s))
        rhs = mp.mpc(chi_factor(s)) * mp.zeta(1 - mp.mpc(s))
        resid = abs(lhs - rhs)

    assert resid < 1e-9


def test_euler_product_partial_close_for_s_gt_1() -> None:
    """Euler product converges for Re(s)>1."""
    s = 2.0
    primes = primes_up_to(1000)
    with mp.workdps(60):
        z_true = complex(mp.zeta(s))
    approx = euler_product_partial(s, primes)
    assert abs(approx - z_true) < 1e-3


@pytest.mark.parametrize("k", [1, 2])
def test_hardy_Z_changes_sign_around_zeros(k: int) -> None:
    """Hardy Z(t) should flip sign around a simple zero."""
    with mp.workdps(60):
        t0 = float(mp.zetazero(k).imag)
    left = hardy_Z(t0 - 0.2)
    right = hardy_Z(t0 + 0.2)

    # Avoid the extremely unlikely case that evaluation hits exactly ~0.
    assert left != 0.0 or right != 0.0
    assert left * right < 0.0


def test_riemann_von_mangoldt_count_monotone() -> None:
    """The main term approximation should be increasing for T>0."""
    a = riemann_von_mangoldt_count(10.0)
    b = riemann_von_mangoldt_count(100.0)
    assert a > 0
    assert b > a
