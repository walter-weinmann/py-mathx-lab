"""Experiment E032 entry point.

Keeps a stable module name (`e032`) while implementation lives in a descriptive
module file.
"""

from __future__ import annotations

from mathxlab.experiments.e032_triplets_quadruplets_counts import main

# ------------------------------------------------------------------------------
__all__ = ["main"]


# ------------------------------------------------------------------------------
if __name__ == "__main__":
    raise SystemExit(main())
