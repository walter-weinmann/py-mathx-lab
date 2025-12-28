"""Experiment E026 entry point.

Keeps a stable module name (`e026`) while implementation lives in a descriptive
module file.
"""

from __future__ import annotations

from mathxlab.experiments.e026_normalized_prime_gaps import main

# ------------------------------------------------------------------------------
__all__ = ["main"]


# ------------------------------------------------------------------------------
if __name__ == "__main__":
    raise SystemExit(main())
