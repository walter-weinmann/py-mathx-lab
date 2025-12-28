"""Experiment E056 entry point.

Keeps a stable module name (`e056`) while implementation lives in a descriptive
module file.
"""

from __future__ import annotations

from mathxlab.experiments.e056_liouville_vs_mertens import main  # re-export

# ------------------------------------------------------------------------------
__all__ = ["main"]


# ------------------------------------------------------------------------------
if __name__ == "__main__":
    raise SystemExit(main())
