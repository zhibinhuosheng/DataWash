import ast
from typing import List, Any, Tuple, Dict
from ...pipeline.pipeline_stage import PipelineStage
from ...utils.file_utils import read_file


class TestCaseClassParseStage(PipelineStage):
    """
    读取源文件，找到与 test_case_number 匹配的 ClassDef 节点，提取文件级 import 依赖。
    输入: List[metadata_dict]
    输出: List[(metadata, class_name, class_node, source_lines, dependencies, import_map)]
    """

    def process(self, data: List[Dict[str, Any]]) -> List[Tuple[Dict[str, Any], str, ast.ClassDef, List[str], str, Dict[str, str]]]:
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

            # 提取文件级 import 依赖
            dependencies, import_map = self._extract_imports(tree)

            results.append((metadata, class_node.name, class_node, source_lines, dependencies, import_map))
        return results

    def _find_class_by_number(self, tree: ast.AST, test_case_number: str) -> ast.ClassDef | None:
        for node in ast.walk(tree):
            if isinstance(node, ast.ClassDef) and test_case_number in node.name:
                return node
        return None

    def _extract_imports(self, tree: ast.Module) -> Tuple[str, Dict[str, str]]:
        """提取文件级 import 语句，返回 (完整语句拼接, 名称→语句映射)"""
        import_stmts = []
        import_map = {}

        for node in tree.body:
            if isinstance(node, ast.ImportFrom):
                names = ", ".join(alias.name for alias in node.names)
                stmt = f"from {node.module} import {names}"
                import_stmts.append(stmt)
                for alias in node.names:
                    import_map[alias.asname or alias.name] = stmt
            elif isinstance(node, ast.Import):
                names = ", ".join(alias.name for alias in node.names)
                stmt = f"import {names}"
                import_stmts.append(stmt)
                for alias in node.names:
                    import_map[alias.asname or alias.name] = stmt

        dependencies = "; ".join(import_stmts)
        return dependencies, import_map
