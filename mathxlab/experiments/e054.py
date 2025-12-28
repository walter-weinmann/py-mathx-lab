"""Experiment E054 entry point.

Keeps a stable module name (`e054`) while implementation lives in a descriptive
module file.
"""

from __future__ import annotations

from mathxlab.experiments.e054_mobius_squarefree_density import main  # re-export

# ------------------------------------------------------------------------------
__all__ = ["main"]


# ------------------------------------------------------------------------------
if __name__ == "__main__":
    raise SystemExit(main())
