from __future__ import annotations

import random

import numpy as np


# ------------------------------------------------------------------------------
def set_global_seed(seed: int) -> None:
    """Set global seeds for deterministic experiment runs.

    Args:
        seed: Integer seed value.
    """
    random.seed(seed)
    np.random.seed(seed)
