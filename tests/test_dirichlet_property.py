"""Property-based tests for Dirichlet characters.

These tests keep moduli small and examples few so they remain fast.
"""

from __future__ import annotations

from math import gcd

import numpy as np
import pytest
from hypothesis import given, settings
from hypothesis import strategies as st

from mathxlab.nt.dirichlet import all_characters, euler_phi, orthogonality_matrix

pytestmark = pytest.mark.property


@given(q=st.integers(min_value=2, max_value=30), n=st.integers(min_value=-200, max_value=200))
@settings(max_examples=40, deadline=None)
def test_character_periodic(q: int, n: int) -> None:
    """Every character is periodic with period q."""
    chars = all_characters(q)
    assert len(chars) == euler_phi(q)
    for chi in chars[: min(5, len(chars))]:
        assert chi(n) == chi(n + q)


@given(
    q=st.integers(min_value=2, max_value=30),
    a=st.integers(min_value=-50, max_value=50),
    b=st.integers(min_value=-50, max_value=50),
)
@settings(max_examples=35, deadline=None)
def test_character_multiplicative(q: int, a: int, b: int) -> None:
    """Principal character is multiplicative."""
    chi0 = all_characters(q)[0]
    assert chi0(a * b) == chi0(a) * chi0(b)


@given(q=st.integers(min_value=2, max_value=30), n=st.integers(min_value=0, max_value=200))
@settings(max_examples=40, deadline=None)
def test_character_zero_on_nonunits(q: int, n: int) -> None:
    """Principal character is 1 on units and 0 on non-units."""
    chi0 = all_characters(q)[0]
    v = chi0(n)
    if gcd(n, q) == 1:
        assert v == 1.0 + 0.0j
    else:
        assert v == 0.0 + 0.0j


@given(q=st.integers(min_value=2, max_value=25))
@settings(max_examples=25, deadline=None)
def test_orthogonality_matrix_property(q: int) -> None:
    """Orthogonality matrix should be close to identity."""
    m = orthogonality_matrix(q)
    eye = np.eye(m.shape[0], dtype=np.complex128)
    assert np.max(np.abs(m - eye)) < 1e-10
