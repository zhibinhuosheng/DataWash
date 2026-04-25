from typing import List, Tuple, Any
from ...pipeline.pipeline_stage import PipelineStage
from ...models.raw_source import RawSourceFile
from ...models.parsed_entity import ParsedEntity, StructuredEntity
from ...parsers.docstring_parser import DocstringParser

class DocstringExtractStage(PipelineStage):
    def __init__(self, docstring_parser: DocstringParser):
        self._docstring_parser = docstring_parser

    def process(self, data: List[Tuple[RawSourceFile, List[ParsedEntity]]]) -> List[Tuple[RawSourceFile, List[StructuredEntity]]]:
        result = []
        for raw_file, entities in data:
            structured_entities = []
            for entity in entities:
                doc_structure = self._docstring_parser.parse_docstring(entity.docstring)
                structured_entities.append(StructuredEntity(
                    name=entity.name,
                    doc_structure=doc_structure,
                    method_implementations=entity.method_implementations,
                    body_source=entity.body_source,
                ))
            result.append((raw_file, structured_entities))
        return result
