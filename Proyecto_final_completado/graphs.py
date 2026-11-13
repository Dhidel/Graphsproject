import pandas as pd
import numpy as np
import networkx as nx
import matplotlib.pyplot as plt



# Aquí se empieza a crear un grafo
def crear_grafo(seleccion, rival):
    archivo = "pases_" + seleccion.lower() + ".csv"
    datos = pd.read_csv(archivo)

    pases = datos[
        (datos["oponente"] == rival) &
        (datos["resultado"] == "Complete")
    ]

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



# Estadisticas y grados de los grafos
def estadisticas(grafo, total):

    realizados = dict(grafo.out_degree(weight="peso"))
    recibidos = dict(grafo.in_degree(weight="peso"))

    jugador_mas_pases = max(realizados, key=realizados.get)
    jugador_mas_recibidos = max(recibidos, key=recibidos.get)

    conexion = max(
        grafo.edges(data=True),
        key=lambda x: x[2]["peso"]
    )

    print("\n--- ESTADISTICAS ---")
    print("Total de pases:", total)

    print("Mas pases realizados:",
          jugador_mas_pases, realizados[jugador_mas_pases])

    print("Mas pases recibidos:",
          jugador_mas_recibidos, recibidos[jugador_mas_recibidos])

    print("Conexion mas frecuente:",
          conexion[0], "->", conexion[1],
          conexion[2]["peso"])

    print("\n--- GRADOS ---")

    for jugador in grafo.nodes():

        print(
            jugador,
            "| Entrada:", grafo.in_degree(jugador),
            "| Salida:", grafo.out_degree(jugador)
        )


# grafica la red de pases
def graficar(grafo, seleccion, rival):

    # Mostrar solamente conexiones de 5 pases o mas
    conexiones = [
        (a, b)
        for a, b, datos in grafo.edges(data=True)
        if datos["peso"] >= 5
    ]

    filtrado = grafo.edge_subgraph(conexiones).copy()

    if filtrado.number_of_nodes() == 0:
        print("No hay conexiones para mostrar.")
        return

    pos = nx.spring_layout(filtrado, seed=42)

    # Nombres automaticos obtenidos del CSV
    nombres = {
        jugador: jugador.split()[-1]
        for jugador in filtrado.nodes()
    }

    # Tamaño segun los pases realizados
    tamanos = [
        500 + grafo.out_degree(jugador, weight="peso") * 10
        for jugador in filtrado.nodes()
    ]

    # Grosor segun la cantidad de pases
    grosores = [
        datos["peso"] / 5
        for a, b, datos in filtrado.edges(data=True)
    ]

    plt.figure(figsize=(13, 9))

    nx.draw_networkx_nodes(
        filtrado, pos,
        node_size=tamanos,
        node_color="skyblue",
        edgecolors="black"
    )

    nx.draw_networkx_labels(
        filtrado, pos,
        labels=nombres,
        font_size=9
    )

    nx.draw_networkx_edges(
        filtrado, pos,
        arrows=True,
        arrowsize=15,
        width=grosores,
        edge_color="gray",
        connectionstyle="arc3,rad=0.15"
    )

    plt.title(f"{seleccion} vs {rival} - Red de pases")
    plt.axis("off")
    plt.tight_layout()
    plt.savefig(f"red_{seleccion}_{rival}.png")
    plt.show()



# matriz y potencias (pedido por christian)
def matrices(grafo):

    jugadores = list(grafo.nodes())

    matriz = nx.to_numpy_array(
        grafo,
        nodelist=jugadores,
        weight=None,
        dtype=int
    )

    print("\n--- MATRIZ DE ADYACENCIA ---")

    print("Orden de jugadores:")
    for i, jugador in enumerate(jugadores):
        print(i, jugador)

    print("\nA:")
    print(matriz)

    print("\nA^2:")
    print(np.linalg.matrix_power(matriz, 2))

    print("\nA^3:")
    print(np.linalg.matrix_power(matriz, 3))



# rutas entre jugadores
def rutas(grafo):

    jugadores = list(grafo.nodes())

    # Ejemplo automatico con dos jugadores del partido
    origen = jugadores[0]
    destino = jugadores[-1]

    print("\n--- RUTAS ---")
    print("Origen:", origen)
    print("Destino:", destino)

    if nx.has_path(grafo, origen, destino):

        ruta = nx.shortest_path(grafo, origen, destino)

        print("Ruta:", " -> ".join(ruta))
        print("Cantidad de conexiones:", len(ruta) - 1)

    else:
        print("No existe una ruta.")


# cadenas de markov (pedido por Christian)
def markov(grafo):

    jugadores = list(grafo.nodes())

    matriz = nx.to_numpy_array(
        grafo,
        nodelist=jugadores,
        weight="peso"
    )

    # Convertir los pases en probabilidades
    for i in range(len(matriz)):

        total = matriz[i].sum()

        if total > 0:
            matriz[i] = matriz[i] / total
        else:
            matriz[i, i] = 1

    print("\n--- MATRIZ DE MARKOV ---")
    print(np.round(matriz, 2))

    print("\nProbabilidades despues de 2 pasos:")
    print(np.round(np.linalg.matrix_power(matriz, 2), 2))
    
 # grafica de grados (pedido)   
def graficar_grados(grafo):

    jugadores = list(grafo.nodes())

    entrada = [grafo.in_degree(j) for j in jugadores]
    salida = [grafo.out_degree(j) for j in jugadores]

    # Ordenamos por grado total
    datos = pd.DataFrame({
        "Jugador": jugadores,
        "Entrada": entrada,
        "Salida": salida
    })

    datos["Total"] = datos["Entrada"] + datos["Salida"]
    datos = datos.sort_values("Total", ascending=False)

    datos = datos.set_index("Jugador")

    datos[["Entrada", "Salida"]].plot(
        kind="bar",
        figsize=(14, 6),
        color=["skyblue", "orange"]
    )

    plt.title("Grados de entrada y salida")
    plt.ylabel("Cantidad de compañeros conectados")
    plt.xlabel("Jugadores")
    plt.xticks(rotation=75, ha="right")
    plt.tight_layout()
    plt.show()
    

# Matriz Inversa (pedido)

def matriz_inversa(grafo):

    jugadores = list(grafo.nodes())

    # Elegimos como destino al jugador que mas pases recibe
    recibidos = dict(grafo.in_degree(weight="peso"))
    destino = max(recibidos, key=recibidos.get)

    # Matriz de pases
    matriz = nx.to_numpy_array(
        grafo,
        nodelist=jugadores,
        weight="peso"
    )

    # Convertimos los pases en probabilidades
    for i in range(len(matriz)):
        total = matriz[i].sum()

        if total > 0:
            matriz[i] = matriz[i] / total
        else:
            matriz[i, i] = 1

    # Convertimos al destino en estado absorbente
    indice = jugadores.index(destino)

    matriz[indice] = 0
    matriz[indice, indice] = 1

    # Quitamos la fila y columna del destino
    indices = [
        i for i in range(len(jugadores))
        if i != indice
    ]

    Q = matriz[np.ix_(indices, indices)]

    identidad = np.eye(len(Q))

    print("\n--- MATRIZ INVERSA ---")
    print("Jugador destino:", destino)

    try:
        inversa = np.linalg.inv(identidad - Q)

        print("\nMatriz fundamental N = (I - Q)^-1:")
        print(np.round(inversa, 2))

    except np.linalg.LinAlgError:
        print("No se puede calcular la inversa.")
        print("Puede haber estados que no llegan al destino.")


# Analisis del partido
def analizar_partido(seleccion, rival):

    grafo, total = crear_grafo(seleccion, rival)

    print("\n============================")
    print(seleccion, "vs", rival)
    print("============================")

    estadisticas(grafo, total)
    matrices(grafo)
    rutas(grafo)
    markov(grafo)
    matriz_inversa(grafo)

    graficar(grafo, seleccion, rival)
    graficar_grados(grafo)

    plt.show()
