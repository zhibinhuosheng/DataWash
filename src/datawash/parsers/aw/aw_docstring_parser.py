import re
from ...models.docstring_structure import AWDocStructure
from ..docstring_parser import DocstringParser


class AWDocstringParser(DocstringParser):
    def parse_docstring(self, docstring: str) -> AWDocStructure:
        if not docstring:
            return AWDocStructure()

        pattern = r"函数功能描述:\s*(.+)"
        match = re.search(pattern, docstring)
        description = match.group(1).strip() if match else ""

        return AWDocStructure(description=description)
