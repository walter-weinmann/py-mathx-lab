"""Pytest performance microbenchmarks for shared functions.

Run via Makefile targets:

- Create/update baseline:
    make pytest-perf-baseline

- Compare against baseline:
    make pytest-perf

The baseline is meant to be used on the same machine. These tests are excluded
from the normal `make pytest` suite.
"""

from __future__ import annotations

from datetime import datetime
from pathlib import Path
from typing import Any

import pytest

from .cases_shared_functions import PerfCase, list_perf_cases
from .perf_harness import (
    CaseResult,
    load_baseline,
    measure_callable,
    repo_root_from_test_file,
    save_baseline,
    write_snapshot,
)


@pytest.mark.perf
@pytest.mark.parametrize("case", list_perf_cases(), ids=lambda c: c.case_id)
def test_perf_shared_function(case: PerfCase, request: pytest.FixtureRequest) -> None:
    """Measure a single perf case and optionally compare against baseline.

    Args:
        case: Performance case definition.
        request: Pytest fixture request.
    """
    min_sample_seconds = float(request.config.getoption("--perf-min-sample-seconds"))
    warmup = int(request.config.getoption("--perf-warmup"))
    samples = int(request.config.getoption("--perf-samples"))
    perf_factor = float(request.config.getoption("--perf-factor"))
    update_baseline = bool(request.config.getoption("--perf-update-baseline"))

    test_file = Path(__file__)
    repo_root = repo_root_from_test_file(test_file)
    baseline_path = repo_root / "tests" / "perf" / "baseline_shared_functions.json"

    fn = case.make_callable()

    timing = measure_callable(
        fn,
        min_sample_seconds=min_sample_seconds,
        warmup=warmup,
        samples=samples,
    )

    # Record for snapshot (written at the end of the session).
    _RESULTS.append(
        CaseResult(
            case_id=case.case_id,
            module=case.module,
            function=case.function,
            description=case.description,
            timing=timing,
            work_units=case.work_units,
            unit_label=case.unit_label,
        )
    )

    baseline = load_baseline(baseline_path)
    baseline_cases: dict[str, Any] = baseline.get("cases", {})

    if update_baseline:
        baseline.setdefault("meta", {})
        baseline["meta"].update(
            {
                "updated_utc": datetime.utcnow().isoformat(timespec="seconds") + "Z",
                "note": "Updated by pytest --perf-update-baseline",
            }
        )
        baseline_cases[case.case_id] = {
            "module": case.module,
            "function": case.function,
            "description": case.description,
            "work_units": case.work_units,
            "unit_label": case.unit_label,
            "seconds_per_call_median": timing.seconds_per_call_median,
            "seconds_per_call_p25": timing.seconds_per_call_p25,
            "seconds_per_call_p75": timing.seconds_per_call_p75,
            "loops_per_sample": timing.loops_per_sample,
            "warmup": timing.warmup,
            "samples": timing.samples,
            "min_sample_seconds": timing.min_sample_seconds,
        }
        baseline["cases"] = baseline_cases
        save_baseline(baseline_path, baseline)
        return

    # If there is no baseline yet, treat this as "record only".
    b = baseline_cases.get(case.case_id)
    if b is None:
        # Keep the test green but make it visible in output.
        print(f"[perf] No baseline for {case.case_id}; run: make pytest-perf-baseline")
        return

    base = float(b["seconds_per_call_median"])
    measured = float(timing.seconds_per_call_median)

    # Allow mild jitter; compare median to median.
    if base <= 0.0:
        pytest.fail(f"Invalid baseline (<= 0) for {case.case_id}")

    limit = base * perf_factor
    if measured > limit:
        pytest.fail(
            f"Perf regression for {case.case_id}: median {measured:.6g}s > "
            f"{perf_factor:.2f}x baseline {base:.6g}s (limit {limit:.6g}s)."
        )


_RESULTS: list[CaseResult] = []


@pytest.fixture(scope="session", autouse=True)
def _write_perf_snapshot(request: pytest.FixtureRequest) -> None:
    """Write a snapshot JSON at the end of the perf run.

    Args:
        request: Pytest fixture request.
    """

    def _finalize() -> None:
        if not _RESULTS:
            return

        repo_root = repo_root_from_test_file(Path(__file__))
        out_dir = repo_root / "perf" / "results"
        ts = datetime.utcnow().strftime("%Y%m%d_%H%M%SZ")
        snapshot_path = out_dir / f"pytest_perf_shared_functions_{ts}.json"

        write_snapshot(snapshot_path, label="pytest-perf", results=_RESULTS)

    request.addfinalizer(_finalize)
