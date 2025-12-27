"""Experiment E007 entry point.

Keeps a stable module name (`e007`) while implementation lives in a descriptive
module file.
"""

from __future__ import annotations

from mathxlab.experiments.e007_mersenne_growth import main

# ------------------------------------------------------------------------------
__all__ = ["main"]


# ------------------------------------------------------------------------------
if __name__ == "__main__":
    raise SystemExit(main())
