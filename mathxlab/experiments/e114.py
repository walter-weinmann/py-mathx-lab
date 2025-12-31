"""Experiment E114 entry point.

Keeps a stable module name (`e114`) while implementation lives in a descriptive
module file.
"""

from __future__ import annotations

from mathxlab.experiments.e114_zeta_eta_truncation_error import main

# ------------------------------------------------------------------------------
__all__ = ["main"]


# ------------------------------------------------------------------------------
if __name__ == "__main__":
    raise SystemExit(main())
