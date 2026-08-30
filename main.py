import os

from document_indexer import (
    DocumentIndexer,
    IndexerSettings,
    ProfileLocal,
    run,
)
from document_indexer.examples.resume import (
    FunctionalDirectionEnricher,
    ResumePayloadBuilder,
    ResumeProjectChunker,
    load_resume_prompt,
    load_resume_schema,
)


def _resume_indexer() -> DocumentIndexer:
    settings = ProfileLocal()
    model = settings.models.extraction_model.strip()
    enricher = None
    if model:
        enricher = FunctionalDirectionEnricher(
            load_resume_schema(),
            load_resume_prompt(),
            base_url=settings.models.ollama_base_url,
            model=model,
            timeout_sec=settings.models.extraction_timeout_sec,
        )
    chunking = settings.chunking
    return DocumentIndexer(
        settings,
        payload_builder=ResumePayloadBuilder(),
        enricher=enricher,
        document_chunker=ResumeProjectChunker(
            window_chars=chunking.window_chars,
            window_overlap=chunking.window_overlap,
        ),
    )


if __name__ == "__main__":
    if os.environ.get("INDEXER_PROFILE") == "resume":
        _resume_indexer().run()
    else:
        run(IndexerSettings())
