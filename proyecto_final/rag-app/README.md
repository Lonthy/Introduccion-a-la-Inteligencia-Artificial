# Sistema RAG para Consulta de PDFs con Gemini y ChromaDB

Este proyecto es una aplicación de **Retrieval-Augmented Generation (RAG)** que permite procesar documentos PDF, dividirlos en fragmentos (*chunks*), almacenarlos en una base de datos vectorial persistente (**ChromaDB**) y realizar consultas en lenguaje natural a través de **Google Gemini** con un estricto umbral de abstención y citas de fuentes.

## Requisitos Previos

* **Python 3.10+**

* Una clave de API de **Google AI Studio** ([Obtener GEMINI_API_KEY](https://aistudio.google.com/))

## Guía de Instalación y Configuración

### 1. Crear y activar el entorno virtual (`venv`)

En la raíz del proyecto, ejecuta el comando correspondiente a tu sistema operativo:

#### En Windows (PowerShell / CMD):

```
# Crear el entorno virtual
python -m venv .venv

# Activar en PowerShell
.\.venv\Scripts\Activate.ps1

# O activar en CMD
.\.venv\Scripts\activate.bat

```

#### En macOS / Linux:

```
# Crear el entorno virtual
python3 -m venv .venv

# Activar
source .venv/bin/activate

```

### 2. Instalar las dependencias con `requirements.txt`

Asegúrate de tener el entorno virtual activado e instala todas las dependencias del proyecto:

```
pip install -r requirements.txt

```

### 3. Configurar las variables de entorno (`.env`)

Crea un archivo `.env` en la raíz del proyecto copiando la plantilla `.env.example`:

```
# En Linux/macOS o Git Bash
cp .env.example .env

# En Windows (PowerShell)
Copy-Item .env.example .env

# En Windows (CMD)
copy .env.example .env

```

Abre el archivo `.env` recién creado con tu editor de texto y reemplaza el valor con tu clave de API:

```
GOOGLE_API_KEY=tu_clave_api_real_aqui

```

## Ejecución de la Aplicación

Para poner en marcha todo el sistema, se deben iniciar dos servicios en terminales independientes (ambas con el entorno virtual activado):

### Paso 1: Levantar la API Backend (FastAPI)

En la primera terminal, ejecuta:

```
uvicorn main:app --reload

```

* La API se iniciará en `http://localhost:8000`

* Documentación interactiva Swagger en `http://localhost:8000/docs`

### Paso 2: Levantar la Interfaz de Usuario (Streamlit)

Abre una **segunda terminal**, activa el `.venv` y ejecuta:

```
streamlit run app.py

```

* Se abrirá automáticamente la interfaz web en `http://localhost:8501`.

## Cómo Probar una Pregunta

1. **Ingestar un Documento:**

   * Abre la interfaz web (`http://localhost:8501`).

   * Ve a la pestaña **Cargar PDF**.

   * Selecciona un archivo PDF de tu equipo (ej. un manual, contrato o artículo). Puedes usar los archivos PDF que se encuentran en la carpeta data.

   * Configura el `Chunk Size` (por defecto `1000`) y `Chunk Overlap` (por defecto `200`).

   * Haz clic en **Procesar e Ingestar**. Espera el mensaje de confirmación con el total de fragmentos guardados.

2. **Realizar una Consulta:**

   * Ve a la pestaña **Consultar Base de Datos**.

   * Escribe una pregunta directamente relacionada con el contenido del PDF que subiste.

   * Haz clic en **Enviar Pregunta**.

3. **Verificar la Respuesta:**

   * **Respuesta exitosa:** El chatbot te dará una respuesta citando explícitamente los fragmentos usados (ej. `[CHUNK #1]`) y mostrará un desplegable con las fuentes originales y sus páginas.

   * **Abstención:** Si preguntas algo que **no está** en el documento o la similitud semántica es baja, el sistema responderá indicando que se abstiene de contestar debido a falta de información suficiente.