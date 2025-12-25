"""Backward-compatible entry point for E001."""

from __future__ import annotations

from mathxlab.experiments.e001 import main  # re-export


# ------------------------------------------------------------------------------
__all__ = ["main"]


# ------------------------------------------------------------------------------
if __name__ == "__main__":
    raise SystemExit(main())
