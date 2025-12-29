"""Pytest configuration for mathxlab.

- Forces a headless Matplotlib backend for CI.
- Adds optional progress logging for slow / long-running test suites.

Use:
    pytest --progress --progress-every=1
"""

from __future__ import annotations

from dataclasses import dataclass

import matplotlib
import pytest


@dataclass(slots=True)
class _ProgressState:
    """Runtime state for progress reporting."""

    total: int = 0
    done: int = 0
    every: int = 1


class _ProgressPlugin:
    """A tiny pytest plugin that prints a progress line every N tests."""

    def __init__(self, state: _ProgressState) -> None:
        """Create the plugin.

        Args:
            state: Shared progress state.
        """
        self._state = state

    def pytest_collection_modifyitems(self, session: pytest.Session, config: pytest.Config, items: list[pytest.Item]) -> None:
        """Record total number of collected tests.

        Args:
            session: Pytest session.
            config: Pytest config.
            items: Collected test items.
        """
        self._state.total = len(items)

    def pytest_runtest_logreport(self, report: pytest.TestReport) -> None:
        """Update progress after each finished test.

        We count once per test item by using the 'teardown' phase, which occurs
        exactly once per item even if setup/call fail.

        Args:
            report: The test report object.
        """
        if report.when != "teardown":
            return

        self._state.done += 1
        if self._state.total <= 0:
            return

        if (self._state.done % self._state.every) != 0 and self._state.done != self._state.total:
            return

        config = report.config  # pytest sets this attribute on reports
        terminal = config.pluginmanager.getplugin("terminalreporter")
        msg = f"[progress] {self._state.done}/{self._state.total} ({(100.0 * self._state.done / self._state.total):.1f}%) {report.nodeid}"

        if terminal is not None:
            terminal.write_line(msg)
        else:
            # Fallback: should still show with -s, but terminalreporter is preferred.
            print(msg, flush=True)


def pytest_addoption(parser: pytest.Parser) -> None:
    """Register custom CLI options.

    Args:
        parser: Pytest argument parser.
    """
    group = parser.getgroup("mathxlab")
    group.addoption(
        "--progress",
        action="store_true",
        default=False,
        help="Print progress lines while running tests.",
    )
    group.addoption(
        "--progress-every",
        action="store",
        type=int,
        default=10,
        help="Print a progress line every N tests (default: 10).",
    )


def pytest_configure(config: pytest.Config) -> None:
    """Configure global test environment.

    Args:
        config: Pytest config.
    """
    matplotlib.use("Agg", force=True)

    # With xdist: only enable on the controller node to avoid duplicated output.
    if hasattr(config, "workerinput"):
        return

    if config.getoption("--progress"):
        every = max(1, int(config.getoption("--progress-every")))
        state = _ProgressState(every=every)
        config.pluginmanager.register(_ProgressPlugin(state), name="mathxlab-progress")
