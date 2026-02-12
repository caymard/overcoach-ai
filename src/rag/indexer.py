"""RAG indexer to load markdown files into ChromaDB via LlamaIndex."""
from pathlib import Path
from typing import List
import chromadb
from llama_index.core import (
    VectorStoreIndex,
    SimpleDirectoryReader,
    StorageContext,
    Settings,
)
from llama_index.vector_stores.chroma import ChromaVectorStore
from llama_index.embeddings.huggingface import HuggingFaceEmbedding
from llama_index.llms.ollama import Ollama
from src.utils.config import config


class RAGIndexer:
    """Indexer for loading Overwatch data into ChromaDB."""
    
    def __init__(self):
        # Initialize ChromaDB client
        self.chroma_client = chromadb.PersistentClient(path=config.CHROMA_DB_PATH)
        
        # Configure LlamaIndex settings
        print("Initializing embedding model...")
        Settings.embed_model = HuggingFaceEmbedding(
            model_name="BAAI/bge-small-en-v1.5"
        )
        
        print("Initializing LLM (Ollama)...")
        Settings.llm = Ollama(
            model=config.OLLAMA_MODEL,
            base_url=config.OLLAMA_BASE_URL,
            request_timeout=120.0
        )
        
        print("✓ RAG components initialized")
        
        self.heroes_collection = None
        self.maps_collection = None
        self.heroes_index = None
        self.maps_index = None
    
    def create_heroes_index(self) -> VectorStoreIndex:
        """Create or load heroes index."""
        print("\nCreating heroes index...")
        
        # Get or create collection
        self.heroes_collection = self.chroma_client.get_or_create_collection("heroes")
        
        # Create vector store
        vector_store = ChromaVectorStore(chroma_collection=self.heroes_collection)
        storage_context = StorageContext.from_defaults(vector_store=vector_store)
        
        # Load documents
        heroes_path = Path(config.DATA_HEROES_PATH)
        print(f"Loading hero markdown files from {heroes_path}...")
        documents = SimpleDirectoryReader(
            input_dir=str(heroes_path),
            required_exts=[".md"],
            recursive=False
        ).load_data()
        
        print(f"Loaded {len(documents)} hero documents")
        
        # Create index
        print("Indexing heroes (this may take a minute)...")
        self.heroes_index = VectorStoreIndex.from_documents(
            documents,
            storage_context=storage_context,
            show_progress=True
        )
        
        print(f"✓ Heroes index created with {len(documents)} documents")
        return self.heroes_index
    
    def create_maps_index(self) -> VectorStoreIndex:
        """Create or load maps index."""
        print("\nCreating maps index...")
        
        # Get or create collection
        self.maps_collection = self.chroma_client.get_or_create_collection("maps")
        
        # Create vector store
        vector_store = ChromaVectorStore(chroma_collection=self.maps_collection)
        storage_context = StorageContext.from_defaults(vector_store=vector_store)
        
        # Load documents
        maps_path = Path(config.DATA_MAPS_PATH)
        print(f"Loading map markdown files from {maps_path}...")
        documents = SimpleDirectoryReader(
            input_dir=str(maps_path),
            required_exts=[".md"],
            recursive=False
        ).load_data()
        
        print(f"Loaded {len(documents)} map documents")
        
        # Create index
        print("Indexing maps (this may take a minute)...")
        self.maps_index = VectorStoreIndex.from_documents(
            documents,
            storage_context=storage_context,
            show_progress=True
        )
        
        print(f"✓ Maps index created with {len(documents)} documents")
        return self.maps_index
    
    def load_existing_indexes(self):
        """Load existing indexes from ChromaDB."""
        print("\nLoading existing indexes...")
        
        try:
            # Load heroes
            self.heroes_collection = self.chroma_client.get_collection("heroes")
            vector_store = ChromaVectorStore(chroma_collection=self.heroes_collection)
            self.heroes_index = VectorStoreIndex.from_vector_store(vector_store)
            print(f"✓ Loaded heroes index ({self.heroes_collection.count()} vectors)")
        except Exception as e:
            print(f"⚠ Could not load heroes index: {e}")
        
        try:
            # Load maps
            self.maps_collection = self.chroma_client.get_collection("maps")
            vector_store = ChromaVectorStore(chroma_collection=self.maps_collection)
            self.maps_index = VectorStoreIndex.from_vector_store(vector_store)
            print(f"✓ Loaded maps index ({self.maps_collection.count()} vectors)")
        except Exception as e:
            print(f"⚠ Could not load maps index: {e}")
    
    def index_all(self):
        """Index all heroes and maps."""
        self.create_heroes_index()
        self.create_maps_index()
    
    def get_stats(self) -> dict:
        """Get indexing statistics."""
        stats = {
            "heroes_count": self.heroes_collection.count() if self.heroes_collection else 0,
            "maps_count": self.maps_collection.count() if self.maps_collection else 0,
        }
        return stats


def main():
    """Main entry point for indexing."""
    print("=" * 60)
    print("Overcoach AI - Data Indexer")
    print("=" * 60)
    
    indexer = RAGIndexer()
    
    # Index all data
    indexer.index_all()
    
    # Show stats
    stats = indexer.get_stats()
    print("\n" + "=" * 60)
    print("Indexing Complete!")
    print("=" * 60)
    print(f"Heroes vectors: {stats['heroes_count']}")
    print(f"Maps vectors: {stats['maps_count']}")
    print(f"Total vectors: {stats['heroes_count'] + stats['maps_count']}")


if __name__ == "__main__":
    main()
