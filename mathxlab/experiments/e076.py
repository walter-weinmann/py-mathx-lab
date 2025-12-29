"""Experiment E076 entry point.

This module exists to provide a stable import path:

    python -m mathxlab.experiments.e076

The implementation lives in the descriptive module:
    mathxlab.experiments.e076_theta_in_progressions
"""

from __future__ import annotations

from mathxlab.experiments.e076_theta_in_progressions import main

__all__ = ["main"]


if __name__ == "__main__":
    raise SystemExit(main())
