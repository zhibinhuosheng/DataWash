import ast
from typing import List, Any, Tuple, Dict
from ...models.corpus_item import CodePair, StepSetup
from ...pipeline.pipeline_stage import PipelineStage


class TestCaseCorpusParseStage(PipelineStage):
    """
    从 ClassDef 节点中提取 prompt-code 对。
    - 以语句层级遍历方法体，保持控制流块(if/else/for/while/try)完整
    - 以 tc.logInfo(...) 中的字符串作为 prompt
    - 以到下一个同级 tc.logInfo 之间的代码作为 code
    - 控制流块内的 tc.logInfo 作为独立的 prompt-code 对递归提取
    - prompt_pos 和 code_pos 为闭区间行号
    """

    def process(self, data: List[Tuple[Dict[str, Any], str, ast.ClassDef, List[str]]]) -> List[Tuple[Dict[str, Any], str, List[CodePair]]]:
        results = []
        for metadata, class_name, class_node, source_lines in data:
            code_pairs = self._extract_pairs_from_class(class_node, source_lines)
            results.append((metadata, class_name, code_pairs))
        return results

    def _extract_pairs_from_class(self, class_node: ast.ClassDef, source_lines: List[str]) -> List[CodePair]:
        raw_pairs = []
        for method in class_node.body:
            if isinstance(method, (ast.FunctionDef, ast.AsyncFunctionDef)):
                pairs = self._extract_from_body(method.body, source_lines)
                raw_pairs.extend(pairs)
        return [
            CodePair(prompt=prompt, code=code, prompt_pos=prompt_pos, code_pos=code_pos, step_index=str(i))
            for i, (prompt, prompt_pos, code, code_pos) in enumerate(raw_pairs)
        ]

    def _extract_from_body(self, body: list, source_lines: List[str]) -> List[Tuple[str, str, str, str]]:
        """从语句列表中提取 prompt-code 对，保持控制流块完整"""
        pairs = []
        current_prompt = None
        current_prompt_pos = None
        code_start_line = None
        code_end_line = None

        for stmt in body:
            if self._is_log_info_stmt(stmt):
                # 保存上一个 pair
                if current_prompt is not None:
                    code = self._format_code(source_lines, code_start_line, code_end_line)
                    code_pos = f"[{code_start_line}, {code_end_line}]" if code else ""
                    pairs.append((current_prompt, current_prompt_pos, code, code_pos))
                # 开始新 pair
                current_prompt = self._get_log_info_message(stmt)
                current_prompt_pos = f"[{stmt.lineno}, {stmt.end_lineno}]"
                code_start_line = stmt.end_lineno + 1
                code_end_line = stmt.end_lineno
            elif self._contains_log_info(stmt):
                # 控制流块内含 logInfo → 整个块加入当前 code，并递归提取嵌套对
                code_end_line = stmt.end_lineno
                nested = self._extract_from_control_flow(stmt, source_lines)
                pairs.extend(nested)
            else:
                # 普通语句，扩展当前 code 范围
                code_end_line = stmt.end_lineno

        # 保存最后一个 pair
        if current_prompt is not None:
            end_line = code_end_line if code_end_line else (body[-1].end_lineno if body else code_start_line)
            code = self._format_code(source_lines, code_start_line, end_line)
            code_pos = f"[{code_start_line}, {end_line}]" if code else ""
            pairs.append((current_prompt, current_prompt_pos, code, code_pos))

        return pairs

    def _extract_from_control_flow(self, node: ast.AST, source_lines: List[str]) -> List[Tuple[str, str, str, str]]:
        """从控制流语句(if/else/for/while/try/with)中递归提取 logInfo 对"""
        pairs = []
        bodies = []

        if isinstance(node, ast.If):
            bodies.append(node.body)
            bodies.append(node.orelse)
        elif isinstance(node, (ast.For, ast.AsyncFor, ast.While)):
            bodies.append(node.body)
            bodies.append(node.orelse)
        elif isinstance(node, ast.Try):
            bodies.append(node.body)
            for handler in node.handlers:
                bodies.append(handler.body)
            bodies.append(node.orelse)
            bodies.append(node.finalbody)
        elif isinstance(node, (ast.With, ast.AsyncWith)):
            bodies.append(node.body)

        for body in bodies:
            if body:
                pairs.extend(self._extract_from_body(body, source_lines))

        return pairs

    # ── 辅助方法 ──

    def _is_log_info_stmt(self, stmt: ast.stmt) -> bool:
        if not isinstance(stmt, ast.Expr):
            return False
        return self._is_log_info_call(stmt.value)

    def _is_log_info_call(self, node: ast.AST) -> bool:
        return (isinstance(node, ast.Call)
                and isinstance(node.func, ast.Attribute)
                and node.func.attr == "logInfo"
                and isinstance(node.func.value, ast.Name)
                and node.func.value.id == "tc"
                and node.args
                and isinstance(node.args[0], (ast.Constant, ast.JoinedStr)))

    def _get_log_info_message(self, stmt: ast.stmt) -> str:
        call = stmt.value if isinstance(stmt, ast.Expr) else stmt
        arg = call.args[0]
        if isinstance(arg, ast.Constant):
            return arg.value
        # ast.JoinedStr (f-string): 拼接各部分，变量用 {name} 占位
        parts = []
        for v in arg.values:
            if isinstance(v, ast.Constant):
                parts.append(str(v.value))
            elif isinstance(v, ast.FormattedValue):
                parts.append("{" + ast.unparse(v.value) + "}")
        return "".join(parts)

    def _contains_log_info(self, node: ast.AST) -> bool:
        for child in ast.walk(node):
            if self._is_log_info_call(child):
                return True
        return False

    def _format_code(self, source_lines: List[str], start_line: int, end_line: int) -> str:
        if start_line is None or end_line is None or start_line > end_line:
            return ""
        lines = source_lines[start_line - 1:end_line]
        return "\n".join(
            line.strip() for line in lines
            if line.strip() and line.strip() != "pass"
        )
