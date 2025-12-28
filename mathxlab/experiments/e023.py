"""Experiment E023 entry point.

Keeps a stable module name (`e023`) while implementation lives in a descriptive
module file.
"""

from __future__ import annotations

from mathxlab.experiments.e023_residue_classes_modq import main

# ------------------------------------------------------------------------------
__all__ = ["main"]


# ------------------------------------------------------------------------------
if __name__ == "__main__":
    raise SystemExit(main())
