"""Experiment E057 entry point.

Keeps a stable module name (`e057`) while implementation lives in a descriptive
module file.
"""

from __future__ import annotations

from mathxlab.experiments.e057_erdos_kac_omega_distribution import main  # re-export

# ------------------------------------------------------------------------------
__all__ = ["main"]


# ------------------------------------------------------------------------------
if __name__ == "__main__":
    raise SystemExit(main())
