"""Experiment e068 entry point (standalone package).

This package mirrors experiment entry points so you can run:

    python -m experiments.e068

The implementation is in:
    mathxlab.experiments.e068
"""

from __future__ import annotations

from mathxlab.experiments.e068 import main

__all__ = ["main"]


if __name__ == "__main__":
    raise SystemExit(main())
