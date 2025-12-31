"""Experiment E112 entry point.

Keeps a stable module name (`e112`) while implementation lives in a descriptive
module file.
"""

from __future__ import annotations

from mathxlab.experiments.e112_prime_race_modq import main

# ------------------------------------------------------------------------------
__all__ = ["main"]


# ------------------------------------------------------------------------------
if __name__ == "__main__":
    raise SystemExit(main())
