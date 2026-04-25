import json
import os
from dataclasses import asdict
from typing import Any, List
from ...models.corpus_item import TestCaseCorpusItem
from ...config.pipeline_config import PipelineConfig
from .write_stage_base import WriteStageBase


class TestCaseFileWriter(WriteStageBase):
    def __init__(self, config: PipelineConfig = None):
        self._config = config

    def process(self, items: Any) -> Any:
        return self._write_output(items)

    def _write_output(self, items: List[TestCaseCorpusItem]) -> str:
        if self._config is None:
            return ""

        output_dir = self._config.output_dir
        os.makedirs(output_dir, exist_ok=True)

        for item in items:
            file_path = os.path.join(output_dir, f"{item.test_case_number}.json")
            with open(file_path, "w", encoding="utf-8") as f:
                json.dump(asdict(item), f, ensure_ascii=False, indent=4)

        return output_dir
