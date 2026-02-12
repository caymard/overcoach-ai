# Quick Start Guide

Get Overcoach AI running in **3 simple steps**.

## Prerequisites

- Python 3.12
- Node.js 18+
- Ollama with Mistral 7B model

## Step 1: Create RAG Database

```bash
python3.12 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

# Ingest data and build vector database (~2 minutes)
python -m src.ingestion.markdown_gen
python -m src.rag.indexer
```

## Step 2: Run Backend

```bash
# Make sure venv is activated
source .venv/bin/activate

# Start API server
uvicorn src.api.main:app --reload
```

Backend will be available at: **http://localhost:8000**

## Step 3: Run Frontend

```bash
# In a new terminal
cd frontend
npm install
npm run dev
```

Frontend will be available at: **http://localhost:5173**

---

## That's it! 🎉

Open **http://localhost:5173** in your browser and start building teams!

---

### Quick Test

Visit http://localhost:5173 and:
1. Select enemy heroes (click on slots)
2. Click **"Help!"** button
3. Wait for AI suggestions (5-60s)

### API Docs

Interactive API documentation: http://localhost:8000/docs
