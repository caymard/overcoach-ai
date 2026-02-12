"""Client for OverFast API to fetch Overwatch data."""
import httpx
from typing import List, Dict, Any, Optional
from src.utils.config import config


class OverFastClient:
    """Client to interact with OverFast API."""
    
    def __init__(self, base_url: str = None):
        self.base_url = base_url or config.OVERFAST_API_URL
        self.client = httpx.Client(timeout=30.0)
    
    def get_heroes(self) -> List[Dict[str, Any]]:
        """Fetch list of all heroes."""
        url = f"{self.base_url}/heroes"
        response = self.client.get(url)
        response.raise_for_status()
        return response.json()
    
    def get_hero_details(self, hero_key: str) -> Dict[str, Any]:
        """Fetch detailed information for a specific hero."""
        url = f"{self.base_url}/heroes/{hero_key}"
        response = self.client.get(url)
        response.raise_for_status()
        return response.json()
    
    def get_maps(self) -> List[Dict[str, Any]]:
        """Fetch list of all maps."""
        url = f"{self.base_url}/maps"
        response = self.client.get(url)
        response.raise_for_status()
        return response.json()
    
    def get_gamemodes(self) -> List[Dict[str, Any]]:
        """Fetch list of all gamemodes."""
        url = f"{self.base_url}/gamemodes"
        response = self.client.get(url)
        response.raise_for_status()
        return response.json()
    
    def close(self):
        """Close the HTTP client."""
        self.client.close()
    
    def __enter__(self):
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()
