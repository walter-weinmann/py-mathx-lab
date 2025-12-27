"""Experiment E033 entry point.

Keeps a stable module name (`e033`) while implementation lives in a descriptive
module file.
"""

from __future__ import annotations

from mathxlab.experiments.e033_bounded_gaps_vs_twins import main

# ------------------------------------------------------------------------------
__all__ = ["main"]


# ------------------------------------------------------------------------------
if __name__ == "__main__":
    raise SystemExit(main())
