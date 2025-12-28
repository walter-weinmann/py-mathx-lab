"""Experiment E049 entry point.

Keeps a stable module name (`e049`) while implementation lives in a descriptive
module file.
"""

from __future__ import annotations

from mathxlab.experiments.e049_wieferich_primes import main

# ------------------------------------------------------------------------------
__all__ = ["main"]


# ------------------------------------------------------------------------------
if __name__ == "__main__":
    raise SystemExit(main())
