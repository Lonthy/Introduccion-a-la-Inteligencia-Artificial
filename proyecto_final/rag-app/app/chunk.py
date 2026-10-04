import os
from typing import List, Dict, Any
from pypdf import PdfReader
from langchain_text_splitters import RecursiveCharacterTextSplitter

class PDFChunker:
    """
    Módulo encargado de cargar archivos PDF y dividirlos en chunks
    optimizados con metadatos para su incrustación.
    """
    def __init__(self, chunk_size: int = 1000, chunk_overlap: int = 200):
        """
        :param chunk_size: Tamaño máximo aproximado de caracteres por chunk.
        :param chunk_overlap: Número de caracteres que se solapan entre chunks consecutivos.
        """
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap,
            length_function=len,
            separators=["\n\n", "\n", ". ", " ", ""]
        )

    def process_pdf(self, pdf_path: str) -> Dict[str, Any]:
        """
        Lee un PDF, lo divide por páginas y posteriormente en chunks.
        Devuelve listas de documents, metadatas e ids listos para ChromaManager.
        """
        if not os.path.exists(pdf_path):
            raise FileNotFoundError(f"El archivo {pdf_path} no existe.")

        reader = PdfReader(pdf_path)
        file_name = os.path.basename(pdf_path)

        documents: List[str] = []
        metadatas: List[Dict[str, Any]] = []
        ids: List[str] = []

        global_chunk_idx = 0

        for page_num, page in enumerate(reader.pages, start=1):
            text = page.extract_text()
            if not text or not text.strip():
                continue  # Salta páginas vacías o escaneadas sin OCR

            # Dividir el texto de la página en fragmentos
            page_chunks = self.text_splitter.split_text(text)

            for chunk_idx, chunk in enumerate(page_chunks):
                chunk_id = f"{file_name}_p{page_num}_c{chunk_idx}_{global_chunk_idx}"
                
                documents.append(chunk)
                metadatas.append({
                    "source": file_name,
                    "page": page_num,
                    "chunk_index": chunk_idx
                })
                ids.append(chunk_id)
                
                global_chunk_idx += 1

        print(f"📄 Procesado '{file_name}': {len(reader.pages)} páginas ➡️ {len(documents)} chunks creados.")
        
        return {
            "documents": documents,
            "metadatas": metadatas,
            "ids": ids
        }