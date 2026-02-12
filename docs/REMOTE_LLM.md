# Remote LLM Configuration

This document shows how to use **Overcoach AI** with remote/cloud LLM providers instead of local Ollama.

## 🌐 Supported Providers

- **Ollama** (local, default)
- **OpenAI** (GPT-4, GPT-3.5-turbo)
- **Azure OpenAI** (Enterprise)
- **GitHub Copilot** (via GitHub Models)

---

## 📝 Quick Start Examples

### Using GitHub Copilot

```bash
# 1. Install OpenAI package
pip install llama-index-llms-openai

# 2. Configure .env
cat >> .env << EOF
LLM_PROVIDER=github
GITHUB_TOKEN=ghp_your_token_here
GITHUB_MODEL=gpt-4o
EOF

# 3. Start server
./start.sh
```

### Using OpenAI

```bash
# 1. Install package
pip install llama-index-llms-openai

# 2. Configure .env
cat >> .env << EOF
LLM_PROVIDER=openai
OPENAI_API_KEY=sk-your-key-here
OPENAI_MODEL=gpt-4-turbo-preview
EOF

# 3. Start server
./start.sh
```

---

## 🔧 Configuration Details

### GitHub Models (Copilot)

```bash
LLM_PROVIDER=github
GITHUB_TOKEN=ghp_...              # Personal Access Token
GITHUB_MODEL=gpt-4o               # or gpt-4-turbo, gpt-3.5-turbo
```

**Get GitHub Token:**
1. https://github.com/settings/tokens
2. Generate new token (classic)
3. Enable "Copilot" scope
4. Copy to `.env`

**Pros**: Free with Copilot subscription, fast (5-10s)  
**Cons**: Requires active Copilot subscription

---

### OpenAI

```bash
LLM_PROVIDER=openai
OPENAI_API_KEY=sk-...
OPENAI_MODEL=gpt-4-turbo-preview  # or gpt-3.5-turbo
```

**Pros**: High quality, fast, easy setup  
**Cons**: Costs ~$0.01-0.10 per request

---

### Azure OpenAI

```bash
LLM_PROVIDER=azure
AZURE_OPENAI_API_KEY=...
AZURE_OPENAI_ENDPOINT=https://....openai.azure.com/
AZURE_OPENAI_DEPLOYMENT=your-deployment
AZURE_OPENAI_API_VERSION=2024-02-15-preview
```

**Pros**: Enterprise-grade, compliant  
**Cons**: More complex setup

---

## ⚡ Performance Comparison

| Provider | Response Time | Quality | Cost |
|----------|--------------|---------|------|
| Ollama (local) | 30-60s | Good | Free |
| OpenAI GPT-3.5 | 2-5s | Good | $ |
| OpenAI GPT-4 | 5-10s | Excellent | $$$ |
| GitHub Models | 5-10s | Excellent | Free* |

*With Copilot subscription

---

## 🚀 Installation

Add the OpenAI package to `requirements.txt`:

```txt
llama-index-llms-openai>=0.1.0
llama-index-llms-azure-openai>=0.1.0  # For Azure
```

Or install manually:

```bash
pip install llama-index-llms-openai llama-index-llms-azure-openai
```

---

## 🔄 Auto-Detection

If `LLM_PROVIDER` is not set, the system auto-detects:

1. `GITHUB_TOKEN` → GitHub Models
2. `OPENAI_API_KEY` → OpenAI
3. `AZURE_OPENAI_API_KEY` → Azure
4. Otherwise → Ollama (default)

---

## 💡 Recommendations

- **For testing**: Ollama (free, local)
- **For production**: GitHub Models (free) or OpenAI GPT-4 (best)
- **For enterprise**: Azure OpenAI

---

See `src/utils/llm_config.py` for implementation details.
