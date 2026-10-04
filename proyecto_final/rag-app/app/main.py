import os
import shutil
import tempfile
from fastapi import FastAPI, UploadFile, File, HTTPException, Query
from pydantic import BaseModel
from typing import List, Dict, Any, Optional

from generate import GeminiRAGService
from chunk import PDFChunker
from store import ChromaManager

from dotenv import find_dotenv, load_dotenv

load_dotenv(find_dotenv())

app = FastAPI(
    title="PDF Ingestion API",
    description="API para procesar PDFs, dividirlos en chunks y guardarlos en ChromaDB.",
    version="1.0.0"
)

# Instanciamos el cliente de ChromaManager al iniciar la aplicación
chroma_manager = ChromaManager()

# Instanciamos el servicio RAG
generate = GeminiRAGService(chroma_manager=chroma_manager)

class QueryRequest(BaseModel):
    query: str
    k: int = 4
    distance_threshold: Optional[float] = 0.65

@app.post("/ingest-pdf/", summary="Cargar y procesar un archivo PDF")
async def ingest_pdf(
    file: UploadFile = File(...),
    chunk_size: int = Query(1000, description="Tamaño máximo de caracteres por chunk"),
    chunk_overlap: int = Query(200, description="Solapamiento entre chunks")
):
    """
    Recibe un archivo PDF, lo guarda temporalmente, extrae sus fragmentos (*chunks*)
    y los almacena de forma persistente en ChromaDB.
    """
    # Validar que el archivo sea un PDF
    if not file.filename.endswith(".pdf"):
        raise HTTPException(status_code=400, detail="El archivo debe tener extensión .pdf")

    # Crear un archivo temporal para guardar el PDF recibido
    with tempfile.TemporaryDirectory() as temp_dir:
        temp_pdf_path = os.path.join(temp_dir, file.filename)
        
        with open(temp_pdf_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        try:
            # 1. Instanciar el chunker y procesar el PDF
            chunker = PDFChunker(chunk_size=chunk_size, chunk_overlap=chunk_overlap)
            data = chunker.process_pdf(temp_pdf_path)

            if not data["documents"]:
                raise HTTPException(status_code=400, detail="No se pudo extraer texto del PDF.")

            # 2. Guardar los fragmentos en ChromaDB
            chroma_manager.add_documents(
                documents=data["documents"],
                metadatas=data["metadatas"],
                ids=data["ids"]
            )

            return {
                "message": "PDF procesado y guardado exitosamente.",
                "filename": file.filename,
                "total_chunks": len(data["documents"])
            }

        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error al procesar el PDF: {str(e)}")

@app.post("/query/", summary="Consultar el Chatbot RAG con Abstención y Citas")
async def query_rag(request: QueryRequest):
    """
    Ejecuta la búsqueda semántica e interroga a Gemini aplicando
    el umbral de abstención y las citas numeradas por fragmentos.
    """
    # Actualizar umbral si el usuario envía uno personalizado
    if request.distance_threshold is not None:
        generate.distance_threshold = request.distance_threshold

    result = generate.answer_query(query=request.query, top_k=request.k)
    
    if result.get("status") == "error":
        raise HTTPException(status_code=500, detail=result.get("message"))
        
    return result

@app.get("/health")
def health_check():
    """
    Verifica el estado de la aplicación.
    """
    return {"status": "ok"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)