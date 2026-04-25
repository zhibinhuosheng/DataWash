import ast
import re
from typing import List, Tuple, Optional
from ..models.raw_source import RawSourceFile
from ..models.parsed_entity import StructuredEntity
from ..models.corpus_item import TestCaseCorpusItem, StepDetail
from ..models.docstring_structure import TestCaseDocStructure
from .enricher import Enricher


class TestCaseEnricher(Enricher):
    def enrich(self, raw: RawSourceFile, structured: List[StructuredEntity]) -> List[TestCaseCorpusItem]:
        items = []
        for entity in structured:
            doc_structure = entity.doc_structure
            if not isinstance(doc_structure, TestCaseDocStructure):
                continue

            pre_conditions = self._match_steps_with_code(
                doc_structure.pre_conditions,
                entity.method_implementations.get("preCondition", ""),
            )
            test_steps = self._match_steps_with_code(
                doc_structure.test_steps,
                entity.method_implementations.get("testSteps", ""),
            )
            post_conditions = self._match_steps_with_code(
                doc_structure.post_conditions,
                entity.method_implementations.get("postCondition", ""),
            )

            items.append(TestCaseCorpusItem(
                metadata=raw.metadata,
                test_case_number=doc_structure.test_case_number,
                test_case_name=doc_structure.test_case_name,
                pre_conditions=pre_conditions,
                test_steps=test_steps,
                post_conditions=post_conditions,
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
