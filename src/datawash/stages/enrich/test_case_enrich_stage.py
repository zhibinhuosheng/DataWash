from ...enrichers.test_case_enricher import TestCaseEnricher
from .enrich_stage_base import EnrichStageBase

class TestCaseEnrichStage(EnrichStageBase):
    def __init__(self):
        super().__init__(enricher=TestCaseEnricher())
