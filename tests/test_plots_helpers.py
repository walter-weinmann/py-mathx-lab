"""Tests for matplotlib helper utilities."""

from __future__ import annotations

from unittest.mock import MagicMock

import matplotlib.figure
import matplotlib.pyplot as plt
import pytest

from mathxlab.plots.helpers import finalize_figure


def test_finalize_figure_helpers() -> None:
    mock_fig = MagicMock(spec=matplotlib.figure.Figure)
    finalize_figure(mock_fig)
    mock_fig.tight_layout.assert_called_once()


def test_finalize_figure_handles_mathtext_tight_layout_failure(
    caplog: pytest.LogCaptureFixture,
) -> None:
    """finalize_figure() should not crash if tight_layout() fails.

    Matplotlib's internal mathtext parser can fail for unsupported commands.
    We want this to be a warning, not a hard failure during experiment runs.
    """
    fig, ax = plt.subplots()
    # Intentionally invalid mathtext: ``\le`` is *not* supported by the
    # lightweight mathtext subset in some configurations.
    ax.set_title(r"$\max_{N\le N_\max} |S(N)|$")

    finalize_figure(fig)

    assert any("tight_layout() failed" in rec.getMessage() for rec in caplog.records)
