"""Experiment E113 entry point.

Keeps a stable module name (`e113`) while implementation lives in a descriptive
module file.
"""

from __future__ import annotations

from mathxlab.experiments.e113_first_prime_per_residue import main

# ------------------------------------------------------------------------------
__all__ = ["main"]


# ------------------------------------------------------------------------------
if __name__ == "__main__":
    raise SystemExit(main())
