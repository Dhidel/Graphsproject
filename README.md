# Graphsproject
first project

# 3
1. Para la lectura de los datos se utilizará la librería pandas
    Las columnas que utilizaré y el porqué:
    - Fase: Para filtrar los de fase de grupos
    - Oponente: Para obtener información para los grafos en cada partido, pues se hará un grafo por cada partido.
    - Jugador Nombre: Para identificar a cada jugador que dió el pase
    - Jugador receptor: Para identificar al jugador que recibió el pase.
    - Resultado: Para filtrar solo los pases que sí se hicieron

2. El grafo será un grafo dirigido, en donde el nodo inicial será el jugador que da el pase y la dirección apuntará al receptor, esto para hacer más visible hacia dónde se hicieron los pases durante el partido y mejorar interpretaciones.

El grafo tendrá peso, el cuál será marcado por la cantidad de pases, entre más pases sean dados de un jugador a otro más pesado será, esto, de nuevo, para hacer visible el estilo de juego y mejorar interpretaciones.

Se obtendrá un grafo por partido y luego un grafo general que englobará los tres encuentros. Esto para identificar variaciones en cada partido y luego para que se pudiese comparar toda la fase con otros equipos.

Se tomará en cuenta únicamente los pases completados para la simplicidad del grafo y la interpretación de los datos.

El criterio del peso será la cantidad de pases

3. Se utilizó NetworkX para construir el grafo y Matplotlip para mostrarlo visualmente

4. Interpretaciones:
    - Argentina vs Arabia Saudí: La cantidad de pases (542) demuestra que, a pesar del resultado, Argentina dominó la mayor parte del pártido. Además, demuestra claramente el estilo de juego marcado de Argentina durante todo el torneo, uno basado en tener el balón, dominar desde la poseción y atacar en base a sus delanteros estrella. Se observa también que los cambios no tuvieron mucha incidencia en el partido, sobretodo el delantero Julián Alvarez, lo cuál es normal pues ingresó cuando el partido se estaba perdiendo y cuando Arabia Saudí estaba encerrado atrás. 
    - Argentina vs México: La caída en los pases (476) nos muestra que el partido fue más parejo de lo que el resultado demuestra, a pesar de que argentina dominó el cuentro no se encontraba tan cómoda, pues sabían que un resultado distinto a la victorio les complicaría la clasificación. Esto se destaca con dos resultados clave del grafo: el primero es el aumento de pases a la banda derecha que se hacen, buscando, por supuesto, a su estrella Lionel Messi, que, por supuesto, aparecería marcando el primer gol del partido; el segundo dato se demuestran con los cambios, sobre todo con Enzo Fernandez, el cuál, a diferencia del partido anterior, recibió mayor cantidad de pases de una mayor cantidad de compañeros, esto es normal pues su ingreso cambió totalmente el partido, a tal grado de marcar el segundo gol del partido, después de este partido se convertiría en titular indiscutible de la selección, no solo durante el mundial sino hasta el día de hoy.
    - Argentina vs Polonia: Los pases en este partido (826) demuestran una clara superioridad en el encuentro y una marcada diferencia respecto al partido anterior, a pesar de que los dos resultados son iguales los partidos son completamente distintos. En este encuentro Argentina dominó completamente el partido de inicio a fin, por eso se puede notar una mayor distribución en los pases, no solo a la banda derecha como en el partido anterior. Además, se puede notar con los cambios, los cinco cambios que ingresaron tuvieron una mayor cantidad de pases que los cambios de los dos partidos anteriores, mostrando un claro dominio y una tranquilidad sobre el encuentro.

En conjunto los 3 pártidos demuestran algo clave, que el estilo de Argentina en 2022 era el dominio del encuentro mediante la poseción y la retención del balón, una constante que se mantendría por todo el mundial, pues en lineas generales fueron los claros dominantes de todos los partidos que tuvieron.
Además, los grafos dejan explicito algo clave de argentina durante el mundial: los cambios, pues no es solo utilizar a los jugadores, es la incidencia que tienen estos en el partido y Lionel Scaloni fue un entrenador que se arriesgó a modificar el equipo constantemente, una clara muestra de ello fueron dos piezas clave del mundial: Julián Alvarez y Enzo Fernandez, que iniciaron desde la banca pero se ganaron la titularidad, en el grafo esto se nota pues van teniendo cada vez más pases recibidos de compañeros conforme pasaban los 3 partidos, llegando a ser titulares en el cuarto.
Otro punto clave es Lionel Messi, el cuál es el jugador al que más compañeros le pasan el balón durante los partidos, siendo más evidente en el partido contra méxico, en el cuál se puede vizualizar en el grafo la diferencia de flechas apuntando hacía él.


