"""Experiment E022 entry point.

Keeps a stable module name (`e022`) while implementation lives in a descriptive
module file.
"""

from __future__ import annotations

from mathxlab.experiments.e022_prime_race_mod4 import main

# ------------------------------------------------------------------------------
__all__ = ["main"]


# ------------------------------------------------------------------------------
if __name__ == "__main__":
    raise SystemExit(main())
