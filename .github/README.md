# Overcoach AI 🎮

> Your AI-powered team composition coach for Overwatch

---

## Quick Links

- 📖 [Full Documentation](README.md)
- 🚀 [Quick Start Guide](QUICKSTART.md)
- 📊 [Project Summary](PROJECT_SUMMARY.md)
- 🧪 [Usage Examples](examples.py)

---

## What is Overcoach AI?

Overcoach AI is an intelligent team composition assistant that uses **RAG (Retrieval-Augmented Generation)** and a **local LLM** to suggest optimal hero picks based on:

- 🗺️ Map selection
- 👥 Enemy team composition  
- ⚔️ Your current team
- 🎯 Specific challenges you're facing

**Everything runs locally** - no API keys, no cloud, no limits!

---

## One-Line Install

```bash
git clone https://github.com/YOUR_USERNAME/overcoach-ai.git
cd overcoach-ai
./start.sh
```

---

## Example Query

```bash
curl -X POST http://localhost:8000/suggest \
  -H "Content-Type: application/json" \
  -d '{
    "map_name": "Kings Row",
    "enemy_team": ["Bastion", "Reinhardt", "Mercy"],
    "current_team": [],
    "difficulties": "Enemy bunker comp is hard to push"
  }'
```

**Response:** Detailed team recommendation with counter strategies, synergies, and alternatives.

---

## Features

✅ **50 heroes** indexed with abilities and counters  
✅ **57 maps** with strategic information  
✅ **Local LLM** (Mistral 7B via Ollama)  
✅ **REST API** with interactive docs  
✅ **Vector search** for semantic hero/map matching  
✅ **No dependencies** on external APIs  

---

## Stack

- **Python 3.12** - Core language
- **FastAPI** - REST API framework
- **LlamaIndex** - RAG orchestration
- **ChromaDB** - Vector database
- **Ollama** - LLM runtime (Mistral 7B)
- **OverFast API** - Overwatch data source

---

## Contributing

Contributions welcome! See [README.md](README.md) for development setup.

---

## License

MIT License - See [LICENSE](LICENSE)

---

**Built with ❤️ for the Overwatch community**
