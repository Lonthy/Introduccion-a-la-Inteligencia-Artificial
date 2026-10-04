import os
from google import genai
from chromadb.api.types import EmbeddingFunction, Documents, Embeddings

class GeminiEmbeddingFunction(EmbeddingFunction):
    """
    Clase puente requerida por Chroma DB. 
    Transforma texto en vectores list[float] usando Google AI.
    """
    def __init__(self, model: str = "gemini-embedding-001"):
        api_key = os.getenv("GOOGLE_API_KEY")
        if not api_key:
            raise ValueError("Por favor, configura la variable de entorno GOOGLE_API_KEY.")
        
        # Inicializa el cliente oficial de Google AI
        self.ai_client = genai.Client(api_key=api_key)
        self.model = model

    def __call__(self, input: Documents) -> Embeddings:
        """Método obligatorio que Chroma llamará automáticamente."""
        texts = list(input)
        try:
            response = self.ai_client.models.embed_content(
                model=self.model,
                contents=texts,
            )
            return [embedding.values for embedding in response.embeddings]
        except Exception as e:
            print(f"Error en GeminiEmbeddingFunction: {e}")
            raise e