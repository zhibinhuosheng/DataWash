from abc import abstractmethod
from typing import List, Any
from ...pipeline.pipeline_stage import PipelineStage


class ReadStageBase(PipelineStage):
    def process(self, data: Any) -> Any:
        self._validate_config(data)
        result = self._read_sources(data)
        self._validate_result(result)
        return result

    def _validate_config(self, data: Any) -> None:
        if data is None:
            raise ValueError("Pipeline config cannot be None")

    @abstractmethod
    def _read_sources(self, data: Any) -> Any:
        raise NotImplementedError

    def _validate_result(self, result: Any) -> None:
        if not result:
            raise ValueError("No data was read from input")
