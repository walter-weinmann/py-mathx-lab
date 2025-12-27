"""Backward-compatible entry point for E025."""

from __future__ import annotations

from mathxlab.experiments.e025 import main  # re-export

# ------------------------------------------------------------------------------
__all__ = ["main"]


# ------------------------------------------------------------------------------
if __name__ == "__main__":
    raise SystemExit(main())
