"""Experiment E125 entry point.

Keeps a stable module name (`e125`) while implementation lives in a descriptive
module file.
"""

from __future__ import annotations

from mathxlab.experiments.e125_sacks_spiral import main

# ------------------------------------------------------------------------------
__all__ = ["main"]


# ------------------------------------------------------------------------------
if __name__ == "__main__":
    raise SystemExit(main())
