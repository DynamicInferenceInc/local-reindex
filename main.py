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
    parse_only_enabled,
    run_resume_parse_audit,
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


def _log_startup() -> None:
    print(
        "Startup INDEXER_PROFILE="
        f"{os.environ.get('INDEXER_PROFILE')!r} "
        f"RESUME_PARSE_ONLY={os.environ.get('RESUME_PARSE_ONLY')!r} "
        f"parse_only={parse_only_enabled()}",
        flush=True,
    )


if __name__ == "__main__":
    _log_startup()
    if os.environ.get("INDEXER_PROFILE") == "resume":
        if parse_only_enabled():
            run_resume_parse_audit(ProfileLocal())
        else:
            _resume_indexer().run()
    else:
        run(IndexerSettings())
