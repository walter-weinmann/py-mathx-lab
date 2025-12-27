"""Experiment E031 entry point.

Keeps a stable module name (`e031`) while implementation lives in a descriptive
module file.
"""

from __future__ import annotations

from mathxlab.experiments.e031_admissibility_mod_obstructions import main

# ------------------------------------------------------------------------------
__all__ = ["main"]


# ------------------------------------------------------------------------------
if __name__ == "__main__":
    raise SystemExit(main())
