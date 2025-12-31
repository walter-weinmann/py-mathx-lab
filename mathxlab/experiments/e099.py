"""Experiment E099 entry point.

Keeps a stable module name (`e099`) while implementation lives in a descriptive
module file.
"""

from __future__ import annotations

from mathxlab.experiments.e099_jordan_totient_atlas import main

# ------------------------------------------------------------------------------
__all__ = ["main"]


# ------------------------------------------------------------------------------
if __name__ == "__main__":
    raise SystemExit(main())
