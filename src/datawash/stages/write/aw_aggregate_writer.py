import json
import os
from dataclasses import asdict
from typing import Any, List
from ...models.corpus_item import AWCorpusItem
from ...config.pipeline_config import PipelineConfig
from .write_stage_base import WriteStageBase


class AWAggregateWriter(WriteStageBase):
    def __init__(self, config: PipelineConfig = None):
        self._config = config

    def process(self, items: Any) -> Any:
        return self._write_output(items)

    def _write_output(self, items: List[AWCorpusItem]) -> str:
        if self._config is None:
            return ""

        output_dir = self._config.output_dir
        os.makedirs(output_dir, exist_ok=True)

        output_path = os.path.join(output_dir, "aw_corpus.json")
        with open(output_path, "w", encoding="utf-8") as f:
            json.dump([asdict(item) for item in items], f, ensure_ascii=False, indent=4)

        return output_path
