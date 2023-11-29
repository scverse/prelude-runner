"""Command line parsing and execution."""
from __future__ import annotations

from argparse import ArgumentParser
from pathlib import Path
from typing import TYPE_CHECKING, Protocol, Sequence

import nbformat

from .core import Preludes, execute

if TYPE_CHECKING:
    from .types import Notebook


def load_preludes(d: Path) -> Preludes:
    """Load prelude code from config directory."""
    return Preludes(
        notebook=(d / "prelude_notebook.py").read_text(),
        cell=(d / "prelude_cell.py").read_text(),
    )


class Args(Protocol):
    """Parsed command line arguments."""

    preludes: Path
    nb_path: Path


def parse_args(argv: Sequence[str] | None = None) -> Args:
    """Parse command line arguments."""
    parser = ArgumentParser()
    parser.add_argument("--preludes", type=Path, help="Path to prelude directory")
    parser.add_argument("nb-path", type=Path, help="Path to notebook directory")
    return parser.parse_args(argv)


def main(argv: Sequence[str] | None = None) -> None:
    """Execute main entry point."""
    args = parse_args(argv)
    preludes = load_preludes(args.preludes)
    for nb_path in args.nb_path.rglob("*.ipynb"):
        nb: Notebook = nbformat.reads(nb_path.read_text(), 4)
        execute(nb, cwd=args.nb_path, preludes=preludes)
