"""Backward-compatible entry point for E121."""

from __future__ import annotations

from mathxlab.experiments.e121 import main  # re-export

# ------------------------------------------------------------------------------
__all__ = ["main"]


# ------------------------------------------------------------------------------
if __name__ == "__main__":
    raise SystemExit(main())
