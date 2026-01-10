"""Deterministic seeding for experiments.

This module sets the global RNG state for both the standard library and NumPy.
Use it at the start of an experiment to make runs reproducible.
"""

from __future__ import annotations

import random

import numpy as np

__all__ = [
    "set_global_seed",
]


# ------------------------------------------------------------------------------
def set_global_seed(seed: int) -> None:
    """
    Set global seeds for deterministic experiment runs.

    Args:
        seed: Integer seed value.

    Examples:
        >>> from mathxlab.exp.random import set_global_seed
        >>> set_global_seed(123)
        >>> import numpy as np; float(np.random.rand(1)[0])
    """
    random.seed(seed)
    np.random.seed(seed)
