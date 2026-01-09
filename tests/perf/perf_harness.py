"""Test-local microbenchmark harness.

This module provides a small, dependency-free timing harness that can be used
inside pytest tests (marked with ``@pytest.mark.perf``).

Why test-local?
- Keeps perf instrumentation out of the mathxlab runtime package.
- Allows running benchmarks via the existing ``make pytest-*`` targets.

Notes on repeatability:
- These numbers are only meaningfully comparable on the *same machine* with
  similar system load.
- By default, perf tests are excluded from the normal ``make pytest`` suite.
"""

from __future__ import annotations

import gc
import json
import platform
from collections.abc import Callable
from dataclasses import dataclass
from datetime import UTC, datetime
from pathlib import Path
from time import perf_counter
from typing import Any


@dataclass(frozen=True, slots=True)
class TimingStats:
    """Summary statistics for a benchmarked callable.

    Attributes:
        seconds_per_call_median: Median seconds per callable invocation.
        seconds_per_call_p25: 25th percentile seconds per call.
        seconds_per_call_p75: 75th percentile seconds per call.
        loops_per_sample: Invocations per measured sample.
        warmup: Warmup samples (not included in stats).
        samples: Measured samples.
        min_sample_seconds: Target minimum duration per sample.
    """

    seconds_per_call_median: float
    seconds_per_call_p25: float
    seconds_per_call_p75: float
    loops_per_sample: int
    warmup: int
    samples: int
    min_sample_seconds: float


@dataclass(frozen=True, slots=True)
class CaseResult:
    """One microbenchmark case result suitable for JSON snapshots."""

    case_id: str
    module: str
    function: str
    description: str
    timing: TimingStats
    work_units: int
    unit_label: str


def repo_root_from_test_file(test_file: Path) -> Path:
    """Infer the repository root directory from a test file path.

    Args:
        test_file: Path to a test module file.

    Returns:
        Repository root path.
    """
    return test_file.resolve().parents[2]


def _percentile(sorted_vals: list[float], q: float) -> float:
    """Compute a simple linear-interpolated percentile for sorted values.

    Args:
        sorted_vals: Values sorted ascending.
        q: Percentile in [0, 100].

    Returns:
        Percentile value.
    """
    if not sorted_vals:
        raise ValueError("sorted_vals must not be empty")
    if q <= 0:
        return float(sorted_vals[0])
    if q >= 100:
        return float(sorted_vals[-1])

    pos = (q / 100.0) * (len(sorted_vals) - 1)
    lo = int(pos)
    hi = min(lo + 1, len(sorted_vals) - 1)
    frac = pos - lo
    return float(sorted_vals[lo] * (1.0 - frac) + sorted_vals[hi] * frac)


def measure_callable[T](
    fn: Callable[[], T],
    *,
    min_sample_seconds: float,
    warmup: int,
    samples: int,
    max_loops: int = 1_000_000_000,
    gc_collect: bool = True,
) -> TimingStats:
    """Measure a callable with adaptive looping and robust summary statistics.

    The harness first determines a loop count such that one measured sample takes
    at least `min_sample_seconds` (within `max_loops`). It then records `samples`
    timings, each consisting of `loops_per_sample` invocations.

    Args:
        fn: Callable to benchmark.
        min_sample_seconds: Minimum target duration for one measured sample.
        warmup: Number of warmup samples (not included in stats).
        samples: Number of measured samples.
        max_loops: Upper bound for adaptive loop count.
        gc_collect: If True, run ``gc.collect()`` before each sample.

    Returns:
        TimingStats with median and inter-quartile range.

    Raises:
        ValueError: If parameters are invalid.
    """
    if min_sample_seconds <= 0:
        raise ValueError("min_sample_seconds must be > 0")
    if warmup < 0:
        raise ValueError("warmup must be >= 0")
    if samples < 1:
        raise ValueError("samples must be >= 1")
    if max_loops < 1:
        raise ValueError("max_loops must be >= 1")

    def run_loops(loops: int) -> float:
        if gc_collect:
            gc.collect()

        gc_was_enabled = gc.isenabled()
        try:
            gc.disable()
            t0 = perf_counter()
            for _ in range(loops):
                fn()
            t1 = perf_counter()
        finally:
            if gc_was_enabled:
                gc.enable()

        return t1 - t0

    for _ in range(warmup):
        _ = run_loops(1)

    loops = 1
    elapsed = run_loops(loops)
    while elapsed < min_sample_seconds and loops < max_loops:
        loops = min(loops * 2, max_loops)
        elapsed = run_loops(loops)

    per_call: list[float] = []
    for _ in range(samples):
        elapsed = run_loops(loops)
        per_call.append(elapsed / float(loops))

    per_call_sorted = sorted(per_call)
    return TimingStats(
        seconds_per_call_median=_percentile(per_call_sorted, 50.0),
        seconds_per_call_p25=_percentile(per_call_sorted, 25.0),
        seconds_per_call_p75=_percentile(per_call_sorted, 75.0),
        loops_per_sample=int(loops),
        warmup=int(warmup),
        samples=int(samples),
        min_sample_seconds=float(min_sample_seconds),
    )


def load_baseline(path: Path) -> dict[str, Any]:
    """Load a perf baseline JSON file.

    Args:
        path: Baseline path.

    Returns:
        Parsed JSON payload (dict). Returns a default empty structure if missing.
    """
    if not path.exists():
        return {"meta": {}, "cases": {}}
    data = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        raise TypeError(f"Expected dict from JSON at {path}, got {type(data)}")
    return data


def save_baseline(path: Path, payload: dict[str, Any]) -> None:
    """Save a perf baseline JSON file with stable formatting.

    Args:
        path: Baseline path.
        payload: JSON payload to write.
    """
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def write_snapshot(results_path: Path, *, label: str, results: list[CaseResult]) -> None:
    """Write a snapshot JSON for a perf run.

    Args:
        results_path: Path to the snapshot JSON.
        label: Stable label for the run (e.g. 'pytest-perf').
        results: Measured case results.
    """
    results_path.parent.mkdir(parents=True, exist_ok=True)

    payload: dict[str, Any] = {
        "suite": {
            "kind": "pytest_perf_microbenchmarks",
            "label": label,
            "created_utc": datetime.now(UTC).isoformat(timespec="seconds").replace("+00:00", "Z"),
            "python": platform.python_version(),
            "platform": platform.platform(),
            "machine": platform.machine(),
            "processor": platform.processor(),
            "cases": len(results),
        },
        "cases": [
            {
                "case_id": r.case_id,
                "module": r.module,
                "function": r.function,
                "description": r.description,
                "work_units": r.work_units,
                "unit_label": r.unit_label,
                "timing": {
                    "seconds_per_call_median": r.timing.seconds_per_call_median,
                    "seconds_per_call_p25": r.timing.seconds_per_call_p25,
                    "seconds_per_call_p75": r.timing.seconds_per_call_p75,
                    "loops_per_sample": r.timing.loops_per_sample,
                    "warmup": r.timing.warmup,
                    "samples": r.timing.samples,
                    "min_sample_seconds": r.timing.min_sample_seconds,
                },
            }
            for r in results
        ],
    }

    results_path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
