"""Experiment E021 entry point.

Keeps a stable module name (`e021`) while implementation lives in a descriptive
module file.
"""

from __future__ import annotations

from mathxlab.experiments.e021_pi_explicit_bounds_sanity import main

# ------------------------------------------------------------------------------
__all__ = ["main"]


# ------------------------------------------------------------------------------
if __name__ == "__main__":
    raise SystemExit(main())
