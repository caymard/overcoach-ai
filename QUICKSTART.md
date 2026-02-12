# Quick Start Guide

## Prerequisites Check

```bash
# 1. Python 3.12
python3.12 --version

# 2. Ollama running
curl http://localhost:11434/api/tags

# 3. Mistral model
ollama list | grep mistral:7b
```

## Installation (5 minutes)

```bash
# 1. Setup environment
python3.12 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

# 2. Ingest data (first time only, ~2 minutes)
python -m src.ingestion.markdown_gen
python -m src.rag.indexer

# 3. Start API
uvicorn src.api.main:app --reload
```

Or use the start script:
```bash
./start.sh
```

## Quick Test

```bash
# Health check
curl http://localhost:8000/health

# Get team suggestion
curl -X POST http://localhost:8000/suggest \
  -H "Content-Type: application/json" \
  -d '{
    "map_name": "Dorado",
    "enemy_team": ["Reinhardt", "Bastion", "Mercy"],
    "current_team": [],
    "difficulties": "Strong bunker defense"
  }'
```

## API Endpoints

- **GET** `/health` - System status
- **GET** `/heroes` - List all heroes
- **GET** `/maps` - List all maps  
- **POST** `/counter` - Get hero counters
- **POST** `/suggest` - Team composition (main feature)

Interactive docs: http://localhost:8000/docs

## Example Usage

```python
import httpx

# Team composition request
response = httpx.post("http://localhost:8000/suggest", json={
    "map_name": "King's Row",
    "enemy_team": ["Reinhardt", "Bastion", "Mercy", "Widowmaker"],
    "current_team": [],
    "difficulties": "Enemy bunker comp, hard to push"
}, timeout=120.0)

result = response.json()
print(result['raw_response'])
```

## Data

- **50 heroes** indexed with abilities, roles, counters
- **57 maps** indexed with gamemodes, strategies
- **Local ChromaDB** for fast semantic search
- **Mistral 7B** for intelligent suggestions

## Response Time

- Health/Heroes/Maps: < 1 second
- Counter queries: 20-30 seconds
- Team suggestions: 30-60 seconds

*(LLM inference time on local hardware)*
