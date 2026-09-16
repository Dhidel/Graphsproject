# Graphsproject
first project

# 3
1. Para la lectura de los datos se utilizará la librería pandas
    Las columnas que utilizaré y el porqué:
    - Match: Porque mi idea inicial es hacer un grafo por cada partido (y si me da tiempo hacer uno combinado)
    - Fase: Para filtrar los de fase de grupos
    - Oponente: Para obtener información para los grafos en cada partido.
    - Minuto: Quizás
    - Jugador Nombre: Para identificar a cada jugador y definir quizá otras estadísticas individuales
    - Jugador receptor: esto va a definir al grafo como dirigido, de x -> y  
    - Resultado: Para filtrar solo los pases que sí se hicieron
    - Longitud: Le dará peso al grafo

2. El grafo será un grafo dirigido, en donde el nodo inicial será el jugador que da el pase y la dirección apuntará al receptor, esto para hacer más visible hacia dónde se hicieron los pases durante el partido y mejorar interpretaciones.

El grafo tendrá peso, el cuál será marcado por la longitud del pase, entre más largo sea más pesado será, esto, de nuevo, para hacer visible el estilo de juego y mejorar interpretaciones.

Se obtendrá un grafo por partido y luego un grafo general que englobará los tres encuentros. Esto para identificar variaciones en cada partido y luego para que se pudiese comparar toda la fase con otros equipos.

Se tomará en cuenta únicamente los pases completados para la simplicidad del grafo y la interpretación de los datos.

El criterio del peso será la longitud de los pases 

