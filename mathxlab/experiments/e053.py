"""Experiment E053 entry point.

Keeps a stable module name (`e053`) while implementation lives in a descriptive
module file.
"""

from __future__ import annotations

from mathxlab.experiments.e053_inverse_totient_multiplicity import main  # re-export

# ------------------------------------------------------------------------------
__all__ = ["main"]


# ------------------------------------------------------------------------------
if __name__ == "__main__":
    raise SystemExit(main())
