from dataclasses import dataclass, field
from typing import List, Dict, Any


@dataclass
class PipelineConfig:
    input_paths: List[str] = field(default_factory=list)
    output_dir: str = ""
    options: Dict[str, Any] = field(default_factory=dict)
