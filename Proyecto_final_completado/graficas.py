"""Graficas del proyecto. Todas se guardan a 300 DPI en la carpeta 'salidas'."""

import unicodedata

import matplotlib.pyplot as plt
import networkx as nx
import numpy as np
from matplotlib.lines import Line2D

from graphs import CARPETA, info_partido
from nombres import nombre_corto, rival_es

DPI = 300

# Colores (paleta validada para daltonismo)
COLOR_SELECCION = {"Argentina": "#2a78d6", "Brasil": "#eb6834"}
COLOR_ENTRADA = "#1baf7a"
COLOR_SALIDA = "#6250d6"
TINTA = "#0b0b0b"
TINTA_SECUNDARIA = "#52514e"
REJILLA = "#e4e3df"
AZULES = ["#fcfcfb", "#cde2fb", "#9ec5f4", "#6da7ec", "#3987e5",
          "#256abf", "#184f95", "#0d366b"]

plt.rcParams.update({
    "font.size": 11,
    "axes.edgecolor": TINTA_SECUNDARIA,
    "axes.labelcolor": TINTA,
    "xtick.color": TINTA_SECUNDARIA,
    "ytick.color": TINTA_SECUNDARIA,
    "axes.spines.top": False,
    "axes.spines.right": False,
    "figure.facecolor": "white",
})


def _sin_tildes(texto):
    texto = unicodedata.normalize("NFD", texto)
    return "".join(c for c in texto if unicodedata.category(c) != "Mn").replace(" ", "_")


def carpeta_partido(seleccion, rival):
    # Una carpeta por partido: no se sobrescriben archivos de otros partidos
    carpeta = CARPETA / "salidas" / f"{seleccion}_vs_{_sin_tildes(rival_es(rival))}"
    carpeta.mkdir(parents=True, exist_ok=True)
    return carpeta


def _guardar(fig, archivo, mostrar):
    fig.savefig(archivo, dpi=DPI, bbox_inches="tight")
    if mostrar:
        plt.show()
    plt.close(fig)
    return archivo


def _tamano_nodo(pases):
    # Area del nodo proporcional a los pases realizados
    return 150 + 22 * pases


def _grosor(peso):
    return 0.6 + peso / 3


# ------------------------------------------------------------------
# Red de pases
# ------------------------------------------------------------------
def graficar(grafo, seleccion, rival, umbral=5, mostrar=False, archivo=None):
    """Red de pases. umbral=1 dibuja el grafo completo sin filtros."""
    conexiones = [(a, b) for a, b, d in grafo.edges(data=True) if d["peso"] >= umbral]
    filtrado = grafo.edge_subgraph(conexiones).copy()
    ocultos = sorted(set(grafo.nodes()) - set(filtrado.nodes()), key=nombre_corto)

    # Posiciones calculadas con el grafo COMPLETO: los jugadores quedan en el
    # mismo lugar en la version filtrada y en la completa
    # (k grande separa los nodos y evita que las etiquetas se encimen)
    pos = nx.spring_layout(grafo.to_undirected(), seed=42,
                           k=3 / np.sqrt(grafo.number_of_nodes()), iterations=300)

    nodos = list(filtrado.nodes())
    tamanos = [_tamano_nodo(grafo.out_degree(j, weight="peso")) for j in nodos]
    grosores = [_grosor(d["peso"]) for _, _, d in filtrado.edges(data=True)]
    color = COLOR_SELECCION[seleccion]

    fig, ax = plt.subplots(figsize=(13, 10.5))

    nx.draw_networkx_edges(
        filtrado, pos, ax=ax,
        nodelist=nodos, node_size=tamanos,
        width=grosores, edge_color=TINTA_SECUNDARIA, alpha=0.55,
        arrows=True, arrowstyle="-|>", arrowsize=16,
        connectionstyle="arc3,rad=0.14",
        min_source_margin=3, min_target_margin=6,
    )
    nx.draw_networkx_nodes(
        filtrado, pos, ax=ax, nodelist=nodos, node_size=tamanos,
        node_color=color, edgecolors="white", linewidths=2,
    )

    # Etiqueta debajo de cada nodo, con fondo blanco para que no se tape
    for jugador, s in zip(nodos, tamanos):
        ax.annotate(
            nombre_corto(jugador), pos[jugador],
            xytext=(0, -(np.sqrt(s) / 2 + 3)), textcoords="offset points",
            ha="center", va="top", fontsize=11, color=TINTA, fontweight="bold",
            bbox=dict(boxstyle="round,pad=0.2", fc="white", ec="none", alpha=0.85),
            zorder=5,
        )

    info = info_partido(seleccion, rival)
    if umbral > 1:
        tipo = f"conexiones con {umbral} o más pases"
        nota = (f"Filtro: se muestran {len(conexiones)} de {grafo.number_of_edges()} "
                f"conexiones (las de {umbral} o más pases completados).")
        if ocultos:
            nota += "\nJugadores sin conexiones que superen el filtro: " + \
                ", ".join(nombre_corto(j) for j in ocultos) + "."
    else:
        tipo = "grafo completo"
        nota = (f"Sin filtro: {grafo.number_of_edges()} conexiones dirigidas entre "
                f"{grafo.number_of_nodes()} jugadores.")

    ax.set_title(f"{seleccion} vs {rival_es(rival)} — Red de pases ({tipo})\n"
                 f"{info['fase']}, {info['fecha']}",
                 fontsize=16, color=TINTA, loc="left", fontweight="bold")
    fig.text(0.01, 0.01,
             "Flecha A → B: pases completados de A hacia B. "
             "Tamaño del nodo: pases realizados. Grosor: cantidad de pases.\n" + nota,
             fontsize=10, color=TINTA_SECUNDARIA, ha="left", va="bottom")

    # Leyendas de tamaño y grosor
    ley_nodos = [plt.scatter([], [], s=_tamano_nodo(p), color=color,
                             edgecolors="white", label=f"{p} pases")
                 for p in (20, 50, 100)]
    ley1 = ax.legend(handles=ley_nodos, title="Pases realizados", loc="upper right",
                     labelspacing=3.2, borderpad=1.4, handletextpad=1.6, frameon=False,
                     bbox_to_anchor=(1.12, 1.0))
    ax.add_artist(ley1)
    ley_aristas = [Line2D([0], [0], color=TINTA_SECUNDARIA, alpha=0.7,
                          lw=_grosor(p), label=f"{p} pase" + ("s" if p > 1 else ""))
                   for p in (umbral if umbral > 1 else 1, 10, 20)]
    ax.legend(handles=ley_aristas, title="Pases entre dos jugadores",
              loc="lower right", frameon=False, bbox_to_anchor=(1.12, 0.12))

    ax.axis("off")
    fig.subplots_adjust(left=0.02, right=0.88, top=0.9, bottom=0.08)

    if archivo is None:
        nombre = "red_completa.png" if umbral <= 1 else f"red_umbral_{umbral}.png"
        archivo = carpeta_partido(seleccion, rival) / nombre
    return _guardar(fig, archivo, mostrar)


# ------------------------------------------------------------------
# Grados de entrada y salida
# ------------------------------------------------------------------
def graficar_grados(grafo, seleccion, rival, mostrar=False, archivo=None):
    jugadores = list(grafo.nodes())
    entrada = np.array([grafo.in_degree(j) for j in jugadores])
    salida = np.array([grafo.out_degree(j) for j in jugadores])

    # Orden por grado total (entrada + salida)
    orden = np.argsort(-(entrada + salida), kind="stable")
    nombres = [nombre_corto(jugadores[i]) for i in orden]
    entrada, salida = entrada[orden], salida[orden]

    x = np.arange(len(nombres))
    ancho = 0.38
    fig, ax = plt.subplots(figsize=(14, 6.5))
    b1 = ax.bar(x - ancho / 2 - 0.01, entrada, ancho, color=COLOR_ENTRADA,
                label="Grado de entrada (recibió de)")
    b2 = ax.bar(x + ancho / 2 + 0.01, salida, ancho, color=COLOR_SALIDA,
                label="Grado de salida (pasó a)")
    ax.bar_label(b1, fontsize=9, color=TINTA_SECUNDARIA, padding=2)
    ax.bar_label(b2, fontsize=9, color=TINTA_SECUNDARIA, padding=2)

    n = grafo.number_of_nodes()
    info = info_partido(seleccion, rival)
    ax.set_title(f"{seleccion} vs {rival_es(rival)} — Grados de entrada y salida\n"
                 f"{info['fase']}, {info['fecha']} · {n} jugadores "
                 f"(máximo posible: {n - 1} compañeros)",
                 loc="left", fontsize=14, color=TINTA, fontweight="bold")
    ax.set_ylabel("Cantidad de compañeros diferentes")
    ax.set_xticks(x, nombres, rotation=45, ha="right")
    ax.set_ylim(0, n)
    ax.yaxis.grid(True, color=REJILLA)
    ax.set_axisbelow(True)
    ax.legend(frameon=False, loc="upper right")
    fig.tight_layout()

    if archivo is None:
        archivo = carpeta_partido(seleccion, rival) / "grados.png"
    return _guardar(fig, archivo, mostrar)


# ------------------------------------------------------------------
# Mapa de calor de una matriz (A, P, N) con nombres de jugadores
# ------------------------------------------------------------------
def mapa_calor(tabla, titulo, archivo, decimales=0, subtitulo=None):
    from matplotlib.colors import LinearSegmentedColormap

    mapa = LinearSegmentedColormap.from_list("azules", AZULES)
    valores = tabla.to_numpy(dtype=float)
    filas, cols = valores.shape

    angosta = cols < 5   # matrices como B (pocas columnas): celdas mas anchas
    fig, ax = plt.subplots(figsize=(max(1.0 + 0.62 * cols, 8), 1.6 + 0.5 * filas))
    im = ax.imshow(valores, cmap=mapa, vmin=0, vmax=max(valores.max(), 1e-9),
                   aspect="auto" if angosta else "equal")
    for i in range(filas):
        for j in range(cols):
            v = valores[i, j]
            texto = f"{v:.{decimales}f}" if decimales else f"{int(round(v))}"
            oscuro = v > 0.55 * valores.max()
            ax.text(j, i, texto, ha="center", va="center", fontsize=8,
                    color="white" if oscuro else TINTA)
    ax.set_xticks(range(cols), tabla.columns, rotation=60, ha="right", fontsize=9)
    ax.set_yticks(range(filas), tabla.index, fontsize=9)
    ax.set_xlabel("Columna (j)")
    ax.set_ylabel("Fila (i)")
    for lado in ax.spines.values():
        lado.set_visible(False)
    titulo_completo = titulo if subtitulo is None else f"{titulo}\n{subtitulo}"
    ax.set_title(titulo_completo, loc="left", fontsize=12, color=TINTA, fontweight="bold")
    fig.colorbar(im, ax=ax, shrink=0.7)
    fig.tight_layout()
    return _guardar(fig, archivo, False)


# ------------------------------------------------------------------
# Comparacion entre partidos y selecciones
# ------------------------------------------------------------------
def graficar_comparacion(tabla, carpeta, mostrar=False):
    """Pequeños multiplos: una metrica por panel, un color por seleccion."""
    carpeta.mkdir(parents=True, exist_ok=True)
    metricas = [
        ("Pases completados", "Pases completados", "{:.0f}"),
        ("Precisión de pase (%)", "Precisión de pase (%)", "{:.1f}"),
        ("Densidad", "Densidad del grafo", "{:.2f}"),
        ("Concentración top-5 (%)", "% de pases en las 5 conexiones principales", "{:.1f}"),
    ]
    etiquetas = [f"{r}\n{s[:3].upper()}" for s, r in zip(tabla["Selección"], tabla["Rival"])]
    colores = [COLOR_SELECCION[s] for s in tabla["Selección"]]
    x = np.arange(len(tabla))

    fig, ejes = plt.subplots(2, 2, figsize=(16, 10))
    for ax, (col, titulo, fmt) in zip(ejes.flat, metricas):
        barras = ax.bar(x, tabla[col], color=colores, width=0.7)
        ax.bar_label(barras, labels=[fmt.format(v) for v in tabla[col]],
                     fontsize=8, color=TINTA_SECUNDARIA, padding=2)
        ax.set_title(titulo, loc="left", fontsize=12, color=TINTA, fontweight="bold")
        ax.set_xticks(x, etiquetas, rotation=60, ha="right", fontsize=8)
        ax.yaxis.grid(True, color=REJILLA)
        ax.set_axisbelow(True)
        ax.set_ylim(0, tabla[col].max() * 1.18)

    leyenda = [plt.Rectangle((0, 0), 1, 1, color=c, label=s)
               for s, c in COLOR_SELECCION.items()]
    fig.legend(handles=leyenda, loc="upper right", ncol=2, frameon=False)
    fig.suptitle("Comparación de los 12 partidos — Argentina (7) y Brasil (5)",
                 x=0.01, ha="left", fontsize=16, color=TINTA, fontweight="bold")
    fig.tight_layout(rect=(0, 0, 1, 0.95))
    archivo_partidos = _guardar(fig, carpeta / "comparacion_partidos.png", mostrar)

    # Promedios por seleccion (metricas normalizadas por partido)
    resumen = [
        ("Pases completados", "Pases completados\npor partido"),
        ("Precisión de pase (%)", "Precisión de\npase (%)"),
        ("Densidad", "Densidad\ndel grafo"),
        ("Grado medio", "Grado medio\n(compañeros)"),
        ("Concentración top-5 (%)", "Concentración\ntop-5 (%)"),
    ]
    fig, ejes = plt.subplots(1, len(resumen), figsize=(16, 4.8))
    for ax, (col, titulo) in zip(ejes, resumen):
        grupos = tabla.groupby("Selección")[col]
        medias, desv = grupos.mean(), grupos.std()
        selecciones = list(medias.index)
        barras = ax.bar(selecciones, medias, yerr=desv, capsize=5,
                        color=[COLOR_SELECCION[s] for s in selecciones],
                        error_kw={"ecolor": TINTA_SECUNDARIA, "lw": 1}, width=0.6)
        ax.bar_label(barras, labels=[f"{m:.2f}" if m < 10 else f"{m:.1f}" for m in medias],
                     fontsize=9, color=TINTA, padding=3, label_type="center")
        ax.set_title(titulo, fontsize=11, color=TINTA, fontweight="bold")
        ax.yaxis.grid(True, color=REJILLA)
        ax.set_axisbelow(True)
    fig.suptitle("Argentina vs Brasil — promedio por partido (barra de error = desviación estándar)",
                 x=0.01, ha="left", fontsize=14, color=TINTA, fontweight="bold")
    fig.tight_layout(rect=(0, 0, 1, 0.92))
    archivo_promedios = _guardar(fig, carpeta / "comparacion_selecciones.png", mostrar)

    return archivo_partidos, archivo_promedios
