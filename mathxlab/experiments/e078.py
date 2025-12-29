"""Experiment E078 entry point.

This module exists to provide a stable import path:

    python -m mathxlab.experiments.e078

The implementation lives in the descriptive module:
    mathxlab.experiments.e078_max_character_sums
"""

from __future__ import annotations

from mathxlab.experiments.e078_max_character_sums import main

__all__ = ["main"]


if __name__ == "__main__":
    raise SystemExit(main())
