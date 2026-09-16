"""Restore hash-verified local artifacts without deleting or replacing files."""

from __future__ import annotations

import argparse
import hashlib
import json
import shutil
from pathlib import Path


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as source:
        for chunk in iter(lambda: source.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source", type=Path, required=True, help="Authorized local archive directory")
    parser.add_argument("--only", choices=("all", "canonical"), default="all")
    args = parser.parse_args()
    root = Path(__file__).resolve().parents[1]
    archive = args.source.resolve(strict=True)
    if not archive.is_dir():
        parser.error("--source must be a directory")
    entries = json.loads((root / "data/artifact-manifest.json").read_text(encoding="utf-8"))
    canonical = {"new2_ssh_training_data.nc", "new2_ssh_testing_data.nc"}
    for entry in entries:
        if args.only == "canonical" and entry["relative"] not in canonical:
            continue
        destination = (root / entry["restore_to"]).resolve()
        destination.relative_to(root / "data")
        if destination.exists():
            if sha256(destination) != entry["sha256"]:
                raise FileExistsError(f"Existing {destination.name} differs; refusing overwrite.")
            print(f"Verified existing: {destination.name}")
            continue
        candidates = archive.rglob(entry["relative"])
        source = next(
            (p for p in candidates if p.is_file() and p.stat().st_size == entry["bytes"]
             and sha256(p) == entry["sha256"]),
            None,
        )
        if source is None:
            raise FileNotFoundError(f"No hash-matching source for {entry['relative']}")
        destination.parent.mkdir(parents=True, exist_ok=True)
        with source.open("rb") as original, destination.open("xb") as copied:
            shutil.copyfileobj(original, copied)
        if sha256(destination) != entry["sha256"]:
            raise RuntimeError(f"Checksum verification failed for {destination.name}")
        print(f"Restored: {destination.name}")


if __name__ == "__main__":
    main()
