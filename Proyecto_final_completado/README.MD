# Análisis de Pases - Mundial Qatar 2022

Proyecto de Grafos y Dígrafos que utiliza Python para analizar las redes de pases de Argentina y Brasil durante el Mundial de Qatar 2022.

El programa representa a los jugadores como nodos y los pases como conexiones dirigidas con pesos, permitiendo analizar cómo circula el balón entre los jugadores.

## Tecnologías utilizadas

- Python
- Pandas
- NumPy
- NetworkX
- Matplotlib

## Funcionalidades

- Construcción y visualización de grafos de pases.
- Estadísticas de pases realizados y recibidos.
- Cálculo y representación de grados de entrada y salida.
- Matrices de adyacencia y sus potencias (A² y A³).
- Búsqueda de rutas entre jugadores.
- Cadenas de Markov y probabilidades de transición.
- Análisis de matrices inversas en modelos de Markov absorbentes.

## Instalación

Instalar las bibliotecas necesarias:

```bash
pip install pandas numpy networkx matplotlib
```

## Ejecución

En el archivo `main.py`, seleccionar el partido que se desea analizar:

```python
from graphs import analizar_partido

analizar_partido("Argentina", "Saudi Arabia")
```

También se pueden analizar otros partidos cambiando la selección y el rival:

```python
analizar_partido("Argentina", "Mexico")
analizar_partido("Brasil", "Serbia")
```

Ejecutar desde la terminal:

```bash
python main.py
```

## Archivos del proyecto

- `main.py`: ejecuta los análisis.
- `graphs.py`: contiene las funciones del programa.
- `pases_argentina.csv`: datos de Argentina.
- `pases_brasil.csv`: datos de Brasil.

## Nota

Los resultados se basan en los pases completados registrados en los CSV. Las rutas representan conexiones posibles entre jugadores y no necesariamente secuencias de pases que ocurrieron durante el partido.

El cálculo de la matriz inversa puede no estar definido para algunos partidos, dependiendo de la estructura de la cadena de Markov.