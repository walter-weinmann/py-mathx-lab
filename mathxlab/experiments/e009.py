"""Experiment E009 entry point.

Keeps a stable module name (`e009`) while implementation lives in a descriptive
module file.
"""

from __future__ import annotations

from mathxlab.experiments.e009_small_factor_scan import main

# ------------------------------------------------------------------------------
__all__ = ["main"]


# ------------------------------------------------------------------------------
if __name__ == "__main__":
    raise SystemExit(main())
