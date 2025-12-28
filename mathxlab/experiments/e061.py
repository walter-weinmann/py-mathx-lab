"""Experiment E061 entry point.

Keeps a stable module name (`e061`) while implementation lives in a descriptive
module file.
"""

from __future__ import annotations

from mathxlab.experiments.e061_chebyshev_psi_prime_powers import main  # re-export

# ------------------------------------------------------------------------------
__all__ = ["main"]


# ------------------------------------------------------------------------------
if __name__ == "__main__":
    raise SystemExit(main())
