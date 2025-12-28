"""Experiment E051 entry point.

Keeps a stable module name (`e051`) while implementation lives in a descriptive
module file.
"""

from __future__ import annotations

from mathxlab.experiments.e051_semiprimes_factorization import main

# ------------------------------------------------------------------------------
__all__ = ["main"]


# ------------------------------------------------------------------------------
if __name__ == "__main__":
    raise SystemExit(main())
