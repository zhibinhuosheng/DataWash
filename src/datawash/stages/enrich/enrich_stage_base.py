from abc import abstractmethod
from typing import List, Tuple, Any
from ...pipeline.pipeline_stage import PipelineStage
from ...models.raw_source import RawSourceFile
from ...models.parsed_entity import StructuredEntity
from ...models.corpus_item import CorpusItem
from ...enrichers.enricher import Enricher

class EnrichStageBase(PipelineStage):
    def __init__(self, enricher: Enricher):
        self._enricher = enricher

    def process(self, data: List[Tuple[RawSourceFile, List[StructuredEntity]]]) -> List[CorpusItem]:
        result = []
        for raw_file, entities in data:
            items = self._enricher.enrich(raw_file, entities)
            result.extend(items)
        return result
