"""Experiment E045 entry point.

Keeps a stable module name (`e045`) while implementation lives in a descriptive
module file.
"""

from __future__ import annotations

from mathxlab.experiments.e045_mr_deterministic_64bit import main

# ------------------------------------------------------------------------------
__all__ = ["main"]


# ------------------------------------------------------------------------------
if __name__ == "__main__":
    raise SystemExit(main())
