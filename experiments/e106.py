"""Backward-compatible entry point for E106."""

from __future__ import annotations

from mathxlab.experiments.e106 import main  # re-export

# ------------------------------------------------------------------------------
__all__ = ["main"]


# ------------------------------------------------------------------------------
if __name__ == "__main__":
    raise SystemExit(main())
