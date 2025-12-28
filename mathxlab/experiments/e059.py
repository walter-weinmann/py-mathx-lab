"""Experiment E059 entry point.

Keeps a stable module name (`e059`) while implementation lives in a descriptive
module file.
"""

from __future__ import annotations

from mathxlab.experiments.e059_abundancy_sigma_over_n import main  # re-export

# ------------------------------------------------------------------------------
__all__ = ["main"]


# ------------------------------------------------------------------------------
if __name__ == "__main__":
    raise SystemExit(main())
