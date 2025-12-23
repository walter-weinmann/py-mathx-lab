import random

import numpy as np

from mathxlab.exp.seeding import set_global_seed


def test_set_global_seed() -> None:
    seed = 42
    set_global_seed(seed)

    # Check random
    r1 = random.random()
    # Check numpy
    n1 = np.random.rand()

    # Re-seed with same value
    set_global_seed(seed)
    r2 = random.random()
    n2 = np.random.rand()

    assert r1 == r2
    assert n1 == n2


def test_different_seeds_different_results() -> None:
    set_global_seed(42)
    r1 = random.random()

    set_global_seed(43)
    r2 = random.random()

    assert r1 != r2
