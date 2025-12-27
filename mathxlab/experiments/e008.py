"""Experiment E008 entry point.

Keeps a stable module name (`e008`) while implementation lives in a descriptive
module file.
"""

from __future__ import annotations

from mathxlab.experiments.e008_lucas_lehmer_scan import main

# ------------------------------------------------------------------------------
__all__ = ["main"]


# ------------------------------------------------------------------------------
if __name__ == "__main__":
    raise SystemExit(main())
