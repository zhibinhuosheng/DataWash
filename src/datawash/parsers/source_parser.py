from abc import ABC, abstractmethod
from typing import List
from ..models.raw_source import RawSourceFile
from ..models.parsed_entity import ParsedEntity

class SourceParser(ABC):
    @abstractmethod
    def parse(self, raw: RawSourceFile) -> List[ParsedEntity]:
        raise NotImplementedError
