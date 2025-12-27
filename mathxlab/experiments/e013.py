"""Experiment E013 entry point.

Keeps a stable module name (`e013`) while implementation lives in a descriptive
module file.
"""

from __future__ import annotations

from mathxlab.experiments.e013_prime_polynomial_counterexample import main

# ------------------------------------------------------------------------------
__all__ = ["main"]


# ------------------------------------------------------------------------------
if __name__ == "__main__":
    raise SystemExit(main())
