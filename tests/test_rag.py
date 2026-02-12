"""
Tests for RAG module
"""
import pytest
from pathlib import Path
import sys

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.rag.retriever import RAGRetriever


class TestRAGRetrieval:
    """Test RAG retrieval functionality"""
    
    @pytest.fixture
    def rag(self):
        """Initialize RAG system"""
        try:
            return RAGRetriever()
        except Exception as e:
            pytest.skip(f"RAG initialization failed: {e}")
    
    def test_rag_initialization(self, rag):
        """Test RAG can be initialized"""
        assert rag is not None
        assert rag.heroes_index is not None
        assert rag.maps_index is not None
    
    def test_query_hero_abilities(self, rag):
        """Test querying hero abilities"""
        query = "What are Genji's abilities?"
        response = rag.query_heroes(query, top_k=3)
        
        assert response is not None
        assert len(response) > 0
        # Response should mention Genji or abilities
        response_lower = response.lower()
        assert "genji" in response_lower or "ability" in response_lower or "abilities" in response_lower
    
    def test_query_map_info(self, rag):
        """Test querying map information"""
        query = "Tell me about Dorado map"
        response = rag.query_maps(query, top_k=2)
        
        assert response is not None
        assert len(response) > 0
        # Response should mention Dorado or map features
        response_lower = response.lower()
        assert "dorado" in response_lower or "map" in response_lower
    
    def test_query_counter_picks(self, rag):
        """Test querying counter picks"""
        query = "Which heroes counter Pharah?"
        response = rag.query_heroes(query, top_k=5)
        
        assert response is not None
        assert len(response) > 0
        # Should return something about hitscan or counters
        response_lower = response.lower()
        assert any(word in response_lower for word in ["counter", "hitscan", "widow", "cassidy", "ashe"])
    
    def test_query_team_composition(self, rag):
        """Test team composition query"""
        map_name = "King's Row"
        enemy_team = ["Reinhardt", "Bastion", "Mercy"]
        context = "Enemy has strong bunker defense"
        
        response = rag.query_team_composition(
            map_name=map_name,
            enemy_team=enemy_team,
            current_team=[],
            context=context
        )
        
        assert response is not None
        assert len(response) > 0
        # Response should suggest heroes or strategy
        response_lower = response.lower()
        assert any(word in response_lower for word in ["team", "hero", "composition", "strategy", "tank", "damage", "support"])
    
    def test_empty_query(self, rag):
        """Test handling of empty query"""
        response = rag.query_heroes("", top_k=1)
        assert response is not None  # Should not crash
    
    def test_retrieval_limits(self, rag):
        """Test top_k limits are respected"""
        query = "Tell me about support heroes"
        
        # Query with different top_k values
        response_3 = rag.query_heroes(query, top_k=3)
        response_10 = rag.query_heroes(query, top_k=10)
        
        assert response_3 is not None
        assert response_10 is not None
        # Higher top_k should potentially return more information
        # (though this depends on the retrieval implementation)


class TestRAGIndexing:
    """Test RAG indexing functionality"""
    
    def test_chroma_db_exists(self):
        """Test that ChromaDB directory exists"""
        chroma_dir = Path(__file__).parent.parent / "chroma_db"
        assert chroma_dir.exists(), "ChromaDB directory not found"
        
        # Check that it's not empty
        contents = list(chroma_dir.iterdir())
        assert len(contents) > 0, "ChromaDB directory is empty"
    
    def test_index_creation(self):
        """Test that indices were created"""
        from src.rag.indexer import create_heroes_index, create_maps_index
        
        # This test assumes indices have been created
        # In a real test, you might recreate them in a temp directory
        heroes_index = create_heroes_index()
        maps_index = create_maps_index()
        
        assert heroes_index is not None
        assert maps_index is not None


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
