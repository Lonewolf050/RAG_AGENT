from sentence_transformers import SentenceTransformer
from typing import List


class EmbeddingGenerator:
    def __init__(self, model_name="all-MiniLM-L6-v2"):
        self.model = SentenceTransformer(model_name)
        print("[Embeddings] Model loaded")
    
    def generate(self, texts: List[str]) -> List[List[float]]:
        return self.model.encode(texts, show_progress_bar=True).tolist()
    
    def generate_single(self, text: str) -> List[float]:
        return self.model.encode([text])[0].tolist()


_generator = None

def get_embedding_generator():
    global _generator
    if _generator is None:
        _generator = EmbeddingGenerator()
    return _generator
