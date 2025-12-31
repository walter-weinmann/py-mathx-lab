"""Experiment E107 entry point.

Keeps a stable module name (`e107`) while implementation lives in a descriptive
module file.
"""

from __future__ import annotations

from mathxlab.experiments.e107_dirichlet_conductor_histogram import main

# ------------------------------------------------------------------------------
__all__ = ["main"]


# ------------------------------------------------------------------------------
if __name__ == "__main__":
    raise SystemExit(main())
