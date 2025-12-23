import numpy as np
import pytest

from mathxlab.num.series import taylor_sin


def test_taylor_sin_degree_zero() -> None:
    x = np.array([0.0, 0.5, 1.0])
    # For sin(x) about 0, degree 0 should be just 0 (constant term)
    y = taylor_sin(x, x0=0.0, degree=0)
    assert np.allclose(y, 0.0)


def test_taylor_sin_degree_one() -> None:
    x = np.array([0.0, 0.5, 1.0])
    # For sin(x) about 0, degree 1 is x
    y = taylor_sin(x, x0=0.0, degree=1)
    assert np.allclose(y, x)


def test_taylor_sin_degree_three() -> None:
    x = np.array([0.0, 0.5, 1.0])
    # For sin(x) about 0, degree 3 is x - x^3/3!
    expected = x - (x**3) / 6.0
    y = taylor_sin(x, x0=0.0, degree=3)
    assert np.allclose(y, expected)


def test_taylor_sin_negative_degree() -> None:
    x = np.array([0.0, 1.0])
    with pytest.raises(ValueError, match="degree must be >= 0"):
        taylor_sin(x, x0=0.0, degree=-1)


def test_taylor_sin_shifted_x0() -> None:
    x = np.array([1.0, 1.5, 2.0])
    x0 = 1.0
    # The implementation uses dx = x - x0 and applies the sin(dx) series
    dx = x - x0
    expected = dx - (dx**3) / 6.0
    y = taylor_sin(x, x0=x0, degree=3)
    assert np.allclose(y, expected)


def test_taylor_sin_high_degree() -> None:
    x = np.array([0.1])
    # High degree should be very close to sin(x) for small x
    y = taylor_sin(x, x0=0.0, degree=10)
    assert np.allclose(y, np.sin(x))
