from dataclasses import dataclass, field
from typing import Dict, Any


@dataclass
class RawSourceFile:
    file_path: str
    source_code: str
    metadata: Dict[str, Any] = field(default_factory=dict)
