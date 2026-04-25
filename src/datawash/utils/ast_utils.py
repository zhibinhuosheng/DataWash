import ast
from typing import Optional

def get_source_segment(source: str, node: ast.AST) -> Optional[str]:
    return ast.get_source_segment(source, node)

def extract_method_source(source: str, class_node: ast.ClassDef, method_name: str) -> Optional[str]:
    for item in class_node.body:
        if isinstance(item, ast.FunctionDef) and item.name == method_name:
            return ast.get_source_segment(source, item)
    return None
