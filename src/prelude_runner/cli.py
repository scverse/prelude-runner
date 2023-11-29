"""Command line parsing and execution."""
from __future__ import annotations

from argparse import ArgumentParser
from pathlib import Path
from typing import TYPE_CHECKING, Protocol

import nbformat

from .core import Preludes, execute

if TYPE_CHECKING:
    from collections.abc import Sequence

    from .types import Notebook


def load_preludes(d: Path, *, suffix: str) -> Preludes:
    """Load prelude code from config directory."""
    paths = {p: (d / f"prelude_{p}").with_suffix(suffix) for p in ("notebook", "cell")}
    notebook, cell = (
        path.read_text() if path.is_file() else None for path in paths.values()
    )
    if notebook is None and cell is None:
        msg = f"No prelude(s) with {suffix=} found in {d}"
        raise FileNotFoundError(msg)
    return Preludes(notebook=notebook, cell=cell)


class Args(Protocol):
    """Parsed command line arguments."""

    preludes: Path
    nb_path: Path


def parse_args(argv: Sequence[str] | None = None) -> Args:
    """Parse command line arguments."""
    parser = ArgumentParser()
    parser.add_argument(
        "--preludes", type=Path, help="Path to prelude directory", required=True
    )
    parser.add_argument("nb_path", type=Path, help="Path to notebook directory")
    return parser.parse_args(argv)


def main(argv: Sequence[str] | None = None) -> None:
    """Execute main entry point."""
    args = parse_args(argv)
    for nb_path in args.nb_path.rglob("*.ipynb"):
        nb: Notebook = nbformat.reads(nb_path.read_text(), 4)
        suffix = nb.metadata["language_info"]["file_extension"]
        preludes = load_preludes(args.preludes, suffix=suffix)
        execute(nb, cwd=args.nb_path, preludes=preludes)
