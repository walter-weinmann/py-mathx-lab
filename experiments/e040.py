"""Backward-compatible entry point for E040."""

from __future__ import annotations

from mathxlab.experiments.e040 import main  # re-export

# ------------------------------------------------------------------------------
__all__ = ["main"]


# ------------------------------------------------------------------------------
if __name__ == "__main__":
    raise SystemExit(main())
