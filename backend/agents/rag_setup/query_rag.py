from .data_loader import DataLoader
from .create_vector_store import VectorStore
from .create_chunks import ChunkCreator
from pathlib import Path
from tqdm import tqdm
from typing import List, Dict
import os

def setup_rag(data_dir: str, model_name: str = "all-MiniLM-L6-v2"):
    # Load documents
    documents = []
    for file_path in Path(data_dir).glob('*'):
        loader = DataLoader(str(file_path))
        docs = loader.load_data()
        documents.extend(docs)
    print(f"Loaded {len(documents)} documents from {data_dir}.")
    
    # Create chunks
    chunk_creator = ChunkCreator()
    chunked_documents = chunk_creator.create_chunks(documents)
    print(f"Created {len(chunked_documents)} chunks from documents.")
    
    # Create vector store with model name
    vector_store = VectorStore(model_name)
    
    # Process in batches
    batch_size = 100
    print(f"Adding {len(chunked_documents)} chunks to vector store...")
    for i in tqdm(range(0, len(chunked_documents), batch_size)):
        batch = chunked_documents[i:i+batch_size]
        docs_to_add = [{'text': doc.page_content, 'metadata': doc.metadata} for doc in batch]
        vector_store.add_documents(docs_to_add)
    
    print("Vector store created and documents added.")
    return vector_store

def load_existing_vector_store(model_name: str = "all-MiniLM-L6-v2"):
    """Load existing vector store without rebuilding"""
    return VectorStore(model_name)

def check_vector_store_exists():
    """Check if vector store already exists"""
    # Fixed path - relative to where script is run from (backend/)
    vector_store_path = "data/vector_store/"
    return os.path.exists(vector_store_path) and os.listdir(vector_store_path)

def similarity_search_with_score(vector_store: VectorStore, query: str, k: int = 5):
    """Wrapper function to perform similarity search with scores"""
    return vector_store.similarity_search_with_score(query, k)

def query_rag(query: str, top_k: int = 3) -> List[Dict[str, str]]:
    """
    Query the RAG system and return relevant documents
    
    Args:
        query: User query
        top_k: Number of top results to return
        
    Returns:
        List of dicts with 'content' and 'metadata' keys
    """
    try:
        # Load existing vector store
        if not check_vector_store_exists():
            print("Warning: Vector store not found. Returning empty results.")
            return []
        
        vector_store = load_existing_vector_store()
        
        # Perform similarity search
        results = similarity_search_with_score(vector_store, query, k=top_k)
        
        # Format results
        formatted_results = []
        for doc, score in results:
            formatted_results.append({
                "content": doc.page_content if hasattr(doc, 'page_content') else str(doc),
                "metadata": doc.metadata if hasattr(doc, 'metadata') else {},
                "score": float(score)
            })
        
        return formatted_results
        
    except Exception as e:
        print(f"RAG query error: {e}")
        return []

