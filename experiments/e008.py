"""Backward-compatible entry point for E008."""

from __future__ import annotations

from mathxlab.experiments.e008 import main  # re-export

# ------------------------------------------------------------------------------
__all__ = ["main"]


# ------------------------------------------------------------------------------
if __name__ == "__main__":
    raise SystemExit(main())
