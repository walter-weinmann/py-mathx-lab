"""Experiment E062 entry point.

Keeps a stable module name (`e062`) while implementation lives in a descriptive
module file.
"""

from __future__ import annotations

from mathxlab.experiments.e062_carmichael_lambda_vs_phi import main  # re-export

# ------------------------------------------------------------------------------
__all__ = ["main"]


# ------------------------------------------------------------------------------
if __name__ == "__main__":
    raise SystemExit(main())
