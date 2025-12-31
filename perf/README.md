# Performance snapshots

This directory stores *committable* performance results for `py-mathx-lab`.

## What is measured?

`tools/run_perf.py` runs **all experiments** as subprocesses (prefer stable entrypoints `e###.py`)
and measures wall-clock runtime per experiment and total suite time.

Each experiment is executed with:

- `--seed 1`
- `--out perf/work/<label>/<exp_id>`

The snapshot also records: OS + Python version + (optional) git commit.

## Snapshots per release

Release snapshots are named from `MVERSION` in `pyproject.toml`.

Run:

```bash
make perf-release
```

This produces:

- `perf/results/<MVERSION>.json`

Commit that file along with the release/tag.

## Developer snapshots

For ad-hoc local measurements:

```bash
make perf
```

This produces a timestamped file like:

- `perf/results/dev_YYYYMMDD_HHMMSS.json`

## Compare two snapshots

```bash
make perf-compare A=<labelA> B=<labelB>
```

Example:

```bash
make perf-compare A=v0.2.0 B=v0.3.0
```

The tool prints a Markdown table with deltas per experiment.

## Notes for meaningful comparisons

- Run on the **same machine** (CPU / OS) when comparing over time.
- Close heavy background tasks.
- If some experiments fail or do not produce artifacts, the snapshot will record this.
