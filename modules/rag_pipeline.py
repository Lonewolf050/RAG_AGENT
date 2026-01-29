import os
from typing import List
from .embeddings import get_embedding_generator
from .vector_db import get_vector_db
from .llm_client import get_llm_client


class RAGPipeline:
    def __init__(self):
        self.embedder = get_embedding_generator()
        self.vector_db = get_vector_db()
        self.llm = get_llm_client()
        print("[RAG] Pipeline ready")
    
    def ingest_documents(self, folder_path: str, chunk_size: int = 500) -> int:
        chunks = []
        metadata = []
        
        for filename in os.listdir(folder_path):
            if filename.endswith(".txt"):
                filepath = os.path.join(folder_path, filename)
                with open(filepath, "r", encoding="utf-8") as f:
                    content = f.read()
                
                file_chunks = self._split_text(content, chunk_size)
                for chunk in file_chunks:
                    chunks.append(chunk)
                    metadata.append({"source": filename})
        
        if chunks:
            embeddings = self.embedder.generate(chunks)
            self.vector_db.add_documents(chunks, embeddings, metadata)
        
        return len(chunks)
    
    def _split_text(self, text: str, chunk_size: int) -> List[str]:
        chunks = []
        words = text.split()
        current_chunk = []
        current_size = 0
        
        for word in words:
            current_chunk.append(word)
            current_size += len(word) + 1
            
            if current_size >= chunk_size:
                chunks.append(" ".join(current_chunk))
                current_chunk = []
                current_size = 0
        
        if current_chunk:
            chunks.append(" ".join(current_chunk))
        
        return chunks
    
    def generate_summary(self, query: str = "Summarize the main content.") -> str:
        query_embedding = self.embedder.generate_single(query)
        results = self.vector_db.search(query_embedding, top_k=3)
        
        context = "\n\n".join([r["text"] for r in results])
        summary = self.llm.generate_summary(context, query)
        
        return summary


_pipeline = None

def get_rag_pipeline():
    global _pipeline
    if _pipeline is None:
        _pipeline = RAGPipeline()
    return _pipeline
