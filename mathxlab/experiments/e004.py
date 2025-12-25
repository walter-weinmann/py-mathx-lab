"""Experiment E004 entry point.

Keeps a stable module name (`e004`) while implementation lives in a descriptive
module file.
"""

from __future__ import annotations

from mathxlab.experiments.e004_sigma_benchmark import main

# ------------------------------------------------------------------------------
__all__ = ["main"]


# ------------------------------------------------------------------------------
if __name__ == "__main__":
    raise SystemExit(main())
