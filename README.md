# Análisis de pases mediante grafos y dígrafos — Mundial de Qatar 2022

- **Integrantes:** Mishelle Molina y Dhidel Osorio
- **Curso:** Álgebra Lineal — Universidad Francisco Marroquín

## Descripción

Proyecto final de Álgebra Lineal. Representamos los pases completados de **Argentina (7 partidos)**
y **Brasil (5 partidos)** en el Mundial de Qatar 2022 como **grafos dirigidos y ponderados**:
cada jugador es un vértice y cada arista i → j indica cuántos pases completó i hacia j.

Con esos grafos calculamos grados de entrada y salida, densidad, la **matriz de adyacencia A**
y sus potencias (A², A³), rutas más cortas, la **matriz de transición de Markov P** y la
**matriz fundamental N = (I − Q)⁻¹** de una cadena de Markov absorbente, junto con las
probabilidades de absorción B = N·R. Al final comparamos los 12 partidos y las dos selecciones.

## Objetivos

**General:** analizar los pases de Argentina y Brasil durante Qatar 2022 con grafos dirigidos,
matrices y cadenas de Markov para identificar patrones en la circulación del balón.

**Específicos:**
1. Identificar a los jugadores con más participación (pases realizados, recibidos y grados).
2. Usar la matriz de adyacencia y sus potencias para estudiar las conexiones entre jugadores.
3. Encontrar rutas entre jugadores y calcular probabilidades con cadenas de Markov.
4. Comparar los resultados entre partidos y selecciones.

## Tecnologías utilizadas

| Herramienta | Uso |
|---|---|
| Python 3.10+ | Lenguaje del proyecto |
| pandas | Lectura y filtrado de los CSV de pases |
| NumPy | Matrices, productos matriciales, inversa y valores propios |
| NetworkX | Construcción del dígrafo, grados y rutas |
| Matplotlib | Redes de pases, gráficas de grados, mapas de calor y comparaciones |
| Git y GitHub | Control de versiones |

## Cómo ejecutar el programa (Windows, PowerShell en VS Code)

```powershell
git clone https://github.com/Dhidel/Graphsproject.git
cd Graphsproject\Proyecto_final_completado

py -m venv .venv                     # crear el entorno virtual (solo la primera vez)
.\.venv\Scripts\Activate.ps1          # activarlo (cada vez que se abre una terminal)
python -m pip install -r requirements.txt   # instalar dependencias (solo la primera vez)

python main.py                       # menú interactivo
python pruebas.py                    # 50 pruebas automáticas (debe terminar en 50/50)
```

Si PowerShell no permite activar el entorno, ejecutar primero
`Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass`.
Las instrucciones completas (incluyendo macOS/Linux y cómo seleccionar el intérprete en
VS Code) están en el README detallado.

## Documentación y resultados

- **README detallado** (fundamento matemático, resultados, interpretaciones y limitaciones):
  [`Proyecto_final_completado/README.MD`](Proyecto_final_completado/README.MD)
- **Resultados para la presentación:**
  [`Proyecto_final_completado/Presentacion/`](Proyecto_final_completado/Presentacion/)
  - [Resumen de resultados](Proyecto_final_completado/Presentacion/Resultados_presentacion.md)
  - [Tabla comparativa de los 12 partidos](Proyecto_final_completado/Presentacion/tabla_12_partidos.md)
  - [Matrices de ejemplo (A, A², A³, P, P², N, B)](Proyecto_final_completado/Presentacion/Matrices_ejemplo.md)
- **Gráficas (300 DPI):**
  [`Proyecto_final_completado/Presentacion/graficas/`](Proyecto_final_completado/Presentacion/graficas/)

## Estructura del repositorio

```
Graphsproject/
├── README.md                      ← este archivo
└── Proyecto_final_completado/
    ├── main.py                    menú interactivo
    ├── graphs.py                  grafo, grados, A, A², A³, rutas, P, Markov absorbente
    ├── graficas.py                gráficas
    ├── comparacion.py             comparación de los 12 partidos
    ├── nombres.py                 nombres cortos de jugadores y rivales
    ├── pruebas.py                 pruebas automáticas
    ├── generar_presentacion.py    genera el material de Presentacion/
    ├── pases_argentina.csv        datos originales
    ├── pases_brasil.csv           datos originales
    ├── requirements.txt
    ├── README.MD                  documentación detallada
    └── Presentacion/              resultados, tablas y gráficas
```
