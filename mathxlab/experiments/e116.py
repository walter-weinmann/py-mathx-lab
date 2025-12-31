"""Experiment E116 entry point.

Keeps a stable module name (`e116`) while implementation lives in a descriptive
module file.
"""

from __future__ import annotations

from mathxlab.experiments.e116_zero_count_vs_rvm import main

# ------------------------------------------------------------------------------
__all__ = ["main"]


# ------------------------------------------------------------------------------
if __name__ == "__main__":
    raise SystemExit(main())
