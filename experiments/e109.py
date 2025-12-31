"""Backward-compatible entry point for E109."""

from __future__ import annotations

from mathxlab.experiments.e109 import main  # re-export

# ------------------------------------------------------------------------------
__all__ = ["main"]


# ------------------------------------------------------------------------------
if __name__ == "__main__":
    raise SystemExit(main())
