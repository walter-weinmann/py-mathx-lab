"""Experiment E052 entry point.

Keeps a stable module name (`e052`) while implementation lives in a descriptive
module file.
"""

from __future__ import annotations

from mathxlab.experiments.e052_totient_ratio_landscape import main  # re-export

# ------------------------------------------------------------------------------
__all__ = ["main"]


# ------------------------------------------------------------------------------
if __name__ == "__main__":
    raise SystemExit(main())
