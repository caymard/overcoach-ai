"""Configuration management for the application."""
import os
from dotenv import load_dotenv

load_dotenv()


class Config:
    """Application configuration."""
    
    # Ollama
    OLLAMA_BASE_URL = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
    OLLAMA_MODEL = os.getenv("OLLAMA_MODEL", "mistral:7b")
    
    # OverFast API
    OVERFAST_API_URL = os.getenv("OVERFAST_API_URL", "https://overfast-api.tekrop.fr")
    
    # ChromaDB
    CHROMA_DB_PATH = os.getenv("CHROMA_DB_PATH", "./chroma_db")
    
    # Data paths
    DATA_HEROES_PATH = "./data/heroes"
    DATA_MAPS_PATH = "./data/maps"
    DATA_RAW_PATH = "./data/raw"


config = Config()
