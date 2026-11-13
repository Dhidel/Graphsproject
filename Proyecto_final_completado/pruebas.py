"""Pruebas automaticas del proyecto.

Ejecutar:  python pruebas.py
No requiere librerias extra: cada prueba imprime OK o FALLA.
"""

import hashlib
import os
import subprocess
import sys

import matplotlib
import matplotlib.image
matplotlib.use("Agg")

import networkx as nx
import numpy as np

from comparacion import tabla_comparativa
from graphs import (ARCHIVOS, CARPETA, crear_grafo, markov_absorbente,
                    matriz_adyacencia, matriz_transicion, partidos_disponibles,
                    validar_jugador, validar_rival, validar_seleccion)

# Huellas SHA-256 de los CSV originales (antes de cualquier cambio)
HUELLAS_CSV = {
    "Argentina": "e4602f1e38be4aa417c6c00bb079b4f4e5ea1bcbd52c5479c859ad4896827079",
    "Brasil": "7570476cf4e10a7dd02faeca9923b5b9d620a2edd8a524927ed3faa463317917",
}

resultados = []


def prueba(nombre, condicion, detalle=""):
    resultados.append(bool(condicion))
    estado = "OK   " if condicion else "FALLA"
    print(f"[{estado}] {nombre}" + (f"  ({detalle})" if detalle else ""))


def lanza_error(funcion, *args):
    try:
        funcion(*args)
    except ValueError as error:
        return str(error)
    return None


# ------------------------------------------------------------------
print("\n== 1. Resultados de los preliminares (Argentina vs Arabia Saudita) ==")
G, total = crear_grafo("Argentina", "Saudi Arabia")
J = list(G.nodes())
O = "Nicolás Hernán Otamendi"
A = matriz_adyacencia(G)
A2, A3 = A @ A, A @ A @ A
P = matriz_transicion(G)

prueba("Otamendi grado de entrada = 12", G.in_degree(O) == 12)
prueba("Otamendi grado de salida = 11", G.out_degree(O) == 11)
prueba("Otamendi 84 pases realizados", G.out_degree(O, weight="peso") == 84)
prueba("Otamendi 80 pases recibidos", G.in_degree(O, weight="peso") == 80)
prueba("Orden: indice 0 = Papu Gómez, indice 3 = Messi",
       J[0] == "Alejandro Darío Gómez" and J[3] == "Lionel Andrés Messi Cuccittini")
prueba("A²[0,3] = 5", A2[0, 3] == 5, f"real {A2[0, 3]}")
prueba("A³[0,3] = 50", A3[0, 3] == 50, f"real {A3[0, 3]}")
ruta = nx.shortest_path(G, J[0], J[-1])
prueba("Ruta Gómez -> Molina -> Acuña",
       ruta == ["Alejandro Darío Gómez", "Nahuel Molina Lucero", "Marcos Javier Acuña"])
i_par = J.index("Leandro Daniel Paredes")
prueba("P(Gómez -> Paredes) = 0.30", np.isclose(P[0, i_par], 6 / 20), f"real {P[0, i_par]:.4f}")
P2 = P @ P
prueba("P²(Gómez -> Otamendi) ≈ 0.21", abs(P2[0, J.index(O)] - 0.2086) < 1e-3,
       f"real {P2[0, J.index(O)]:.4f}")

# Conteo independiente desde el CSV (sin NetworkX)
import pandas as pd
datos = pd.read_csv(ARCHIVOS["Argentina"])
pases = datos[(datos.oponente == "Saudi Arabia") & (datos.resultado == "Complete")]
prueba("Total de pases completados = conteo directo del CSV", total == len(pases) == 542)
prueba("Pesos = conteo directo del CSV (Otamendi -> Cuti Romero = 18)",
       G["Nicolás Hernán Otamendi"]["Cristian Gabriel Romero"]["peso"] ==
       ((pases.jugador_nombre == O) & (pases.receptor_nombre == "Cristian Gabriel Romero")).sum() == 18)

print("\n== 2. Matriz fundamental contra México (igual a los preliminares) ==")
GM, _ = crear_grafo("Argentina", "Mexico")
mex = markov_absorbente(GM, "Otamendi")
fila0 = [1.73, 0.29, 0.51, 0.96, 0.25, 0.92, 0.73, 0.65, 0.92, 0.51, 0.01, 0.1, 0.05, 0.1, 0.1]
ultima = [0.6, 0.51, 0.36, 0.61, 0.14, 0.9, 0.47, 0.36, 1.1, 0.47, 0.02, 0.07, 0.07, 0.32, 1.14]
N = mex["N"].to_numpy()
prueba("México: Otamendi es el unico absorbente", mex["absorbentes"] == [O])
prueba("México: primera fila de N igual al documento", np.allclose(N[0].round(2), fila0))
prueba("México: ultima fila de N igual al documento", np.allclose(N[-1].round(2), ultima))

print("\n== 3. Arabia Saudita: caso corregido (Julián Álvarez absorbente) ==")
ksa = markov_absorbente(G, "Otamendi")
prueba("Absorbentes = Otamendi y Julián Álvarez",
       ksa["absorbentes"] == [O, "Julián Álvarez"])
prueba("N existe (antes era singular)", ksa["valida"])
B = ksa["B"].to_numpy()
prueba("B: filas suman 1 y valores en [0,1]",
       np.allclose(B.sum(1), 1) and (B >= -1e-12).all() and (B <= 1 + 1e-12).all())
prueba("El modelo anterior (Álvarez dentro de Q) si era singular",
       np.isclose(np.linalg.det(np.eye(len(J) - 1) -
                                P[np.ix_([k for k in range(len(J)) if J[k] != O],
                                         [k for k in range(len(J)) if J[k] != O])]), 0))

# Verificacion independiente por simulacion (Monte Carlo) de B y t
rng = np.random.default_rng(0)
inicio = J.index("Alejandro Darío Gómez")
absorbentes = {J.index(a) for a in ksa["absorbentes"]}
llegadas, pasos_total, n_sim = 0, 0, 20000
for _ in range(n_sim):
    estado, pasos = inicio, 0
    while estado not in absorbentes:
        estado = rng.choice(len(J), p=P[estado])
        pasos += 1
    llegadas += estado == J.index(O)
    pasos_total += pasos
b_sim, t_sim = llegadas / n_sim, pasos_total / n_sim
prueba("Simulación: P(terminar en Otamendi desde Gómez) ≈ B",
       abs(b_sim - B[0, 0]) < 0.01, f"simulado {b_sim:.3f}, B = {B[0, 0]:.3f}")
prueba("Simulación: pases hasta absorción desde Gómez ≈ t",
       abs(t_sim - ksa["t"].iloc[0]) < 0.15, f"simulado {t_sim:.2f}, t = {ksa['t'].iloc[0]:.2f}")

print("\n== 4. Deteccion de clases cerradas (grafo de prueba) ==")
H = nx.DiGraph()
H.add_weighted_edges_from([("a", "b", 3), ("b", "a", 2), ("c", "a", 1), ("c", "d", 4),
                           ("d", "c", 1)], weight="peso")
res = markov_absorbente(H, "d")
prueba("Detecta la clase cerrada {a, b} y no invierte",
       not res["valida"] and res["clases_cerradas"] == [["a", "b"]])

print("\n== 5. Los 12 partidos: propiedades de A, P, N y B ==")
partidos = [(s, r) for s in ("Argentina", "Brasil") for r in partidos_disponibles(s)]
prueba("Hay 12 partidos (7 Argentina + 5 Brasil)", len(partidos) == 12)
for s, r in partidos:
    G, total = crear_grafo(s, r)
    A = matriz_adyacencia(G)
    P = matriz_transicion(G)
    W = nx.to_numpy_array(G, weight="peso")
    salida = W.sum(1)
    ok_P = all(np.allclose(P[i], W[i] / salida[i]) for i in range(len(W)) if salida[i] > 0)
    res = markov_absorbente(G, "Otamendi" if s == "Argentina" else "Marquinhos")
    Bm, Nm = res["B"].to_numpy(), res["N"].to_numpy()
    Q = res["Q"].to_numpy()
    t_solve = np.linalg.solve(np.eye(len(Q)) - Q, np.ones(len(Q)))
    checks = [
        set(np.unique(A)) <= {0, 1} and np.trace(A) == 0,
        (np.linalg.matrix_power(A, 2) == A @ A).all(),
        (np.linalg.matrix_power(A, 3) == A @ A @ A).all(),
        W.sum() == total,
        np.allclose(P.sum(1), 1) and (P >= 0).all() and (P <= 1).all(),
        ok_P,
        np.allclose(np.linalg.matrix_power(P, 2), P @ P),
        res["valida"] and res["radio_espectral"] < 1,
        np.allclose(Nm @ (np.eye(len(Q)) - Q), np.eye(len(Q))),
        np.allclose(res["t"].to_numpy(), t_solve),
        np.allclose(Bm.sum(1), 1) and (Bm >= -1e-12).all() and (Bm <= 1 + 1e-12).all(),
    ]
    prueba(f"{s} vs {r}: A, A², A³, P, P², N, t, B", all(checks),
           f"{sum(checks)}/{len(checks)} verificaciones")

tabla = tabla_comparativa()
prueba("Tabla comparativa con 12 filas", len(tabla) == 12)
prueba("Tabla: pases completados coinciden con los CSV",
       all(tabla["Pases completados"].iloc[k] == crear_grafo(s, r)[1]
           for k, (s, r) in enumerate(partidos)))

print("\n== 6. Entradas invalidas ==")
prueba("Seleccion inexistente -> mensaje claro",
       "no valida" in (lanza_error(validar_seleccion, "Uruguay") or ""))
prueba("'Brazil' y 'brasil' se aceptan",
       validar_seleccion("Brazil") == validar_seleccion("brasil") == "Brasil")
prueba("Rival inexistente -> mensaje claro",
       "Partidos disponibles" in (lanza_error(validar_rival, "Argentina", "Spain") or ""))
prueba("Rival en español o minusculas se acepta",
       validar_rival("Argentina", "arabia saudita") == "Saudi Arabia" and
       validar_rival("Argentina", "mexico") == "Mexico")
prueba("Jugador inexistente -> mensaje claro",
       "no participo" in (lanza_error(validar_jugador, GM, "Pelé") or ""))
prueba("Jugador por nombre corto ('messi')",
       validar_jugador(GM, "messi") == "Lionel Andrés Messi Cuccittini")

print("\n== 7. Menu interactivo con entradas invalidas (desde otra carpeta) ==")
entorno = dict(os.environ, MPLBACKEND="Agg", PYTHONIOENCODING="utf-8")
entrada = "abc\n9\n1\n1\n99\n1\n\n\n\nx\n\nn\n3\n"
proceso = subprocess.run([sys.executable, str(CARPETA / "main.py")], input=entrada,
                         capture_output=True, text=True, encoding="utf-8",
                         cwd=CARPETA.parent, env=entorno, timeout=600)
salida = proceso.stdout
prueba("El menu rechaza entradas no validas", salida.count("Entrada no valida") >= 4)
prueba("El menu analiza Argentina vs Arabia Saudita y termina sin errores",
       "Argentina vs Arabia Saudita" in salida and "Hasta luego" in salida
       and proceso.returncode == 0, proceso.stderr[-300:])

print("\n== 8. Graficas y archivos ==")
carpeta = CARPETA / "salidas" / "Argentina_vs_Arabia_Saudita"
for nombre in ("red_umbral_5.png", "red_completa.png", "grados.png"):
    archivo = carpeta / nombre
    if archivo.exists():
        alto, ancho = matplotlib.image.imread(archivo).shape[:2]
        prueba(f"{nombre} generado a 300 DPI", ancho > 3000, f"{ancho}x{alto} px")
    else:
        prueba(f"{nombre} generado", False)

for seleccion, huella in HUELLAS_CSV.items():
    real = hashlib.sha256(ARCHIVOS[seleccion].read_bytes()).hexdigest()
    prueba(f"CSV de {seleccion} sin modificar", real == huella)

print(f"\nResultado: {sum(resultados)}/{len(resultados)} pruebas correctas.")
sys.exit(0 if all(resultados) else 1)
