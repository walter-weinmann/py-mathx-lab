"""Experiment E079 entry point.

This module exists to provide a stable import path:

    python -m mathxlab.experiments.e079

The implementation lives in the descriptive module:
    mathxlab.experiments.e079_primitive_characters_conductors
"""

from __future__ import annotations

from mathxlab.experiments.e079_primitive_characters_conductors import main

__all__ = ["main"]


if __name__ == "__main__":
    raise SystemExit(main())
