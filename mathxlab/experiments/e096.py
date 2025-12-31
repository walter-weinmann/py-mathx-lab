"""Experiment E096 entry point.

Keeps a stable module name (`e096`) while implementation lives in a descriptive
module file.
"""

from __future__ import annotations

from mathxlab.experiments.e096_tau_record_holders import main

# ------------------------------------------------------------------------------
__all__ = ["main"]


# ------------------------------------------------------------------------------
if __name__ == "__main__":
    raise SystemExit(main())
