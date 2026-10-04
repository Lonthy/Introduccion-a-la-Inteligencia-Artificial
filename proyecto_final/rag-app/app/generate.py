import os
from typing import List, Dict, Any, Optional
from google import genai
from store import ChromaManager

class GeminiRAGService:
    """
    Servicio RAG con umbral de abstención, citas de documentos 
    y formateo de chunks numerados para Google Gemini.
    """
    def __init__(
        self,
        chroma_manager: Optional[ChromaManager] = None,
        model_name: str = "gemini-3.5-flash-lite",
        distance_threshold: float = 0.65
    ):
        """
        :param chroma_manager: Instancia de ChromaManager.
        :param model_name: Nombre del modelo de Gemini a utilizar.
        :param distance_threshold: Umbral máximo de distancia coseno para considerar un chunk válido.
                                   (Valores menores indican mayor similitud. Si la distancia es > threshold, se descarta).
        """
        api_key = os.getenv("GOOGLE_API_KEY")
        if not api_key:
            raise ValueError("Por favor, configura la variable de entorno GOOGLE_API_KEY.")

        self.client = genai.Client(api_key=api_key)
        self.model_name = model_name
        self.chroma_manager = chroma_manager or ChromaManager()
        self.distance_threshold = distance_threshold

    def _filter_and_format_chunks(self, search_results: Dict[str, Any]) -> tuple[str, List[Dict[str, Any]]]:
        """
        Filtra los fragmentos por el umbral de distancia y genera la lista numerada.
        """
        documents = search_results.get("documents", [[]])[0]
        metadatas = search_results.get("metadatas", [[]])[0]
        distances = search_results.get("distances", [[]])[0] if "distances" in search_results else []

        valid_chunks = []
        context_lines = []

        for idx, (doc, meta) in enumerate(zip(documents, metadatas), start=1):
            distance = distances[idx - 1] if idx - 1 < len(distances) else 0.0

            # Validar umbral de distancia (para metrica Cosine: 0 es identico, > 0.65 suele ser poco relevante)
            if distance <= self.distance_threshold:
                source_file = meta.get("source", "Documento Desconocido")
                page_num = meta.get("page", "N/A")

                chunk_entry = {
                    "number": idx,
                    "text": doc,
                    "source": source_file,
                    "page": page_num,
                    "distance": distance
                }
                valid_chunks.append(chunk_entry)

                context_lines.append(
                    f"[CHUNK #{idx}]\n"
                    f"Fuente: {source_file} (Página {page_num})\n"
                    f"Contenido:\n{doc}\n"
                    f"----------------------------------------"
                )

        formatted_context = "\n\n".join(context_lines)
        return formatted_context, valid_chunks

    def answer_query(self, query: str, top_k: int = 4) -> Dict[str, Any]:
        """
        Realiza la búsqueda vectorial, aplica el umbral y genera la respuesta con Gemini.
        """
        # 1. Recuperar contexto de ChromaDB
        search_results = self.chroma_manager.query_top_k(query_text=query, k=top_k)
        formatted_context, valid_chunks = self._filter_and_format_chunks(search_results)

        # 2. Verificar umbral de abstención por falta de relevancia vectorial
        if not valid_chunks or not formatted_context.strip():
            return {
                "status": "abstained",
                "answer": "Lo siento, no se encontró información lo suficientemente relevante en los documentos cargados para responder a tu consulta.",
                "used_chunks": [],
                "citations": []
            }

        # 3. Diseñar el Prompt estricto para Gemini
        system_instruction = (
            "Eres un asistente de consulta documental estricto y preciso. "
            "Tu única tarea es responder a la pregunta del usuario utilizando EXCLUSIVAMENTE los fragmentos (chunks) proporcionados.\n\n"
            "REGLAS OBLIGATORIAS:\n"
            "1. Si los fragmentos provistos NO contienen la información necesaria para responder con certeza, DEBES ABSTENERTE de responder "
            "y contestar exactamente con la frase: 'ABSTENCION: La información proporcionada en los documentos no es suficiente para responder esta consulta.'\n"
            "2. NO utilices conocimiento externo ni asumas información que no esté directamente en los fragmentos.\n"
            "3. Cada afirmación de tu respuesta DEBE citar explícitamente el número de chunk usado entre corchetes, por ejemplo: [CHUNK #1] o [CHUNK #2].\n"
            "4. Al final de tu respuesta, agrega una sección 'Fuentes Consultadas:' listando el archivo y página de los chunks citados."
        )

        prompt = f"CONTEXTO DISPONIBLE:\n{formatted_context}\n\nPREGUNTA DEL USUARIO:\n{query}"

        try:
            # 4. Generar respuesta usando la API de Gemini
            response = self.client.models.generate_content(
                model=self.model_name,
                contents=prompt,
                config={
                    "system_instruction": system_instruction,
                    "temperature": 0.0  # Temperatura 0 para mayor fidelidad al texto
                }
            )

            answer_text = response.text.strip()

            # 5. Evaluar si el modelo decidió abstenerse
            if "ABSTENCION:" in answer_text:
                return {
                    "status": "abstained",
                    "answer": "Lo siento, la información disponible en los documentos no es suficiente para responder con certeza a tu consulta.",
                    "used_chunks": valid_chunks,
                    "citations": []
                }

            # Extraer las citas únicas para el resumen de metadatos
            citations = [
                {"chunk_number": chunk["number"], "source": chunk["source"], "page": chunk["page"]}
                for chunk in valid_chunks
            ]

            return {
                "status": "success",
                "answer": answer_text,
                "used_chunks": valid_chunks,
                "citations": citations
            }

        except Exception as e:
            return {
                "status": "error",
                "message": f"Error al comunicarse con Gemini: {str(e)}"
            }