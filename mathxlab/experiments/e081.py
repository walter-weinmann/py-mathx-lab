"""Experiment E081 entry point.

This module exists to provide a stable import path:

    python -m mathxlab.experiments.e081

The implementation lives in the descriptive module:
    mathxlab.experiments.e081_sign_changes_table
"""

from __future__ import annotations

from mathxlab.experiments.e081_sign_changes_table import main

__all__ = ["main"]


if __name__ == "__main__":
    raise SystemExit(main())
