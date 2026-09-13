# Ejercicio 1 — Comparar BFS, UCS, DFS, DLS e IDS en el mapa de Rumania

## Pareja Origen-Destino: Sibiu → Neamt

| Programa | Path | Depth | Cost | Expanded | Status |
|---|---|---|---|---|---|
| `02_breadth_first_search.py` | Sibiu → Fagaras → Bucharest → Urziceni → Vaslui → Iasi → Neamt | 6 roads | 716 km | 19 nodes | success |
| `03_uniform_cost_search.py` | Sibiu → Rimnicu Vilcea → Pitesti → Bucharest → Urziceni → Vaslui → Iasi → Neamt | 7 roads | 684 km | 19 nodes | success |
| `04_depth_first_search.py` | Sibiu → Arad → Timisoara → Lugoj → Mehadia → Drobeta → Craiova → Pitesti → Bucharest → Urziceni → Vaslui → Iasi → Neamt | 12 roads | 1279 km | 15 nodes | success |
| `05_depth_limited_search.py` (limit 5) | N/A | N/A | N/A | 33 nodes | cutoff |
| `05_depth_limited_search.py` (limit 6)| Sibiu → Fagaras → Bucharest → Urziceni → Vaslui → Iasi → Neamt | 6 roads | 716 km | 22 nodes | success |
| `06_iterative_deepening_search.py` | Sibiu → Fagaras → Bucharest → Urziceni → Vaslui → Iasi → Neamt | 6 roads | 716 km | 93 nodes | success |

Tras ejecutar todos los programas de busqueda y realizar un análisis se puede observar que el algoritmo BFS dio como resultado un camino diferente a UCS. Se puede observar que BFS opta por utlizar el camino de Fagaras mientras que UCS va por el camino de Rimnicu Vilcea. Esto se debe a que BFS siempre obta por expandir el nodo menos profundo que aun no se ha expandido, lo cual hace que encuentre el nodo meta en la menor cantidad de pasos, mientras que el UCS, al tomar en cuenta los costos priorizando los nodos de menor costo, es capaz de encontrar el resultado que toma la menor cantidad de kilometros, incluso aunque esto implique recorrer una mayor cantidad de nodos.

Tambien se puede observar que IDS tuvo la misma profundidad que BFS. Ambos algoritmos buscan la solucion que requiere pasar por el menor número de nodos, la diferencia es que IDS no necesita tener cada nodo en memoria todo el tiempo, por lo que es mas eficiente en terminos de espacio, pero mas lento en tiempo.

El algoritmo DFS fue el que tomo el camino mas largo para llegar a Neamt, tanto en terminos de caminos como de kilometros recorridos. Esto suscede debido a que DFS recorre todos los nodos en orden hasta que ya no puede llegar mas profundo, en este caso en particular Arad era el primer nodo en la lista, por lo que tomo ese camino y siguio recorriendo ese camino hasta llegar a Neamt. Se puede observar como a pesar de haber tomado un camino mas largo expandio una menor cantidad de nodos que los primeros dos algoritmos.

Tras probar DLS desde limite 2 se encontro el que el primer limite en el cual encuentra la meta es 6, las ejecuciones utilizando limites del 2 al 5 fallaron. Como se puede observar en la tabla, la profundida en la que los algoritmos IDS y BFS encontraron la meta fue de 6, y por la forma en la que funcionan estos algoritmos, se puede confirmar que esta es la profundidad mas baja que se puede tener para llegar a Neamt, por esto mismo es que todos los parametros de limite debajo de 6 fallan, es imposible llegar a Neamt desde Sibiu pasando por menos de 6 caminos, lo cual lleva a que DLS se quede corto y no alcance la meta.