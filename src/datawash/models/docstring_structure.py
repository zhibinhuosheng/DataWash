from abc import ABC
from dataclasses import dataclass, field
from typing import List


@dataclass
class DocstringStructure(ABC):
    pass


@dataclass
class TestCaseDocStructure(DocstringStructure):
    test_case_number: str = ""
    test_case_name: str = ""
    step_descriptions: List[str] = field(default_factory=list)


@dataclass
class AWDocStructure(DocstringStructure):
    description: str = ""
