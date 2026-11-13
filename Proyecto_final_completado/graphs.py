"""Calculos del proyecto: grafo de pases, grados, matrices, rutas y Markov.

Todas las matrices usan el MISMO orden de jugadores: list(grafo.nodes()).
Las filas y columnas se muestran con el nombre de cada jugador para que
no haya confusion con los indices.
"""

import unicodedata
from pathlib import Path

import networkx as nx
import numpy as np
import pandas as pd

from nombres import FASES_ES, nombre_corto, rival_es

# Rutas relativas a este archivo: el programa funciona desde cualquier carpeta
CARPETA = Path(__file__).resolve().parent

ARCHIVOS = {
    "Argentina": CARPETA / "pases_argentina.csv",
    "Brasil": CARPETA / "pases_brasil.csv",
}

# Destino por defecto del modelo absorbente: un defensa central que jugo
# TODOS los partidos de su seleccion, para que los resultados sean comparables.
#  - Otamendi: 7/7 partidos de Argentina (destino usado en los preliminares).
#  - Marquinhos: 5/5 partidos de Brasil (el que mas pases recibe entre ellos).
DESTINO_POR_DEFECTO = {
    "Argentina": "Nicolás Hernán Otamendi",
    "Brasil": "Marcos Aoás Corrêa",
}

_cache_datos = {}


# ------------------------------------------------------------------
# Validacion de entradas
# ------------------------------------------------------------------
def _normalizar(texto):
    # minusculas y sin tildes, para comparar entradas del usuario
    texto = unicodedata.normalize("NFD", str(texto).strip().lower())
    return "".join(c for c in texto if unicodedata.category(c) != "Mn")


def validar_seleccion(seleccion):
    opciones = {"argentina": "Argentina", "brasil": "Brasil", "brazil": "Brasil"}
    clave = _normalizar(seleccion)
    if clave not in opciones:
        raise ValueError(
            f"Seleccion '{seleccion}' no valida. Opciones: Argentina o Brasil."
        )
    return opciones[clave]


def cargar_datos(seleccion):
    seleccion = validar_seleccion(seleccion)
    if seleccion not in _cache_datos:
        archivo = ARCHIVOS[seleccion]
        if not archivo.exists():
            raise FileNotFoundError(f"No se encontro el archivo de datos: {archivo}")
        _cache_datos[seleccion] = pd.read_csv(archivo)
    return _cache_datos[seleccion]


def partidos_disponibles(seleccion):
    # Rivales en orden cronologico (nombre en ingles, como en el CSV)
    datos = cargar_datos(seleccion)
    partidos = datos[["fecha", "oponente"]].drop_duplicates().sort_values("fecha")
    return list(partidos["oponente"])


def info_partido(seleccion, rival):
    datos = cargar_datos(seleccion)
    fila = datos[datos["oponente"] == rival].iloc[0]
    return {
        "fecha": fila["fecha"],
        "fase": FASES_ES.get(fila["fase"], fila["fase"]),
    }


def validar_rival(seleccion, rival):
    # Acepta el nombre en ingles (CSV) o en español: "Mexico", "México", "mexico"
    seleccion = validar_seleccion(seleccion)
    for opcion in partidos_disponibles(seleccion):
        if _normalizar(rival) in (_normalizar(opcion), _normalizar(rival_es(opcion))):
            return opcion
    disponibles = ", ".join(rival_es(r) for r in partidos_disponibles(seleccion))
    raise ValueError(
        f"{seleccion} no jugo contra '{rival}'. Partidos disponibles: {disponibles}."
    )


def validar_jugador(grafo, jugador):
    # Acepta nombre completo o nombre corto ("Messi", "otamendi")
    for nombre in grafo.nodes():
        if _normalizar(jugador) in (_normalizar(nombre), _normalizar(nombre_corto(nombre))):
            return nombre
    disponibles = ", ".join(nombre_corto(j) for j in grafo.nodes())
    raise ValueError(
        f"El jugador '{jugador}' no participo en este partido. Jugadores: {disponibles}."
    )


# ------------------------------------------------------------------
# Construccion del grafo (codigo original de Dhidel, con validacion)
# ------------------------------------------------------------------
def crear_grafo(seleccion, rival):
    seleccion = validar_seleccion(seleccion)
    rival = validar_rival(seleccion, rival)
    datos = cargar_datos(seleccion)

    # Solo pases completados de ese partido (un rival = un partido en los CSV)
    pases = datos[
        (datos["oponente"] == rival) &
        (datos["resultado"] == "Complete")
    ]

    # Peso de la arista = cantidad de pases completados de i hacia j
    conteo = (
        pases.groupby(["jugador_nombre", "receptor_nombre"])
        .size()
        .reset_index(name="peso")
    )

    grafo = nx.from_pandas_edgelist(
        conteo,
        source="jugador_nombre",
        target="receptor_nombre",
        edge_attr="peso",
        create_using=nx.DiGraph()
    )

    return grafo, len(pases)


def tabla_matriz(matriz, filas, columnas=None):
    # Convierte una matriz de numpy en tabla con nombres de jugadores
    columnas = filas if columnas is None else columnas
    return pd.DataFrame(
        matriz,
        index=[nombre_corto(j) for j in filas],
        columns=[nombre_corto(j) for j in columnas],
    )


def _imprimir(titulo, tabla, decimales=None):
    print(f"\n{titulo}")
    if decimales is not None:
        tabla = tabla.round(decimales)
    with pd.option_context("display.width", 250, "display.max_columns", None,
                           "display.max_rows", None):
        print(tabla)


# ------------------------------------------------------------------
# Estadisticas y grados
# ------------------------------------------------------------------
def tabla_grados(grafo):
    jugadores = list(grafo.nodes())
    return pd.DataFrame({
        "Jugador": [nombre_corto(j) for j in jugadores],
        # grado ponderado = total de pases completados
        "Pases realizados": [grafo.out_degree(j, weight="peso") for j in jugadores],
        "Pases recibidos": [grafo.in_degree(j, weight="peso") for j in jugadores],
        # grado sin peso = cantidad de compañeros diferentes
        "Grado entrada": [grafo.in_degree(j) for j in jugadores],
        "Grado salida": [grafo.out_degree(j) for j in jugadores],
    })


def estadisticas(grafo, total):
    realizados = dict(grafo.out_degree(weight="peso"))
    recibidos = dict(grafo.in_degree(weight="peso"))

    jugador_mas_pases = max(realizados, key=realizados.get)
    jugador_mas_recibidos = max(recibidos, key=recibidos.get)
    conexion = max(grafo.edges(data=True), key=lambda x: x[2]["peso"])

    print("\n--- ESTADISTICAS ---")
    print("Total de pases completados:", total)
    print("Jugadores (vertices):", grafo.number_of_nodes())
    print("Conexiones dirigidas (aristas):", grafo.number_of_edges())
    print(f"Densidad: {nx.density(grafo):.3f}")
    print("Mas pases realizados:", nombre_corto(jugador_mas_pases),
          realizados[jugador_mas_pases])
    print("Mas pases recibidos:", nombre_corto(jugador_mas_recibidos),
          recibidos[jugador_mas_recibidos])
    print("Conexion mas frecuente:", nombre_corto(conexion[0]), "->",
          nombre_corto(conexion[1]), conexion[2]["peso"])

    print("\n--- GRADOS ---")
    print("Grado = compañeros diferentes. Pases = grado ponderado (total de pases).")
    with pd.option_context("display.width", 200):
        print(tabla_grados(grafo).to_string(index=False))


# ------------------------------------------------------------------
# Matriz de adyacencia y potencias
# ------------------------------------------------------------------
def matriz_adyacencia(grafo):
    jugadores = list(grafo.nodes())
    # weight=None -> matriz binaria (1 si hay al menos un pase de i a j)
    return nx.to_numpy_array(grafo, nodelist=jugadores, weight=None, dtype=int)


def matrices(grafo):
    jugadores = list(grafo.nodes())
    A = matriz_adyacencia(grafo)
    A2 = np.linalg.matrix_power(A, 2)   # producto matricial A @ A
    A3 = np.linalg.matrix_power(A, 3)   # A @ A @ A

    print("\n--- MATRIZ DE ADYACENCIA ---")
    print("Orden de jugadores (igual en todas las matrices):")
    for i, jugador in enumerate(jugadores):
        print(i, nombre_corto(jugador))

    _imprimir("A (1 = existe al menos un pase de la fila hacia la columna):",
              tabla_matriz(A, jugadores))
    _imprimir("A^2[i,j] = recorridos dirigidos de 2 conexiones de i a j:",
              tabla_matriz(A2, jugadores))
    _imprimir("A^3[i,j] = recorridos dirigidos de 3 conexiones de i a j:",
              tabla_matriz(A3, jugadores))
    print("Nota: son recorridos POSIBLES en el grafo (pueden repetir jugadores),")
    print("no secuencias de pases que hayan ocurrido en el partido.")

    return A, A2, A3


# ------------------------------------------------------------------
# Rutas
# ------------------------------------------------------------------
def rutas(grafo, origen=None, destino=None):
    jugadores = list(grafo.nodes())

    # Ejemplo por defecto: primer y ultimo jugador del orden de la matriz
    origen = jugadores[0] if origen is None else validar_jugador(grafo, origen)
    destino = jugadores[-1] if destino is None else validar_jugador(grafo, destino)

    print("\n--- RUTAS ---")
    print("Origen:", nombre_corto(origen))
    print("Destino:", nombre_corto(destino))

    if origen == destino:
        print("El origen y el destino son el mismo jugador.")
        return None

    if not nx.has_path(grafo, origen, destino):
        print("No existe una ruta dirigida entre estos jugadores.")
        return None

    # Ruta mas corta = menor cantidad de conexiones (no usa pesos)
    ruta = nx.shortest_path(grafo, origen, destino)
    largo = len(ruta) - 1
    cantidad = len(list(nx.all_shortest_paths(grafo, origen, destino)))

    print("Ruta mas corta:", " -> ".join(nombre_corto(j) for j in ruta))
    print("Cantidad de conexiones:", largo)
    print("Rutas distintas con ese largo minimo:", cantidad)

    # Relacion con las potencias de A
    A = matriz_adyacencia(grafo)
    i, j = jugadores.index(origen), jugadores.index(destino)
    Ak = np.linalg.matrix_power(A, largo)
    print(f"Comprobacion: A^{largo}[{i},{j}] = {Ak[i, j]} recorridos de {largo} "
          f"conexiones, y A^k[{i},{j}] = 0 para todo k < {largo}.")
    print("Es la ruta con menos conexiones, no la mas probable ni una jugada real.")
    return ruta


# ------------------------------------------------------------------
# Cadenas de Markov
# ------------------------------------------------------------------
def matriz_transicion(grafo):
    jugadores = list(grafo.nodes())
    matriz = nx.to_numpy_array(grafo, nodelist=jugadores, weight="peso")

    # P[i,j] = pases completados de i a j / total de pases completados de i
    for i in range(len(matriz)):
        total = matriz[i].sum()
        if total > 0:
            matriz[i] = matriz[i] / total
        else:
            # Jugador sin pases completados (sumidero): el balon "se queda"
            # con el. Se modela como estado absorbente P[i,i] = 1 para que
            # la fila sume 1.
            matriz[i, i] = 1

    return matriz


def markov(grafo):
    jugadores = list(grafo.nodes())
    P = matriz_transicion(grafo)
    P2 = np.linalg.matrix_power(P, 2)

    print("\n--- MATRIZ DE MARKOV ---")
    sumideros = [j for j in jugadores if grafo.out_degree(j) == 0]
    if sumideros:
        print("Jugadores sin pases completados (P[i,i] = 1, estado absorbente):",
              ", ".join(nombre_corto(j) for j in sumideros))
    _imprimir("P[i,j] = probabilidad de que el siguiente pase completado de i vaya a j:",
              tabla_matriz(P, jugadores), 2)
    _imprimir("P^2[i,j] = probabilidad de estar en j despues de 2 pases completados:",
              tabla_matriz(P2, jugadores), 2)
    print("Las probabilidades estan condicionadas a que el pase se complete.")

    return P, P2


# ------------------------------------------------------------------
# Markov absorbente y matriz fundamental
# ------------------------------------------------------------------
def clases_cerradas(grafo, jugadores):
    # Clases cerradas del subgrafo: componentes fuertemente conexas
    # de las que no sale ninguna conexion
    sub = grafo.subgraph(jugadores)
    condensado = nx.condensation(sub)
    return [
        sorted(condensado.nodes[c]["members"])
        for c in condensado.nodes()
        if condensado.out_degree(c) == 0
    ]


def markov_absorbente(grafo, destino):
    """Construye Q, R, N, t y B. Devuelve un diccionario con los resultados.

    Estados absorbentes: el destino + los sumideros (jugadores sin pases
    completados). Todos los demas son transitorios.
    """
    jugadores = list(grafo.nodes())
    destino = validar_jugador(grafo, destino)
    P = matriz_transicion(grafo)

    sumideros = [j for j in jugadores if grafo.out_degree(j) == 0 and j != destino]
    absorbentes = [destino] + sumideros
    transitorios = [j for j in jugadores if j not in absorbentes]

    resultado = {
        "destino": destino,
        "absorbentes": absorbentes,
        "transitorios": transitorios,
        "valida": False,
    }

    # Condicion para que exista (I - Q)^-1: desde cada estado transitorio
    # se debe poder llegar a algun estado absorbente. Si no, hay una clase
    # cerrada de transitorios, Q tiene valor propio 1 e I - Q es singular.
    alcanzan = set()
    for a in absorbentes:
        alcanzan |= nx.ancestors(grafo, a)
    atrapados = [j for j in transitorios if j not in alcanzan]

    if atrapados:
        resultado["clases_cerradas"] = clases_cerradas(grafo, atrapados)
        return resultado

    t_idx = [jugadores.index(j) for j in transitorios]
    a_idx = [jugadores.index(j) for j in absorbentes]

    Q = P[np.ix_(t_idx, t_idx)]   # transitorio -> transitorio
    R = P[np.ix_(t_idx, a_idx)]   # transitorio -> absorbente
    I = np.eye(len(Q))

    N = np.linalg.inv(I - Q)          # matriz fundamental
    t = N @ np.ones(len(Q))           # pases esperados hasta la absorcion
    B = N @ R                         # probabilidades de absorcion

    # Verificaciones numericas
    radio = max(abs(np.linalg.eigvals(Q)))
    assert radio < 1, "El radio espectral de Q debe ser menor que 1"
    assert np.allclose((I - Q) @ N, I), "N no es la inversa de I - Q"
    assert np.allclose(B.sum(axis=1), 1), "Las filas de B deben sumar 1"
    assert (B >= -1e-12).all() and (B <= 1 + 1e-12).all()

    resultado.update({
        "valida": True,
        "Q": tabla_matriz(Q, transitorios),
        "R": tabla_matriz(R, transitorios, absorbentes),
        "N": tabla_matriz(N, transitorios),
        "t": pd.Series(t, index=[nombre_corto(j) for j in transitorios],
                       name="Pases esperados"),
        "B": tabla_matriz(B, transitorios, absorbentes),
        "radio_espectral": radio,
        "condicion": np.linalg.cond(I - Q),
    })
    return resultado


def matriz_inversa(grafo, destino=None, seleccion=None):
    if destino is None:
        destino = destino_por_defecto(grafo, seleccion)

    res = markov_absorbente(grafo, destino)

    print("\n--- MARKOV ABSORBENTE: N = (I - Q)^-1 ---")
    print("Jugador destino:", nombre_corto(res["destino"]))
    print("Estados absorbentes:", ", ".join(nombre_corto(j) for j in res["absorbentes"]))
    if len(res["absorbentes"]) > 1:
        print("  (ademas del destino, los jugadores que no completaron ningun pase")
        print("   tambien son absorbentes: si el balon llega a ellos, la cadena termina)")

    if not res["valida"]:
        print("No se puede calcular N: hay estados transitorios que no pueden")
        print("llegar a ningun estado absorbente (clases cerradas):")
        for clase in res["clases_cerradas"]:
            print("  ", ", ".join(nombre_corto(j) for j in clase))
        print("En ese caso Q tiene valor propio 1 y la matriz I - Q es singular.")
        return res

    print(f"Condicion verificada: todos los transitorios alcanzan un absorbente "
          f"(radio espectral de Q = {res['radio_espectral']:.3f} < 1).")

    _imprimir("N[i,j] = numero esperado de veces que j tiene el balon, empezando en i, "
              "antes de la absorcion:", res["N"], 2)
    _imprimir("t = N·1 = pases esperados hasta llegar a CUALQUIER estado absorbente:",
              res["t"], 2)
    _imprimir("B = N·R = probabilidad de terminar en cada estado absorbente:",
              res["B"], 3)

    if len(res["absorbentes"]) > 1:
        print("Importante: como hay mas de un absorbente, t NO es el tiempo esperado")
        print("hasta llegar especificamente al destino; B indica la probabilidad")
        print("de que el balon termine en el destino o en otro absorbente.")
    else:
        print("Como el destino es el unico absorbente, t = pases esperados hasta")
        print("que el balon llegue al destino (B es 1 en todas las filas).")
    print("N no calcula rutas: resume visitas esperadas segun las probabilidades de P.")
    return res


def destino_por_defecto(grafo, seleccion=None):
    # Usa el central fijo de cada seleccion; si no jugo, el que mas pases recibe
    if seleccion is not None:
        candidato = DESTINO_POR_DEFECTO[validar_seleccion(seleccion)]
        if candidato in grafo:
            return candidato
    recibidos = dict(grafo.in_degree(weight="peso"))
    return max(recibidos, key=recibidos.get)


# ------------------------------------------------------------------
# Analisis completo de un partido
# ------------------------------------------------------------------
def analizar_partido(seleccion, rival, origen=None, destino=None,
                     destino_markov=None, umbral=5, graficas=True, mostrar=False):
    # origen/destino: jugadores para la ruta mas corta
    # destino_markov: estado absorbente principal (por defecto Otamendi/Marquinhos)
    seleccion = validar_seleccion(seleccion)
    rival = validar_rival(seleccion, rival)
    grafo, total = crear_grafo(seleccion, rival)
    info = info_partido(seleccion, rival)

    print("\n============================")
    print(seleccion, "vs", rival_es(rival), f"({info['fase']}, {info['fecha']})")
    print("============================")

    estadisticas(grafo, total)
    matrices(grafo)
    rutas(grafo, origen, destino)
    markov(grafo)
    matriz_inversa(grafo, destino_markov, seleccion)

    archivos = []
    if graficas:
        # importacion local: los calculos no dependen de matplotlib
        from graficas import graficar, graficar_grados
        archivos.append(graficar(grafo, seleccion, rival, umbral, mostrar))
        if umbral > 1:
            archivos.append(graficar(grafo, seleccion, rival, 1, mostrar))
        archivos.append(graficar_grados(grafo, seleccion, rival, mostrar))
        print("\nGraficas guardadas:")
        for archivo in archivos:
            print("  ", archivo)
    return grafo
