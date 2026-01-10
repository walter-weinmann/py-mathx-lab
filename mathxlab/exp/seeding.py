"""Deterministic seeding for experiments.

This is an alias module kept for compatibility with older experiment code.
Prefer `mathxlab.exp.random.set_global_seed` for new code.
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
        >>> from mathxlab.exp.seeding import set_global_seed
        >>> set_global_seed  # doctest: +SKIP
    """
    random.seed(seed)
    np.random.seed(seed)
