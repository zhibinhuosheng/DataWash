from abc import abstractmethod
from typing import Any
from ...pipeline.pipeline_stage import PipelineStage
from ...models.corpus_item import CorpusItem

class WriteStageBase(PipelineStage):
    def process(self, items: Any) -> Any:
        self._validate_items(items)
        return self._write_output(items)

    def _validate_items(self, items: Any) -> None:
        if items is None:
            raise ValueError("No items to write")

    @abstractmethod
    def _write_output(self, items: Any) -> Any:
        raise NotImplementedError
