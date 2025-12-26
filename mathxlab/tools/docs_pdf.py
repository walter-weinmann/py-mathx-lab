"""
Build Sphinx LaTeX/PDF documentation and copy the PDF into docs/_static.

This script is designed to be executed as a module:

    python -m mathxlab.tools.docs_pdf

It runs Sphinx in LaTeX mode and then compiles via latexmk.
"""

from __future__ import annotations

import argparse
import shutil
import subprocess
import sys
from dataclasses import dataclass
from pathlib import Path


# ------------------------------------------------------------------------------
@dataclass(frozen=True)
class DocsPdfPaths:
    """Paths used by the PDF build.

    Args:
        repo_root: Repository root directory.
        docs_dir: Sphinx docs source directory.
        build_dir: Sphinx build directory (contains latex/).
        latex_dir: Output directory for LaTeX files.
        static_dir: Directory where static files live (HTML also serves from here).
    """

    repo_root: Path
    docs_dir: Path
    build_dir: Path
    latex_dir: Path
    static_dir: Path


# ------------------------------------------------------------------------------
def _run(cmd: list[str], cwd: Path, quiet: bool) -> None:
    """Run a command and raise on failure.

    Args:
        cmd: Command arguments.
        cwd: Working directory.
        quiet: If True, suppress stdout/stderr unless the command fails.
    """
    if quiet:
        proc = subprocess.run(
            cmd,
            cwd=str(cwd),
            text=True,
            capture_output=True,
        )
        if proc.returncode != 0:
            sys.stderr.write(proc.stdout)
            sys.stderr.write(proc.stderr)
            raise subprocess.CalledProcessError(proc.returncode, cmd)
        return

    subprocess.run(cmd, cwd=str(cwd), check=True)


# ------------------------------------------------------------------------------
def _detect_repo_root() -> Path:
    """Detect repository root as the parent of the 'docs' directory.

    Returns:
        Repository root directory.

    Raises:
        FileNotFoundError: If no 'docs' directory can be found.
    """
    here = Path(__file__).resolve()
    for parent in [here.parent, *here.parents]:
        if (parent / "docs").is_dir():
            return parent
    raise FileNotFoundError("Could not find repo root (missing 'docs/' directory).")


# ------------------------------------------------------------------------------
def _build_latex(paths: DocsPdfPaths, quiet: bool) -> None:
    """Build LaTeX files using Sphinx.

    Args:
        paths: Paths configuration.
        quiet: If True, reduce Sphinx verbosity.
    """
    cmd = [
        sys.executable,
        "-m",
        "sphinx",
        "-b",
        "latex",
    ]
    if quiet:
        cmd.append("-q")
    cmd += [str(paths.docs_dir), str(paths.latex_dir)]
    _run(cmd=cmd, cwd=paths.repo_root, quiet=quiet)


# ------------------------------------------------------------------------------
def _compile_pdf(paths: DocsPdfPaths, tex_name: str, quiet: bool) -> Path | None:
    """Compile the produced LaTeX into a PDF via latexmk.

    Args:
        paths: Paths configuration.
        tex_name: Main .tex file name (e.g. 'py-mathx-lab.tex').
        quiet: If True, reduce latexmk output.

    Returns:
        Path to the generated PDF, or None if latexmk is missing.

    Raises:
        FileNotFoundError: If the expected PDF is not produced.
    """
    if shutil.which("latexmk") is None:
        if not quiet:
            print("Warning: 'latexmk' not found. Skipping PDF compilation.")
        return None

    latexmk_cmd = [
        "latexmk",
        "-xelatex",
        "-halt-on-error",
        "-file-line-error",
        "-interaction=nonstopmode",
    ]
    latexmk_cmd.append("-quiet" if quiet else "-verbose")
    latexmk_cmd.append(tex_name)

    _run(cmd=latexmk_cmd, cwd=paths.latex_dir, quiet=quiet)

    pdf_path = paths.latex_dir / Path(tex_name).with_suffix(".pdf").name
    if not pdf_path.exists():
        raise FileNotFoundError(f"PDF not generated: {pdf_path}")
    return pdf_path


# ------------------------------------------------------------------------------
def _copy_pdf_to_static(pdf_path: Path, static_dir: Path) -> Path:
    """Copy the PDF to docs/_static so HTML can link to it.

    Args:
        pdf_path: Source PDF path.
        static_dir: Destination directory.

    Returns:
        Destination PDF path.
    """
    static_dir.mkdir(parents=True, exist_ok=True)
    dst = static_dir / pdf_path.name
    shutil.copy2(pdf_path, dst)
    return dst


# ------------------------------------------------------------------------------
def main() -> int:
    """CLI entrypoint.

    Returns:
        Process exit code.
    """
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--tex",
        default="py-mathx-lab.tex",
        help="Main LaTeX file name produced by Sphinx (default: py-mathx-lab.tex).",
    )
    parser.add_argument(
        "--quiet",
        action="store_true",
        help="Reduce Sphinx/latexmk output.",
    )
    args = parser.parse_args()

    repo_root = _detect_repo_root()
    docs_dir = repo_root / "docs"
    build_dir = docs_dir / "_build"
    latex_dir = build_dir / "latex"
    static_dir = docs_dir / "_static"

    paths = DocsPdfPaths(
        repo_root=repo_root,
        docs_dir=docs_dir,
        build_dir=build_dir,
        latex_dir=latex_dir,
        static_dir=static_dir,
    )

    latex_dir.mkdir(parents=True, exist_ok=True)

    _build_latex(paths=paths, quiet=args.quiet)
    pdf_path = _compile_pdf(paths=paths, tex_name=args.tex, quiet=args.quiet)

    if pdf_path:
        dst = _copy_pdf_to_static(pdf_path=pdf_path, static_dir=paths.static_dir)
        if not args.quiet:
            print(f"PDF copied to: {dst}")

    return 0


# ------------------------------------------------------------------------------
if __name__ == "__main__":
    raise SystemExit(main())
