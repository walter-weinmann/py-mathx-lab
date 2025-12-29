"""Experiment E068 entry point.

This module exists to provide a stable import path:

    python -m mathxlab.experiments.e068

The implementation lives in the descriptive module:
    mathxlab.experiments.e068_lseries_vs_euler_product
"""

from __future__ import annotations

from mathxlab.experiments.e068_lseries_vs_euler_product import main

__all__ = ["main"]


if __name__ == "__main__":
    raise SystemExit(main())
