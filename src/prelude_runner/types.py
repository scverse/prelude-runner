"""Types more specific than NotebookNode."""
from __future__ import annotations

from typing import Any, Literal, Protocol, TypedDict


class CellMetadata(TypedDict):
    """Common metadata for all cells."""

    tags: list[str]


class Cell(Protocol):
    """A cell in a notebook."""

    cell_type: Literal["markdown", "code"]
    metadata: CellMetadata
    source: str


class Output(Protocol):
    """A code cell’s output."""

    output_type: Literal[
        "stream",
        "display_data",
        "execute_result",
        "error",
        "update_display_data",
    ]
    data: dict[str, str]


class Stream(Protocol):
    """One type of output from a code cell."""

    output_type: Literal["stream"]
    name: Literal["stdout", "stderr"]
    text: str


class CodeCell(Cell):
    """A code cell."""

    cell_type: Literal["code"]
    # TODO: add other output types  # noqa: TD003
    outputs: list[Stream | Any]


class NotebookMetadata(TypedDict):
    """Common metadata for all notebooks."""

    language_info: dict[str, str]


class Notebook(Protocol):
    """A Jupyter notebook."""

    metadata: NotebookMetadata
    cells: list[Cell]
