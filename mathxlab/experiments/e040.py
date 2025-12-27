"""Experiment E040 entry point.

Keeps a stable module name (`e040`) while implementation lives in a descriptive
module file.
"""

from __future__ import annotations

from mathxlab.experiments.e040_palindromic_primes_11 import main

# ------------------------------------------------------------------------------
__all__ = ["main"]


# ------------------------------------------------------------------------------
if __name__ == "__main__":
    raise SystemExit(main())
