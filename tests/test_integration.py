"""
End-to-end integration tests
"""
import pytest
import httpx
import time
from pathlib import Path
import sys

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent))


BASE_URL = "http://localhost:8000"
TIMEOUT = 120.0  # LLM queries can be slow


class TestAPIIntegration:
    """Test full API integration"""
    
    @pytest.fixture(scope="class")
    def client(self):
        """Create HTTP client"""
        return httpx.Client(base_url=BASE_URL, timeout=TIMEOUT)
    
    def test_server_is_running(self, client):
        """Test that API server is accessible"""
        try:
            response = client.get("/health")
            assert response.status_code == 200
        except httpx.ConnectError:
            pytest.skip("API server not running. Start with: ./start.sh")
    
    def test_full_workflow(self, client):
        """Test complete workflow: list heroes, list maps, get suggestion"""
        
        # Step 1: Get heroes list
        heroes_response = client.get("/heroes")
        assert heroes_response.status_code == 200
        heroes = heroes_response.json()
        assert "heroes" in heroes
        assert len(heroes["heroes"]) > 0
        
        # Step 2: Get maps list
        maps_response = client.get("/maps")
        assert maps_response.status_code == 200
        maps = maps_response.json()
        assert "maps" in maps
        assert len(maps["maps"]) > 0
        
        # Step 3: Get counter suggestion
        counter_response = client.post(
            "/counter",
            json={"hero_name": "Pharah"}
        )
        assert counter_response.status_code == 200
        counter = counter_response.json()
        assert "counters" in counter
        
        # Step 4: Get team composition suggestion
        suggest_response = client.post(
            "/suggest",
            json={
                "map_name": "King's Row",
                "enemy_team": ["Reinhardt", "Bastion"],
                "current_team": [],
                "difficulties": "Strong bunker defense"
            }
        )
        assert suggest_response.status_code == 200
        suggestion = suggest_response.json()
        assert "recommended_team" in suggestion
        assert "strategy" in suggestion
        assert len(suggestion["recommended_team"]) > 0
    
    def test_multiple_llm_providers(self, client):
        """Test that API works with different LLM providers"""
        # This test verifies the response structure is consistent
        # regardless of the LLM provider configured
        
        response = client.post(
            "/suggest",
            json={
                "map_name": "Dorado",
                "enemy_team": ["Winston", "Tracer", "Genji"],
                "current_team": [],
                "difficulties": "Fast dive composition"
            }
        )
        
        assert response.status_code == 200
        data = response.json()
        
        # Verify response structure
        assert "recommended_team" in data
        assert "strategy" in data
        assert "synergies" in data
        assert "alternatives" in data
        assert "raw_response" in data
        
        # Verify recommended_team structure
        assert isinstance(data["recommended_team"], list)
        if len(data["recommended_team"]) > 0:
            hero = data["recommended_team"][0]
            assert "name" in hero
            assert "role" in hero
            assert "reasoning" in hero
    
    def test_parsing_consistency(self, client):
        """Test that parsing works consistently across different responses"""
        test_cases = [
            {
                "map_name": "Hanamura",
                "enemy_team": ["Bastion", "Torbjorn", "Symmetra"],
                "current_team": [],
                "difficulties": "Heavy defense"
            },
            {
                "map_name": "Numbani",
                "enemy_team": ["Roadhog", "Junkrat", "Moira"],
                "current_team": [],
                "difficulties": "Hook combos"
            }
        ]
        
        for test_case in test_cases:
            response = client.post("/suggest", json=test_case)
            assert response.status_code == 200
            
            data = response.json()
            team = data["recommended_team"]
            
            # Should not have parsing failure
            if len(team) > 0:
                first_hero = team[0]["name"]
                assert "Parsing failed" not in first_hero
                assert "raw_response" not in first_hero.lower()
            
            # Should have actual strategy text
            assert len(data["strategy"]) > 20
            assert "raw_response" not in data["strategy"].lower()


class TestPerformance:
    """Performance benchmarks"""
    
    @pytest.fixture
    def client(self):
        return httpx.Client(base_url=BASE_URL, timeout=TIMEOUT)
    
    def test_response_times(self, client):
        """Test that response times are reasonable"""
        try:
            # Health check should be very fast
            start = time.time()
            response = client.get("/health")
            health_time = time.time() - start
            assert health_time < 1.0, f"Health check too slow: {health_time}s"
            
            # List operations should be fast
            start = time.time()
            client.get("/heroes")
            heroes_time = time.time() - start
            assert heroes_time < 2.0, f"List heroes too slow: {heroes_time}s"
            
            # LLM queries will be slower, just ensure they complete
            start = time.time()
            response = client.post(
                "/counter",
                json={"hero_name": "Genji"}
            )
            counter_time = time.time() - start
            print(f"\nCounter query time: {counter_time:.2f}s")
            assert counter_time < TIMEOUT
            
        except httpx.ConnectError:
            pytest.skip("API server not running")


if __name__ == "__main__":
    pytest.main([__file__, "-v", "-s"])
