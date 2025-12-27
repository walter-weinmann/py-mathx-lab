"""Experiment E039 entry point.

Keeps a stable module name (`e039`) while implementation lives in a descriptive
module file.
"""

from __future__ import annotations

from mathxlab.experiments.e039_sophie_germain_safe_primes import main

# ------------------------------------------------------------------------------
__all__ = ["main"]


# ------------------------------------------------------------------------------
if __name__ == "__main__":
    raise SystemExit(main())
