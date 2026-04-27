import ast
from typing import List, Any, Tuple, Dict
from ...pipeline.pipeline_stage import PipelineStage
from ...utils.file_utils import read_file


class TestCaseClassParseStage(PipelineStage):
    """
    读取源文件，找到与 test_case_number 匹配的 ClassDef 节点。
    输入: List[metadata_dict]
    输出: List[(metadata, class_name, class_node, source_lines)]
    """

    def process(self, data: List[Dict[str, Any]]) -> List[Tuple[Dict[str, Any], str, ast.ClassDef, List[str]]]:
        results = []
        for metadata in data:
            test_case_number = metadata.get("test_case_number", "")
            source_path = metadata.get("file_full_path", metadata.get("file_path", ""))
            source_code = read_file(source_path) if source_path else ""
            if not source_code:
                continue

            tree = ast.parse(source_code)
            source_lines = source_code.splitlines()

            # 找到类名中包含 test_case_number 的 ClassDef
            class_node = self._find_class_by_number(tree, test_case_number)
            if class_node is None:
                continue

            results.append((metadata, class_node.name, class_node, source_lines))
        return results

    def _find_class_by_number(self, tree: ast.AST, test_case_number: str) -> ast.ClassDef | None:
        for node in ast.walk(tree):
            if isinstance(node, ast.ClassDef) and test_case_number in node.name:
                return node
        return None
