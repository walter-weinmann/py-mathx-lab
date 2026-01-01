"""Experiment E124 entry point.

Keeps a stable module name (`e124`) while implementation lives in a descriptive
module file.
"""

from __future__ import annotations

from mathxlab.experiments.e124_klauber_triangle import main

# ------------------------------------------------------------------------------
__all__ = ["main"]


# ------------------------------------------------------------------------------
if __name__ == "__main__":
    raise SystemExit(main())
