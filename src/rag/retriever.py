"""RAG retriever for querying indexed Overwatch data."""
import chromadb
from typing import List, Dict, Any
from llama_index.core import VectorStoreIndex, Settings
from llama_index.vector_stores.chroma import ChromaVectorStore
from llama_index.embeddings.huggingface import HuggingFaceEmbedding
from src.utils.config import config
from src.utils.llm_config import configure_llm, get_provider_from_env


class RAGRetriever:
    """Retriever for querying Overwatch heroes and maps data."""
    
    def __init__(self):
        # Initialize ChromaDB client
        self.chroma_client = chromadb.PersistentClient(path=config.CHROMA_DB_PATH)
        
        # Configure embeddings
        Settings.embed_model = HuggingFaceEmbedding(
            model_name="BAAI/bge-small-en-v1.5"
        )
        
        # Configure LLM (auto-detect or use explicit provider)
        provider = get_provider_from_env()
        configure_llm(provider)
        
        # Load indexes
        self.heroes_index = None
        self.maps_index = None
        self._load_indexes()
    
    def _load_indexes(self):
        """Load existing indexes from ChromaDB."""
        try:
            # Load heroes index
            heroes_collection = self.chroma_client.get_collection("heroes")
            heroes_vector_store = ChromaVectorStore(chroma_collection=heroes_collection)
            self.heroes_index = VectorStoreIndex.from_vector_store(heroes_vector_store)
            print(f"✓ Loaded heroes index ({heroes_collection.count()} vectors)")
        except Exception as e:
            print(f"⚠ Could not load heroes index: {e}")
        
        try:
            # Load maps index
            maps_collection = self.chroma_client.get_collection("maps")
            maps_vector_store = ChromaVectorStore(chroma_collection=maps_collection)
            self.maps_index = VectorStoreIndex.from_vector_store(maps_vector_store)
            print(f"✓ Loaded maps index ({maps_collection.count()} vectors)")
        except Exception as e:
            print(f"⚠ Could not load maps index: {e}")
    
    def query_heroes(self, query: str, top_k: int = 5) -> str:
        """Query heroes knowledge base."""
        if not self.heroes_index:
            return "Heroes index not loaded."
        
        query_engine = self.heroes_index.as_query_engine(similarity_top_k=top_k)
        response = query_engine.query(query)
        return str(response)
    
    def query_maps(self, query: str, top_k: int = 5) -> str:
        """Query maps knowledge base."""
        if not self.maps_index:
            return "Maps index not loaded."
        
        query_engine = self.maps_index.as_query_engine(similarity_top_k=top_k)
        response = query_engine.query(query)
        return str(response)
    
    def query_team_composition(
        self,
        context: Dict[str, Any],
        top_k_heroes: int = 10,
        top_k_maps: int = 3
    ) -> str:
        """
        Query for team composition suggestions based on context.
        
        Args:
            context: Dictionary containing:
                - map: Map name
                - enemy_team: List of enemy hero names
                - current_team: List of current team hero names (optional)
                - difficulties: Description of difficulties faced (optional)
            top_k_heroes: Number of hero documents to retrieve
            top_k_maps: Number of map documents to retrieve
        
        Returns:
            Composition suggestion from LLM
        """
        if not self.heroes_index or not self.maps_index:
            return "Indexes not fully loaded."
        
        # Build query
        map_name = context.get("map", "")
        enemy_team = context.get("enemy_team", [])
        current_team = context.get("current_team", [])
        difficulties = context.get("difficulties", "")
        
        # Retrieve relevant heroes info
        heroes_query = f"""Information about heroes that counter {', '.join(enemy_team)} on map {map_name}. 
        Also information about {', '.join(enemy_team)} to understand their weaknesses.
        Include abilities, synergies, and counter strategies."""
        
        heroes_engine = self.heroes_index.as_query_engine(similarity_top_k=top_k_heroes)
        heroes_context = heroes_engine.query(heroes_query)
        
        # Retrieve map info
        maps_query = f"Information about {map_name} map: strategy, key positions, recommended heroes"
        maps_engine = self.maps_index.as_query_engine(similarity_top_k=top_k_maps)
        maps_context = maps_engine.query(maps_query)
        
        # Build optimized prompt
        prompt = f"""You are an expert Overwatch coach. Suggest an optimal 5-hero team composition.

**CONTEXT:**
Map: {map_name}
Enemy Team: {', '.join(enemy_team) if enemy_team else 'Unknown'}
Current Team: {', '.join(current_team) if current_team else 'Empty - need full team'}
Difficulties: {difficulties if difficulties else 'None specified'}

**KNOWLEDGE:**
{heroes_context}

Map Info: {maps_context}

**YOUR RESPONSE MUST BE STRUCTURED AS:**

1. RECOMMENDED TEAM (exactly 5 heroes):
Tank: [Hero Name] - [One sentence why]
Damage: [Hero Name] - [One sentence why]
Damage: [Hero Name] - [One sentence why]
Support: [Hero Name] - [One sentence why]
Support: [Hero Name] - [One sentence why]

2. COUNTER STRATEGY:
[2-3 sentences explaining how this team counters the enemy]

3. KEY SYNERGIES:
[2-3 sentences about ability combos and team playstyle]

4. ALTERNATIVES:
[List 2-3 substitute heroes with brief reasons]

Keep responses concise and actionable. Focus on current Overwatch meta.
"""
        
        # Query with full context
        response = Settings.llm.complete(prompt)
        return str(response)


def main():
    """Test the retriever."""
    print("=" * 60)
    print("RAG Retriever Test")
    print("=" * 60)
    
    retriever = RAGRetriever()
    
    # Test 1: Simple hero query
    print("\n--- Test 1: Query about Genji ---")
    response = retriever.query_heroes("What are Genji's abilities and role?")
    print(response[:500] + "..." if len(response) > 500 else response)
    
    # Test 2: Map query
    print("\n--- Test 2: Query about Dorado ---")
    response = retriever.query_maps("Tell me about Dorado map")
    print(response[:500] + "..." if len(response) > 500 else response)
    
    # Test 3: Team composition
    print("\n--- Test 3: Team Composition Suggestion ---")
    context = {
        "map": "King's Row",
        "enemy_team": ["Reinhardt", "Bastion", "Mercy"],
        "current_team": [],
        "difficulties": "Enemy has strong bunker defense"
    }
    response = retriever.query_team_composition(context)
    print(response)


if __name__ == "__main__":
    main()
