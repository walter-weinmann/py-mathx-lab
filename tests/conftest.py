"""Pytest configuration for mathxlab.

This configuration provides:
- A headless Matplotlib backend (Agg) for CI stability.
- Modest progress logging for slow test runs (or when explicitly enabled).

Progress logging is intentionally lightweight and prints a single line every N tests.
"""

from __future__ import annotations

from dataclasses import dataclass
import time

import matplotlib
import pytest


@dataclass(frozen=True, slots=True)
class _ProgressState:
    """Runtime state for progress reporting."""

    total_selected: int
    total_slow: int
    every: int
    enabled: bool


def pytest_addoption(parser: pytest.Parser) -> None:
    """Register command-line options.

    Args:
        parser: The pytest argument parser.
    """
    group = parser.getgroup("mathxlab")
    group.addoption(
        "--progress",
        action="store_true",
        default=False,
        help="Enable modest progress logging during the test run.",
    )
    group.addoption(
        "--progress-every",
        action="store",
        type=int,
        default=0,
        help=(
            "Print a progress line every N tests (0 = auto). "
            "Auto uses 1 for slow-only runs, otherwise 20."
        ),
    )


def pytest_configure(config: pytest.Config) -> None:
    """Configure global test environment.

    Args:
        config: The pytest configuration object.
    """
    matplotlib.use("Agg", force=True)
    config.addinivalue_line("markers", "slow: marks slow integration/smoke tests")

    markexpr = (getattr(config.option, "markexpr", "") or "").strip()
    auto_enable = bool(markexpr) and "slow" in markexpr and "not slow" not in markexpr
    enabled = bool(config.getoption("--progress")) or auto_enable

    every_opt = int(config.getoption("--progress-every") or 0)
    if every_opt > 0:
        every = every_opt
    else:
        every = 1 if auto_enable else 20

    config._mathxlab_progress = _ProgressState(  # type: ignore[attr-defined]
        total_selected=0,
        total_slow=0,
        every=max(1, every),
        enabled=enabled,
    )
    config._mathxlab_progress_started_at = time.monotonic()  # type: ignore[attr-defined]
    config._mathxlab_progress_seen = 0  # type: ignore[attr-defined]


def pytest_collection_finish(session: pytest.Session) -> None:
    """Finalize progress state once pytest knows the selected items."""
    config = session.config
    state: _ProgressState = config._mathxlab_progress  # type: ignore[attr-defined]
    items = list(getattr(session, "items", []))
    total_selected = len(items)
    total_slow = sum(1 for it in items if it.get_closest_marker("slow") is not None)

    config._mathxlab_progress = _ProgressState(  # type: ignore[attr-defined]
        total_selected=total_selected,
        total_slow=total_slow,
        every=state.every,
        enabled=state.enabled,
    )


def pytest_runtest_setup(item: pytest.Item) -> None:
    """Log modest progress when enabled.

    Args:
        item: The test item about to run.
    """
    config = item.config
    state: _ProgressState = getattr(config, "_mathxlab_progress", None)  # type: ignore[attr-defined]
    if not state or not state.enabled:
        return

    seen = int(getattr(config, "_mathxlab_progress_seen", 0)) + 1  # type: ignore[attr-defined]
    config._mathxlab_progress_seen = seen  # type: ignore[attr-defined]

    if seen == 1 or seen == state.total_selected or (seen % state.every == 0):
        total = state.total_selected or 0
        pct = (100.0 * seen / total) if total else 0.0
        tr = config.pluginmanager.get_plugin("terminalreporter")
        if tr is not None:
            tr.write_line(f"[progress] {seen}/{total} ({pct:5.1f}%) {item.nodeid}")


def pytest_sessionfinish(session: pytest.Session, exitstatus: int) -> None:
    """Print a short end-of-run progress line when enabled."""
    config = session.config
    state: _ProgressState = getattr(config, "_mathxlab_progress", None)  # type: ignore[attr-defined]
    if not state or not state.enabled:
        return

    started_at = float(getattr(config, "_mathxlab_progress_started_at", time.monotonic()))  # type: ignore[attr-defined]
    elapsed_s = time.monotonic() - started_at

    tr = config.pluginmanager.get_plugin("terminalreporter")
    if tr is not None:
        tr.write_line(
            f"[progress] finished: {state.total_selected} tests ({state.total_slow} slow), elapsed {elapsed_s:.1f}s"
        )
