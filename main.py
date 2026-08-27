import os

from document_indexer import (
    DocumentIndexer,
    IndexerSettings,
    JsonSchemaEnricher,
    ProfileLocal,
    run,
)
from document_indexer.examples.resume import (
    ResumePayloadBuilder,
    load_resume_prompt,
    load_resume_schema,
)


def _resume_indexer() -> DocumentIndexer:
    settings = ProfileLocal()
    model = settings.models.extraction_model.strip()
    enricher = None
    if model:
        enricher = JsonSchemaEnricher(
            load_resume_schema(),
            load_resume_prompt(),
            base_url=settings.models.ollama_base_url,
            model=model,
            timeout_sec=settings.models.extraction_timeout_sec,
        )
    return DocumentIndexer(
        settings,
        payload_builder=ResumePayloadBuilder(),
        enricher=enricher,
    )


if __name__ == "__main__":
    if os.environ.get("INDEXER_PROFILE") == "resume":
        _resume_indexer().run()
    else:
        run(IndexerSettings())
