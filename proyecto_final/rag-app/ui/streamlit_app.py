import streamlit as st
import requests

# Configuración de la página
st.set_page_config(
    page_title="Gestor RAG - PDF Ingestion",
    page_icon="",
    layout="wide"
)

API_URL = "http://localhost:8000"

st.title("PDF Chunking & Vector Search")
st.markdown("Procesa tus documentos PDF e insértalos en ChromaDB mediante la API FastAPI.")

# Crear dos pestañas en la interfaz
tab_ingest, tab_query = st.tabs(["Cargar PDF", "Consultar Base de Datos"])

# -------------------------------------------------------------------
# Pestaña 1: Carga e Ingesta de PDFs
# -------------------------------------------------------------------
with tab_ingest:
    st.header("Ingestar nuevo PDF")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        uploaded_file = st.file_uploader("Selecciona un archivo PDF", type=["pdf"])
    
    with col2:
        st.subheader("Configuración de Chunks")
        chunk_size = st.number_input("Chunk Size", min_value=100, max_value=4000, value=1000, step=100)
        chunk_overlap = st.number_input("Chunk Overlap", min_value=0, max_value=1000, value=200, step=50)

    if st.button("Procesar e Ingestar", type="primary"):
        if uploaded_file is not None:
            with st.spinner("Enviando y procesando el archivo PDF..."):
                try:
                    files = {"file": (uploaded_file.name, uploaded_file.getvalue(), "application/pdf")}
                    params = {
                        "chunk_size": chunk_size,
                        "chunk_overlap": chunk_overlap
                    }
                    
                    response = requests.post(f"{API_URL}/ingest-pdf/", files=files, params=params)
                    
                    # Intentar parsear JSON de forma segura
                    try:
                        data = response.json()
                    except Exception:
                        data = None

                    if response.status_code == 200 and data:
                        st.success(f"¡Éxito! Archivo `{data['filename']}` procesado correctamente.")
                        st.metric(label="Total de Chunks Creados", value=data["total_chunks"])
                    else:
                        # Si no es JSON, mostramos el texto plano devuelto por el backend
                        error_msg = data.get("detail") if isinstance(data, dict) else response.text
                        st.error(f"Error ({response.status_code}): {error_msg}")

                except requests.exceptions.ConnectionError:
                    st.error("No se pudo conectar con la API de FastAPI. Asegúrate de que `main.py` esté ejecutándose en `http://localhost:8000`.")
        else:
            st.warning("Por favor, selecciona un archivo PDF antes de procesar.")
# -------------------------------------------------------------------
# Pestaña 2: Búsqueda Semántica
# -------------------------------------------------------------------
with tab_query:
    st.header("Consultar al Chatbot RAG")
    
    query_text = st.text_input("Escribe tu pregunta:")
    col_k, col_thresh = st.columns(2)
    
    with col_k:
        top_k = st.slider("Chunks a recuperar (K)", min_value=1, max_value=10, value=4)
    with col_thresh:
        threshold = st.slider("Umbral de Abstención (Distancia Máx)", min_value=0.1, max_value=1.0, value=0.65, step=0.05)
    
    if st.button("Enviar Pregunta", type="primary"):
        if query_text.strip():
            with st.spinner("Consultando fuentes y analizando respuesta con Gemini..."):
                payload = {
                    "query": query_text,
                    "k": top_k,
                    "distance_threshold": threshold
                }
                
                response = requests.post(f"{API_URL}/query/", json=payload)
                
                if response.status_code == 200:
                    data = response.json()
                    status = data.get("status")
                    answer = data.get("answer")
                    
                    if status == "abstained":
                        st.warning(f"**Respuesta rechazada por el sistema:**\n\n{answer}")
                    else:
                        st.markdown("### Respuesta del Chatbot")
                        st.write(answer)
                        
                        # Mostrar acordeón con los Chunks entregados al modelo
                        with st.expander("Ver fragmentos (chunks) evaluados"):
                            for chunk in data.get("used_chunks", []):
                                st.markdown(f"**[CHUNK #{chunk['number']}]** — *{chunk['source']} (Página {chunk['page']})* | Distancia: `{chunk['distance']:.4f}`")
                                st.text(chunk["text"])
                                st.divider()
                else:
                    st.error(f"Error ({response.status_code}): {response.text}")
        else:
            st.warning("Escribe una pregunta antes de enviar.")