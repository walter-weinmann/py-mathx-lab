"""Experiment E058 entry point.

Keeps a stable module name (`e058`) while implementation lives in a descriptive
module file.
"""

from __future__ import annotations

from mathxlab.experiments.e058_divisor_count_records import main  # re-export

# ------------------------------------------------------------------------------
__all__ = ["main"]


# ------------------------------------------------------------------------------
if __name__ == "__main__":
    raise SystemExit(main())
