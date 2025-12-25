"""Experiment E006 entry point.

Keeps a stable module name (`e006`) while implementation lives in a descriptive
module file.
"""

from __future__ import annotations

from mathxlab.experiments.e006_near_misses import main

# ------------------------------------------------------------------------------
__all__ = ["main"]


# ------------------------------------------------------------------------------
if __name__ == "__main__":
    raise SystemExit(main())
