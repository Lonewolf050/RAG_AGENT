import faiss
import numpy as np
import pickle
import os
from typing import List, Dict


class VectorDB:
    def __init__(self, db_path="./data/faiss_db"):
        self.db_path = db_path
        self.index_path = os.path.join(db_path, "index.faiss")
        self.docs_path = os.path.join(db_path, "documents.pkl")
        self.documents = []
        self.index = None
        self.dimension = 384
        
        os.makedirs(db_path, exist_ok=True)
        self._load_or_create()
        print(f"[VectorDB] Ready with {len(self.documents)} documents")
    
    def _load_or_create(self):
        if os.path.exists(self.index_path) and os.path.exists(self.docs_path):
            self.index = faiss.read_index(self.index_path)
            with open(self.docs_path, "rb") as f:
                self.documents = pickle.load(f)
        else:
            self.index = faiss.IndexFlatL2(self.dimension)
    
    def add_documents(self, texts: List[str], embeddings: List[List[float]], metadata: List[Dict] = None):
        vectors = np.array(embeddings).astype("float32")
        self.index.add(vectors)
        
        for i, text in enumerate(texts):
            self.documents.append({
                "text": text,
                "metadata": metadata[i] if metadata else {}
            })
        
        self._save()
    
    def search(self, query_embedding: List[float], top_k: int = 3) -> List[Dict]:
        query = np.array([query_embedding]).astype("float32")
        distances, indices = self.index.search(query, top_k)
        
        results = []
        for i, idx in enumerate(indices[0]):
            if idx < len(self.documents):
                results.append({
                    "text": self.documents[idx]["text"],
                    "score": float(distances[0][i])
                })
        return results
    
    def _save(self):
        faiss.write_index(self.index, self.index_path)
        with open(self.docs_path, "wb") as f:
            pickle.dump(self.documents, f)


_db = None

def get_vector_db():
    global _db
    if _db is None:
        _db = VectorDB()
    return _db
