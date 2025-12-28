"""Experiment E055 entry point.

Keeps a stable module name (`e055`) while implementation lives in a descriptive
module file.
"""

from __future__ import annotations

from mathxlab.experiments.e055_mertens_random_walk import main  # re-export

# ------------------------------------------------------------------------------
__all__ = ["main"]


# ------------------------------------------------------------------------------
if __name__ == "__main__":
    raise SystemExit(main())
