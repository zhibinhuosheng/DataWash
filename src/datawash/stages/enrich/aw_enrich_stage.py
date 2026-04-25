from ...enrichers.aw_enricher import AWEnricher
from .enrich_stage_base import EnrichStageBase

class AWEnrichStage(EnrichStageBase):
    def __init__(self):
        super().__init__(enricher=AWEnricher())
