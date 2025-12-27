"""Experiment E010 entry point.

Keeps a stable module name (`e010`) while implementation lives in a descriptive
module file.
"""

from __future__ import annotations

from mathxlab.experiments.e010_perfect_numbers_from_mersenne import main

# ------------------------------------------------------------------------------
__all__ = ["main"]


# ------------------------------------------------------------------------------
if __name__ == "__main__":
    raise SystemExit(main())
