from __future__ import annotations

import argparse
import shutil
import subprocess
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Sequence


# ------------------------------------------------------------------------------
@dataclass(frozen=True)
class DocsPdfPaths:
    """Resolved paths for Sphinx docs PDF build and copy.

    Args:
        docs_dir: Root Sphinx docs directory (contains conf.py).
        build_dir: Sphinx build directory (e.g. docs/_build).
    """

    docs_dir: Path
    build_dir: Path

    @property
    def latex_dir(self) -> Path:
        """Directory where Sphinx writes LaTeX output."""
        return self.build_dir / "latex"

    @property
    def html_pdf_dir(self) -> Path:
        """Directory where the PDF is copied for linking in HTML output."""
        return self.build_dir / "html" / "_static" / "pdf"


# ------------------------------------------------------------------------------
def _run(
    cmd: Sequence[str],
    *,
    cwd: Path | None = None,
    verbose: bool = False,
) -> None:
    """Run a command, raising SystemExit on failure.

    Args:
        cmd: Command and arguments.
        cwd: Optional working directory.
        verbose: If True, stream output. If False, capture and print only on error.

    Raises:
        SystemExit: If the command fails.
    """
    if verbose:
        try:
            subprocess.run(cmd, cwd=str(cwd) if cwd else None, check=True)
        except subprocess.CalledProcessError as exc:
            raise SystemExit(exc.returncode) from exc
        return

    proc = subprocess.run(
        cmd,
        cwd=str(cwd) if cwd else None,
        text=True,
        capture_output=True,
    )
    if proc.returncode != 0:
        if proc.stdout:
            print(proc.stdout, end="")
        if proc.stderr:
            print(proc.stderr, end="", file=sys.stderr)
        raise SystemExit(proc.returncode)


# ------------------------------------------------------------------------------
def _build_latex_sources(paths: DocsPdfPaths, *, verbose: bool) -> None:
    """Build LaTeX sources via Sphinx.

    Args:
        paths: Resolved docs paths.
        verbose: Verbosity flag.
    """
    paths.latex_dir.mkdir(parents=True, exist_ok=True)
    _run(
        [sys.executable, "-m", "sphinx", "-b", "latex", "-q", str(paths.docs_dir), str(paths.latex_dir)],
        cwd=None,
        verbose=verbose,
    )


# ------------------------------------------------------------------------------
def _pick_main_tex_file(latex_dir: Path) -> Path | None:
    """Pick the main Sphinx-generated .tex file.

    Args:
        latex_dir: Directory containing LaTeX output.

    Returns:
        Path to the selected .tex file, or None if not found.
    """
    candidates = [p for p in latex_dir.glob("*.tex") if not p.name.lower().startswith("sphinx")]
    if not candidates:
        return None
    return max(candidates, key=lambda p: p.stat().st_size)


# ------------------------------------------------------------------------------
def _latexmk_available() -> bool:
    """Check whether latexmk is available on PATH."""
    return shutil.which("latexmk") is not None


# ------------------------------------------------------------------------------
def _run_latexmk(latex_dir: Path, main_tex: Path, *, verbose: bool, engine: str) -> None:
    """Run latexmk to produce a PDF from the main .tex file.

    Args:
        latex_dir: Directory where LaTeX sources live.
        main_tex: The main .tex file to compile.
        verbose: Verbosity flag.
        engine: LaTeX engine ("xelatex" or "pdflatex").
    """
    # Use xelatex by default to handle Unicode (e.g. σ) reliably on Windows.
    # latexmk supports: -xelatex / -pdf (pdflatex)
    engine_flag = "-xelatex" if engine.lower() == "xelatex" else "-pdf"

    cmd = [
        "latexmk",
        "-xelatex",
        "-quiet",
        "-interaction=nonstopmode",
        "-halt-on-error",
        "py-mathx-lab.tex",
    ]

    cmd.append(main_tex.name)

    _run(cmd, cwd=latex_dir, verbose=verbose)


# ------------------------------------------------------------------------------
def _copy_pdfs_to_html(paths: DocsPdfPaths) -> list[Path]:
    """Copy generated PDFs into the HTML static folder.

    Args:
        paths: Resolved docs paths.

    Returns:
        List of copied PDF paths in the destination folder.
    """
    pdfs = sorted(paths.latex_dir.glob("*.pdf"))
    paths.html_pdf_dir.mkdir(parents=True, exist_ok=True)

    copied: list[Path] = []
    for pdf in pdfs:
        dest = paths.html_pdf_dir / pdf.name
        dest.write_bytes(pdf.read_bytes())
        copied.append(dest)

    return copied


# ------------------------------------------------------------------------------
def _parse_args(argv: Sequence[str]) -> argparse.Namespace:
    """Parse CLI args."""
    parser = argparse.ArgumentParser(description="Build Sphinx PDF (optional) and copy into HTML output.")
    parser.add_argument("--docs-dir", required=True, help="Sphinx docs root directory (contains conf.py).")
    parser.add_argument("--build-dir", required=True, help="Sphinx build directory (e.g. docs/_build).")
    parser.add_argument("--engine", choices=["xelatex", "pdflatex"], default="xelatex", help="LaTeX engine.")
    parser.add_argument("--verbose", action="store_true", help="Stream full tool output.")
    parser.add_argument("--quiet", action="store_true", help="Alias for non-verbose mode (default).")
    return parser.parse_args(list(argv))


# ------------------------------------------------------------------------------
def main(argv: Sequence[str]) -> int:
    """CLI entry point.

    Returns:
        Process exit code.
    """
    args = _parse_args(argv)
    verbose = bool(args.verbose)

    paths = DocsPdfPaths(docs_dir=Path(args.docs_dir), build_dir=Path(args.build_dir))
    _build_latex_sources(paths, verbose=verbose)

    main_tex = _pick_main_tex_file(paths.latex_dir)
    if main_tex is None:
        print("Skipping PDF build: no main .tex file found in LaTeX output.", file=sys.stderr)
        return 0

    if not _latexmk_available():
        print("Skipping PDF build: latexmk not found on PATH.", file=sys.stderr)
        return 0

    _run_latexmk(paths.latex_dir, main_tex, verbose=verbose, engine=args.engine)

    copied = _copy_pdfs_to_html(paths)
    if copied:
        names = ", ".join(p.name for p in copied)
        print(f"Copied PDF(s) to HTML static folder: {names}")
    else:
        print("No PDFs produced (latexmk ran but no *.pdf found).", file=sys.stderr)

    return 0


# ------------------------------------------------------------------------------
if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
