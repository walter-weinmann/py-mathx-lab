"""Experiment E108 entry point.

Keeps a stable module name (`e108`) while implementation lives in a descriptive
module file.
"""

from __future__ import annotations

from mathxlab.experiments.e108_dirichlet_orthogonality_heatmap import main

# ------------------------------------------------------------------------------
__all__ = ["main"]


# ------------------------------------------------------------------------------
if __name__ == "__main__":
    raise SystemExit(main())
