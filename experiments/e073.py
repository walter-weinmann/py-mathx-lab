"""Experiment e073 entry point (standalone package).

This package mirrors experiment entry points so you can run:

    python -m experiments.e073

The implementation is in:
    mathxlab.experiments.e073
"""

from __future__ import annotations

from mathxlab.experiments.e073 import main

__all__ = ["main"]


if __name__ == "__main__":
    raise SystemExit(main())
