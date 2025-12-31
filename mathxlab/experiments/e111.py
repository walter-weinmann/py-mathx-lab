"""Experiment E111 entry point.

Keeps a stable module name (`e111`) while implementation lives in a descriptive
module file.
"""

from __future__ import annotations

from mathxlab.experiments.e111_L_euler_product_vs_series import main

# ------------------------------------------------------------------------------
__all__ = ["main"]


# ------------------------------------------------------------------------------
if __name__ == "__main__":
    raise SystemExit(main())
