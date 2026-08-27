# local-reindex

Consumer-профиль `document-indexer` для локальной папки. Payload как у
дефолтного индексатора, без LLM-полей резюме.

Настройки — вложенные ключи `SOURCE__` / `QDRANT__` / `MODELS__` в `.env`.
Compose подключает файл как `env_file`; `IndexerSettings()` в `main.py`
читает переменные процесса.

## Docker

Из корня `core-reindex`:

```bash
cp local-reindex/.env.example local-reindex/.env
docker compose up -d --build local-reindex
docker compose logs -f local-reindex
```

`SOURCE__WATCH_PATH` должен совпадать с `LOCAL_DOCS_CONTAINER` в корневом
`.env`. Документы кладутся на хосте в `LOCAL_DOCS_HOST`.

Qdrant и Ollama на хосте. Из контейнера — `http://host.docker.internal:...`.

## Нативный запуск

В `.env` для хоста:

```dotenv
SOURCE__WATCH_PATH=docs
QDRANT__URL=http://127.0.0.1:6333
MODELS__OLLAMA_BASE_URL=http://127.0.0.1:11434
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
