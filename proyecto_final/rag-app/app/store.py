import chromadb
from typing import List, Dict, Any
from embed import GeminiEmbeddingFunction

class ChromaManager:
    def __init__(self, db_path: str = "../chroma", collection_name: str = "gemini_collection"):
        """
        Inicializa el cliente persistente de Chroma e inyecta la función de Google AI.
        """
        # 1. Instanciar la función externa de embeddings
        self.embedding_fn = GeminiEmbeddingFunction()

        # 2. Configurar cliente local persistente de Chroma
        self.chroma_client = chromadb.PersistentClient(path=db_path)
        
        # 3. Crear o conectar la colección usando la función inyectada
        self.collection = self.chroma_client.get_or_create_collection(
            name=collection_name,
            embedding_function=self.embedding_fn,
            metadata={"hnsw:space": "cosine"} # Métrica de distancia: Similitud de coseno
        )

    def add_documents(self, documents: List[str], metadatas: List[Dict[str, Any]], ids: List[str]):
        """Guarda los textos. Chroma llamará internamente al módulo de Gemini."""
        self.collection.add(
            documents=documents,
            metadatas=metadatas,
            ids=ids
        )
        print(f"✅ {len(documents)} documentos guardados de forma persistente en Chroma.")

    def query_top_k(self, query_text: str, k: int = 2) -> Dict[str, Any]:
        """Realiza una consulta Top-K basada en similitud semántica."""
        results = self.collection.query(
            query_texts=[query_text],
            n_results=k
        )
        return results