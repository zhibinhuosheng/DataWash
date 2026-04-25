from abc import abstractmethod
from typing import List, Any
from ...pipeline.pipeline_stage import PipelineStage
from ...models.raw_source import RawSourceFile

class ReadStageBase(PipelineStage):
    def process(self, data: Any) -> List[RawSourceFile]:
        self._validate_config(data)
        raw_files = self._read_sources(data)
        self._validate_raw_files(raw_files)
        return raw_files

    def _validate_config(self, data: Any) -> None:
        if data is None:
            raise ValueError("Pipeline config cannot be None")

    @abstractmethod
    def _read_sources(self, data: Any) -> List[RawSourceFile]:
        raise NotImplementedError

    def _validate_raw_files(self, files: List[RawSourceFile]) -> None:
        if not files:
            raise ValueError("No source files were read")
