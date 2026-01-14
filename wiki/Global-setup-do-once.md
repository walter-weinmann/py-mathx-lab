# Global setup (do once)

This is the one-time setup checklist for a new machine.

## System prerequisites

- Python toolchain (as required by the repo).
- Optional: LaTeX toolchain if you build PDFs.
- Git + common CLI tools.

## Repo prerequisites

- `uv` installed and available on PATH.
- Ability to run `make` targets (or their Windows equivalents).

## Verify setup

- `uv sync --extra dev`
- `make pytest`
- `make docs`

If all three succeed, your setup is complete.

See also:
- [Getting started](Getting-started)
