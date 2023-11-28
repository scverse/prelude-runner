from dataclasses import dataclass
from pathlib import Path
from typing import Any

from jupyter_client.manager import KernelManager
from nbclient import NotebookClient
from nbclient.util import ensure_async
from nbformat import NotebookNode

from .types import CodeCell, Notebook


@dataclass
class Preludes:
    notebook: str | None = None
    cell: str | None = None


def add_reproducible_hooks(client: NotebookClient, preludes: Preludes) -> None:
    async def execute(source: str) -> None:
        await ensure_async(
            client.kc.execute(
                source, silent=True, store_history=False, allow_stdin=False
            )
        )

    async def on_notebook_start(notebook: Notebook) -> None:
        await execute(preludes.notebook)

    async def on_cell_execute(cell: CodeCell, cell_index: int) -> None:
        await execute(preludes.cell)

    client.on_notebook_start = on_notebook_start
    client.on_cell_execute = on_cell_execute


def execute(
    nb: NotebookNode,
    preludes: Preludes,
    *,
    cwd: Path | None = None,
    km: KernelManager | None = None,
    **kwargs: Any,
) -> NotebookNode:
    """Execute a notebook's code, updating outputs within the notebook object."""
    resources = {}
    if cwd is not None:
        resources["metadata"] = {"path": cwd}
    client = NotebookClient(nb=nb, resources=resources, km=km, **kwargs)
    add_reproducible_hooks(client, preludes)
    return client.execute()
