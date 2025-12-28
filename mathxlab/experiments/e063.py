"""Experiment E063 entry point.

Keeps a stable module name (`e063`) while implementation lives in a descriptive
module file.
"""

from __future__ import annotations

from mathxlab.experiments.e063_dirichlet_convolution_identities import main  # re-export

# ------------------------------------------------------------------------------
__all__ = ["main"]


# ------------------------------------------------------------------------------
if __name__ == "__main__":
    raise SystemExit(main())
