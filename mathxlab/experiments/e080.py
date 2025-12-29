"""Experiment E080 entry point.

This module exists to provide a stable import path:

    python -m mathxlab.experiments.e080

The implementation lives in the descriptive module:
    mathxlab.experiments.e080_bias_fraction_curve
"""

from __future__ import annotations

from mathxlab.experiments.e080_bias_fraction_curve import main

__all__ = ["main"]


if __name__ == "__main__":
    raise SystemExit(main())
