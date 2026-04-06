from dataclasses import dataclass, field
from pathlib import Path
from typing import Optional


@dataclass
class InputFile:
    path: Path
    extension: str
    kind: str
    size_bytes: int
    raw_bytes: bytes
    text: Optional[str] = None
    notes: list[str] = field(default_factory=list)