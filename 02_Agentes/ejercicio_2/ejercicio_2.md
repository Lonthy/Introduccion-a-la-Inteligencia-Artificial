# Ejercicio 2 — Descripción PEAS de agentes inteligentes

## Asistente virtual de voz

- **Performance:** precisión en la detección de comandos de voz, tiempo de respuesta a un comando, calidad de audio, relevancia de las respuestas proporcionadas, cantidad de activaciones falsas y que tan entendible es la voz del agente.
- **Environment:** las personas que interactuan con el agente y sus diferentes voces/acentos, el lugar fisico donde se encuentra (varia la acustica dependiendo del tamaño del lugar o si esta en el exterior o el interior), los ruidos externos alrededor, los sistemas con los que tiene que interactuar para cumplir los comandos (internet, bluetooth, sistemas de correo electronico, etc.). Es estocastico.
- **Actuators:** las bocinas para reproducir la voz, conexiones de API para ajustar el volumen, enviar correos, reproducir musica, apagar/encender las luces, proporcionar la informacion de una busqueda, etc. (existen muchos posbiles comandos y muchas posibles conexiones a sistemas digitales que puede tener un asistente virtual de voz.)
- **Sensors:** microfono, detección de notificaciones o alertas via internet, lectura de comandos manuales por medio de un dispositivo bluetooth.

**Justificación:** es estocastico porque no es posible determinar que comando se le va a proporcionar al agente por parte del usuario.

## Robot aspirador doméstico

- **Performance:** tiempo en el que completa la limpieza, precision para detectar suciedad, que tan limpio quedo el lugar al terminar, cantidad de choques, velocidad, eficiencia de la bateria.
- **Environment:** habitacion que se tiene que limpiar, cantidad de suciedad en el espacio, objetos o muebles en el suelo, contenedor para guardar lo que se aspira, tipo de suelo de la habitación y personas o mascotas dentro de la habitacion. Es secuencial.
- **Actuators:** aspiradora para succionar la suciedad, las ruedas y el motor que utiliza para moverse, cepillos giratorios para recoger el polvo, sistema de carga para la bateria, sistema para depositar la suciedad acumulada
- **Sensors:** nivel de bateria, sensor de proximidad para detectar objetos en el camino, sensor de suciedad, detector de velocidad, detector de colisones, capacidad actual del contenedor.

**Justificación:** es secuencial ya que dependiendo de donde este el robot la acción que va a tomar va a ser diferente, y cada vez que se mueve o limpia la siguiente acción va a ser diferente.

## Sistema de recomendación de streaming

- **Performance:** cantidad de recomendaciones, que tan acertadas son estas, tiempo de generación de las recomendaciones, cantidad de personas que toman alguna de ellas.
- **Environment:** estructura de la plataforma de streaming, peliculas o canciones disponibles en la plataforma, personas que la utilizan y sus gustos, historial de busqueda del usuario dentro de la misma plataforma, categorias en las que se divide el contenido, lugar de origen del usuario, fecha y hora. Es dinámico.
- **Actuators:** motor de busqueda para recomendaciones relacionadas a la busqueda, sistema de auto-reproducción de las recomendaciones, display de secciones de recomendados.
- **Sensors:** analizador del historial de busqueda, detección interacciones del usuario con distinto contenido, tiempo de vista del usuario en contenido dentro de categorias determinadas, detección de fecha y hora, detección de la ubicación del usuario.

**Justificación:** es dinámico ya que el ambiente cambia constantemente, ya sea con nuevo contenido siendo añadido a la plataforma, o el mismo usuario cambiando sus gustos dependiendo de diferentes factores (ej. su humor.)

## Vehículo autónomo en ciudad

- **Performance:** velocidad, precisión de los sensores de proximidad, eficiencia de las rutas, capacidad para seguir leyes de transito (velocidad maxima en diferentes calles, sentido de las calles, respeto a diferentes señalamientos,) seguridad de los pasajeros, tiempo de reacción a cambios bruscos (ej. un animal se cruza en el camino), eficiencia del uso de combustible, comodidad de los pasajeros y precisión de los sensores visuales (detección de semaforos, peatones, otros vehiculos, etc.)
- **Environment:** pasajeros dentro del vehiculo, calidad y tipo de la calle, otros vehiculos, peatones, semaforos, señalamientos, lineas y limites en la calle, edificios de los alrededores, leyes de transito locales, condiciones climatologicas, etc. (el ambiente de un vehiculo autónomo es basicamente el mundo real, por lo que su ambiente es muy extenso.) Es parcialmente observable.
- **Actuators:** sistemas de aceleracion, frenado, volante, faros, luces de señal (intermitentes y luces de estacionamiento), limpiaparabrisas, manejo de velocidades del motor y claxón.
- **Sensors:** camaras, sensores de proximidad, velocimetro, acelerometro, nivel de gasolina, nivel de bateria, sensores de estado del vehiculo (nivel de las llantas, aceite, estado del motor, etc.), GPS y cuentakilómetros.

**Justificación:** es parcialmente observable ya que no es posible ver lo que el vehiculo se va a encontrar en cada momento. Al doblar una esquina el vehiculo se va encontrar con un ambiente y obstaculos diferentes a los que tenia antes y no hay manera de observar esto con anticipación.

## Agente de trading algorítmico en bolsa

- **Performance:** factor de ganancias, rentabilidad acumulada, rentabilidad anualizada, velocidad de procesamiento, porcentaje de trades que generaron ganancias.
- **Environment:** la bolsa de valores, las empresas en las que se esta invirtiendo, los bancos que se estan utilizando para manejar el dinero, los que permiten conectarse con los bancos para realizar los trades. Es dinamico.
- **Actuators:** sistema de deposito y retiro de dinero, mecanismos que envian la solicitud de comprar o vender, modulos para detener inversiones que generan perdidas, sistemas de ajuste que cambian las cantidades que se invierten.
- **Sensors:** lecturas de las ganancias corporativas de las diferentes empresas, los indicadores economicos (ej. la inflación), monitores de la bolsa de trabajo, analizadores de redes sociales.

**Justificación:** es dinamico ya que la bolsa de valores es algo que cambia constantemente, el valor de las empresas siempre esta subiendo y bajando por lo que el agente necesita tener en cuenta estos cambios.

## Sistema de diagnóstico médico asistido por IA

- **Performance:** claridad de las imagenes tomadas, precisión del análisis de estas imagenes para determinar datos importantes en ellas, cercania del resultado del análisis con la documentación ya existente, capacidad para medir correctamente signos vitales.
- **Environment:** las tecnologías médicas que se van a utilizar (rayos X, resonancias magnéticas, ect.), el hospital o consultorio, los pacientes sometidos a análisis, los doctores u otro personal médico. Es dinámico.
- **Actuators:** generadores de texto (para proporcionar un análisis escrito), sistema de envio de alertas y correos electronicos (para reportar resultados), impresoras, vistas que resaltan hallazgos importantes en el análisis.
- **Sensors:** camaras, sistemas de imagenes medicas (rayos x, resonancias magnéticas, etc.), medidores de signos vitales, termometro y lectura de entradas de sintomas.

**Justificación:** es dinámico ya que durante el diagnostico los signos vitales del paciente pueden variar de distintas maneras mientras se realiza el diagnóstico.

## Dron de inspección de infraestructura

- **Performance:** precisión del análisis para determinar fallos en la infraestructura, tiempo requerido para realizar la inspección, maxima altura del dron.
- **Environment:** condiciones climatológicas, obstaculos en el aire, disposición de las estructuras a analizar, condición del dron, lugar fisico en el cual esta volando, hora del dia, altura. Es continuo.
- **Actuators:** visualización del resultado de la inspección, salida de texto con recomendaciónes de acciónes a realizar para corregir las fallas.
- **Sensors:** camaras, sensores de proximidad, velocímetro, altímetro, sensores de estado del dron.

**Justificación:** es continuo debido a que ciertas acciones como la altura o la velocidad del dron varian constantemente y no es posible limitarlo a un numero finito de posibilidades.

## Agente jugador de ajedrez

- **Performance:** tiempo para realizar un movimiento, movimientos requeridos para ganar la partida, número de victorias, empates y derrotas, numero de movimientos ilegales, precisión de los movimientos.
- **Environment:** el tablero, las piezas en juego, el otro jugador (ya sea humano u otro agente), la posición actual de las piezas. Es discreto.
- **Actuators:** Motores de brazos robot para mover las piezas (en caso de ajedrez físico), APIs para realizar movimientos en tableros virtuales.
- **Sensors:** Camaras, reloj, APIs para revisar el estado del tablero. 

**Justificación:** Es discreto ya que en cada posición del table solo hay un número finito de movimientos que se pueden hacer, por lo que el agente lo que hace es encontrar el mejor movimiento posible de los disponibles.