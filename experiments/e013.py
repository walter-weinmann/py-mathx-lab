"""Backward-compatible entry point for E013."""

from __future__ import annotations

from mathxlab.experiments.e013 import main  # re-export

# ------------------------------------------------------------------------------
__all__ = ["main"]


# ------------------------------------------------------------------------------
if __name__ == "__main__":
    raise SystemExit(main())
