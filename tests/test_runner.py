from pathlib import Path
from typing import TYPE_CHECKING

import nbclient
import pytest
from nbclient.exceptions import CellExecutionError
from nbformat import v4
from prelude_runner.cli import load_preludes, main
from prelude_runner.core import Preludes, execute

if TYPE_CHECKING:
    from prelude_runner.types import CodeCell, Notebook

tests_dir = Path(__file__).parent


@pytest.fixture(scope="session")
def preludes() -> Preludes:
    return load_preludes(tests_dir / "data/config")


@pytest.mark.parametrize(
    ("code", "expected"),
    [
        pytest.param("import random; print(random.randint(0, 10))", "6", id="stdlib"),
        pytest.param(
            "import numpy as np; print(np.random.randint(0, 10))",
            "5",
            id="numpy",
        ),
    ],
)
def test_execute(preludes: Preludes, code: str, expected: str) -> None:
    cell: CodeCell = v4.new_code_cell(cell_type="code", source=code)
    nb: Notebook = v4.new_notebook(cells=[cell])
    execute(nb, preludes)
    assert cell.outputs[0].text.strip() == expected


def test_traceback_intact(preludes: Preludes) -> None:
    """Tests that the traceback reports the same line and cell numbers."""

    def mk_nb() -> None:
        cell: CodeCell = v4.new_code_cell(cell_type="code", source="1/0")
        nb: Notebook = v4.new_notebook(cells=[cell])
        return nb

    with pytest.raises(CellExecutionError) as exc_rr:
        execute(mk_nb(), preludes)
    with pytest.raises(CellExecutionError) as exc_orig:
        nbclient.execute(mk_nb())
    assert exc_rr.value.traceback == exc_orig.value.traceback


def test_cli() -> None:
    nb_path = tests_dir / "data/notebooks"
    main([nb_path])
