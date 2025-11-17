from typing import List, Dict, Any, Tuple

import numpy as np
import chromadb
import uuid
from sentence_transformers import SentenceTransformer


class Document:
    """Simple document class to hold content and metadata"""
    def __init__(self, page_content: str, metadata: Dict[str, Any]):
        self.page_content = page_content
        self.metadata = metadata


class VectorStore:
    def __init__(self, model_name: str):
        self.client = chromadb.PersistentClient(path="data/vector_store/")
        self.collection = self.client.get_or_create_collection(name="documents_collection")
        self.embedding_model = SentenceTransformer(model_name)

    def add_documents(self, documents: List[Dict[str, Any]]):
        texts = [doc['text'] for doc in documents]
        metadatas = [doc['metadata'] for doc in documents]
        self.embeddings = [self.embedding_model.encode(text).tolist() for text in texts]
        ids = [str(uuid.uuid4()) for _ in range(len(texts))]

        self.collection.add(
            ids=ids,
            embeddings=self.embeddings,
            metadatas=metadatas,
            documents=texts
        )
        print(f"Added {len(texts)} documents to the vector store.")
        

    def query(self, query: str, top_k: int = 5) -> List[Tuple[str, Dict[str, Any]]]:
        query_embedding = self.embedding_model.encode(query).tolist()
        results = self.collection.query(
            query_embeddings=[query_embedding],
            n_results=top_k
        )
        return list(zip(results['documents'][0], results['metadatas'][0]))

    def similarity_search_with_score(self, query: str, k: int = 5) -> List[Tuple[Document, float]]:
        """Search with distance scores"""
        query_embedding = self.embedding_model.encode(query).tolist()
        results = self.collection.query(
            query_embeddings=[query_embedding],
            n_results=k,
            include=['documents', 'metadatas', 'distances']
        )
        
        # Return (document, score) tuples
        docs_with_scores = []
        for i in range(len(results['documents'][0])):
            doc_content = results['documents'][0][i]
            doc_metadata = results['metadatas'][0][i]
            score = results['distances'][0][i]  # L2 distance
            
            # Create Document object
            doc = Document(page_content=doc_content, metadata=doc_metadata)
            docs_with_scores.append((doc, score))
        
        return docs_with_scores
    
