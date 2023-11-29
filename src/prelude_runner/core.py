"""Main exports."""
from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING, Any

from nbclient import NotebookClient
from nbclient.util import ensure_async

if TYPE_CHECKING:
    from pathlib import Path

    from jupyter_client.manager import KernelManager

    from .types import CodeCell, Notebook


@dataclass
class Preludes:
    """Prelude code to execute before notebook and cell."""

    notebook: str | None = None
    cell: str | None = None


def add_prelude_hooks(client: NotebookClient, preludes: Preludes) -> None:
    """Add hooks for prelude execution to NotebookClient."""

    async def execute(source: str) -> None:
        await ensure_async(
            client.kc.execute(
                source,
                silent=True,
                store_history=False,
                allow_stdin=False,
            ),
        )

    async def on_notebook_start(notebook: Notebook) -> None:  # noqa: ARG001
        await execute(preludes.notebook)

    async def on_cell_execute(cell: CodeCell, cell_index: int) -> None:  # noqa: ARG001
        await execute(preludes.cell)

    client.on_notebook_start = on_notebook_start
    client.on_cell_execute = on_cell_execute


def execute(
    nb: Notebook,
    preludes: Preludes,
    *,
    cwd: Path | None = None,
    km: KernelManager | None = None,
    **kwargs: Any,  # noqa: ANN401
) -> Notebook:
    """Execute a notebook's code, updating outputs within the notebook object."""
    resources = {}
    if cwd is not None:
        resources["metadata"] = {"path": cwd}
    client = NotebookClient(nb=nb, resources=resources, km=km, **kwargs)
    add_prelude_hooks(client, preludes)
    return client.execute()
