# Proyecto final

## Dominio y tamaño del corpus

El corpus consiste de 8 archivos .PDF descargados de Wikipedia, uno de ellos habla sobre las Maravillas del mundo y los otros 7 hablan sobre cada una de las 7 Maravillas del mundo antiguo (El Coloso de Rodas, la Estatua de Zeus en Olimpia, el Faro de Alejandría, la Gran Pirámide de Guiza, los Jardines Colgantes de Babilonia, el Mausoleo de Halicarnaso y el Templo de Artemisa).
 
Los documentos tienen entre 7 y 12 páginas, se generaron 208 chunks en total y se utilizó el modelo de embedding "gemini-embedding-001".

## Cómo particionaste (tamaño, overlap) y por qué

Para guardarlo en la base de datos vectorial se utilizó una configuración de chunks de Chunk Size = 1000 y Chunk Overlap = 200 (se pueden configurar estos parámetros al procesar los PDF). El uso de un Chunk Size = 1000 y un Chunk Overlap = 200 es una de las configuraciones estándar más comunes al usar RAG.

1,000 caracteres equivalen aproximadamente a 150-200 palabras en español (2 a 3 párrafos cortos). Esto garantiza que cada fragmento contenga una idea completa o un argumento con suficiente contexto independiente.

El overlap representa el 20% del tamaño del chunk, esto evita el Boundary Problem (asegura que el final del primer chunk y el inicio del segundo compartan información, garantizando que ninguna idea quede a medias.) y ayuda a preservar el contexto.

## Cómo decides abstenerte

Para decidir si responder o abstenerse, el programa utiliza 2 filtros, distancia del coseno y un prompting estricto en Gemini.

La distancia maxima utilizada para los ejemplos es de 0.65 (esto también puede ser configurado al momento de hacer la consulta,) por lo que si ninguno de los chunks recuperados (igualmente es posible configurar la cantidad de chunks que se recuperan, para el ejemplo se utilizaron 4) tiene una distancia del coseno mayor al limite el sistema se abstiene automáticamente de responder.

Para el segundo filtro el prompt hecho a Gemini incluye la frase "Si los fragmentos provistos NO contienen la información necesaria para responder con certeza, DEBES ABSTENERTE de responder" y "NO utilices conocimiento externo ni asumas información que no esté directamente en los fragmentos." asegurando así que Gemini no conteste utilizando información externa. 

## Qué sale de Google AI (embeddings vs. generación) y qué hace Chroma

Para el embedding, Google AI se encarga de convertir el contenido a vectores numéricos utilizando el modelo "gemini-embedding-001" en "embed.py" mientras que ChromaDB simplemente utiliza la función self.collection.add, y esta internamente llama al módulo de Gemini para hacer el embedding antes de guardarla en una base de datos vectorial persistente.

Mientras tanto, para la generación, ChromaDB se encarga de realizar el calculo de distancia del coseno para encontrar los k fragmentos vectoriales mas similares a la pregunta hecha por el usuario y se los envía a Google AI, el cual actúa como el modelo de lenguaje (utilizando el modelo "gemini-3.5-flash-lite") que lee, razona y redacta respuestas en lenguaje natural, usando como entrada el contexto con los chunks numerados que recuperó ChromaDB, la misma pregunta inicial del usuario, y las especificaciones que estan dentro del mismo sistema, para despues dar la respuesta final redactada, incluyendo las citas explícita o la señal de haberse abstenido.