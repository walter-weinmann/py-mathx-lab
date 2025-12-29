"""Experiment E064 entry point.

This module exists to provide a stable import path:

    python -m mathxlab.experiments.e064

The implementation lives in the descriptive module:
    mathxlab.experiments.e064_dirichlet_character_tables
"""

from __future__ import annotations

from mathxlab.experiments.e064_dirichlet_character_tables import main

__all__ = ["main"]


if __name__ == "__main__":
    raise SystemExit(main())
