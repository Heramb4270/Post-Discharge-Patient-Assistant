from typing import List
import numpy as np
from sentence_transformers import SentenceTransformer

class Embeddings:
    def __init__(self, model_name: str):
        self.model = SentenceTransformer(model_name)

    def embed_documents(self, documents: List[str]) -> np.ndarray:
        return self.model.encode(documents)

    def embed_query(self, query: str) -> np.ndarray:
        return self.model.encode([query])[0]
