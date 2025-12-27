"""Experiment E035 entry point.

Keeps a stable module name (`e035`) while implementation lives in a descriptive
module file.
"""

from __future__ import annotations

from mathxlab.experiments.e035_primes_in_ap import main

# ------------------------------------------------------------------------------
__all__ = ["main"]


# ------------------------------------------------------------------------------
if __name__ == "__main__":
    raise SystemExit(main())
