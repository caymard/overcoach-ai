# Overcoach AI

AI-powered team composition coach for Overwatch using RAG (Retrieval-Augmented Generation) with local LLM.

## 🎮 Features

- **Team Composition Suggestions**: Get AI-powered team recommendations based on map, enemy team, and context
- **Hero Counter Information**: Query which heroes counter specific threats
- **Heroes & Maps Database**: Access comprehensive information about all Overwatch heroes and maps
- **Local or Remote LLM**: Use local Ollama (Mistral 7B) or cloud providers (OpenAI, GitHub Copilot)
- **Vector Search**: ChromaDB-powered semantic search over hero abilities and map strategies

## 🏗️ Architecture

- **FastAPI**: REST API server
- **LlamaIndex**: RAG framework
- **ChromaDB**: Local vector database
- **Ollama**: Local LLM runtime (Mistral 7B)
- **OverFast API**: Data source for heroes and maps

## 📋 Prerequisites

- **Python 3.12** (ChromaDB compatibility)
- **Ollama** installed with Mistral 7B model
- At least 8GB RAM for LLM inference

## 🚀 Quick Start

### 1. Setup Environment

```bash
# Clone repository
cd overwatch-rag

# Create virtual environment (Python 3.12)
python3.12 -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### 2. Pull Ollama Model

```bash
ollama pull mistral:7b
```

### 3. Ingest Data (First Time Only)

```bash
# Fetch heroes and maps data, generate markdown files
python -m src.ingestion.markdown_gen

# Index data into ChromaDB
python -m src.rag.indexer
```

### 4. Start API Server

```bash
uvicorn src.api.main:app --host 0.0.0.0 --port 8000
```

The API will be available at: `http://localhost:8000`

Interactive docs: `http://localhost:8000/docs`

## 📚 API Endpoints

### Health Check
```bash
GET /health
```

Returns system status, Ollama connection, and index statistics.

### List Heroes
```bash
GET /heroes
```

Returns all available Overwatch heroes.

### List Maps
```bash
GET /maps
```

Returns all available Overwatch maps.

### Get Hero Counters
```bash
POST /counter
Content-Type: application/json

{
  "hero_name": "Bastion"
}
```

### Suggest Team Composition
```bash
POST /suggest
Content-Type: application/json

{
  "map_name": "King's Row",
  "enemy_team": ["Reinhardt", "Bastion", "Mercy", "Widowmaker"],
  "current_team": [],
  "difficulties": "Enemy has strong bunker defense"
}
```

## 🧪 Testing

Run the test suite:

```bash
# Make sure API server is running
python tests/test_api.py
```

Or use curl:

```bash
# Health check
curl http://localhost:8000/health

# Team suggestion
curl -X POST http://localhost:8000/suggest \
  -H "Content-Type: application/json" \
  -d '{
    "map_name": "Dorado",
    "enemy_team": ["Reinhardt", "Bastion", "Mercy"],
    "current_team": [],
    "difficulties": "Strong bunker defense"
  }'
```

## 📁 Project Structure

```
overwatch-rag/
├── data/
│   ├── heroes/          # Hero markdown files (50)
│   ├── maps/            # Map markdown files (57)
│   └── raw/             # Raw JSON from API
├── src/
│   ├── api/
│   │   ├── main.py      # FastAPI app
│   │   └── models.py    # Pydantic models
│   ├── rag/
│   │   ├── indexer.py   # ChromaDB indexing
│   │   ├── retriever.py # Query engine
│   │   └── prompts.py   # LLM prompts
│   ├── ingestion/
│   │   ├── overfast_client.py  # API client
│   │   └── markdown_gen.py     # Data ingestion
│   └── utils/
│       └── config.py    # Configuration
├── tests/
│   └── test_api.py      # API tests
├── chroma_db/           # Vector database
├── requirements.txt
└── README.md
```

## ⚙️ Configuration

Edit `.env` file to customize:

```bash
OLLAMA_BASE_URL=http://localhost:11434
OLLAMA_MODEL=mistral:7b
OVERFAST_API_URL=https://overfast-api.tekrop.fr
CHROMA_DB_PATH=./chroma_db
```

## 🔧 Development

### Re-index Data

If you want to refresh the data:

```bash
# Re-fetch from OverFast API
python -m src.ingestion.markdown_gen

# Re-index into ChromaDB
rm -rf chroma_db/
python -m src.rag.indexer
```

### Test RAG Retrieval

```bash
python -m src.rag.retriever
```

## 🐛 Troubleshooting

### ChromaDB Import Error (Python 3.14+)
ChromaDB is not compatible with Python 3.14+. Use Python 3.12:
```bash
python3.12 -m venv .venv
```

### Ollama Connection Failed
Ensure Ollama is running:
```bash
# Check if Ollama is running (API call)
curl http://localhost:11434/api/tags

# If not running, start it
ollama serve
```

### Model Not Found
The start script will automatically download Mistral 7B via Ollama API if not present. 
Manual download if needed:
```bash
# Via API (no CLI required)
curl http://localhost:11434/api/pull -d '{"name": "mistral:7b"}'

# Or via CLI if available
ollama pull mistral:7b
```

### Slow Response Times
- Mistral 7B needs 5-15 seconds for inference
- Consider using a smaller model (e.g., `llama3.2:3b`)
- Increase hardware resources (RAM, CPU)

## 📊 Performance

- **Data**: 50 heroes + 57 maps indexed
- **Vector DB**: ~107 document chunks
- **Response Time**: 10-30 seconds per composition suggestion
- **LLM**: Mistral 7B (Q4_K_M quantization)

## 🎯 Future Enhancements

- [ ] Frontend UI (React/Vue)
- [ ] Real-time meta updates
- [ ] User feedback system
- [ ] Hero synergy visualization
- [ ] Multi-language support
- [ ] Fine-tuned Overwatch-specific model

## 📄 License

MIT License

## 🙏 Credits

- **OverFast API**: Hero and map data
- **Ollama**: Local LLM runtime
- **LlamaIndex**: RAG framework
- **ChromaDB**: Vector database

## ⚡ Performance Optimization

### Model Preloading

The `start.sh` script automatically preloads the Mistral 7B model into Ollama's memory on startup, eliminating the "cold start" delay on first request.

**What happens:**
1. Script checks if model is available
2. Sends a warmup request to Ollama
3. Model stays loaded in memory
4. FastAPI performs additional LLM warmup on startup

**Benefits:**
- First API request is ~10-20 seconds faster
- Consistent response times
- Better user experience

**Manual preload:**
```bash
curl -s http://localhost:11434/api/generate -d '{
  "model": "mistral:7b",
  "prompt": "Ready",
  "stream": false
}'
```


---

## 🎨 Frontend

The project now includes a web frontend built with React + TypeScript + Vite.

### Starting the Frontend

```bash
# Terminal 1: Start backend
./start.sh

# Terminal 2: Start frontend
cd frontend
npm install
npm run dev
```

Then open http://localhost:5173

### Features

- **Interactive Team Builder**: Select heroes for enemy and friendly teams
- **Map Selection**: Searchable dropdown with thumbnails
- **Difficulty Input**: Describe your problem
- **AI Suggestions**: Get instant team recommendations
- **Beautiful UI**: Tailwind CSS with Overwatch theme

See `frontend/README.md` for more details.
