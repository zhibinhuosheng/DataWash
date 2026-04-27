from ..config.pipeline_config import PipelineConfig
from .pipeline import Pipeline


class PipelineBuilder:
    @staticmethod
    def build_test_case_pipeline(config: PipelineConfig) -> Pipeline:
        from ..stages.read.test_case_json_reader import TestCaseJsonReader
        from ..stages.parse.test_case_class_parse_stage import TestCaseClassParseStage
        from ..stages.parse.test_case_corpus_parse_stage import TestCaseCorpusParseStage
        from ..stages.enrich.test_case_enrich_stage import TestCaseEnrichStage
        from ..stages.write.test_case_file_writer import TestCaseFileWriter

        pipeline = Pipeline()
        pipeline.add_stage(TestCaseJsonReader()) \
                .add_stage(TestCaseClassParseStage()) \
                .add_stage(TestCaseCorpusParseStage()) \
                .add_stage(TestCaseEnrichStage()) \
                .add_stage(TestCaseFileWriter(config=config))
        return pipeline

    @staticmethod
    def build_aw_pipeline(config: PipelineConfig) -> Pipeline:
        from ..stages.read.aw_json_reader import AWJsonReader
        from ..stages.parse.ast_parse_stage import ASTParseStage
        from ..parsers.aw.aw_parser import AWFunctionParser
        from ..stages.extract.docstring_extract_stage import DocstringExtractStage
        from ..parsers.aw.aw_docstring_parser import AWDocstringParser
        from ..stages.enrich.aw_enrich_stage import AWEnrichStage
        from ..stages.write.aw_aggregate_writer import AWAggregateWriter

        pipeline = Pipeline()
        pipeline.add_stage(AWJsonReader()) \
                .add_stage(ASTParseStage(parser=AWFunctionParser())) \
                .add_stage(DocstringExtractStage(docstring_parser=AWDocstringParser())) \
                .add_stage(AWEnrichStage()) \
                .add_stage(AWAggregateWriter(config=config))
        return pipeline
