# Ejercicio 1 — Comparar Greedy y A* en el mapa de Rumania

## Pareja Origen-Destino: Sibiu → Neamt

| Programa | Path | Depth | Cost | Expanded | Heuristic |
|---|---|---|---|---|---|
| `03_greedy_best_first_search.py` | Sibiu → Fagaras → Bucharest → Urziceni → Vaslui → Iasi → Neamt | 6 roads | 716 km | 7 nodes | Euclidean distance to Neamt (map coordinates) |
| `04_a_star_search.py` | Sibiu → Rimnicu Vilcea → Pitesti → Bucharest → Urziceni → Vaslui → Iasi → Neamt | 7 roads | 684 km | 15 nodes | Euclidean distance to Neamt (map coordinates) |

Tras comparar el resultado de los algoritmos con calculos propios se puede observar que A* encontro el camino mas eficiente en terminos de kilometros cuando se utiliza la distancia euclidiana hacia Neamt como heurisitca. En este caso especifico el algoritmo Greedy no coincidio con A*, Greedy fue por el camino de Fagaras, mientras que A* fue por Rimnicu Vilcea, esto se debe a que al decidir cual camino tomar, Greedy busca simplemente el nodo que tenga la menor distancia euclidiana a Neamt h(n), que en este caso seria Fagaras, sin embargo al observar el grafo se puede ver que Fagaras esta mas cerca de Neamt en terminos de distancia euclidiana pero el camino total es mas caro. Mientras tanto A* utiliza la formula f(n) = g(n) + h(n), por lo que si toma en cuenta el costo total del camino que esta tomando. Siguiendo esta formula, A* primero expande el nodo de Rimnicu Vilcea porque es el que tiene un f(n) menor, luego ve que el nodo de Fagaras tiene un menor f(n) de todas las opciones (principalmente por su h(n)) y lo expande, y al hacerlo ve que al final si es mejor continuar por el camino de Rimnicu, siguiendo a Pitesti, por lo que al final termina tomando esta ruta.

Se puede observar al analizar los resultados que f(n) nunca disminuye al ejecutar A*, lo cual se debe a que este siempre escoje un camino que avance hacia la meta, sumando las distancias que ha recorrido, ya que la distancia euclidiana nunca llega a ser menor que 0, y solo es 0 si ya te encuentras en la meta, por lo que esta es una heuristica consistente.