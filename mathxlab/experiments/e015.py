"""Experiment E015 entry point.

Keeps a stable module name (`e015`) while implementation lives in a descriptive
module file.
"""

from __future__ import annotations

from mathxlab.experiments.e015_wilson_test_infeasibility import main

# ------------------------------------------------------------------------------
__all__ = ["main"]


# ------------------------------------------------------------------------------
if __name__ == "__main__":
    raise SystemExit(main())
