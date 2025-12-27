"""Experiment E025 entry point.

Keeps a stable module name (`e025`) while implementation lives in a descriptive
module file.
"""

from __future__ import annotations

from mathxlab.experiments.e025_prime_gaps_nonmonotone import main

# ------------------------------------------------------------------------------
__all__ = ["main"]


# ------------------------------------------------------------------------------
if __name__ == "__main__":
    raise SystemExit(main())
