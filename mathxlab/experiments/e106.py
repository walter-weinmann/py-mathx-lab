"""Experiment E106 entry point.

Keeps a stable module name (`e106`) while implementation lives in a descriptive
module file.
"""

from __future__ import annotations

from mathxlab.experiments.e106_dirichlet_characters_real_vs_complex import main

# ------------------------------------------------------------------------------
__all__ = ["main"]


# ------------------------------------------------------------------------------
if __name__ == "__main__":
    raise SystemExit(main())
