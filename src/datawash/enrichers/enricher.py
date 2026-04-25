from abc import ABC, abstractmethod
from typing import List
from ..models.raw_source import RawSourceFile
from ..models.parsed_entity import StructuredEntity
from ..models.corpus_item import CorpusItem

class Enricher(ABC):
    @abstractmethod
    def enrich(self, raw: RawSourceFile, structured: List[StructuredEntity]) -> List[CorpusItem]:
        raise NotImplementedError
