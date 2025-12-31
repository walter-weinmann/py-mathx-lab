"""Tests for Dirichlet characters."""

from __future__ import annotations

from math import gcd

import numpy as np

from mathxlab.nt.dirichlet import (
    DirichletCharacter,
    all_characters,
    character_table,
    euler_phi,
    orthogonality_matrix,
    reduced_residues,
)


def test_all_characters_count_matches_phi() -> None:
    """Number of Dirichlet characters mod q equals phi(q)."""
    q = 15
    chars = all_characters(q)
    assert len(chars) == euler_phi(q)


def test_character_table_shape() -> None:
    """character_table returns matrix of shape (phi(q), q)."""
    q = 12
    mat = character_table(q)
    assert mat.shape == (euler_phi(q), q)


def test_character_table_row_method_exists() -> None:
    """DirichletCharacter.table() exists and returns length q."""
    q = 10
    chi = all_characters(q)[0]
    row = chi.table()
    assert isinstance(chi, DirichletCharacter)
    assert row.shape == (q,)
    assert row.dtype == np.complex128


def test_principal_character_values() -> None:
    """Principal character is 1 on units and 0 on non-units."""
    q = 12
    chi0 = all_characters(q)[0]
    assert chi0.is_principal is True

    for n in range(q):
        v = chi0(n)
        if gcd(n, q) == 1:
            assert abs(v - (1.0 + 0.0j)) < 1e-12
        else:
            assert abs(v - (0.0 + 0.0j)) < 1e-12


def test_orthogonality_matrix_is_identity_approx() -> None:
    """Orthogonality matrix should be approximately identity."""
    q = 15
    m = orthogonality_matrix(q)
    eye = np.eye(euler_phi(q), dtype=np.complex128)
    err = np.max(np.abs(m - eye))
    assert err < 1e-10


def test_reduced_residues_matches_phi() -> None:
    """reduced_residues(q) should be a complete reduced residue system."""
    q = 10
    rr = reduced_residues(q)

    assert rr == [1, 3, 7, 9]
    assert rr == sorted(rr)
    assert len(rr) == euler_phi(q)
    assert len(set(rr)) == len(rr)
    assert all(1 <= a < q for a in rr)
    assert all(gcd(a, q) == 1 for a in rr)
