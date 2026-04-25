from abc import ABC
from dataclasses import dataclass, field
from typing import List, Optional, Dict, Any


@dataclass
class CorpusItem(ABC):
    pass


@dataclass
class StepDetail:
    description: str
    log_info: Optional[str] = None
    implementation_code: str = ""


@dataclass
class TestCaseCorpusItem(CorpusItem):
    metadata: Dict[str, Any] = field(default_factory=dict)
    test_case_number: str = ""
    test_case_name: str = ""
    pre_conditions: List[StepDetail] = field(default_factory=list)
    test_steps: List[StepDetail] = field(default_factory=list)
    post_conditions: List[StepDetail] = field(default_factory=list)


@dataclass
class AWCorpusItem(CorpusItem):
    function_name: str = ""
    description: str = ""
    implementation_code: str = ""
