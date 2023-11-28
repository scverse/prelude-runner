from argparse import ArgumentParser
from pathlib import Path
from typing import Protocol

from .core import Preludes, execute


def load_preludes(d: Path) -> Preludes:
    return Preludes(
        notebook=(d / "prelude_notebook.py").read_text(),
        cell=(d / "prelude_cell.py").read_text(),
    )


class Args(Protocol):
    preludes: Path
    nb_path: Path


def parse_args(argv: list[str] | None = None) -> Args:
    parser = ArgumentParser(argv)
    parser.add_argument("--preludes", type=Path, help="Path to prelude directory")
    parser.add_argument("nb-path", type=Path, help="Path to notebook directory")
    return parser.parse_args()


def main(argv: list[str] | None = None) -> None:
    args = parse_args(argv)
    preludes = load_preludes(args.preludes)
    for nb in args.nb_path.rglob("*.ipynb"):
        execute(nb, cwd=args.nb_path, preludes=preludes)