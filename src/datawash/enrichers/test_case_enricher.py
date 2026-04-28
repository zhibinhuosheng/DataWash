from typing import List, Any
from ..models.corpus_item import TestCaseCorpusItem
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
        # 顶层字段
        "file_name": "file_name",
        "test_framework": "test_framework",
        "dataset_type": "dataset_type",
        "case_id": "case_id",
        "path": "path",
        # 嵌套对象 → 顶层 dict
        "tmss_original.dataset_type": "dataset_type",
        "product_info": "product_info",
        "git_info": "git_info",
        # tc_info 嵌套字段映射
        "case_info.test_case_name": "tc_info.test_case_name",
        "case_info.test_step": "tc_info.test_step",
        "case_info.test_environment_type": "tc_info.test_environment_type",
        "case_info.test_feature": "tc_info.test_feature",
        "case_info.test_case_number": "tc_info.test_case_number",
        "case_info.test_activity": "tc_info.test_activity",
        "case_info.pre_condition": "tc_info.pre_condition",
        "case_info.test_case_type": "tc_info.test_case_type",
        "case_info.expected_result": "tc_info.expected_result",
    }

    def enrich(self, metadata: dict, parsed_data: Any) -> List[TestCaseCorpusItem]:
        class_name, code_pairs, dependencies = parsed_data

        # 按 FIELD_MAPPING 提取字段
        mapped = self._map_fields(metadata)

        # 确保 class_name 来自 AST 解析
        mapped["class_name"] = class_name

        # 填入 dependencies（来自 AST import 解析）
        mapped["dependencies"] = dependencies

        # 填入 code_pair_list
        mapped["code_pair_list"] = code_pairs

        return [TestCaseCorpusItem(**mapped)]

    def _map_fields(self, metadata: dict) -> dict:
        """按 FIELD_MAPPING 从输入 JSON 中提取并映射字段"""
        result = {}
        for input_key, output_key in self.FIELD_MAPPING.items():
            value = self._get_nested(metadata, input_key)
            if value is None:
                continue
            self._set_nested(result, output_key, value)
        return result

    def _get_nested(self, d: dict, key: str) -> Any:
        """获取嵌套字典值，如 'case_info.test_case_name'"""
        keys = key.split(".")
        current = d
        for k in keys:
            if not isinstance(current, dict) or k not in current:
                return None
            current = current[k]
        return current

    def _set_nested(self, d: dict, key: str, value: Any):
        """设置嵌套字典值，如 'tc_info.test_case_name'"""
        keys = key.split(".")
        current = d
        for k in keys[:-1]:
            if k not in current:
                current[k] = {}
            current = current[k]
        current[keys[-1]] = value
