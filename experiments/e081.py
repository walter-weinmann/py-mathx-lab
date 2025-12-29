"""Experiment e081 entry point (standalone package).

This package mirrors experiment entry points so you can run:

    python -m experiments.e081

The implementation is in:
    mathxlab.experiments.e081
"""

from __future__ import annotations

from mathxlab.experiments.e081 import main

__all__ = ["main"]


if __name__ == "__main__":
    raise SystemExit(main())
