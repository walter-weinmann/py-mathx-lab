"""Experiment E074 entry point.

This module exists to provide a stable import path:

    python -m mathxlab.experiments.e074

The implementation lives in the descriptive module:
    mathxlab.experiments.e074_prime_race_mod8_leaderboard
"""

from __future__ import annotations

from mathxlab.experiments.e074_prime_race_mod8_leaderboard import main

__all__ = ["main"]


if __name__ == "__main__":
    raise SystemExit(main())
