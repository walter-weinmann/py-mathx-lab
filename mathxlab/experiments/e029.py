"""Experiment E029 entry point.

Keeps a stable module name (`e029`) while implementation lives in a descriptive
module file.
"""

from __future__ import annotations

from mathxlab.experiments.e029_twin_primes_heuristic import main

# ------------------------------------------------------------------------------
__all__ = ["main"]


# ------------------------------------------------------------------------------
if __name__ == "__main__":
    raise SystemExit(main())
