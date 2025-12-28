"""Experiment E047 entry point.

Keeps a stable module name (`e047`) while implementation lives in a descriptive
module file.
"""

from __future__ import annotations

from mathxlab.experiments.e047_fermat_numbers import main

# ------------------------------------------------------------------------------
__all__ = ["main"]


# ------------------------------------------------------------------------------
if __name__ == "__main__":
    raise SystemExit(main())
