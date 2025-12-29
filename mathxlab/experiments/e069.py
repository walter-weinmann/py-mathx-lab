"""Experiment E069 entry point.

This module exists to provide a stable import path:

    python -m mathxlab.experiments.e069

The implementation lives in the descriptive module:
    mathxlab.experiments.e069_l1_convergence
"""

from __future__ import annotations

from mathxlab.experiments.e069_l1_convergence import main

__all__ = ["main"]


if __name__ == "__main__":
    raise SystemExit(main())
