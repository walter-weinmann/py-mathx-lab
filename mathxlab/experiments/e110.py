"""Experiment E110 entry point.

Keeps a stable module name (`e110`) while implementation lives in a descriptive
module file.
"""

from __future__ import annotations

from mathxlab.experiments.e110_L_series_partial_sums import main

# ------------------------------------------------------------------------------
__all__ = ["main"]


# ------------------------------------------------------------------------------
if __name__ == "__main__":
    raise SystemExit(main())
