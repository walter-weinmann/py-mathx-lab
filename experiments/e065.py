"""Experiment e065 entry point (standalone package).

This package mirrors experiment entry points so you can run:

    python -m experiments.e065

The implementation is in:
    mathxlab.experiments.e065
"""

from __future__ import annotations

from mathxlab.experiments.e065 import main

__all__ = ["main"]


if __name__ == "__main__":
    raise SystemExit(main())
