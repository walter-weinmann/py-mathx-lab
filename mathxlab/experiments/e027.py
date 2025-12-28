"""Experiment E027 entry point.

Keeps a stable module name (`e027`) while implementation lives in a descriptive
module file.
"""

from __future__ import annotations

from mathxlab.experiments.e027_record_gaps_vs_log2 import main

# ------------------------------------------------------------------------------
__all__ = ["main"]


# ------------------------------------------------------------------------------
if __name__ == "__main__":
    raise SystemExit(main())
