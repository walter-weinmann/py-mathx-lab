"""Experiment E044 entry point.

Keeps a stable module name (`e044`) while implementation lives in a descriptive
module file.
"""

from __future__ import annotations

from mathxlab.experiments.e044_ss_vs_mr import main

# ------------------------------------------------------------------------------
__all__ = ["main"]


# ------------------------------------------------------------------------------
if __name__ == "__main__":
    raise SystemExit(main())
