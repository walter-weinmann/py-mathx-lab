from __future__ import annotations

from collections.abc import Iterator
from contextlib import contextmanager
from unittest.mock import patch

import matplotlib as mpl

from mathxlab.utils.plotting import LatexToolchainStatus, configure_matplotlib, make_math_label


@contextmanager
def _preserve_rcparams() -> Iterator[None]:
    """Preserve and restore Matplotlib rcParams to avoid cross-test pollution."""
    original = mpl.rcParams.copy()
    try:
        yield
    finally:
        mpl.rcParams.update(original)


def test_make_math_label_wraps_and_preserves() -> None:
    """`make_math_label` should wrap expressions in `$...$` without double-wrapping."""
    assert make_math_label(r"\pi(x)") == r"$\pi(x)$"
    assert make_math_label(r"  \pi(x)  ") == r"$\pi(x)$"
    assert make_math_label(r"$\pi(x)$") == r"$\pi(x)$"


def test_configure_matplotlib_enables_tex_when_toolchain_available() -> None:
    """`configure_matplotlib` should enable usetex when toolchain is reported available."""
    with (
        _preserve_rcparams(),
        patch(
            "mathxlab.utils.plotting.detect_latex_toolchain",
            return_value=LatexToolchainStatus(latex=True, dvipng=True, dvisvgm=False),
        ),
    ):
        enabled = configure_matplotlib(use_tex=True, tex_preamble=[r"\usepackage{amsmath}"])
        assert enabled is True
        assert bool(mpl.rcParams["text.usetex"]) is True
        assert r"\usepackage{amsmath}" in str(mpl.rcParams.get("text.latex.preamble", ""))


def test_configure_matplotlib_falls_back_when_toolchain_missing() -> None:
    """`configure_matplotlib` should fall back to mathtext if TeX is requested but unavailable."""
    with (
        _preserve_rcparams(),
        patch(
            "mathxlab.utils.plotting.detect_latex_toolchain",
            return_value=LatexToolchainStatus(latex=False, dvipng=False, dvisvgm=False),
        ),
    ):
        enabled = configure_matplotlib(use_tex=True)
        assert enabled is False
        assert bool(mpl.rcParams["text.usetex"]) is False


def test_configure_matplotlib_applies_rcparams_override() -> None:
    """Explicit rcparams should override the base configuration."""
    with _preserve_rcparams():
        configure_matplotlib(use_tex=False, rcparams={"axes.grid": False})
        assert bool(mpl.rcParams["axes.grid"]) is False
