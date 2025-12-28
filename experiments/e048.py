"""Backward-compatible entry point for E048."""

from __future__ import annotations

from mathxlab.experiments.e048 import main  # re-export

# ------------------------------------------------------------------------------
__all__ = ["main"]


# ------------------------------------------------------------------------------
if __name__ == "__main__":
    raise SystemExit(main())
