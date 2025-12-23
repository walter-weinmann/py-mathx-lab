from unittest.mock import patch

from mathxlab.viz.mpl import finalize_figure


def test_finalize_figure() -> None:
    with (
        patch("matplotlib.pyplot.title") as mock_title,
        patch("matplotlib.pyplot.xlabel") as mock_xlabel,
        patch("matplotlib.pyplot.ylabel") as mock_ylabel,
        patch("matplotlib.pyplot.grid") as mock_grid,
        patch("matplotlib.pyplot.tight_layout") as mock_tight_layout,
    ):
        finalize_figure(title="Test Title", xlabel="X", ylabel="Y", grid=True)

        mock_title.assert_called_once_with("Test Title")
        mock_xlabel.assert_called_once_with("X")
        mock_ylabel.assert_called_once_with("Y")
        mock_grid.assert_called_once_with(True)
        mock_tight_layout.assert_called_once()


def test_finalize_figure_no_grid() -> None:
    with (
        patch("matplotlib.pyplot.title"),
        patch("matplotlib.pyplot.xlabel"),
        patch("matplotlib.pyplot.ylabel"),
        patch("matplotlib.pyplot.grid") as mock_grid,
        patch("matplotlib.pyplot.tight_layout"),
    ):
        finalize_figure(title="T", xlabel="X", ylabel="Y", grid=False)
        mock_grid.assert_not_called()
