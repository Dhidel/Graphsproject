# Análisis de pases mediante grafos y dígrafos — Mundial de Qatar 2022, Argentina y Brasil

Proyecto final de Álgebra Lineal. Representamos los pases de Argentina y Brasil como
**grafos dirigidos y ponderados** y los analizamos con matrices de adyacencia, grados,
rutas y **cadenas de Markov** (incluyendo la matriz fundamental de una cadena absorbente).

## 1. Objetivo

**General:** analizar los pases de Argentina y Brasil durante Qatar 2022 con grafos
dirigidos, matrices y cadenas de Markov para identificar patrones en la circulación del balón.

**Específicos:**
1. Identificar a los jugadores con más participación (pases realizados, recibidos y grados).
2. Usar la matriz de adyacencia y sus potencias para estudiar las conexiones.
3. Encontrar rutas entre jugadores y calcular probabilidades con cadenas de Markov.
4. Comparar los resultados entre partidos y selecciones.

## 2. Instalación

Requiere Python 3.10 o superior (probado con Python 3.14, pandas 3.0, numpy 2.5,
networkx 3.6 y matplotlib 3.11).

```bash
pip install -r requirements.txt
```

## 3. Ejecución

El programa funciona desde cualquier carpeta (las rutas se calculan con `pathlib` y `__file__`).

```bash
python main.py                  # menú interactivo
python pruebas.py               # 50 pruebas automáticas
python generar_presentacion.py  # regenera la carpeta Presentacion
```

El menú permite elegir la **selección**, el **partido**, el **jugador de origen y destino**
de la ruta, el **jugador destino del modelo de Markov**, el filtro de la gráfica y si
se abren las gráficas. Las entradas inválidas se rechazan con un mensaje y se vuelven a pedir.

También se puede usar desde Python:

```python
from graphs import analizar_partido
analizar_partido("Argentina", "Arabia Saudita", origen="Papu Gómez", destino="Acuña",
                 destino_markov="Otamendi", umbral=5)

from comparacion import imprimir_comparacion
imprimir_comparacion()          # tabla y gráficas de los 12 partidos
```

Los nombres de selección, rival y jugadores aceptan mayúsculas/minúsculas, tildes
opcionales, español o inglés ("México"/"Mexico") y nombre corto o completo ("Messi").

## 4. Partidos disponibles (12)

| Argentina (7) | Fase | Brasil (5) | Fase |
|---|---|---|---|
| Arabia Saudita | Grupos | Serbia | Grupos |
| México | Grupos | Suiza | Grupos |
| Polonia | Grupos | Camerún | Grupos |
| Australia | Octavos | Corea del Sur | Octavos |
| Países Bajos | Cuartos | Croacia | Cuartos |
| Croacia | Semifinal | | |
| Francia | Final | | |

## 5. Archivos

| Archivo | Contenido |
|---|---|
| `main.py` | Menú interactivo |
| `graphs.py` | Cálculos: grafo, grados, A, A², A³, rutas, P, P², Markov absorbente |
| `graficas.py` | Red de pases, grados, mapas de calor y comparaciones (300 DPI) |
| `comparacion.py` | Tabla de los 12 partidos y comparación Argentina vs Brasil |
| `nombres.py` | Nombres cortos de jugadores y rivales en español |
| `pruebas.py` | Pruebas automáticas |
| `generar_presentacion.py` | Genera gráficas y tablas de `Presentacion/` |
| `pases_argentina.csv`, `pases_brasil.csv` | Datos originales (no se modifican) |
| `Presentacion/` | Material para la presentación |
| `salidas/` | Gráficas generadas al ejecutar (una carpeta por partido, no se sube a git) |

## 6. Funcionalidades y fundamento matemático

### 6.1 Grafo
- **Vértice** = jugador. **Arista dirigida i → j** = al menos un pase completado de i a j.
- **Peso** w(i,j) = cantidad de pases completados de i a j (solo `resultado == "Complete"`
  y solo el partido elegido).
- **Grado de salida / entrada** = cantidad de compañeros *diferentes* a los que pasó / de los que recibió.
- **Grado ponderado** de salida / entrada = total de pases completados realizados / recibidos.
- **Densidad** = m / (n(n−1)): fracción de las conexiones posibles que sí ocurrieron.
- En un dígrafo, la suma de grados de entrada es igual a la de salida (= m), por eso el
  **grado medio de entrada y de salida son iguales** (m/n).

### 6.2 Matriz de adyacencia y potencias
- A[i,j] = 1 si existe la arista i → j, 0 si no (matriz binaria, diagonal en 0).
- A² = A·A y A³ = A·A·A se calculan con **multiplicación matricial** (`np.linalg.matrix_power`).
- (A^k)[i,j] = número de **recorridos dirigidos** de k conexiones de i a j. Un recorrido
  puede repetir jugadores y **no es una jugada que haya ocurrido**: es una posibilidad
  dentro del grafo (que además junta a jugadores que quizá nunca coincidieron en la cancha).
- Todas las matrices usan el mismo orden de jugadores y se imprimen con sus nombres.

### 6.3 Rutas
- `nx.shortest_path` sobre el dígrafo: respeta la dirección y minimiza la **cantidad de
  conexiones** (no usa pesos). Si no existe ruta dirigida, el programa lo indica.
- Se muestra también cuántas rutas mínimas distintas hay y se comprueba con A^k:
  si la ruta mínima tiene k conexiones, A^k[i,j] > 0 y A^m[i,j] = 0 para m < k.
- La ruta más corta **no es** la más probable ni una jugada real.

### 6.4 Cadena de Markov
- P[i,j] = w(i,j) / Σ_k w(i,k): probabilidad de que el **siguiente pase completado** de i vaya a j.
- Cada fila suma 1. Si un jugador no completó ningún pase (sumidero), se define P[i,i] = 1
  (estado absorbente). Ocurre solo una vez en los 12 partidos: Julián Álvarez contra Arabia Saudita.
- P² = P·P: probabilidad de que el balón esté en j después de dos pases completados.

### 6.5 Markov absorbente y matriz fundamental
1. **Absorbentes:** el jugador destino (por defecto **Otamendi** en Argentina y
   **Marquinhos** en Brasil, ambos centrales que jugaron todos los partidos de su selección)
   **y todos los sumideros**. El resto son **transitorios**.
2. **Condición de existencia:** se verifica con el grafo que desde cada transitorio se pueda
   llegar a algún absorbente. Si no, existe una **clase cerrada** de transitorios, Q tiene
   valor propio 1 y **I − Q es singular**; el programa muestra esa clase y no invierte.
   (No se usa pseudoinversa.)
3. Se reordena P como `[[Q, R], [0, I]]` y se calcula:
   - **N = (I − Q)⁻¹**: N[i,j] = número esperado de veces que el jugador j tiene el balón,
     empezando en i, antes de la absorción (incluye la posesión inicial si i = j).
     N = I + Q + Q² + … converge porque el radio espectral de Q es < 1.
   - **t = N·1**: número esperado de pases hasta llegar a **cualquier** estado absorbente.
   - **B = N·R**: B[i,k] = probabilidad de que, empezando en i, el balón termine en el absorbente k.
4. Si el destino es el único absorbente, t es el número esperado de pases hasta llegar al
   destino. **Si hay más de un absorbente, t no es el tiempo hasta el destino**; B indica la
   probabilidad de terminar en cada uno.
5. N **no calcula rutas**: resume visitas esperadas según las probabilidades de P.

## 7. Resultados

La tabla completa está en `Presentacion/tabla_12_partidos.md`.

### 7.1 Resultados de los preliminares (Argentina vs Arabia Saudita) — se mantienen

| Resultado | Preliminares | Versión final |
|---|---|---|
| Otamendi: grado de entrada / salida | 12 / 11 | 12 / 11 |
| Otamendi: pases realizados / recibidos | 84 / 80 | 84 / 80 |
| A²[Papu Gómez, Messi] / A³[Papu Gómez, Messi] | 5 / 50 | 5 / 50 |
| Ruta Papu Gómez → Acuña | Gómez → Molina → Acuña | igual (única ruta de 2 conexiones) |
| P(Papu Gómez → Paredes) | ≈30 % | 6/20 = 30 % |
| P²(Papu Gómez → Otamendi) | ≈21 % | 20.86 % |
| N contra México | calculada | idéntica |
| N contra Arabia Saudita | no se pudo calcular | **ahora sí** (ver 7.2) |

### 7.2 El problema de la inversa contra Arabia Saudita (resuelto)
Julián Álvarez recibió 4 pases pero no completó ninguno: su fila de pesos es cero y en P
queda P[Álvarez, Álvarez] = 1, o sea, es **otro estado absorbente**. La versión anterior lo
dejaba dentro de Q; su fila de I − Q era cero, det(I − Q) = 0 y no existía la inversa.

Ahora Álvarez se trata como absorbente junto con Otamendi. Q pasa a tener radio espectral
0.835 < 1 y N existe. Resultado: desde cualquier jugador, el balón termina en Otamendi con
probabilidad entre 0.76 (Acuña) y 0.95 (Tagliafico); el resto termina en Álvarez. Aquí
t ≈ 4 a 7 pases es el tiempo hasta **cualquiera** de los dos absorbentes.

### 7.3 Comparación de los 12 partidos (promedio por partido)

| Métrica | Argentina (7) | Brasil (5) |
|---|---|---|
| Pases completados | 562.7 ± 145.6 | 555.2 ± 59.0 |
| Precisión de pase (%) | 84.9 ± 3.6 | 86.8 ± 1.3 |
| Jugadores | 16.1 | 16.0 |
| Conexiones | 133.3 ± 12.5 | 131.2 ± 5.2 |
| Densidad | 0.55 ± 0.06 | 0.55 ± 0.02 |
| Grado medio (compañeros) | 8.26 ± 0.72 | 8.20 ± 0.33 |
| % de pases en las 5 conexiones principales | **14.3 ± 1.3** | **18.7 ± 1.5** |

*Precisión = pases completados / todos los pases registrados del equipo en ese partido.*

- **Volumen y estructura muy parecidos.** Las dos selecciones completaron ≈ 555–563 pases
  por partido con densidad 0.55 y ≈ 8.2 compañeros por jugador.
- **La diferencia más clara es la concentración.** Brasil concentró más su juego en pocas
  parejas: en **todos** sus partidos las 5 conexiones principales suman más del 17 % de los
  pases, y en **ningún** partido de Argentina superan el 16.8 %. Argentina repartió más el balón.
- **Argentina es más variable** (desviación de 145.6 pases contra 59.0 en Brasil): va de 358
  pases (Croacia) a 826 (Polonia).
- **Jugadores más influyentes.** En Argentina, Otamendi es el que más pases realiza en 3 de
  los 7 partidos (Arabia Saudita, México y Países Bajos). Desde octavos, Enzo Fernández es el
  que más pases realiza en 3 de 4 partidos y el que más recibe en los 4. En Brasil, el que
  más pases realiza es siempre un defensa (Alex Sandro, Marquinhos ×2, Dani Alves, Thiago Silva).
- **t medio** (pases hasta llegar al destino) solo se compara dentro de cada selección,
  porque el destino es distinto (Otamendi / Marquinhos). Se excluye Arabia Saudita, que
  tiene otro absorbente. Argentina: 6.75 (México) a 12.44 (Croacia). Brasil: 6.29 (Suiza,
  donde Marquinhos fue el eje) a 18.10 (Camerún, con suplentes).

### 7.4 Interpretaciones por partido (revisadas con los datos)

Se recuperaron las interpretaciones de las versiones anteriores (`git show a213d46^:README.md`
y `git show a213d46^:WORLD_CUP_2022/README.md`) y se corrigieron las que no coincidían con los datos.

**Argentina**
- **Arabia Saudita (542 pases):** Otamendi fue el eje (más pases realizados, recibidos y
  mayor grado de entrada). Julián Álvarez casi no participó: recibió 4 pases y no completó
  ninguno, lo que lo convierte en un estado absorbente en el modelo de Markov.
- **México (476 pases, el menor de la fase de grupos):** Messi fue el jugador al que
  pasaron **más compañeros diferentes** (grado de entrada 13, el máximo del partido).
  *Corrección:* la versión anterior decía que Enzo Fernández recibió más pases de más
  compañeros que en el partido anterior; los datos no lo confirman (Arabia Saudita: 34 pases
  de 10 compañeros; México: 20 pases de 10 compañeros).
- **Polonia (826 pases, el máximo):** la red más densa de los 12 partidos (0.64) y la mayor
  precisión (90.9 %). De Paul fue el centro (142 realizados, 138 recibidos). Enzo Fernández
  (86 realizados) y Julián Álvarez (25 recibidos de 10 compañeros) tienen aquí una
  participación mucho mayor que en los dos partidos anteriores.
- **Eliminatorias:** Enzo Fernández es el que más pases recibe en los 4 partidos
  (Australia, Países Bajos, Croacia, Francia). Contra Croacia (358 pases) Argentina tuvo su
  menor volumen; la final contra Francia tiene la menor densidad (0.47).
- **Messi:** está entre los 3 jugadores con mayor grado de entrada en 6 de 7 partidos, contando
  empates (la excepción es Polonia). Es el primero solo contra México.

**Brasil**
- Los tres partidos de grupos tienen un volumen parecido (539, 507 y 512 pases).
- **Suiza:** Thiago Silva y Marquinhos combinaron **60 pases** (29 + 31), el doble que la
  segunda pareja del partido (Alex Sandro–Thiago Silva, 30). Es el partido con mayor
  concentración (21.1 % en las 5 conexiones principales). *Corrección:* la versión anterior
  decía "casi el doble de cualquier otra conexión de los tres partidos"; contra Camerún,
  Bremer–Militão sumaron 50.
- **Serbia:** juego más repartido. Alex Sandro→Thiago Silva (19), Marquinhos→Thiago Silva (19),
  Danilo→Marquinhos (19) y Alex Sandro→Neymar (17) tienen valores parecidos (verificado).
- **Camerún:** la red cambia por la rotación de jugadores. Aparecen 6 jugadores que no
  estuvieron en los dos partidos anteriores (Bremer, Dani Alves, Ederson, Everton Ribeiro,
  Fabinho, Pedro), y desaparecen Thiago Silva, Alex Sandro, Danilo, Casemiro, Neymar y
  Vinícius Jr. *Corrección:* Marquinhos y Raphinha sí aparecen contra Camerún. Que Brasil ya
  estuviera clasificado es contexto histórico, no un dato del CSV.

*Nota:* las afirmaciones anteriores sobre "dominio" o "posesión" no pueden comprobarse con
estos CSV, porque solo contienen los pases de Argentina y Brasil, no los del rival. Por eso se
retiraron.

## 8. Limitaciones del modelo

1. **Probabilidades condicionadas:** P solo usa pases completados; no modela pérdidas de
   balón, tiros ni faltas. "30 %" significa "de los pases que Papu Gómez completó".
2. **Sin memoria (propiedad de Markov):** el siguiente pase depende solo de quién tiene el
   balón, no de cómo llegó ni del minuto, el marcador o la posición en la cancha.
3. **Homogeneidad:** P es la misma durante los 90 minutos (o 120), aunque el juego cambie.
4. **Agregación de cambios:** el grafo junta a titulares y suplentes; A^k y N pueden combinar
   jugadores que nunca estuvieron juntos en la cancha.
5. **Pocas observaciones:** filas de P con pocos pases (Acuña completó 18 contra Arabia
   Saudita) dan probabilidades poco estables.
6. **Sumideros:** P[i,i] = 1 es una convención del modelo para que la fila sume 1, no
   significa que el jugador se quede con el balón.
7. **Recorridos ≠ jugadas:** A² y A³ cuentan posibilidades, no secuencias observadas.
8. **Destino fijo:** t y N dependen del destino elegido; solo son comparables con el mismo destino.

## 9. Conclusiones

- Los conceptos de álgebra lineal se aplicaron con éxito y se verificaron numéricamente en los
  12 partidos. Se comprobó que A² = A·A, que las filas de P suman 1, que (I − Q)·N = I y que
  las filas de B suman 1. Una simulación independiente (Monte Carlo) confirma B y t.
- El problema de la matriz inversa de los preliminares no era un error numérico, sino una
  condición matemática: había un segundo estado absorbente (Julián Álvarez). Al modelarlo
  correctamente, N existe en los 12 partidos.
- Argentina y Brasil tienen redes de tamaño, densidad y conectividad casi iguales. La
  diferencia está en **cómo se reparte el balón**: Brasil concentra más su juego en pocas
  parejas (su conexión más frecuente es siempre entre defensas), y Argentina lo distribuye más y varía más entre partidos.
- En Argentina se observa la consolidación de Enzo Fernández como eje del equipo desde el
  tercer partido.
