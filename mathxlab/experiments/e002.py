"""Experiment E002 entry point.

Keeps a stable module name (`e002`) while implementation lives in a descriptive
module file.
"""

from __future__ import annotations

from mathxlab.experiments.e002_even_perfect_growth import main

# ------------------------------------------------------------------------------
__all__ = ["main"]


# ------------------------------------------------------------------------------
if __name__ == "__main__":
    raise SystemExit(main())
