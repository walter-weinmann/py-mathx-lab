"""Experiment E117 entry point.

Keeps a stable module name (`e117`) while implementation lives in a descriptive
module file.
"""

from __future__ import annotations

from mathxlab.experiments.e117_functional_equation_check import main

# ------------------------------------------------------------------------------
__all__ = ["main"]


# ------------------------------------------------------------------------------
if __name__ == "__main__":
    raise SystemExit(main())
