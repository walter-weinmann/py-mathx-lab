"""Run a performance suite and store results in the repository.

This tool runs *all* experiments as subprocesses (stable entrypoints preferred)
and measures wall-clock execution time for each experiment.

The resulting JSON snapshot is written to `perf/results/<label>.json`, where:

- in `--mode dev`, label is timestamped (e.g. dev_20251231_061500)
- in `--mode release`, label is read from `MVERSION` in `pyproject.toml`

The snapshot is designed to be committed per release so that performance changes
can be tracked over time.

Notes:
- For meaningful comparisons, run on the same machine (CPU, OS) and Python version.
- Experiments are executed with the common CLI args:
    --out <workdir>/<exp_id> --seed 1
"""

from __future__ import annotations

import argparse
import json
import os
import platform
import re
import subprocess
import sys
import time
from dataclasses import dataclass
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

try:
    import tomllib  # Python 3.11+
except ImportError:  # pragma: no cover
    tomllib = None  # type: ignore[assignment]


_RE_ENTRYPOINT = re.compile(r"^(e\d{3})\.py$")
_RE_IMPL = re.compile(r"^(e\d{3})_.+\.py$")


@dataclass(frozen=True, slots=True)
class ExperimentTarget:
    """A runnable experiment target."""

    exp_id: str
    module: str
    kind: str  # "entrypoint" or "impl"
    file_name: str


@dataclass(frozen=True, slots=True)
class ExperimentResult:
    """Performance + execution outcome for one experiment."""

    exp_id: str
    module: str
    kind: str
    seconds: float
    returncode: int
    artifacts_ok: bool
    error: str | None


def _utc_timestamp_compact() -> str:
    """Return a compact UTC timestamp string."""
    return datetime.now(tz=UTC).strftime("%Y%m%d_%H%M%S")


def _repo_root() -> Path:
    """Resolve repository root based on this file's location."""
    return Path(__file__).resolve().parents[2]


def _read_pyproject(repo_root: Path) -> dict[str, Any]:
    """Read and parse pyproject.toml.

    Args:
        repo_root: Repository root directory.

    Returns:
        Parsed TOML as nested dict.

    Raises:
        FileNotFoundError: If `pyproject.toml` is missing.
        RuntimeError: If TOML parsing is unavailable or fails.
    """
    path = repo_root / "pyproject.toml"
    if not path.exists():
        raise FileNotFoundError(f"pyproject.toml not found at: {path}")
    if tomllib is None:  # pragma: no cover
        raise RuntimeError("tomllib is not available; need Python 3.11+ to parse pyproject.toml.")
    try:
        return tomllib.loads(path.read_text(encoding="utf-8"))
    except Exception as exc:  # pragma: no cover
        raise RuntimeError(f"Failed to parse pyproject.toml: {exc}") from exc


def _find_key_recursive(obj: Any, key: str) -> str | None:
    """Find the first occurrence of a key in a nested TOML dict.

    Args:
        obj: Nested mapping/list structure.
        key: Key to look for (case-sensitive).

    Returns:
        The value as string if found and string-like, otherwise None.
    """
    if isinstance(obj, dict):
        if key in obj:
            val = obj[key]
            return str(val)
        for v in obj.values():
            found = _find_key_recursive(v, key)
            if found is not None:
                return found
    if isinstance(obj, list):
        for v in obj:
            found = _find_key_recursive(v, key)
            if found is not None:
                return found
    return None


def _get_release_label(repo_root: Path) -> str:
    """Get release label from `MVERSION` or `version` in pyproject.toml.

    Args:
        repo_root: Repository root directory.

    Returns:
        Release label string.

    Raises:
        KeyError: If version cannot be found.
    """
    data = _read_pyproject(repo_root=repo_root)
    mv = _find_key_recursive(data, "MVERSION")
    if mv is None:
        mv = _find_key_recursive(data, "version")
    if mv is None:
        raise KeyError("Could not find 'MVERSION' or 'version' in pyproject.toml (case-sensitive).")
    return str(mv).strip()


def _safe_label(label: str) -> str:
    """Make a label safe for filenames."""
    s = label.strip()
    s = s.replace(" ", "_")
    s = re.sub(r"[^A-Za-z0-9._-]+", "-", s)
    s = re.sub(r"-{2,}", "-", s).strip("-")
    if not s:
        return "unknown"
    return s


def _discover_experiments(repo_root: Path) -> list[ExperimentTarget]:
    """Discover runnable experiments under `mathxlab/experiments`.

    Preference:
        Use stable entrypoint modules `e###.py` if present; otherwise use
        the descriptive implementation module `e###_*.py`.

    Args:
        repo_root: Repository root.

    Returns:
        Sorted list of experiment targets.
    """
    exp_dir = repo_root / "mathxlab" / "experiments"
    if not exp_dir.is_dir():
        raise FileNotFoundError(f"Experiment directory not found: {exp_dir}")

    entrypoints: dict[str, Path] = {}
    impls: dict[str, list[Path]] = {}

    for path in exp_dir.iterdir():
        if not path.is_file() or path.suffix != ".py":
            continue
        m = _RE_ENTRYPOINT.match(path.name)
        if m:
            entrypoints[m.group(1)] = path
            continue
        m = _RE_IMPL.match(path.name)
        if m:
            impls.setdefault(m.group(1), []).append(path)

    exp_ids = sorted(set(entrypoints) | set(impls))
    targets: list[ExperimentTarget] = []
    for exp_id in exp_ids:
        if exp_id in entrypoints:
            targets.append(
                ExperimentTarget(
                    exp_id=exp_id,
                    module=f"mathxlab.experiments.{exp_id}",
                    kind="entrypoint",
                    file_name=entrypoints[exp_id].name,
                )
            )
        else:
            # Choose the first implementation module in lexical order for stability.
            candidates = sorted(impls[exp_id], key=lambda p: p.name)
            chosen = candidates[0]
            targets.append(
                ExperimentTarget(
                    exp_id=exp_id,
                    module=f"mathxlab.experiments.{chosen.stem}",
                    kind="impl",
                    file_name=chosen.name,
                )
            )

    return targets


def _artifacts_ok(out_dir: Path) -> bool:
    """Check whether standard experiment artifacts exist.

    Args:
        out_dir: Experiment output directory.

    Returns:
        True if report.md, params.json and at least one figure exist.
    """
    report_ok = (out_dir / "report.md").is_file()
    params_ok = (out_dir / "params.json").is_file()
    figs_dir = out_dir / "figures"
    figs_ok = figs_dir.is_dir() and any(
        p.suffix.lower() in {".png", ".svg", ".pdf"} for p in figs_dir.iterdir()
    )
    return report_ok and params_ok and figs_ok


def _run_one(
    *,
    target: ExperimentTarget,
    work_root: Path,
    seed: int,
    timeout_seconds: int,
) -> ExperimentResult:
    """Run a single experiment module and time it.

    Args:
        target: Experiment target.
        work_root: Working directory root for output.
        seed: Deterministic seed.
        timeout_seconds: Hard timeout per experiment.

    Returns:
        ExperimentResult with timing and outcome.
    """
    out_dir = work_root / target.exp_id
    out_dir.mkdir(parents=True, exist_ok=True)

    cmd = [
        sys.executable,
        "-m",
        target.module,
        "--out",
        str(out_dir),
        "--seed",
        str(seed),
    ]

    t0 = time.perf_counter()
    error: str | None = None
    returncode = 0
    try:
        proc = subprocess.run(
            cmd,
            cwd=_repo_root(),
            capture_output=True,
            text=True,
            timeout=timeout_seconds,
        )
        returncode = proc.returncode
        if returncode != 0:
            # Keep a short message; full stdout/stderr are too large for snapshot diffs.
            err_tail = (proc.stderr or proc.stdout or "").strip().splitlines()[-10:]
            error = "\n".join(err_tail) if err_tail else "Non-zero exit code."
    except subprocess.TimeoutExpired:
        returncode = 124
        error = f"Timeout after {timeout_seconds}s."
    except Exception as exc:  # pragma: no cover
        returncode = 125
        error = f"Runner error: {exc}"
    t1 = time.perf_counter()

    artifacts_ok = _artifacts_ok(out_dir=out_dir) if returncode == 0 else False

    return ExperimentResult(
        exp_id=target.exp_id,
        module=target.module,
        kind=target.kind,
        seconds=round(t1 - t0, 6),
        returncode=returncode,
        artifacts_ok=artifacts_ok,
        error=error,
    )


def _git_info(repo_root: Path) -> dict[str, str]:
    """Return basic git info if available."""

    def _run(args: list[str]) -> str | None:
        try:
            p = subprocess.run(
                args, cwd=repo_root, stdout=subprocess.PIPE, stderr=subprocess.DEVNULL, text=True
            )
            if p.returncode == 0:
                return p.stdout.strip()
        except Exception:
            return None
        return None

    head = _run(["git", "rev-parse", "HEAD"])
    branch = _run(["git", "rev-parse", "--abbrev-ref", "HEAD"])
    return {k: v for k, v in {"head": head, "branch": branch}.items() if v}


def _write_snapshot(path: Path, payload: dict[str, Any], *, overwrite: bool) -> None:
    """Write JSON snapshot."""
    path.parent.mkdir(parents=True, exist_ok=True)
    if path.exists() and not overwrite:
        raise FileExistsError(f"Snapshot already exists: {path} (use --overwrite to replace)")
    path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def main(argv: list[str] | None = None) -> int:
    """CLI entry point.

    Args:
        argv: Optional argv list for testing.

    Returns:
        Exit code (0 on success).
    """
    p = argparse.ArgumentParser(description="Run performance suite across all experiments.")
    p.add_argument(
        "--mode", choices=["dev", "release"], default="dev", help="Snapshot naming mode."
    )
    p.add_argument("--label", default=None, help="Optional explicit label (overrides mode).")
    p.add_argument("--seed", type=int, default=1, help="Seed passed to all experiments.")
    p.add_argument("--timeout-seconds", type=int, default=120, help="Timeout per experiment.")
    p.add_argument("--overwrite", action="store_true", help="Overwrite existing snapshot file.")
    p.add_argument("--keep-work", action="store_true", help="Do not delete work directory.")
    p.add_argument("--results-dir", default="perf/results", help="Directory for stored snapshots.")
    p.add_argument("--work-dir", default="perf/work", help="Directory used for experiment outputs.")

    args = p.parse_args(argv)

    repo_root = _repo_root()

    if args.label:
        label = args.label
    elif args.mode == "release":
        label = _get_release_label(repo_root=repo_root)
    else:
        label = f"dev_{_utc_timestamp_compact()}"

    label = _safe_label(label)
    results_dir = repo_root / args.results_dir
    work_dir = repo_root / args.work_dir / label

    targets = _discover_experiments(repo_root=repo_root)
    if not targets:
        raise RuntimeError("No experiments discovered under mathxlab/experiments.")

    work_dir.mkdir(parents=True, exist_ok=True)

    suite_t0 = time.perf_counter()
    results: list[ExperimentResult] = []
    for t in targets:
        results.append(
            _run_one(
                target=t,
                work_root=work_dir,
                seed=args.seed,
                timeout_seconds=args.timeout_seconds,
            )
        )
    suite_t1 = time.perf_counter()

    payload: dict[str, Any] = {
        "label": label,
        "mode": args.mode,
        "timestamp_utc": datetime.now(tz=UTC).isoformat(),
        "python": {
            "executable": sys.executable,
            "version": sys.version,
            "implementation": platform.python_implementation(),
        },
        "platform": {
            "system": platform.system(),
            "release": platform.release(),
            "machine": platform.machine(),
            "processor": platform.processor(),
        },
        "git": _git_info(repo_root=repo_root),
        "suite": {
            "experiments_total": len(results),
            "experiments_ok": sum(1 for r in results if r.returncode == 0),
            "artifacts_ok": sum(1 for r in results if r.artifacts_ok),
            "seconds_total": round(suite_t1 - suite_t0, 6),
        },
        "experiments": [
            {
                "exp_id": r.exp_id,
                "module": r.module,
                "kind": r.kind,
                "seconds": r.seconds,
                "returncode": r.returncode,
                "artifacts_ok": r.artifacts_ok,
                "error": r.error,
            }
            for r in results
        ],
    }

    snapshot_path = results_dir / f"{label}.json"
    _write_snapshot(snapshot_path, payload, overwrite=args.overwrite)

    if not args.keep_work:
        # Best-effort cleanup.
        try:
            for root, dirs, files in os.walk(work_dir, topdown=False):
                for fn in files:
                    Path(root, fn).unlink(missing_ok=True)  # Python 3.14
                for dn in dirs:
                    Path(root, dn).rmdir()
            work_dir.rmdir()
        except Exception:
            pass

    # Console summary.
    failures = [r for r in results if r.returncode != 0]
    print(f"Snapshot: {snapshot_path}")
    print(f"Experiments: {len(results)}  OK: {len(results) - len(failures)}  Fail: {len(failures)}")
    print(f"Artifacts OK: {sum(1 for r in results if r.artifacts_ok)}")
    print(f"Total seconds: {payload['suite']['seconds_total']}")
    if failures:
        print("Failures:")
        for r in failures[:10]:
            print(f"  - {r.exp_id} ({r.module}) rc={r.returncode}")
        return 2
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
