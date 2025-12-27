"""Experiment E020 entry point.

Keeps a stable module name (`e020`) while implementation lives in a descriptive
module file.
"""

from __future__ import annotations

from mathxlab.experiments.e020_pi_vs_li_numeric import main

# ------------------------------------------------------------------------------
__all__ = ["main"]


# ------------------------------------------------------------------------------
if __name__ == "__main__":
    raise SystemExit(main())
