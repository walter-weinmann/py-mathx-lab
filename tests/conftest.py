"""Pytest configuration for mathxlab.

This file ensures a headless Matplotlib backend is used in tests.
"""

from __future__ import annotations

import matplotlib


def pytest_configure() -> None:
    """Configure global test environment."""
    matplotlib.use("Agg", force=True)
