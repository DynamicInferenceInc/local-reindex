# local-reindex

Профиль `document-indexer` для локальной папки. Один процесс = одна коллекция Qdrant.

Настройки — вложенные ключи `SOURCE__*`, `QDRANT__*`, `MODELS__*` (как в `document-indexer`).
`IndexerSettings` / `ProfileLocal` читают `.env` из рабочей директории.

## Зависимости

Нужны запущенные **Ollama** и **Qdrant** на хосте. Если они уже подняты
`it-consultant-1c` (контейнеры `it-consultant-ollama` / `it-consultant-qdrant`),
достаточно портов `11434` и `6333`. Модель эмбеддингов: `nomic-embed-text`.

Документы кладите в каталог `SOURCE__WATCH_PATH` (по умолчанию `docs/`).

## Нативный запуск

```bash
cp .env.example .env
# при необходимости поправьте SOURCE__WATCH_PATH и QDRANT__*

python3.12 -m venv .venv
source .venv/bin/activate
pip install --upgrade pip
pip install --index-url https://download.pytorch.org/whl/cpu torch torchvision
pip install -e .
python main.py
```

Первый прогон сверкает папку с Qdrant, дальше watchdog индексирует create/modify/delete.

VLM для картинок по умолчанию выключен (`MODELS__PICTURE_DESCRIPTION_ENABLED=false`).
Чтобы включить, поставьте `true` и заранее скачайте модель: `ollama pull qwen3-vl:8b`.

## Docker

Образ собирается поверх `document-indexer`. Из контейнера Qdrant/Ollama обычно
доступны как `http://host.docker.internal:6333` и `:11434` — поменяйте URL в `.env`.

```bash
cp .env.example .env
docker compose up -d --build local-reindex
docker compose logs -f local-reindex
```
