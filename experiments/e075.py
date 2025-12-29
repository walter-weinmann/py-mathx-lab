"""Experiment e075 entry point (standalone package).

This package mirrors experiment entry points so you can run:

    python -m experiments.e075

The implementation is in:
    mathxlab.experiments.e075
"""

from __future__ import annotations

from mathxlab.experiments.e075 import main

__all__ = ["main"]


if __name__ == "__main__":
    raise SystemExit(main())
