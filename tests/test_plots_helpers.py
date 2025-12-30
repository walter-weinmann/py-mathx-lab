from unittest.mock import MagicMock

import matplotlib.figure

from mathxlab.plots.helpers import finalize_figure


def test_finalize_figure_helpers() -> None:
    mock_fig = MagicMock(spec=matplotlib.figure.Figure)
    finalize_figure(mock_fig)
    mock_fig.tight_layout.assert_called_once()
