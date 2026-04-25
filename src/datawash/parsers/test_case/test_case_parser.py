import ast
from typing import List, Dict
from ...models.raw_source import RawSourceFile
from ...models.parsed_entity import ParsedEntity
from ..source_parser import SourceParser


class TestCaseParser(SourceParser):
    def parse(self, raw: RawSourceFile) -> List[ParsedEntity]:
        tree = ast.parse(raw.source_code)
        entities = []
        for node in ast.walk(tree):
            if isinstance(node, ast.ClassDef) and node.name.startswith("Test_"):
                docstring = ast.get_docstring(node) or ""
                method_implementations = self._extract_methods(raw.source_code, node)
                entities.append(ParsedEntity(
                    name=node.name,
                    docstring=docstring,
                    method_implementations=method_implementations,
                    body_source="",
                ))
        return entities

    def _extract_methods(self, source: str, class_node: ast.ClassDef) -> Dict[str, str]:
        methods = {}
        for item in class_node.body:
            if isinstance(item, ast.FunctionDef):
                source_segment = ast.get_source_segment(source, item)
                if source_segment:
                    methods[item.name] = source_segment
        return methods
