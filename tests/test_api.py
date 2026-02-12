"""Test script for the API endpoints."""
import httpx
import json


BASE_URL = "http://localhost:8000"


def test_health():
    """Test health endpoint."""
    print("=" * 60)
    print("Testing /health endpoint")
    print("=" * 60)
    
    response = httpx.get(f"{BASE_URL}/health")
    print(f"Status: {response.status_code}")
    print(json.dumps(response.json(), indent=2))
    print()


def test_heroes():
    """Test heroes list endpoint."""
    print("=" * 60)
    print("Testing /heroes endpoint")
    print("=" * 60)
    
    response = httpx.get(f"{BASE_URL}/heroes")
    heroes = response.json()
    print(f"Status: {response.status_code}")
    print(f"Total heroes: {len(heroes)}")
    print(f"Sample (first 5):")
    for hero in heroes[:5]:
        print(f"  - {hero['name']} ({hero['role']})")
    print()


def test_maps():
    """Test maps list endpoint."""
    print("=" * 60)
    print("Testing /maps endpoint")
    print("=" * 60)
    
    response = httpx.get(f"{BASE_URL}/maps")
    maps = response.json()
    print(f"Status: {response.status_code}")
    print(f"Total maps: {len(maps)}")
    print(f"Sample (first 5):")
    for map_data in maps[:5]:
        print(f"  - {map_data['name']} ({', '.join(map_data['gamemodes'])})")
    print()


def test_counter():
    """Test hero counter endpoint."""
    print("=" * 60)
    print("Testing /counter endpoint")
    print("=" * 60)
    
    payload = {
        "hero_name": "Bastion"
    }
    
    response = httpx.post(f"{BASE_URL}/counter", json=payload, timeout=30.0)
    print(f"Status: {response.status_code}")
    result = response.json()
    print(f"Hero: {result['hero']}")
    print(f"Counters:\n{result['counters'][:500]}...")
    print()


def test_team_composition():
    """Test team composition suggestion endpoint."""
    print("=" * 60)
    print("Testing /suggest endpoint")
    print("=" * 60)
    
    payload = {
        "map_name": "Dorado",
        "enemy_team": ["Reinhardt", "Bastion", "Mercy", "Widowmaker"],
        "current_team": [],
        "difficulties": "Enemy has strong bunker defense with Bastion behind Reinhardt shield"
    }
    
    print(f"Request payload:")
    print(json.dumps(payload, indent=2))
    print("\nSending request (this may take 30-60 seconds)...")
    
    response = httpx.post(f"{BASE_URL}/suggest", json=payload, timeout=120.0)
    print(f"\nStatus: {response.status_code}")
    result = response.json()
    
    print("\n--- RESPONSE ---")
    print(result['raw_response'])
    print()


def main():
    """Run all tests."""
    print("\n🎮 Overcoach AI - API Test Suite\n")
    
    try:
        test_health()
        test_heroes()
        test_maps()
        test_counter()
        test_team_composition()
        
        print("=" * 60)
        print("✅ All tests completed successfully!")
        print("=" * 60)
        
    except Exception as e:
        print(f"\n❌ Test failed: {e}")


if __name__ == "__main__":
    main()
