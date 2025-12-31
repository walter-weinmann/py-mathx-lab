"""Experiment E120 entry point.

Keeps a stable module name (`e120`) while implementation lives in a descriptive
module file.
"""

from __future__ import annotations

from mathxlab.experiments.e120_pretentious_distance_proxy import main

# ------------------------------------------------------------------------------
__all__ = ["main"]


# ------------------------------------------------------------------------------
if __name__ == "__main__":
    raise SystemExit(main())
