"""Experiment E034 entry point.

Keeps a stable module name (`e034`) while implementation lives in a descriptive
module file.
"""

from __future__ import annotations

from mathxlab.experiments.e034_twin_window_variance import main

# ------------------------------------------------------------------------------
__all__ = ["main"]


# ------------------------------------------------------------------------------
if __name__ == "__main__":
    raise SystemExit(main())
