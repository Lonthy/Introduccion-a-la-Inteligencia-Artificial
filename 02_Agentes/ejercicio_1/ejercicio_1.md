# Ejercicio 1 — Cambiar la ubicación del Wumpus y los pits

 4 | .  P  .  . 
 3 | P  .  W  . 
 2 | .  .  .  G 
 1 | >  .  .  P 
    -----------
     1  2  3  4

Tras ejecutar el código utilizando esta nueva configuración del mundo de Wumpus obtuve resultados algo diferentes que utilizando el mapa clásico. El agente de simple reflex no logro conseguir el oro, al igual que en el original, y se quedo atorado en la casilla [3,1] dando vueltas. Los agentes model based y goal based, a diferencia de con el mapa clásico, no lograron llegar al oro, quedándose atorados en la casilla [3,2], dando vueltas de manera similar al agente simple reflex. El agente utility based si logró salir con el oro y le tomo 27 pasos, mientras que el learning agent lo hizo en tan solo 16 pasos.

Como se puede observar, el agente de simple reflex falló en ambos casos, quedándose tanto en el mapa clásico como en el nuevo apenas se topa con una brisa. Por la manera en la que esta programado el agente de simple reflex, apenas percibe una brisa su respuesta es girar a la derecha, y debido a que girar a la derecha no cambia la casilla en la que se encuentra, este vuelve a percibir la brisa, llevando a que vuelva a girar a la derecha, entrando en un bucle hasta que se acaban los pasos permitidos. Esto se debe a que esta hecho un simple if que al recibir la brisa como entrada siempre va a reaccionar con la acción girar, la cual no causa que deje de recibir esta misma entrada. La razón por la que esto funciona así es porque el agente, al ser uno de simple reflex, no tiene memoria de las casillas anteriores, por lo que al entrar a una casilla con brisa y percibirla, este sabe que una casilla adyacente tiene un hueco, pero al no recordar de cual viene, no tiene manera de asegurar que ninguna de las casillas a su alrededor es segura, causando que no pueda moverse y se quede simplemente girando a la derecha. Los demás agentes no tienen este problema, ya que guardan lo que percibieron en las casillas anteriores, por lo que saben que pueden regresar de donde vienen sin peligro de caer en un hueco.

Para comprobar que como cambia el resultado del agente model based, modifique el mapa clásico (ya que en este el agente si logra salir con el oro) de la siguiente manera:

 4 | .  .  .  P  	4 | .  .  .  P
 3 | W  G  P  . 	3 | W  G  P  .
 2 | .  .  .  . 	2 | .  .  .  .
 1 | >  P  .  . 	1 | >  .  .  P
    -----------  	   -----------
     1  2  3  4		    1  2  3  4


En el caso del primer mapa, el agente model based se queda atorado en la primera casilla dando vueltas. Esto se debe a que al no tener alguna casilla segura a la cual regresar (ya que es la casilla inicial) el agente no sabe hacia donde puede ir y simplemente gira sin poder avanzar en ninguna dirección, por lo que simplemente se termina el numero de pasos permitidos sin que la flecha se mueva del inicio.

Cuando se ejecuta utilizando el segundo mapa, el agente basado en modelo si logra salir con el oro, pero le toma 23 pasos, a diferencia de los 19 pasos que ocupa con la configuración clásica. Esto sucede debido a que al estar mas lejos el hueco, el agente tiene que recorrer mas casillas para percibir la brisa, lo que hace que le tome mas movimientos el corregir su curso y encontrar la ruta correcta.