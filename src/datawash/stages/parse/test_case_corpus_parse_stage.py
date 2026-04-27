import ast
from typing import List, Any, Tuple, Dict
from ...models.corpus_item import CodePair, StepSetup
from ...pipeline.pipeline_stage import PipelineStage


class TestCaseCorpusParseStage(PipelineStage):
    """
    从 ClassDef 节点中提取 prompt-code 对。
    - 遍历 class 中所有方法
    - 以 tc.logInfo(...) 中的字符串作为 prompt
    - 以到下一个 tc.logInfo 之间的代码作为 code
    - 同时提取 prompt_pos 和 code_pos（行号位置）
    """

    def process(self, data: List[Tuple[Dict[str, Any], str, ast.ClassDef, List[str]]]) -> List[Tuple[Dict[str, Any], str, List[CodePair]]]:
        results = []
        for metadata, class_name, class_node, source_lines in data:
            code_pairs = self._extract_pairs_from_class(class_node, source_lines)
            results.append((metadata, class_name, code_pairs))
        return results

    def _extract_pairs_from_class(self, class_node: ast.ClassDef, source_lines: List[str]) -> List[CodePair]:
        code_pairs = []
        step_index = 0

        for method in class_node.body:
            if not isinstance(method, (ast.FunctionDef, ast.AsyncFunctionDef)):
                continue

            method_pairs = self._extract_pairs_from_method(method, source_lines, step_index)
            code_pairs.extend(method_pairs)
            step_index += len(method_pairs)

        return code_pairs

    def _extract_pairs_from_method(
        self,
        method: ast.FunctionDef,
        source_lines: List[str],
        start_index: int,
    ) -> List[CodePair]:
        pairs = []
        log_info_calls = self._find_log_info_calls(method)

        if not log_info_calls:
            return pairs

        for i, call_info in enumerate(log_info_calls):
            prompt = call_info["message"]
            prompt_pos = call_info["pos"]

            code_start_line = call_info["end_line"]
            if i + 1 < len(log_info_calls):
                code_end_line = log_info_calls[i + 1]["start_line"]
            else:
                code_end_line = method.end_lineno

            code_lines = source_lines[code_start_line - 1:code_end_line - 1]
            code = "\n".join(
                line.strip() for line in code_lines
                if line.strip() and line.strip() != "pass"
            )

            code_pos = f"{code_start_line}-{code_end_line}" if code else ""

            pairs.append(CodePair(
                prompt=prompt,
                code=code,
                prompt_pos=prompt_pos,
                code_pos=code_pos,
                step_index=str(start_index + i),
            ))

        return pairs

    def _find_log_info_calls(self, method: ast.FunctionDef) -> List[dict]:
        calls = []
        for node in ast.walk(method):
            if not isinstance(node, ast.Call):
                continue

            if (isinstance(node.func, ast.Attribute)
                    and node.func.attr == "logInfo"
                    and isinstance(node.func.value, ast.Name)
                    and node.func.value.id == "tc"
                    and node.args
                    and isinstance(node.args[0], ast.Constant)):
                calls.append({
                    "message": node.args[0].value,
                    "start_line": node.lineno,
                    "end_line": node.end_lineno + 1,
                    "pos": f"{node.lineno}-{node.end_lineno}",
                })

        calls.sort(key=lambda c: c["start_line"])
        return calls
