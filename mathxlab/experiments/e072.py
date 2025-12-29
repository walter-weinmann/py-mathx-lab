"""Experiment E072 entry point.

This module exists to provide a stable import path:

    python -m mathxlab.experiments.e072

The implementation lives in the descriptive module:
    mathxlab.experiments.e072_prime_race_mod4
"""

from __future__ import annotations

from mathxlab.experiments.e072_prime_race_mod4 import main

__all__ = ["main"]


if __name__ == "__main__":
    raise SystemExit(main())
