# local-reindex

Consumer-профиль `document-indexer` для локальной папки.

Настройки берутся из `.env` в этой папке. Compose подключает его как
`env_file`; `IndexerSettings()` в `main.py` читает переменные процесса.

## Docker

Из корня `core-reindex`:

```bash
cp local-reindex/.env.example local-reindex/.env
docker compose up -d --build local-reindex
docker compose logs -f local-reindex
```

`WATCH_PATH` в `.env` должен совпадать с `LOCAL_DOCS_CONTAINER` в корневом
`.env`. Документы кладутся на хосте в `LOCAL_DOCS_HOST`.

Qdrant и Ollama должны быть на хосте. Из контейнера адрес — обычно
`http://host.docker.internal:...`.

## Нативный запуск

Для `python main.py` на хосте поменяйте в `.env`:

```dotenv
WATCH_PATH=docs
QDRANT_URL=http://127.0.0.1:6333
OLLAMA_BASE_URL=http://127.0.0.1:11434
```

```bash
python3.12 -m venv .venv
source .venv/bin/activate
pip install --upgrade pip
pip install --index-url https://download.pytorch.org/whl/cpu torch torchvision
pip install -e .
cp .env.example .env
python main.py
```
