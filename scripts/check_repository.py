"""Run lightweight checks without training or modifying research inputs."""

from __future__ import annotations

import importlib.util
import json
import re
import sys
from pathlib import Path
from tempfile import TemporaryDirectory

sys.dont_write_bytecode = True


def main() -> None:
    root = Path(__file__).resolve().parents[1]
    sys.path.insert(0, str(root / "src"))
    notebooks = sorted(root.glob("notebooks/**/*.ipynb"))
    code_cells = 0
    has_schema = importlib.util.find_spec("nbformat") is not None
    if has_schema:
        import nbformat
    for path in notebooks:
        notebook = json.loads(path.read_text(encoding="utf-8"))
        if has_schema:
            nbformat.validate(nbformat.from_dict(notebook))
        for index, cell in enumerate(notebook["cells"]):
            source = "".join(cell["source"])
            assert not re.search(r"[\u3400-\u4dbf\u4e00-\u9fff]", source)
            assert not re.search(r"[A-Za-z]:\\|/home/[^/]+/", source)
            if cell["cell_type"] == "code":
                compile(source, f"{path.name}:cell-{index}", "exec")
                assert cell["outputs"] == [] and cell["execution_count"] is None
                code_cells += 1
    for folder in [root / "src", root / "scripts"]:
        for path in folder.glob("*.py"):
            compile(path.read_text(encoding="utf-8"), str(path), "exec")

    from project_paths import NotebookPaths

    with TemporaryDirectory() as temporary:
        test_root = Path(temporary)
        (test_root / "data").mkdir()
        sample = test_root / "data" / "sample.nc"
        sample.write_bytes(b"synthetic input")
        paths = NotebookPaths(test_root)
        assert paths.input_path("sample.nc") == sample
        target = paths.output_path("generated.nc")
        target.write_bytes(b"synthetic output")
        try:
            paths.output_path("generated.nc")
        except FileExistsError:
            pass
        else:
            raise AssertionError("Output overwrite guard failed")
        try:
            paths.output_path("../sample.nc")
        except ValueError:
            pass
        else:
            raise AssertionError("Parent traversal guard failed")
        assert sample.read_bytes() == b"synthetic input"

    numeric_status = "not run (NumPy unavailable)"
    if importlib.util.find_spec("numpy") is not None:
        import numpy as np
        from swath_rossby_wave import inversion

        observed = np.array([2.0, 4.0])
        coefficients, estimate = inversion(observed, np.eye(2), np.eye(2))
        assert np.allclose(coefficients, [1.0, 2.0])
        assert np.allclose(estimate, [1.0, 2.0])
        numeric_status = "passed (two-variable regularized inversion)"

    print(f"Syntax and cleared-output checks: {len(notebooks)} notebooks, {code_cells} code cells passed")
    print(f"Notebook schema: {'passed' if has_schema else 'not run (nbformat unavailable)'}")
    print("Input preservation, overwrite and traversal guards: passed")
    print(f"Numerical smoke check: {numeric_status}")
    print("Full scientific pipeline and model training: not run")


if __name__ == "__main__":
    main()
