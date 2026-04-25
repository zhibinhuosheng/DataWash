from typing import List, Any
from .pipeline_stage import PipelineStage

class Pipeline:
    def __init__(self):
        self._stages: List[PipelineStage] = []

    def add_stage(self, stage: PipelineStage) -> "Pipeline":
        self._stages.append(stage)
        return self

    def run(self, initial_data: Any = None) -> Any:
        data = initial_data
        for stage in self._stages:
            data = stage.process(data)
        return data
