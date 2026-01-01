"""Experiment E126 entry point.

Keeps a stable module name (`e126`) while implementation lives in a descriptive
module file.
"""

from __future__ import annotations

from mathxlab.experiments.e126_hexagonal_number_spiral import main

# ------------------------------------------------------------------------------
__all__ = ["main"]


# ------------------------------------------------------------------------------
if __name__ == "__main__":
    raise SystemExit(main())
