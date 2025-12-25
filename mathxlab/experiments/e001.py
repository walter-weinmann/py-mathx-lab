"""Experiment E001 entry point.

Keeps a stable module name (`e001`) while implementation lives in a descriptive
module file.
"""

from __future__ import annotations

from mathxlab.experiments.e001_taylor_error_landscapes import main

# ------------------------------------------------------------------------------
__all__ = ["main"]


# ------------------------------------------------------------------------------
if __name__ == "__main__":
    raise SystemExit(main())
