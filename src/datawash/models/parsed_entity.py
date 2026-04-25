from __future__ import annotations

from dataclasses import dataclass, field
from typing import Optional, Dict, List, Any


@dataclass
class ParsedEntity:
    name: str
    docstring: Optional[str] = None
    method_implementations: Dict[str, str] = field(default_factory=dict)
    body_source: str = ""


@dataclass
class StructuredEntity:
    name: str
    doc_structure: Any  # DocstringStructure
    method_implementations: Dict[str, str] = field(default_factory=dict)
    body_source: str = ""
