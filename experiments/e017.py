"""Backward-compatible entry point for E017."""

from __future__ import annotations

from mathxlab.experiments.e017 import main  # re-export

# ------------------------------------------------------------------------------
__all__ = ["main"]


# ------------------------------------------------------------------------------
if __name__ == "__main__":
    raise SystemExit(main())
