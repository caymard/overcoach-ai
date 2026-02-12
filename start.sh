#!/bin/bash
# Start script for Overcoach AI

set -e

echo "🎮 Overcoach AI"
echo "=============================="
echo ""

# Check if venv exists
if [ ! -d ".venv" ]; then
    echo "❌ Virtual environment not found!"
    echo "   Run: python3.12 -m venv .venv"
    exit 1
fi

# Activate venv
source .venv/bin/activate

# Check if Ollama is running
echo "Checking Ollama..."
if curl -s http://localhost:11434/api/tags > /dev/null 2>&1; then
    echo "✓ Ollama is running"
else
    echo "❌ Ollama is not running!"
    echo "   Start it with: ollama serve"
    exit 1
fi

# Check if mistral:7b is available via API
echo "Checking for Mistral 7B model..."
if curl -s http://localhost:11434/api/tags | grep -q "mistral:7b"; then
    echo "✓ Mistral 7B model found"
else
    echo "⚠ Mistral 7B not found, pulling via API..."
    echo "   This may take several minutes (4GB download)..."
    curl -s http://localhost:11434/api/pull -d '{
      "name": "mistral:7b"
    }' | grep -q "success" && echo "✓ Model downloaded" || echo "⚠ Download may be in progress"
fi

# Preload the model into memory
echo ""
echo "Preloading Mistral 7B into memory..."
curl -s http://localhost:11434/api/generate -d '{
  "model": "mistral:7b",
  "prompt": "Hello",
  "stream": false
}' > /dev/null 2>&1 && echo "✓ Model loaded into memory" || echo "⚠ Could not preload model"

# Check if data is indexed
if [ ! -d "chroma_db" ] || [ -z "$(ls -A chroma_db)" ]; then
    echo ""
    echo "⚠ ChromaDB not initialized!"
    echo "   Running data ingestion..."
    python -m src.ingestion.markdown_gen
    python -m src.rag.indexer
fi

echo ""
echo "✓ All checks passed!"
echo ""
echo "Starting API server..."
echo "  - API: http://localhost:8000"
echo "  - Docs: http://localhost:8000/docs"
echo ""

# Start server
uvicorn src.api.main:app --host 0.0.0.0 --port 8000 --reload
