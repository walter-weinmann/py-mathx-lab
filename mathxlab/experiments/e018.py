"""Experiment E018 entry point.

Keeps a stable module name (`e018`) while implementation lives in a descriptive
module file.
"""

from __future__ import annotations

from mathxlab.experiments.e018_mr_base_choice_counterexamples import main

# ------------------------------------------------------------------------------
__all__ = ["main"]


# ------------------------------------------------------------------------------
if __name__ == "__main__":
    raise SystemExit(main())
