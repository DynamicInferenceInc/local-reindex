# local-reindex

Один образ, два режима через `INDEXER_PROFILE`:

- `default` (или переменная не `resume`) — обычный payload, `run(IndexerSettings())`;
- `resume` — `ResumeProjectChunker` + `ResumePayloadBuilder` + `FunctionalDirectionEnricher`, коллекция `docs-cv`.

## Docker

Из корня `core-reindex`:

```bash
cp local-reindex/.env.example local-reindex/.env
cp local-reindex/.env.cv.example local-reindex/.env.cv
docker compose up -d --build local-reindex local-cv
docker compose logs -f local-reindex local-cv
```

| Сервис | env | папка на хосте | коллекция |
|---|---|---|---|
| `local-reindex` | `.env` | `LOCAL_DOCS_HOST` | `docs-local` |
| `local-cv` | `.env.cv` | `LOCAL_CV_HOST` | `docs-cv` |

`SOURCE__WATCH_PATH` в каждом файле должен совпадать с контейнерным путём
в корневом `.env` (`/data/docs` и `/data/cv`).

Обычные документы — в `LOCAL_DOCS_HOST`, резюме — в `LOCAL_CV_HOST`
(по умолчанию `local-reindex/cv/`).

Для resume: `ollama pull qwen3:8b` (text LLM, не VLM).

## Нативный запуск

Обычный индекс:

```bash
cp .env.example .env
python main.py
```

Resume:

```bash
cp .env.cv.example .env.cv
set -a && source .env.cv && set +a
python main.py
```
