"""Backward-compatible entry point for E014."""

from __future__ import annotations

from mathxlab.experiments.e014 import main  # re-export

# ------------------------------------------------------------------------------
__all__ = ["main"]


# ------------------------------------------------------------------------------
if __name__ == "__main__":
    raise SystemExit(main())
