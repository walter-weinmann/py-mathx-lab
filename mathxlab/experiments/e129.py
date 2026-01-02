"""Experiment E129 entry point.

Keeps a stable module name (`e129`) while implementation lives in a descriptive
module file.
"""

from __future__ import annotations

from mathxlab.experiments.e129_euler_lucky_constants import main

# ------------------------------------------------------------------------------
__all__ = ["main"]


# ------------------------------------------------------------------------------
if __name__ == "__main__":
    raise SystemExit(main())
