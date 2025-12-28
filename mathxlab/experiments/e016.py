"""Experiment E016 entry point.

Keeps a stable module name (`e016`) while implementation lives in a descriptive
module file.
"""

from __future__ import annotations

from mathxlab.experiments.e016_trial_division_vs_mr import main

# ------------------------------------------------------------------------------
__all__ = ["main"]


# ------------------------------------------------------------------------------
if __name__ == "__main__":
    raise SystemExit(main())
