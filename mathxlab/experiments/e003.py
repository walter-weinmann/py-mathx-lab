"""Experiment E003 entry point.

Keeps a stable module name (`e003`) while implementation lives in a descriptive
module file.
"""

from __future__ import annotations

from mathxlab.experiments.e003_abundancy_index_landscape import main

# ------------------------------------------------------------------------------
__all__ = ["main"]


# ------------------------------------------------------------------------------
if __name__ == "__main__":
    raise SystemExit(main())
