from typing import List, Tuple, Any
from ...pipeline.pipeline_stage import PipelineStage
from ...models.raw_source import RawSourceFile
from ...models.parsed_entity import ParsedEntity
from ...parsers.source_parser import SourceParser

class ASTParseStage(PipelineStage):
    def __init__(self, parser: SourceParser):
        self._parser = parser

    def process(self, data: List[RawSourceFile]) -> List[Tuple[RawSourceFile, List[ParsedEntity]]]:
        result = []
        for raw_file in data:
            entities = self._parser.parse(raw_file)
            result.append((raw_file, entities))
        return result
