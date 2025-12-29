"""Experiment E065 entry point.

This module exists to provide a stable import path:

    python -m mathxlab.experiments.e065

The implementation lives in the descriptive module:
    mathxlab.experiments.e065_dirichlet_orthogonality
"""

from __future__ import annotations

from mathxlab.experiments.e065_dirichlet_orthogonality import main

__all__ = ["main"]


if __name__ == "__main__":
    raise SystemExit(main())
