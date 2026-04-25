from abc import ABC, abstractmethod
from ..models.docstring_structure import DocstringStructure

class DocstringParser(ABC):
    @abstractmethod
    def parse_docstring(self, docstring: str) -> DocstringStructure:
        raise NotImplementedError
