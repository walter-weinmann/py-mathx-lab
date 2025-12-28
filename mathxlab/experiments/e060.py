"""Experiment E060 entry point.

Keeps a stable module name (`e060`) while implementation lives in a descriptive
module file.
"""

from __future__ import annotations

from mathxlab.experiments.e060_jordan_totient_family import main  # re-export

# ------------------------------------------------------------------------------
__all__ = ["main"]


# ------------------------------------------------------------------------------
if __name__ == "__main__":
    raise SystemExit(main())
