# local-reindex

Consumer-профиль `document-indexer` для локальной папки. Документы — в `docs/`.

Нативно (Qdrant и Ollama на этой машине):

```bash
python3.12 -m venv .venv
source .venv/bin/activate
pip install --upgrade pip
pip install --index-url https://download.pytorch.org/whl/cpu torch torchvision
pip install -e .
cp .env.example .env   # если ещё нет
python main.py
```

Деплой обоих профилей — из `../document_indexer`:

```bash
docker compose up -d --build
docker logs -f local-reindex
```
