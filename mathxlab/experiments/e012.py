"""E012 entry point.

Keeps a stable module name (`e012`) while implementation lives in a descriptive
module file.
"""

from __future__ import annotations

from mathxlab.experiments.e012_fermat_pseudoprimes import main

# ------------------------------------------------------------------------------
__all__ = ["main"]


# ------------------------------------------------------------------------------
if __name__ == "__main__":
    raise SystemExit(main())
