# Resultados para la presentación

**Análisis de pases mediante grafos y dígrafos — Mundial de Qatar 2022, Argentina y Brasil**

Todos los números salen del programa (`python generar_presentacion.py` y `python pruebas.py`).
Las imágenes están en `graficas/` a 300 DPI.

---

## 1. Qué hicimos (en una frase por concepto)

| Concepto | Qué representa en el fútbol |
|---|---|
| Vértice | Un jugador |
| Arista dirigida i → j | i le completó al menos un pase a j |
| Peso | Cuántos pases completados hubo de i a j |
| Grado de salida / entrada | A cuántos compañeros diferentes pasó / de cuántos recibió |
| Grado ponderado | Total de pases realizados / recibidos |
| Matriz A | Tabla de 0 y 1: ¿existe la conexión? |
| A², A³ | Cuántos recorridos posibles de 2 o 3 conexiones hay |
| Matriz P | Probabilidad de a quién va el siguiente pase completado |
| P² | Probabilidad después de 2 pases |
| N = (I − Q)⁻¹ | Cuántas veces se espera que cada jugador toque el balón antes de la absorción (llegar al destino o a otro estado absorbente) |

**Diapositivas sugeridas:** `red_arg_arabia_saudita.png`, `grados_arg_arabia_saudita.png`,
`matriz_A_arabia.png`, `matriz_P_arabia.png`, `matriz_N_mexico.png`, `matriz_B_arabia.png`,
`red_bra_suiza.png`, `comparacion_selecciones.png`, `comparacion_partidos.png`.

---

## 2. Ejemplos numéricos fáciles de explicar (Argentina vs Arabia Saudita)

### Grados — Otamendi
- Grado de entrada **12**: recibió pases de 12 compañeros diferentes.
- Grado de salida **11**: pasó a 11 compañeros diferentes.
- Grado ponderado: **84** pases realizados y **80** recibidos (el máximo del partido en ambos).

### A² — ¿por qué A²[Papu Gómez, Messi] = 5?
A²[i,j] = Σₖ A[i,k]·A[k,j]: cuenta los jugadores k que **reciben de Gómez y le pasan a Messi**.
Son exactamente 5: **Cuti Romero, Paredes, Molina, Otamendi y Di María**.
Por eso hay 5 recorridos de dos conexiones: Gómez → k → Messi.

A³[Gómez, Messi] = **50**: recorridos de tres conexiones. Ojo: Gómez solo dio 20 pases,
pero A³ cuenta **posibilidades** dentro del grafo, no jugadas que ocurrieron.

### P — la fila de Papu Gómez (20 pases completados)

| Hacia | Paredes | Messi | Tagliafico | Cuti Romero | Otamendi | Molina | Di María |
|---|---|---|---|---|---|---|---|
| Pases | 6 | 4 | 4 | 2 | 2 | 1 | 1 |
| P | **0.30** | 0.20 | 0.20 | 0.10 | 0.10 | 0.05 | 0.05 |

La fila suma 1. "30 %" significa: de los pases que Gómez **completó**, el 30 % fue a Paredes.

### P² — dos pases después
P²[Gómez, Otamendi] = **0.21**: según el modelo, hay un 21 % de probabilidad de que el balón
esté en Otamendi después de dos pases completados que empiezan en Gómez.

### Ruta más corta
Papu Gómez → **Molina** → Acuña (2 conexiones). Es la única ruta de largo 2
(A²[Gómez, Acuña] = 1, A[Gómez, Acuña] = 0). Es la de **menos conexiones**, no la más
probable ni una jugada real.

---

## 3. Matriz fundamental — Argentina vs México (destino: Otamendi)

Otamendi es el único estado absorbente. Fila de **Messi** en N:
- N[Messi, Messi] = **1.75**: empezando en Messi, se espera que él tenga el balón 1.75 veces
  (contando la posesión inicial) antes de que llegue a Otamendi.
- N[Messi, De Paul] = **0.98** y N[Messi, Mac Allister] = **0.91**: son los compañeros que más
  tocan el balón en ese trayecto.
- t[Messi] = **7.41**: se esperan 7.41 pases hasta que el balón llegue a Otamendi.
- El valor más bajo de t es el de Cuti Romero (4.29 pases) y el más alto el de Palacios (8.28).

Estos valores son **idénticos** a los de los preliminares.

---

## 4. El problema de la matriz inversa contra Arabia Saudita y su solución

**Problema (preliminares):** `np.linalg.inv(I − Q)` fallaba: la matriz era singular.

**Causa exacta:** Julián Álvarez entró, recibió **8 pases completados de 4 compañeros
diferentes** (Enzo Fernández 3, Messi 2, Acuña 2 y Di María 1) y **no completó ningún pase**.
- Grado de entrada = 4 (compañeros diferentes), grado de entrada ponderado = 8 (pases
  recibidos) y grado de salida = 0.
- Como su grado de salida es 0, su fila de pases es cero, así que en P queda P[Álvarez, Álvarez] = 1: es un **estado absorbente**.
- El código anterior solo quitaba a Otamendi de Q y dejaba a Álvarez dentro.
- La fila de Álvarez en I − Q quedaba en ceros, así que det(I − Q) = 0.
- En términos de valores propios: Q tenía valor propio 1, porque Álvarez forma una **clase
  cerrada** dentro de los transitorios.

**Condición para que exista (I − Q)⁻¹:** desde **cada** estado transitorio se debe poder llegar
a algún estado absorbente. Eso equivale a que el radio espectral de Q sea menor que 1, y
entonces N = I + Q + Q² + … converge.

**Solución:** tratar a **todos** los estados absorbentes como absorbentes (Otamendi **y**
Álvarez). Antes de invertir, el programa verifica la condición con el grafo; si no se
cumple, muestra la clase cerrada y no invierte. No se usa pseudoinversa.

**Resultado:** radio espectral de Q = 0.835 < 1, N existe y además se calcula:
- **B = N·R** (`matriz_B_arabia.png`): probabilidad de terminar en Otamendi o en Álvarez.
  Desde Tagliafico es 0.95 a Otamendi; desde Acuña, 0.76 a Otamendi y 0.24 a Álvarez
  (en proporción, Acuña es el que más le pasaba a Álvarez: 11 % de sus pases completados).
- **t = N·1**: entre 4.0 y 7.0 pases hasta llegar a **cualquiera** de los dos absorbentes.
  **No** es el tiempo hasta Otamendi.

**Comprobación independiente:** se simularon 20 000 cadenas desde Papu Gómez. El 91.2 %
terminó en Otamendi (B = 0.913), con 5.96 pases en promedio (t = 5.99).

---

## 5. Comparación Argentina vs Brasil (promedio por partido: Argentina 7, Brasil 5)

| Métrica | Argentina | Brasil |
|---|---|---|
| Pases completados | 562.7 | 555.2 |
| Precisión de pase | 84.9 % | 86.8 % |
| Densidad | 0.55 | 0.55 |
| Grado medio (compañeros) | 8.26 | 8.20 |
| % de pases en las 5 conexiones principales | **14.3 %** | **18.7 %** |

**En palabras sencillas:**
- Las dos selecciones pasan **la misma cantidad** de balón y conectan con **los mismos**
  compañeros en promedio.
- La diferencia está en **cómo lo reparten**: Brasil concentra su juego en pocas parejas de
  defensas (todos sus partidos superan el 17 % en las 5 conexiones principales; ningún
  partido de Argentina pasa de 16.8 %).
- Ejemplo extremo: contra Suiza, Thiago Silva y Marquinhos se pasaron el balón **60 veces**,
  el doble que la segunda pareja del partido.
- Argentina es más variable: de 358 pases (Croacia) a 826 (Polonia). Polonia fue su red más
  densa (0.64) y con mejor precisión (90.9 %).
- En Argentina se ve el crecimiento de **Enzo Fernández**: desde octavos es el que más pases
  recibe en los 4 partidos.
- Brasil contra Camerún cambia por la rotación de jugadores: aparecen 6 jugadores nuevos y
  t medio sube a 18.1 pases (el balón tarda más en llegar a Marquinhos).

---

## 6. Conclusiones

1. Los grafos dirigidos y ponderados representan bien la circulación del balón. Los grados
   identifican a los jugadores eje: Otamendi y De Paul al inicio; Enzo Fernández desde octavos.
2. A, A², A³, P y P² se verificaron en los 12 partidos (50 pruebas automáticas correctas).
3. El problema de la inversa no era un error de cálculo, sino una **condición matemática**: un
   segundo estado absorbente. Al modelarlo bien, N existe en los 12 partidos.
4. Argentina y Brasil tienen redes casi iguales en tamaño y densidad. Brasil concentra más su
   juego en pocas parejas y Argentina lo distribuye más.

---

## 7. Limitaciones del modelo

1. P solo usa **pases completados**: no hay pérdidas, tiros ni faltas, y las probabilidades
   son condicionales.
2. **Sin memoria:** el siguiente pase depende solo de quién tiene el balón.
3. **Homogénea:** la misma P para todo el partido.
4. Titulares y suplentes están en el mismo grafo: A^k y N pueden "conectar" a jugadores que
   no coincidieron en la cancha.
5. Filas de P con pocos pases (Acuña: 18) son poco estables.
6. P[i,i] = 1 para jugadores sin pases completados es una convención del modelo.
7. t y N dependen del destino elegido: solo se comparan con el mismo destino.
8. Los CSV no tienen los pases del rival, así que no se puede medir posesión ni dominio.

---

## 8. Posibles preguntas del catedrático

**¿Por qué A³[Gómez, Messi] = 50 si Gómez solo dio 20 pases?**
Porque A³ cuenta recorridos posibles de 3 conexiones en el grafo (pueden repetir jugadores),
no pases reales. Además, A no tiene pesos.

**¿Por qué A² se calcula con producto matricial y no elevando cada elemento?**
Porque (A·A)[i,j] = Σₖ A[i,k]A[k,j] suma los caminos i → k → j. Si se eleva cada elemento al
cuadrado, A no cambia (0² = 0 y 1² = 1).

**¿Qué significa N[i,j]?**
El número esperado de veces que el jugador j tiene el balón, empezando en i, antes de la
absorción. No es una ruta ni una probabilidad (puede ser mayor que 1).

**¿Cuándo existe (I − Q)⁻¹?**
Cuando desde todo estado transitorio se puede llegar a un absorbente, o sea, cuando el radio
espectral de Q es menor que 1. Entonces N = Σ Qᵏ converge.

**¿Por qué no usaron la pseudoinversa?**
Porque la matriz era singular por una razón del modelo (otro absorbente). La pseudoinversa
habría dado números sin interpretación. Lo correcto era corregir el modelo.

**¿t es el tiempo hasta llegar a Otamendi?**
Solo si Otamendi es el único absorbente (México). Contra Arabia Saudita, t es el tiempo hasta
llegar a Otamendi **o** a Álvarez, y B da la probabilidad de cada uno.

**¿Por qué Otamendi y Marquinhos como destino?**
Son centrales que jugaron todos los partidos de su selección. Así, t es comparable entre
partidos de la misma selección. Otamendi además era el destino de los preliminares.

**¿La ruta más corta es la jugada más probable?**
No. `shortest_path` minimiza la cantidad de conexiones sin usar pesos. La más probable
maximizaría el producto de probabilidades de P.

**¿Por qué el grado medio de entrada es igual al de salida?**
Porque cada arista suma 1 al grado de salida de un jugador y 1 al de entrada de otro. Las dos
sumas valen m, y los promedios valen m/n.

**¿Cómo compararon selecciones con distinta cantidad de partidos (7 y 5)?**
Con promedios por partido, desviación estándar y métricas normalizadas (densidad, precisión,
porcentaje de concentración), no con totales acumulados.

**¿Es realista una cadena de Markov para el fútbol?**
Es una simplificación útil para describir patrones de circulación. No predice jugadas: ignora
la posición, el tiempo, el rival y las pérdidas de balón (ver limitaciones).
