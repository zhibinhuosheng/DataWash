import ast
from typing import List
from ...models.raw_source import RawSourceFile
from ...models.parsed_entity import ParsedEntity
from ..source_parser import SourceParser


class AWFunctionParser(SourceParser):
    def parse(self, raw: RawSourceFile) -> List[ParsedEntity]:
        tree = ast.parse(raw.source_code)
        entities = []
        for node in ast.iter_child_nodes(tree):
            if isinstance(node, ast.FunctionDef) and node.name.startswith("aw_"):
                docstring = ast.get_docstring(node) or ""
                body_source = self._extract_body_source(raw.source_code, node)
                entities.append(ParsedEntity(
                    name=node.name,
                    docstring=docstring,
                    body_source=body_source,
                ))
        return entities

    def _extract_body_source(self, source: str, func_node: ast.FunctionDef) -> str:
        lines = source.split("\n")
        body_lines = []
        for stmt in func_node.body:
            if isinstance(stmt, ast.Expr) and isinstance(stmt.value, ast.Constant):
                continue
            if isinstance(stmt, ast.Pass):
                continue
            start = stmt.lineno - 1
            end = stmt.end_lineno
            for i in range(start, end):
                body_lines.append(lines[i])
        raw = "\n".join(body_lines)
        return self._dedent(raw)

    def _dedent(self, code: str) -> str:
        lines = code.split("\n")
        non_empty = [line for line in lines if line.strip()]
        if not non_empty:
            return ""
        min_indent = min(len(line) - len(line.lstrip()) for line in non_empty)
        return "\n".join(line[min_indent:] if len(line) >= min_indent else line for line in lines).strip()
