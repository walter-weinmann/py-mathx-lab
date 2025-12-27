"""Experiment E011 entry point.

Keeps a stable module name (`e011`) while implementation lives in a descriptive
module file.
"""

from __future__ import annotations

from mathxlab.experiments.e011_mersenne_prime_heuristic import main

# ------------------------------------------------------------------------------
__all__ = ["main"]


# ------------------------------------------------------------------------------
if __name__ == "__main__":
    raise SystemExit(main())
