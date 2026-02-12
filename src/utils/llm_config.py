"""Configuration for different LLM providers."""
from typing import Literal
from llama_index.llms.ollama import Ollama
from llama_index.llms.openai import OpenAI
from llama_index.llms.azure_openai import AzureOpenAI
from llama_index.core import Settings
import os

LLMProvider = Literal["ollama", "openai", "azure", "github"]


def configure_llm(provider: LLMProvider = "ollama"):
    """
    Configure LLM based on provider choice.
    
    Args:
        provider: One of "ollama", "openai", "azure", "github"
    
    Environment Variables Required:
        Ollama:
            - OLLAMA_BASE_URL (default: http://localhost:11434)
            - OLLAMA_MODEL (default: mistral:7b)
        
        OpenAI:
            - OPENAI_API_KEY
            - OPENAI_MODEL (default: gpt-4-turbo-preview)
        
        Azure OpenAI:
            - AZURE_OPENAI_API_KEY
            - AZURE_OPENAI_ENDPOINT
            - AZURE_OPENAI_DEPLOYMENT
            - AZURE_OPENAI_API_VERSION (default: 2024-02-15-preview)
        
        GitHub Copilot (via GitHub Models):
            - GITHUB_TOKEN (Personal Access Token with model access)
            - GITHUB_MODEL (default: gpt-4o)
    """
    
    if provider == "ollama":
        # Local Ollama
        base_url = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
        model = os.getenv("OLLAMA_MODEL", "mistral:7b")
        
        Settings.llm = Ollama(
            model=model,
            base_url=base_url,
            request_timeout=120.0
        )
        print(f"✓ LLM configured: Ollama ({model})")
    
    elif provider == "openai":
        # OpenAI API
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            raise ValueError("OPENAI_API_KEY environment variable required")
        
        model = os.getenv("OPENAI_MODEL", "gpt-4-turbo-preview")
        
        Settings.llm = OpenAI(
            api_key=api_key,
            model=model,
            temperature=0.7,
            max_tokens=1024
        )
        print(f"✓ LLM configured: OpenAI ({model})")
    
    elif provider == "azure":
        # Azure OpenAI
        api_key = os.getenv("AZURE_OPENAI_API_KEY")
        endpoint = os.getenv("AZURE_OPENAI_ENDPOINT")
        deployment = os.getenv("AZURE_OPENAI_DEPLOYMENT")
        
        if not all([api_key, endpoint, deployment]):
            raise ValueError("Azure OpenAI requires: AZURE_OPENAI_API_KEY, AZURE_OPENAI_ENDPOINT, AZURE_OPENAI_DEPLOYMENT")
        
        api_version = os.getenv("AZURE_OPENAI_API_VERSION", "2024-02-15-preview")
        
        Settings.llm = AzureOpenAI(
            api_key=api_key,
            azure_endpoint=endpoint,
            deployment_name=deployment,
            api_version=api_version,
            temperature=0.7,
            max_tokens=1024
        )
        print(f"✓ LLM configured: Azure OpenAI ({deployment})")
    
    elif provider == "github":
        # GitHub Models API (compatible with OpenAI API)
        github_token = os.getenv("GITHUB_TOKEN")
        if not github_token:
            raise ValueError("GITHUB_TOKEN environment variable required")
        
        model = os.getenv("GITHUB_MODEL", "gpt-4o")
        
        # GitHub Models uses OpenAI-compatible API
        Settings.llm = OpenAI(
            api_key=github_token,
            api_base="https://models.inference.ai.azure.com",
            model=model,
            temperature=0.7,
            max_tokens=1024
        )
        print(f"✓ LLM configured: GitHub Models ({model})")
    
    else:
        raise ValueError(f"Unknown provider: {provider}. Choose from: ollama, openai, azure, github")
    
    return Settings.llm


def get_provider_from_env() -> LLMProvider:
    """
    Automatically detect LLM provider from environment variables.
    
    Priority:
    1. LLM_PROVIDER env var (explicit choice)
    2. Auto-detect based on available API keys
    3. Default to Ollama
    """
    explicit_provider = os.getenv("LLM_PROVIDER", "").lower()
    if explicit_provider in ["ollama", "openai", "azure", "github"]:
        return explicit_provider
    
    # Auto-detect
    if os.getenv("GITHUB_TOKEN"):
        return "github"
    elif os.getenv("OPENAI_API_KEY"):
        return "openai"
    elif os.getenv("AZURE_OPENAI_API_KEY"):
        return "azure"
    else:
        return "ollama"
