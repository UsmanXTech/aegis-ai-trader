from __future__ import annotations

from dataclasses import asdict, dataclass
import hashlib
import json
from pathlib import Path


@dataclass(frozen=True)
class ResearchManifest:
    dataset_path: str
    dataset_sha256: str
    parameters: dict[str, object]


def create_manifest(dataset_path: str | Path, parameters: dict[str, object]) -> ResearchManifest:
    path = Path(dataset_path)
    digest = hashlib.sha256(path.read_bytes()).hexdigest()
    return ResearchManifest(str(path), digest, parameters)


def write_manifest(manifest: ResearchManifest, output: str | Path) -> None:
    Path(output).write_text(json.dumps(asdict(manifest), indent=2), encoding="utf-8")
