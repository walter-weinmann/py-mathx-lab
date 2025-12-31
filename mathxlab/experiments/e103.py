"""Experiment E103 entry point.

Keeps a stable module name (`e103`) while implementation lives in a descriptive
module file.
"""

from __future__ import annotations

from mathxlab.experiments.e103_chebyshev_psi_prime_powers import main

# ------------------------------------------------------------------------------
__all__ = ["main"]


# ------------------------------------------------------------------------------
if __name__ == "__main__":
    raise SystemExit(main())
