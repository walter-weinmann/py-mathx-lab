"""Experiment E115 entry point.

Keeps a stable module name (`e115`) while implementation lives in a descriptive
module file.
"""

from __future__ import annotations

from mathxlab.experiments.e115_hardy_Z_sign_changes_scan import main

# ------------------------------------------------------------------------------
__all__ = ["main"]


# ------------------------------------------------------------------------------
if __name__ == "__main__":
    raise SystemExit(main())
