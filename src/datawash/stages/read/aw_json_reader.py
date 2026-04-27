import json
import os
from typing import List, Any
from ...models.raw_source import RawSourceFile
from ...utils.file_utils import read_file
from .read_stage_base import ReadStageBase


class AWJsonReader(ReadStageBase):
    def _read_sources(self, data: Any) -> List[RawSourceFile]:
        config = data
        raw_files = []
        for input_path in [config.input_path]:
            input_data = json.loads(read_file(input_path))
            file_paths = input_data.get("file_paths", [])
            for file_path in file_paths:
                source_file = file_path
                source_code = read_file(source_file)
                raw_files.append(RawSourceFile(
                    file_path=file_path,
                    source_code=source_code,
                    metadata={},
                ))
        return raw_files
