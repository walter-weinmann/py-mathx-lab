"""Experiment E041 entry point.

Keeps a stable module name (`e041`) while implementation lives in a descriptive
module file.
"""

from __future__ import annotations

from mathxlab.experiments.e041_fermat_numbers_counterexample import main

# ------------------------------------------------------------------------------
__all__ = ["main"]


# ------------------------------------------------------------------------------
if __name__ == "__main__":
    raise SystemExit(main())
