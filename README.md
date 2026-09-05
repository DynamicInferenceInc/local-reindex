# local-reindex

Один образ, два режима через `CHUNKING__STRATEGY`:

- `table_aware` — обычные документы, коллекция `docs-local`;
- `resume_project` — резюме, коллекция `docs-cv`.

`document_indexer` сам выбирает чанкер, payload и LLM по стратегии.

## Docker

Из корня `core-reindex`:

```bash
cp local-reindex/.env.example local-reindex/.env
cp local-reindex/.env.cv.example local-reindex/.env.cv
docker compose up -d --build local-reindex local-cv
docker compose logs -f local-reindex local-cv
```

| Сервис | env | папка на хосте | коллекция | стратегия |
|---|---|---|---|---|
| `local-reindex` | `.env` | `LOCAL_DOCS_HOST` | `docs-local` | `table_aware` |
| `local-cv` | `.env.cv` | `LOCAL_CV_HOST` | `docs-cv` | `resume_project` |

`SOURCE__WATCH_PATH` в каждом файле должен совпадать с контейнерным путём
в корневом `.env` (`/data/docs` и `/data/cv`).

Обычные документы — в `LOCAL_DOCS_HOST`, резюме — в `LOCAL_CV_HOST`
(по умолчанию `local-reindex/cv/`).

Для resume: `ollama pull qwen3.8:27b-q8_0` (или `qwen3.8:27b`) — text LLM, не VLM.
Параметры под DGX Spark уже в `.env.cv.example`: `num_ctx=65536`, `num_predict=8192`,
таймаут 1800 с, `think=false`. На стороне Ollama: `OLLAMA_FLASH_ATTENTION=1`,
`OLLAMA_KEEP_ALIVE=-1`, `OLLAMA_NUM_PARALLEL=1`.

## Resume: что делает LLM

1. Парсер вытаскивает проекты из таблиц/размеченных блоков (шаблонные CV).
2. Если проектов нет или осталось много неразобранного текста — LLM ищет
   проекты в этом остатке и записывает их в те же шесть полей (`extraction_source=llm`).
3. Один вызов на резюме дозаполняет пустые поля и ставит `functional_direction` /
   `solution_platform`; значения парсера не перезаписываются.
4. Если проектов нет вообще — чанки `experience` (по местам работы) и один `profile`.
5. Каждое значение от LLM проверяется на наличие в тексте резюме, иначе отбрасывается.
6. `prose` с `needs_review=true` — только если LLM выключена или упала.

Аудит перед полной переиндексацией: в `.env.cv` выставить `RESUME_LLM_AUDIT=1`
(без embed/Qdrant), положить в `LOCAL_CV_HOST` 10–20 нешаблонных резюме, запустить `local-cv`.
В `LOCAL_CV_HOST` появятся `.resume_report.txt/.csv` и `.resume_chunks.jsonl` — сверить
чанки с исходниками. `RESUME_PARSE_ONLY=1` — тот же аудит без LLM.

После каждого reindex в логе и в `.resume_report.txt/.csv` — таблица
`ФИО | Должность | Проектов | из них LLM | Мест работы | Проверить | Файл` по всем резюме
коллекции, итоги и списки файлов без ФИО/должности.

Смена схемы: `QDRANT__INDEX_VERSION=resume-v20` переиндексирует все резюме.

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
