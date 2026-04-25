import json
import os
from typing import List, Any
from ...models.raw_source import RawSourceFile
from ...utils.file_utils import read_file, list_json_files
from .read_stage_base import ReadStageBase


class TestCaseJsonReader(ReadStageBase):
    def _read_sources(self, data: Any) -> List[RawSourceFile]:
        config = data
        raw_files = []
        for input_path in config.input_paths:
            json_files = list_json_files(input_path) if os.path.isdir(input_path) else [input_path]
            for json_file in json_files:
                metadata = json.loads(read_file(json_file))
                source_file = os.path.join(config.source_root, metadata["source_file_path"])
                source_code = read_file(source_file)
                raw_files.append(RawSourceFile(
                    file_path=metadata["source_file_path"],
                    source_code=source_code,
                    metadata=metadata,
                ))
        return raw_files
