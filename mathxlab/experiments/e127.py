"""Experiment E127 entry point.

Keeps a stable module name (`e127`) while implementation lives in a descriptive
module file.
"""

from __future__ import annotations

from mathxlab.experiments.e127_quadratic_prime_streak_atlas import main

# ------------------------------------------------------------------------------
__all__ = ["main"]


# ------------------------------------------------------------------------------
if __name__ == "__main__":
    raise SystemExit(main())
