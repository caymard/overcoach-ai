#!/usr/bin/env python3
"""
Example usage of the Overwatch RAG API.
Demonstrates common use cases.
"""
import httpx
import json
from time import sleep


BASE_URL = "http://localhost:8000"


def example_1_list_resources():
    """Example 1: List all heroes and maps."""
    print("=" * 60)
    print("EXAMPLE 1: Listing Heroes and Maps")
    print("=" * 60)
    
    # Get heroes
    response = httpx.get(f"{BASE_URL}/heroes")
    heroes = response.json()
    print(f"\n✓ Found {len(heroes)} heroes")
    print("Tanks:", [h['name'] for h in heroes if h['role'] == 'tank'][:5])
    
    # Get maps
    response = httpx.get(f"{BASE_URL}/maps")
    maps = response.json()
    print(f"\n✓ Found {len(maps)} maps")
    print("Escort maps:", [m['name'] for m in maps if 'escort' in m['gamemodes']][:5])
    print()


def example_2_counter_query():
    """Example 2: Find counters for a specific hero."""
    print("=" * 60)
    print("EXAMPLE 2: Finding Counters for Pharah")
    print("=" * 60)
    
    payload = {"hero_name": "Pharah"}
    
    print("Querying RAG system...")
    response = httpx.post(f"{BASE_URL}/counter", json=payload, timeout=60.0)
    result = response.json()
    
    print(f"\n--- Counters for {result['hero']} ---")
    print(result['counters'][:600] + "...\n")


def example_3_basic_composition():
    """Example 3: Basic team composition request."""
    print("=" * 60)
    print("EXAMPLE 3: Basic Team Composition (No Enemy Info)")
    print("=" * 60)
    
    payload = {
        "map_name": "Numbani",
        "enemy_team": [],
        "current_team": [],
        "difficulties": ""
    }
    
    print(f"Request: Need team for {payload['map_name']}")
    print("Querying RAG system (this takes ~20-30 seconds)...")
    
    response = httpx.post(f"{BASE_URL}/suggest", json=payload, timeout=120.0)
    result = response.json()
    
    print("\n--- AI Suggestion ---")
    print(result['raw_response'][:800] + "...\n")


def example_4_advanced_composition():
    """Example 4: Advanced composition with full context."""
    print("=" * 60)
    print("EXAMPLE 4: Advanced Team Composition (Full Context)")
    print("=" * 60)
    
    payload = {
        "map_name": "King's Row",
        "enemy_team": [
            "Reinhardt",
            "Bastion", 
            "Torbjörn",
            "Mercy",
            "Baptiste"
        ],
        "current_team": ["D.Va"],
        "difficulties": "Enemy has double bunker with Bastion and Torbjörn. Hard to push through choke points."
    }
    
    print("Context:")
    print(f"  Map: {payload['map_name']}")
    print(f"  Enemy: {', '.join(payload['enemy_team'])}")
    print(f"  Current Team: {', '.join(payload['current_team'])}")
    print(f"  Issue: {payload['difficulties']}")
    print("\nQuerying RAG system (this takes ~30-45 seconds)...")
    
    response = httpx.post(f"{BASE_URL}/suggest", json=payload, timeout=120.0)
    result = response.json()
    
    print("\n--- AI RECOMMENDATION ---")
    print(result['raw_response'])
    print()


def main():
    """Run all examples."""
    print("\n🎮 Overcoach AI - Usage Examples\n")
    
    # Check API is running
    try:
        response = httpx.get(f"{BASE_URL}/health", timeout=5.0)
        health = response.json()
        print(f"✓ API Status: {health['status']}")
        print(f"✓ Heroes indexed: {health['heroes_indexed']}")
        print(f"✓ Maps indexed: {health['maps_indexed']}")
        print()
    except Exception as e:
        print(f"❌ Cannot connect to API at {BASE_URL}")
        print(f"   Make sure the server is running: uvicorn src.api.main:app --reload")
        return
    
    # Run examples
    example_1_list_resources()
    sleep(1)
    
    example_2_counter_query()
    sleep(2)
    
    example_3_basic_composition()
    sleep(2)
    
    example_4_advanced_composition()
    
    print("=" * 60)
    print("✅ All examples completed!")
    print("=" * 60)
    print("\nNext steps:")
    print("  - Explore interactive docs: http://localhost:8000/docs")
    print("  - Try your own queries with different contexts")
    print("  - Experiment with different maps and enemy compositions")
    print()


if __name__ == "__main__":
    main()
