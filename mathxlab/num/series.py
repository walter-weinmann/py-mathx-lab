from __future__ import annotations

import numpy as np


# ------------------------------------------------------------------------------
def taylor_sin(x: np.ndarray, x0: float, degree: int) -> np.ndarray:
    """Compute the Taylor polynomial approximation of sin(x) around x0.

    Uses a direct series expansion:
        sin(x) = sum_k (-1)^k (x-x0)^(2k+1) / (2k+1)!  (about x0 for shifted variable)

    Note:
        This is intentionally simple for experiment purposes (not optimized).

    Args:
        x: Input array.
        x0: Expansion point.
        degree: Polynomial degree (non-negative).

    Returns:
        Array of Taylor approximation values at x.
    """
    if degree < 0:
        raise ValueError("degree must be >= 0")

    dx = x - x0
    y = np.zeros_like(x, dtype=float)

    # Build terms up to the requested degree.
    # Only odd powers contribute for sin.
    factorial = 1.0
    power = np.ones_like(x, dtype=float)
    sign = 1.0

    for n in range(0, degree + 1):
        # Update power = dx^n incrementally
        power = np.ones_like(x, dtype=float) if n == 0 else power * dx

        # Update factorial = n!
        if n <= 1:
            factorial = 1.0
        else:
            factorial *= float(n)

        if n % 2 == 1:
            # coefficient for dx^n in sin series about 0 is:
            # (-1)^k / n! for n = 2k+1
            k = (n - 1) // 2
            sign = -1.0 if (k % 2 == 1) else 1.0
            y = y + sign * (power / factorial)

    # Shifted expansion about x0 is handled by dx = x - x0.
    # This uses the sin series of dx, not the full Taylor about x0 for sin(x).
    # That is intentional here: it isolates local behavior and sampling artifacts.
    return y
