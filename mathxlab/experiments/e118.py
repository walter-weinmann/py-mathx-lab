"""Experiment E118 entry point.

Keeps a stable module name (`e118`) while implementation lives in a descriptive
module file.
"""

from __future__ import annotations

from mathxlab.experiments.e118_euler_product_breakdown import main

# ------------------------------------------------------------------------------
__all__ = ["main"]


# ------------------------------------------------------------------------------
if __name__ == "__main__":
    raise SystemExit(main())
