"""Experiment E067 entry point.

This module exists to provide a stable import path:

    python -m mathxlab.experiments.e067

The implementation lives in the descriptive module:
    mathxlab.experiments.e067_gauss_sums
"""

from __future__ import annotations

from mathxlab.experiments.e067_gauss_sums import main

__all__ = ["main"]


if __name__ == "__main__":
    raise SystemExit(main())
