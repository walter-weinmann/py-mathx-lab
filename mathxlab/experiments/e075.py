"""Experiment E075 entry point.

This module exists to provide a stable import path:

    python -m mathxlab.experiments.e075

The implementation lives in the descriptive module:
    mathxlab.experiments.e075_race_statistic_distribution
"""

from __future__ import annotations

from mathxlab.experiments.e075_race_statistic_distribution import main

__all__ = ["main"]


if __name__ == "__main__":
    raise SystemExit(main())
