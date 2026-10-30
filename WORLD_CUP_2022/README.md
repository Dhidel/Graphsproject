# WORLD_CUP_2022-BRASIL 

CONSTRUCCIÓN DEL GRAFO: 

-Grafo dirigido: Elegimos un grafo dirigido porque en cada pase importa quién manda la pelota y quién la recibe. Por ejemplo, si Vinícius le da un pase a Neymar, se representa como Vinícius → Neymar, ya que esto no significa que Neymar también le haya dado un pase a Vinícius. Así podemos ver mejor cómo circula el balón entre los jugadores.

-Grafo con pesos: Elegimos usar pesos porque queremos representar cuántos pases completados hizo un jugador hacia otro. Por ejemplo, si Casemiro completó 15 pases hacia Neymar, esa conexión tendría un peso de 15. Esto nos ayuda a identificar qué jugadores se conectan más entre sí y cuáles son las conexiones más importantes del equipo.

-Grafo por partido: Decidimos realizar un grafo por cada partido de la fase de grupos porque así podemos analizar cómo cambió la forma de jugar de Brasil dependiendo del oponente. Esto nos permite comparar las conexiones entre los jugadores en cada partido e identificar diferencias en la circulación del balón.

-Pases completos: Decidimos utilizar únicamente los pases completados porque queremos representar las conexiones que realmente ocurrieron entre los jugadores. Un pase incompleto no genera una conexión efectiva entre el emisor y el receptor, por lo que usamos los pases completos para representar de manera más clara cómo circuló el balón.


INTERPRETACIÓN DEL GRAFO:
-Los tres partidos tienen un número de pases completos parecido: 539 contra Serbia, 507 contra Suiza y 512 contra Camerún. Eso muestra un estilo de posesión constante, sin importar el rival.
Contra Suiza la bola pasó mucho más por un mismo par de jugadores. Thiago y Marcos combinaron 60 pases entre los dos, casi el doble de cualquier otra conexión en los tres partidos. El grafo deja ver como Brasil se apoya en jugadores claves para construir sus jugadas, en vez de repartir el balón entre todo el equipo.

-Contra Serbia el juego se ve más repartido. No hay una conexión que domine como con Suiza. Varias parejas, Alex y Thiago, Marcos y Thiago, Danilo y Marcos, Alex y Neymar, llegan a números parecidos, entre 17 y 19 pases cada una. Serbia dejó más espacios y Brasil circuló con más variedad de compañeros.

-El grafo de Camerún es totalmente diferente. Los nombres de los jugadores que dominaron los partidos en Serbia y Suiza, Alex, Thiago, Marcos, Danilo, Carlos, Neymar, Vinícius, Raphael, casi no aparecen. En su lugar salen otros jugadores: Gleison, Fábio, Éder, Daniel, Gabriel, Ederson, Bruno. Esto coincide con la historia real del Mundial de ese año porque Brasil ya estaba clasificado antes de ese partido y el entrenador decidió no poner a los jugadores titulares. El cambio en el grafo viene de un cambio de plantilla y es super importante para no malinterpretar los datos.

-Con los tres grafos juntos se ve un Brasil enfocado en tener el balón y construir sus jugadas desde atrás sin importar el rival, pero adaptando cómo lo reparte según el nivel de cierre defensivo del contrario. Lo concentra en pocos jugadores contra bloques compactos como Suiza y lo reparte más contra rivales que ceden espacio como Serbia. El ejemplo de Camerún muestra como al cambair de plantilla de jugadores, cambian la forma del grafo tanto como la táctica misma.