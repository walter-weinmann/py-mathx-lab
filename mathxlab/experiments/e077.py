"""Experiment E077 entry point.

This module exists to provide a stable import path:

    python -m mathxlab.experiments.e077

The implementation lives in the descriptive module:
    mathxlab.experiments.e077_indicator_via_characters
"""

from __future__ import annotations

from mathxlab.experiments.e077_indicator_via_characters import main

__all__ = ["main"]


if __name__ == "__main__":
    raise SystemExit(main())
