"""Comparacion de los 12 partidos y de Argentina vs Brasil."""

import networkx as nx
import pandas as pd

from graphs import (CARPETA, DESTINO_POR_DEFECTO, cargar_datos, crear_grafo,
                    info_partido, markov_absorbente, partidos_disponibles)
from nombres import nombre_corto, rival_es

SELECCIONES = ["Argentina", "Brasil"]


def metricas_partido(seleccion, rival):
    grafo, total = crear_grafo(seleccion, rival)
    datos = cargar_datos(seleccion)
    intentados = (datos["oponente"] == rival).sum()
    info = info_partido(seleccion, rival)

    n = grafo.number_of_nodes()
    m = grafo.number_of_edges()
    realizados = dict(grafo.out_degree(weight="peso"))
    recibidos = dict(grafo.in_degree(weight="peso"))
    max_r = max(realizados, key=realizados.get)
    max_c = max(recibidos, key=recibidos.get)

    pesos = sorted((d["peso"] for _, _, d in grafo.edges(data=True)), reverse=True)
    a, b, d = max(grafo.edges(data=True), key=lambda x: x[2]["peso"])

    # Jugadores destacados: mayor participacion (pases realizados + recibidos)
    participacion = {j: realizados[j] + recibidos[j] for j in grafo.nodes()}
    top3 = sorted(participacion, key=participacion.get, reverse=True)[:3]

    # Markov absorbente con destino fijo por seleccion
    destino = DESTINO_POR_DEFECTO[seleccion]
    absorb = markov_absorbente(grafo, destino)
    extra = [nombre_corto(j) for j in absorb["absorbentes"][1:]]

    return {
        "Selección": seleccion,
        "Rival": rival_es(rival),
        "Fase": info["fase"],
        "Fecha": info["fecha"],
        "Jugadores": n,
        "Pases completados": total,
        "Pases intentados": int(intentados),
        "Precisión de pase (%)": round(100 * total / intentados, 1),
        "Conexiones": m,
        "Densidad": round(nx.density(grafo), 3),
        # En un digrafo la suma de grados de entrada = suma de grados de salida = m,
        # por eso el promedio de entrada y el de salida son iguales (m / n).
        "Grado medio entrada": round(sum(d for _, d in grafo.in_degree()) / n, 2),
        "Grado medio salida": round(sum(d for _, d in grafo.out_degree()) / n, 2),
        "Grado medio": round(m / n, 2),
        "Pases por jugador": round(total / n, 1),
        "Más pases realizados": f"{nombre_corto(max_r)} ({realizados[max_r]})",
        "Más pases recibidos": f"{nombre_corto(max_c)} ({recibidos[max_c]})",
        "Conexión más frecuente": f"{nombre_corto(a)} → {nombre_corto(b)} ({d['peso']})",
        "Concentración top-5 (%)": round(100 * sum(pesos[:5]) / total, 1),
        "Jugadores destacados": ", ".join(nombre_corto(j) for j in top3),
        "Destino Markov": nombre_corto(destino),
        "Otros absorbentes": ", ".join(extra) if extra else "—",
        "t medio": round(absorb["t"].mean(), 2) if absorb["valida"] else None,
    }


def tabla_comparativa():
    filas = []
    for seleccion in SELECCIONES:
        for rival in partidos_disponibles(seleccion):
            filas.append(metricas_partido(seleccion, rival))
    return pd.DataFrame(filas)


def comparar_selecciones(tabla):
    """Promedio y desviacion estandar POR PARTIDO (Argentina 7, Brasil 5)."""
    columnas = ["Jugadores", "Pases completados", "Precisión de pase (%)",
                "Conexiones", "Densidad", "Grado medio", "Pases por jugador",
                "Concentración top-5 (%)"]
    resumen = tabla.groupby("Selección")[columnas].agg(["mean", "std"]).round(2)
    resumen.insert(0, ("Partidos", "n"), tabla.groupby("Selección").size())
    return resumen


def comparar_t_medio(tabla):
    """t medio solo es comparable entre partidos con el mismo destino y
    sin absorbentes adicionales (misma estructura del modelo)."""
    comparables = tabla[tabla["Otros absorbentes"] == "—"]
    return comparables.groupby(["Selección", "Destino Markov"])["t medio"].agg(
        ["count", "mean", "std", "min", "max"]).round(2)


def imprimir_comparacion(tabla=None, graficas=True, mostrar=False):
    if tabla is None:
        tabla = tabla_comparativa()

    with pd.option_context("display.width", 250, "display.max_columns", None,
                           "display.max_colwidth", 60):
        print("\n=== TABLA COMPARATIVA DE LOS 12 PARTIDOS ===")
        print(tabla[["Selección", "Rival", "Fase", "Jugadores", "Pases completados",
                     "Precisión de pase (%)", "Conexiones", "Densidad",
                     "Grado medio entrada", "Grado medio salida"]].to_string(index=False))
        print()
        print(tabla[["Selección", "Rival", "Más pases realizados", "Más pases recibidos",
                     "Conexión más frecuente", "Concentración top-5 (%)"]].to_string(index=False))
        print()
        print(tabla[["Selección", "Rival", "Jugadores destacados", "Destino Markov",
                     "Otros absorbentes", "t medio"]].to_string(index=False))

        print("\n=== ARGENTINA VS BRASIL (promedio por partido ± desviación) ===")
        print(comparar_selecciones(tabla))

        print("\n=== t medio (pases esperados hasta la absorción) ===")
        print("Solo partidos con un unico absorbente (el destino). El destino es")
        print("distinto en cada seleccion (Otamendi / Marquinhos), por eso t se")
        print("compara entre partidos de la MISMA seleccion, no entre selecciones.")
        print(comparar_t_medio(tabla))

    archivos = []
    if graficas:
        from graficas import graficar_comparacion
        archivos = graficar_comparacion(tabla, CARPETA / "salidas" / "comparacion", mostrar)
        print("\nGraficas guardadas:")
        for archivo in archivos:
            print("  ", archivo)
    return tabla
