"""
Tests for data ingestion module
"""
import pytest
from pathlib import Path
import sys
import json

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.ingestion.overfast_client import OverFastClient
from src.ingestion.markdown_gen import MarkdownGenerator


class TestOverFastClient:
    """Test OverFast API client"""
    
    @pytest.fixture
    def client(self):
        return OverFastClient()
    
    def test_client_initialization(self, client):
        """Test client can be initialized"""
        assert client is not None
        assert client.base_url == "https://overfast-api.tekrop.fr"
    
    def test_get_heroes_list(self, client):
        """Test fetching heroes list"""
        heroes = client.get_heroes()
        
        assert heroes is not None
        assert len(heroes) > 0
        assert "key" in heroes[0]
        assert "name" in heroes[0]
    
    def test_get_hero_details(self, client):
        """Test fetching specific hero details"""
        hero = client.get_hero_details("ana")
        
        assert hero is not None
        assert hero["name"] == "Ana"
        assert "role" in hero
        assert "abilities" in hero
    
    def test_get_maps_list(self, client):
        """Test fetching maps list"""
        maps = client.get_maps()
        
        assert maps is not None
        assert len(maps) > 0
        assert "name" in maps[0]
        assert "gamemodes" in maps[0]


class TestMarkdownGeneration:
    """Test markdown generation from API data"""
    
    @pytest.fixture
    def generator(self):
        return MarkdownGenerator()
    
    def test_generate_hero_markdown(self, generator):
        """Test hero markdown generation"""
        hero_data = {
            "name": "Ana",
            "role": "support",
            "description": "Support sniper healer",
            "abilities": [
                {
                    "name": "Biotic Rifle",
                    "description": "Shoot to heal allies or damage enemies",
                    "icon": "https://example.com/icon.png"
                }
            ],
            "hitpoints": {
                "health": 200,
                "armor": 0,
                "shields": 0,
                "total": 200
            },
            "story": {
                "summary": "One of the founding members of Overwatch",
                "chapters": []
            }
        }
        
        markdown = generator.generate_hero_markdown("ana", hero_data)
        
        assert markdown is not None
        assert "# Ana" in markdown
        assert "## Basic Information" in markdown
        assert "support" in markdown.lower()
        assert "## Abilities" in markdown
        assert "Biotic Rifle" in markdown
        assert "## Hitpoints" in markdown
        assert "200" in markdown
    
    def test_generate_map_markdown(self, generator):
        """Test map markdown generation"""
        map_data = {
            "name": "King's Row",
            "screenshot": "https://example.com/screenshot.jpg",
            "gamemodes": ["escort", "hybrid"],
            "location": "London, England",
            "country_code": "GB"
        }
        
        markdown = generator.generate_map_markdown(map_data)
        
        assert markdown is not None
        assert "# King's Row" in markdown
        assert "## Basic Information" in markdown
        assert "escort" in markdown.lower()
        assert "## Location" in markdown or "London" in markdown


class TestDataFiles:
    """Test generated data files"""
    
    def test_hero_files_exist(self):
        """Test that hero markdown files exist"""
        heroes_dir = Path(__file__).parent.parent / "data" / "heroes"
        
        if heroes_dir.exists():
            hero_files = list(heroes_dir.glob("*.md"))
            assert len(hero_files) > 0, "No hero markdown files found"
            
            # Check a sample hero file
            sample_file = hero_files[0]
            content = sample_file.read_text()
            assert len(content) > 100, f"Hero file {sample_file.name} seems too short"
            assert "# " in content, f"Hero file {sample_file.name} missing title"
    
    def test_map_files_exist(self):
        """Test that map markdown files exist"""
        maps_dir = Path(__file__).parent.parent / "data" / "maps"
        
        if maps_dir.exists():
            map_files = list(maps_dir.glob("*.md"))
            assert len(map_files) > 0, "No map markdown files found"
            
            # Check a sample map file
            sample_file = map_files[0]
            content = sample_file.read_text()
            assert len(content) > 50, f"Map file {sample_file.name} seems too short"
            assert "# " in content, f"Map file {sample_file.name} missing title"
    
    def test_raw_json_backup(self):
        """Test that raw JSON backups exist"""
        raw_dir = Path(__file__).parent.parent / "data" / "raw"
        
        if raw_dir.exists():
            json_files = list(raw_dir.glob("*.json"))
            if len(json_files) > 0:
                # Validate JSON structure
                sample_file = json_files[0]
                with open(sample_file) as f:
                    data = json.load(f)
                    assert isinstance(data, dict), "JSON file should contain a dict"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
