import re
from typing import List
from ...models.docstring_structure import TestCaseDocStructure
from ..docstring_parser import DocstringParser


class TestCaseDocstringParser(DocstringParser):
    def parse_docstring(self, docstring: str) -> TestCaseDocStructure:
        if not docstring:
            return TestCaseDocStructure()

        return TestCaseDocStructure(
            test_case_number=self._extract_field(docstring, "TestCaseNumber"),
            test_case_name=self._extract_field(docstring, "TestCaseName"),
            pre_conditions=self._extract_numbered_items(docstring, "preCondition"),
            test_steps=self._extract_numbered_items(docstring, "testSteps"),
            post_conditions=self._extract_numbered_items(docstring, "postCondition"),
        )

    def _extract_field(self, text: str, field_name: str) -> str:
        pattern = rf"{field_name}:\s*(.+)"
        match = re.search(pattern, text)
        return match.group(1).strip() if match else ""

    def _extract_numbered_items(self, text: str, section_name: str) -> List[str]:
        pattern = rf"{section_name}:\s*\n(.*?)(?=\n\w+:|$)"
        match = re.search(pattern, text, re.DOTALL)
        if not match:
            return []
        section = match.group(1)
        item_pattern = r"^\d+\.(.+)$"
        items = re.findall(item_pattern, section, re.MULTILINE)
        return [item.strip() for item in items]
