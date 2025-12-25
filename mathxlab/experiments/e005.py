"""Experiment E005 entry point.

Keeps a stable module name (`e005`) while implementation lives in a descriptive
module file.
"""

from __future__ import annotations

from mathxlab.experiments.e005_odd_perfect_filter_pipeline import main

# ------------------------------------------------------------------------------
__all__ = ["main"]


# ------------------------------------------------------------------------------
if __name__ == "__main__":
    raise SystemExit(main())
