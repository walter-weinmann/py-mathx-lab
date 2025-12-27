"""Experiment E046 entry point.

Keeps a stable module name (`e046`) while implementation lives in a descriptive
module file.
"""

from __future__ import annotations

from mathxlab.experiments.e046_prime_testing_pipeline import main

# ------------------------------------------------------------------------------
__all__ = ["main"]


# ------------------------------------------------------------------------------
if __name__ == "__main__":
    raise SystemExit(main())
