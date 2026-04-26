import ast
import re
from typing import List, Tuple, Optional
from ..models.raw_source import RawSourceFile
from ..models.parsed_entity import StructuredEntity
from ..models.corpus_item import TestCaseCorpusItem, StepDetail
from ..models.docstring_structure import TestCaseDocStructure
from .enricher import Enricher


class TestCaseEnricher(Enricher):
    # ============================================================
    # [字段映射] 定义输入 JSON 字段 → 输出 JSON 字段的映射
    # 格式: "输入字段名": "输出字段名"
    # - 需要改名：如 "source_file_path": "file_path"
    # - 同名透传：如 "test_case_number": "test_case_number"
    # - 不需要出现在输出的字段：不写在这里就行
    # ============================================================
    FIELD_MAPPING = {
        "source_file_path": "file_path",
        "test_case_number": "test_case_number",
        "test_case_name": "test_case_name",
        "repo_path": "repo_path",
        "module": "module",
        "priority": "priority",
        "expected_result": "expected_result",
    }

    def enrich(self, raw: RawSourceFile, structured: List[StructuredEntity]) -> List[TestCaseCorpusItem]:
        items = []
        for entity in structured:
            doc_structure = entity.doc_structure
            if not isinstance(doc_structure, TestCaseDocStructure):
                continue

            # 合并所有方法的步骤为统一的 code_pair_list
            all_step_descriptions = doc_structure.step_descriptions
            all_method_source = ""
            for method_name in ["preCondition", "testSteps", "postCondition"]:
                source = entity.method_implementations.get(method_name, "")
                if source:
                    all_method_source += source + "\n"

            code_pair_list = self._match_steps_with_code(all_step_descriptions, all_method_source)

            # 按 FIELD_MAPPING 从输入 JSON 提取字段
            mapped_fields = {}
            for input_key, output_key in self.FIELD_MAPPING.items():
                if input_key in raw.metadata:
                    mapped_fields[output_key] = raw.metadata[input_key]

            items.append(TestCaseCorpusItem(
                code_pair_list=code_pair_list,
                **mapped_fields,
            ))
        return items

    def _match_steps_with_code(self, step_descriptions: List[str], method_source: str) -> List[StepDetail]:
        if not step_descriptions or not method_source:
            return [StepDetail(description=d, implementation_code="") for d in step_descriptions]

        log_info_blocks = self._split_by_log_info(method_source)

        results = []
        for i, description in enumerate(step_descriptions):
            log_info = None
            implementation_code = ""
            if i < len(log_info_blocks):
                log_info = log_info_blocks[i]["log_message"]
                implementation_code = log_info_blocks[i]["code_block"].strip()
            results.append(StepDetail(
                description=description,
                log_info=log_info,
                implementation_code=implementation_code,
            ))
        return results

    def _split_by_log_info(self, method_source: str) -> List[dict]:
        lines = method_source.split("\n")
        blocks = []
        current_log_message = None
        current_code_lines = []

        for line in lines:
            match = re.match(r'\s*tc\.logInfo\("(.+?)"\)', line)
            if match:
                if current_log_message is not None:
                    blocks.append({
                        "log_message": current_log_message,
                        "code_block": "\n".join(current_code_lines),
                    })
                current_log_message = match.group(1)
                current_code_lines = []
            elif current_log_message is not None:
                stripped = line.strip()
                if stripped and not stripped.startswith("def ") and stripped != "pass":
                    current_code_lines.append(stripped)

        if current_log_message is not None:
            blocks.append({
                "log_message": current_log_message,
                "code_block": "\n".join(current_code_lines),
            })

        return blocks
