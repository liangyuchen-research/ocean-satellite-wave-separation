"""Portable, non-destructive file access for the research notebooks."""

from __future__ import annotations

import os
from pathlib import Path


class NotebookPaths:
    def __init__(self, root: Path, output_group: str = "preprocessing") -> None:
        self.root = Path(root).resolve()
        self.data = Path(os.environ.get("OCEAN_DATA_DIR", self.root / "data")).resolve()
        self.artifacts = Path(
            os.environ.get("OCEAN_ARTIFACT_DIR", self.root / "artifacts")
        ).resolve()
        group = self._relative_name(output_group)
        self.output = self.artifacts / group

    @staticmethod
    def _relative_name(name: str | Path) -> Path:
        text = str(name).replace("\\", "/")
        candidate = Path(text)
        if candidate.is_absolute() or ":" in text or ".." in candidate.parts:
            raise ValueError("Use a relative artifact name without parent-directory traversal.")
        return candidate

    def input_path(self, name: str | Path) -> Path:
        relative = self._relative_name(name)
        locations = (self.output, self.artifacts / "preprocessing", self.data)
        for folder in locations:
            candidate = folder / relative
            if candidate.is_file():
                return candidate
        raise FileNotFoundError(
            f"Required input {relative} was not found. Restore authorized source data "
            "or generate the previous preprocessing stage. See docs/reproduction.md."
        )

    def input_glob(self, pattern: str) -> list[str]:
        relative = self._relative_name(pattern)
        matches = {}
        # Generated files take precedence over restored data with the same name.
        for folder in (self.output, self.artifacts / "preprocessing", self.data):
            for candidate in sorted(folder.glob(str(relative))):
                if candidate.is_file():
                    matches.setdefault(candidate.name, str(candidate))
        if not matches:
            raise FileNotFoundError(
                f"No inputs match {relative}. See the required inputs in docs/reproduction.md."
            )
        return sorted(matches.values())

    def output_path(self, name: str | Path) -> Path:
        relative = self._relative_name(name)
        destination = self.output / relative
        if destination.exists():
            raise FileExistsError(
                f"Refusing to replace {destination.name}. Select a new experiment output "
                "directory to preserve the previous result."
            )
        destination.parent.mkdir(parents=True, exist_ok=True)
        return destination
