from typing import Any, Literal, Protocol, TypedDict


class CellMetadata(TypedDict):
    tags: list[str]


class Cell(Protocol):
    cell_type: Literal["markdown", "code"]
    metadata: CellMetadata
    source: str


class Output(Protocol):
    output_type: Literal[
        "stream", "display_data", "execute_result", "error", "update_display_data"
    ]
    data: dict[str, str]


class Stream(Protocol):
    output_type: Literal["stream"]
    name: Literal["stdout", "stderr"]
    text: str


class CodeCell(Cell):
    cell_type: Literal["code"]
    outputs: list[Stream | Any]  # TODO


class NotebookMetadata(TypedDict):
    language_info: dict[str, str]


class Notebook(Protocol):
    metadata: NotebookMetadata
    cells: list[Cell]
