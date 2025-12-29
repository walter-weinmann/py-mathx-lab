"""Experiment E070 entry point.

This module exists to provide a stable import path:

    python -m mathxlab.experiments.e070

The implementation lives in the descriptive module:
    mathxlab.experiments.e070_primes_in_progressions_counts
"""

from __future__ import annotations

from mathxlab.experiments.e070_primes_in_progressions_counts import main

__all__ = ["main"]


if __name__ == "__main__":
    raise SystemExit(main())
