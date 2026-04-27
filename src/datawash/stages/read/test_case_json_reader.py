import json
import os
from typing import List, Any, Dict
from ...utils.file_utils import read_file, list_json_files
from .read_stage_base import ReadStageBase


class TestCaseJsonReader(ReadStageBase):
    """
    读取输入文件夹中的所有 JSON 文件，返回 metadata 列表。
    源码读取交给后续的 TestCaseCorpusParseStage。
    """

    def _read_sources(self, data: Any) -> List[Dict[str, Any]]:
        config = data
        results = []

        json_files = list_json_files(config.input_path) if os.path.isdir(config.input_path) else [config.input_path]
        for json_file in json_files:
            metadata = json.loads(read_file(json_file))
            results.append(metadata)

        return results
