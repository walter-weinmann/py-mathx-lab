"""Experiment E019 entry point.

Keeps a stable module name (`e019`) while implementation lives in a descriptive
module file.
"""

from __future__ import annotations

from mathxlab.experiments.e019_prime_density_pnt import main

# ------------------------------------------------------------------------------
__all__ = ["main"]


# ------------------------------------------------------------------------------
if __name__ == "__main__":
    raise SystemExit(main())
