"""Experiment E071 entry point.

This module exists to provide a stable import path:

    python -m mathxlab.experiments.e071

The implementation lives in the descriptive module:
    mathxlab.experiments.e071_progressions_pnt_error
"""

from __future__ import annotations

from mathxlab.experiments.e071_progressions_pnt_error import main

__all__ = ["main"]


if __name__ == "__main__":
    raise SystemExit(main())
