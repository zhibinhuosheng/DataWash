from typing import List, Tuple, Any
from ...pipeline.pipeline_stage import PipelineStage
from ...models.corpus_item import CorpusItem
from ...enrichers.enricher import Enricher


class EnrichStageBase(PipelineStage):
    def __init__(self, enricher: Enricher):
        self._enricher = enricher

    def process(self, data: List[Tuple]) -> List[CorpusItem]:
        result = []
        for metadata, class_name, code_pairs in data:
            items = self._enricher.enrich(metadata, (class_name, code_pairs))
            result.extend(items)
        return result
