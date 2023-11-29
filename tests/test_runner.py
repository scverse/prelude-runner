import shutil
from contextlib import chdir
from pathlib import Path
from typing import cast

import nbclient
import pytest
from nbclient.exceptions import CellExecutionError
from nbformat import v4
from prelude_runner.cli import load_preludes, main
from prelude_runner.core import Preludes, execute
from prelude_runner.types import CodeCell, Notebook, Stream

tests_dir = Path(__file__).parent
preludes_dir = tests_dir / "data/config"
nbs_dir = tests_dir / "data/notebooks"


@pytest.fixture(scope="session")
def preludes_py() -> Preludes:
    return load_preludes(preludes_dir, suffix=".py")


def mk_code_nb(source: str) -> Notebook:
    cell = cast(CodeCell, v4.new_code_cell(cell_type="code", source=source))
    return cast(Notebook, v4.new_notebook(cells=[cell]))


@pytest.mark.parametrize(
    ("source", "expected"),
    [
        pytest.param("import random; print(random.randint(0, 10))", "6", id="stdlib"),
        pytest.param(
            "import numpy as np; print(np.random.randint(0, 10))",
            "5",
            id="numpy",
        ),
    ],
)
def test_execute(preludes_py: Preludes, source: str, expected: str) -> None:
    nb = mk_code_nb(source)
    execute(nb, preludes_py)
    cell = cast(CodeCell, nb.cells[0])
    stream = cast(Stream, cell.outputs[0])
    assert stream.text.strip() == expected


def test_traceback_intact(preludes_py: Preludes) -> None:
    """Tests that the traceback reports the same line and cell numbers."""
    with pytest.raises(CellExecutionError) as exc_rr:
        execute(mk_code_nb("1/0"), preludes_py)
    with pytest.raises(CellExecutionError) as exc_orig:
        nbclient.execute(mk_code_nb("1/0"))
    assert exc_rr.value.traceback == exc_orig.value.traceback


def test_cli(tmp_path: Path) -> None:
    with chdir(tmp_path):
        shutil.copytree(nbs_dir, "notebooks")
        main([f"--preludes={preludes_dir}", "notebooks"])
        assert Path("notebooks/r.txt").read_text() == "6"
