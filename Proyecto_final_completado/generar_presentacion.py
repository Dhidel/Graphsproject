"""Genera el material de la carpeta Presentacion (graficas, tablas y matrices).

Ejecutar:  python generar_presentacion.py
El archivo Resultados_presentacion.md se escribio a mano a partir de estos datos.
"""

import numpy as np

from comparacion import comparar_selecciones, tabla_comparativa
from graficas import graficar, graficar_comparacion, graficar_grados, mapa_calor
from graphs import (CARPETA, crear_grafo, markov_absorbente, matriz_adyacencia,
                    matriz_transicion, tabla_matriz)

SALIDA = CARPETA / "Presentacion"
GRAFICAS = SALIDA / "graficas"


def tabla_md(tabla, decimales=2, indice=True):
    """Tabla en formato Markdown (sin dependencias extra)."""
    tabla = tabla.round(decimales)
    columnas = ([""] if indice else []) + [str(c) for c in tabla.columns]
    lineas = ["| " + " | ".join(columnas) + " |",
              "|" + "---|" * len(columnas)]
    for nombre, fila in tabla.iterrows():
        valores = [str(v) for v in fila]
        if indice:
            valores = [f"**{nombre}**"] + valores
        lineas.append("| " + " | ".join(valores) + " |")
    return "\n".join(lineas)


def main():
    GRAFICAS.mkdir(parents=True, exist_ok=True)

    # --- Redes de pases y grados ---
    partidos = [
        ("Argentina", "Saudi Arabia", "arg_arabia_saudita"),
        ("Argentina", "Mexico", "arg_mexico"),
        ("Argentina", "France", "arg_francia_final"),
        ("Brasil", "Serbia", "bra_serbia"),
        ("Brasil", "Switzerland", "bra_suiza"),
    ]
    for seleccion, rival, nombre in partidos:
        grafo, _ = crear_grafo(seleccion, rival)
        graficar(grafo, seleccion, rival, 5, archivo=GRAFICAS / f"red_{nombre}.png")
        graficar_grados(grafo, seleccion, rival, archivo=GRAFICAS / f"grados_{nombre}.png")
    grafo, _ = crear_grafo("Argentina", "Saudi Arabia")
    graficar(grafo, "Argentina", "Saudi Arabia", 1,
             archivo=GRAFICAS / "red_arg_arabia_saudita_completa.png")

    # --- Tabla y graficas comparativas ---
    tabla = tabla_comparativa()
    graficar_comparacion(tabla, GRAFICAS)
    tabla.to_csv(SALIDA / "tabla_12_partidos.csv", index=False, encoding="utf-8-sig")
    resumen = comparar_selecciones(tabla)
    resumen.columns = [f"{a} ({'promedio' if b == 'mean' else 'desv.' if b == 'std' else b})"
                       for a, b in resumen.columns]
    with open(SALIDA / "tabla_12_partidos.md", "w", encoding="utf-8") as f:
        f.write("# Tabla comparativa de los 12 partidos\n\n")
        f.write("Generada por `generar_presentacion.py` a partir de los CSV.\n\n")
        f.write("## Estructura del grafo\n\n")
        f.write(tabla_md(tabla[["Selección", "Rival", "Fase", "Jugadores",
                                "Pases completados", "Pases intentados",
                                "Precisión de pase (%)", "Conexiones", "Densidad",
                                "Grado medio entrada", "Grado medio salida",
                                "Pases por jugador", "Concentración top-5 (%)"]],
                         indice=False))
        f.write("\n\n## Jugadores\n\n")
        f.write(tabla_md(tabla[["Selección", "Rival", "Más pases realizados",
                                "Más pases recibidos", "Conexión más frecuente",
                                "Jugadores destacados"]], indice=False))
        f.write("\n\n## Markov absorbente (destino fijo por selección)\n\n")
        f.write(tabla_md(tabla[["Selección", "Rival", "Destino Markov",
                                "Otros absorbentes", "t medio"]], indice=False))
        f.write("\n\n## Argentina vs Brasil (promedio por partido)\n\n")
        f.write(tabla_md(resumen))
        f.write("\n")

    # --- Matrices de ejemplo con nombres ---
    grafo, _ = crear_grafo("Argentina", "Saudi Arabia")
    jugadores = list(grafo.nodes())
    A = matriz_adyacencia(grafo)
    P = matriz_transicion(grafo)
    tablas = {
        "A": tabla_matriz(A, jugadores),
        "A2": tabla_matriz(np.linalg.matrix_power(A, 2), jugadores),
        "A3": tabla_matriz(np.linalg.matrix_power(A, 3), jugadores),
        "P": tabla_matriz(P, jugadores),
        "P2": tabla_matriz(np.linalg.matrix_power(P, 2), jugadores),
    }
    ksa = markov_absorbente(grafo, "Otamendi")
    grafo_mex, _ = crear_grafo("Argentina", "Mexico")
    mex = markov_absorbente(grafo_mex, "Otamendi")

    sub = "Argentina vs Arabia Saudita"
    mapa_calor(tablas["A"], "Matriz de adyacencia A", GRAFICAS / "matriz_A_arabia.png",
               subtitulo=sub + " · 1 = existe al menos un pase de la fila a la columna")
    mapa_calor(tablas["A2"], "A² = A·A: recorridos de 2 conexiones",
               GRAFICAS / "matriz_A2_arabia.png", subtitulo=sub)
    mapa_calor(tablas["P"], "Matriz de transición P", GRAFICAS / "matriz_P_arabia.png", 2,
               subtitulo=sub + " · cada fila suma 1")
    mapa_calor(tablas["P2"], "P²: probabilidades después de 2 pases",
               GRAFICAS / "matriz_P2_arabia.png", 2, subtitulo=sub)
    mapa_calor(mex["N"], "Matriz fundamental N = (I − Q)⁻¹ (destino: Otamendi)",
               GRAFICAS / "matriz_N_mexico.png", 2, subtitulo="Argentina vs México")
    mapa_calor(ksa["B"], "B = N·R: probabilidad de absorción",
               GRAFICAS / "matriz_B_arabia.png", 2,
               subtitulo=sub + " · absorbentes: Otamendi y Julián Álvarez")

    with open(SALIDA / "Matrices_ejemplo.md", "w", encoding="utf-8") as f:
        f.write("# Matrices de ejemplo con nombres de jugadores\n\n")
        f.write("Generado por `generar_presentacion.py`. Filas = jugador que da el pase "
                "(i), columnas = jugador que lo recibe (j). El orden de jugadores es el "
                "mismo en A, A², A³, P y P².\n\n")
        f.write("## Argentina vs Arabia Saudita\n\n")
        descripciones = {
            "A": "A — adyacencia binaria",
            "A2": "A² — recorridos dirigidos de 2 conexiones",
            "A3": "A³ — recorridos dirigidos de 3 conexiones",
            "P": "P — matriz de transición (Julián Álvarez: P[i,i] = 1, sin pases completados)",
            "P2": "P² — probabilidades después de 2 transiciones",
        }
        for clave, titulo in descripciones.items():
            f.write(f"### {titulo}\n\n{tabla_md(tablas[clave])}\n\n")
        f.write("### Markov absorbente (destino Otamendi; Julián Álvarez también es absorbente)\n\n")
        f.write(f"N = (I − Q)⁻¹\n\n{tabla_md(ksa['N'])}\n\n")
        f.write(f"t = N·1 (pases esperados hasta llegar a cualquier absorbente)\n\n"
                f"{tabla_md(ksa['t'].to_frame())}\n\n")
        f.write(f"B = N·R (probabilidad de absorción)\n\n{tabla_md(ksa['B'], 3)}\n\n")
        f.write("## Argentina vs México (destino Otamendi, único absorbente)\n\n")
        f.write(f"N = (I − Q)⁻¹\n\n{tabla_md(mex['N'])}\n\n")
        f.write(f"t = N·1 (pases esperados hasta llegar a Otamendi)\n\n"
                f"{tabla_md(mex['t'].to_frame())}\n")

    print("Material generado en", SALIDA)


if __name__ == "__main__":
    main()
