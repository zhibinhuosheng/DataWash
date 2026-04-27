from abc import ABC
from dataclasses import dataclass, field, asdict
from typing import List, Optional, Dict, Any


@dataclass
class CorpusItem(ABC):
    pass


@dataclass
class StepSetup:
    step_setup_code: str = ""
    step_instance_var: str = ""
    step_method_var: str = ""


@dataclass
class CodePair:
    # ============================================================
    # [字段映射] 输出 JSON 中 code_pair_list 每项的字段
    # 按 output_template.json 中的 code_pair_list 定义
    # ============================================================
    prompt: str = ""                        # tc.logInfo 中的字符串
    code: str = ""                          # 到下一个 tc.logInfo 之间的代码
    prompt_id: str = ""
    prompt_pos: str = ""                    # prompt 在源文件中的位置
    code_pos: str = ""                      # code 在源文件中的位置
    step_dependencies: str = ""
    step_setup: StepSetup = field(default_factory=StepSetup)
    step_teardown: str = ""
    step_index: str = ""


@dataclass
class TestCaseCorpusItem(CorpusItem):
    # ============================================================
    # [字段映射] 输出 JSON 的顶层字段
    # 按 output_template.json 定义
    # 新增/删减字段改这里
    # ============================================================
    file_name: str = ""
    language: str = ""
    test_framework: str = ""
    dependencies: str = ""
    class_name: str = ""
    path: str = ""
    test_suite: str = ""
    dataset_type: str = ""
    product_info: Dict[str, Any] = field(default_factory=dict)
    git_info: Dict[str, Any] = field(default_factory=dict)
    tc_info: Dict[str, Any] = field(default_factory=dict)
    case_id: str = ""
    code_pair_list: List[CodePair] = field(default_factory=list)

    def to_dict(self) -> Dict[str, Any]:
        d = asdict(self)
        return d


@dataclass
class AWCorpusItem(CorpusItem):
    function_name: str = ""
    description: str = ""
    implementation_code: str = ""
