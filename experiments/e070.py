"""Experiment e070 entry point (standalone package).

This package mirrors experiment entry points so you can run:

    python -m experiments.e070

The implementation is in:
    mathxlab.experiments.e070
"""

from __future__ import annotations

from mathxlab.experiments.e070 import main

__all__ = ["main"]


if __name__ == "__main__":
    raise SystemExit(main())
