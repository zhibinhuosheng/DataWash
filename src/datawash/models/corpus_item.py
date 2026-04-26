from abc import ABC
from dataclasses import dataclass, field, asdict
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
    # ============================================================
    # [字段映射] 输出 JSON 的顶层字段在这里定义
    # 字段确定后：
    #   - 新增字段：在下面加一行声明
    #   - 删除字段：删掉对应行
    #   - 改字段名：改左边的 Python 属性名
    # 同时配合 enrichers/test_case_enricher.py 的 FIELD_MAPPING
    # ============================================================
    file_path: str = ""
    test_case_number: str = ""
    test_case_name: str = ""
    code_pair_list: List[StepDetail] = field(default_factory=list)
    # 以下为透传字段，按需增删
    repo_path: str = ""
    module: str = ""
    priority: str = ""
    expected_result: str = ""

    def to_dict(self) -> Dict[str, Any]:
        d = asdict(self)
        return d


@dataclass
class AWCorpusItem(CorpusItem):
    function_name: str = ""
    description: str = ""
    implementation_code: str = ""
