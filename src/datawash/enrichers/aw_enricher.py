from typing import List
from ..models.raw_source import RawSourceFile
from ..models.parsed_entity import StructuredEntity
from ..models.corpus_item import AWCorpusItem
from ..models.docstring_structure import AWDocStructure
from .enricher import Enricher


class AWEnricher(Enricher):
    def enrich(self, raw: RawSourceFile, structured: List[StructuredEntity]) -> List[AWCorpusItem]:
        items = []
        for entity in structured:
            doc_structure = entity.doc_structure
            if not isinstance(doc_structure, AWDocStructure):
                continue
            items.append(AWCorpusItem(
                function_name=entity.name,
                description=doc_structure.description,
                implementation_code=entity.body_source,
            ))
        return items
