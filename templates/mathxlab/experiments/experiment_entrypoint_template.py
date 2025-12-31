"""Backward-compatible entry point for EXXX.

Keeps a stable module name (`exxx`) while the implementation lives in a descriptive
module file (for example `exxx_<slug>.py`).
"""

from __future__ import annotations

from mathxlab.experiments.exxx_<slug> import main

# ------------------------------------------------------------------------------
__all__ = ["main"]


# ------------------------------------------------------------------------------
if __name__ == "__main__":
    raise SystemExit(main())
