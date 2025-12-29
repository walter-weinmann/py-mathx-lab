"""Experiment E073 entry point.

This module exists to provide a stable import path:

    python -m mathxlab.experiments.e073

The implementation lives in the descriptive module:
    mathxlab.experiments.e073_prime_race_mod3
"""

from __future__ import annotations

from mathxlab.experiments.e073_prime_race_mod3 import main

__all__ = ["main"]


if __name__ == "__main__":
    raise SystemExit(main())
