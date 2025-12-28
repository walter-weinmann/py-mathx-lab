"""Experiment E028 entry point.

Keeps a stable module name (`e028`) while implementation lives in a descriptive
module file.
"""

from __future__ import annotations

from mathxlab.experiments.e028_jumping_champions import main

# ------------------------------------------------------------------------------
__all__ = ["main"]


# ------------------------------------------------------------------------------
if __name__ == "__main__":
    raise SystemExit(main())
