"""
Datos y Grafo de los pases de Argentina durante la fase de grupos del Qatar 2022
"""

import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt

lec = pd.read_csv("pases_argentina.csv")

# - 3.1 FILTROS

columnas = ["fase", "oponente", "minuto", "jugador_nombre", "receptor_nombre", "resultado"]
lf= pd.read_csv("pases_argentina.csv", usecols= columnas)
fg = lf[lf["fase"] == "Group Stage"]
# print(lf)


# NETWORKX Y DATOS

P1 = lf[(lf["fase"] == "Group Stage") & (lf["oponente"]== "Saudi Arabia") & (lf["resultado"] == "Complete")]
# print(P1)

c_pases = ( P1.groupby(["jugador_nombre", "receptor_nombre"])
                .size()
                .reset_index(name = "peso"))
# print(c_pases)

G1 = nx.from_pandas_edgelist( c_pases, source= "jugador_nombre", target="receptor_nombre", edge_attr="peso", create_using=nx.DiGraph())
# print(G1.number_of_nodes())
# print(G1.number_of_edges())

plt.figure(figsize=(16, 16), facecolor="#36b63e")

pos = {
    "Damián Emiliano Martínez": (10, 50),
    "Nicolás Alejandro Tagliafico": (30, 85),
    "Nicolás Hernán Otamendi": (25, 62),
    "Cristian Gabriel Romero": (25, 38),
    "Nahuel Molina Lucero": (30, 15),
    "Alejandro Darío Gómez": (50, 75),
    "Leandro Daniel Paredes": (45, 50),
    "Rodrigo Javier De Paul": (50, 25),
    "Ángel Fabián Di María Hernández": (75, 80), 
    "Lautaro Javier Martínez": (80, 50),
    "Lionel Andrés Messi Cuccittini": (75, 20),
    "Julián Álvarez": (115, 80),
    "Enzo Fernandez": (115, 60),
    "Lisandro Martínez": (115, 40),
    "Marcos Javier Acuña": (115, 20),
}

nx.draw_networkx_nodes(
    G1, pos, node_size=2500, node_color="#7FCDE7", edgecolors="#FAF9F9"
)
nx.draw_networkx_labels(
    G1, pos, font_size=8, font_family="sans-serif", font_weight="bold"
)
nx.draw_networkx_edges(
    G1, pos, arrows=True, arrowstyle="-|>",  arrowsize=10,  edge_color="#232222",  connectionstyle="arc3,rad=0.1",  node_size=2500
    )

etiquetas_pesos = nx.get_edge_attributes(G1, "peso")

nx.draw_networkx_edge_labels(
    G1, pos, edge_labels=etiquetas_pesos, font_size=7, font_color="black", connectionstyle="arc3,rad=0.1",
)

plt.title("Argentina vs Arabia Saudita - Pases completados", fontsize=14)
plt.axis("off")
plt.tight_layout()
plt.show()






# P2 = lf[(lf["fase"] == "Group Stage") & (lf["oponente"]== "Poland") & (lf["resultado"] == "Complete")]
# print(P2)

# P3 = lf[(lf["fase"] == "Group Stage") & (lf["oponente"]== "Mexico") & (lf["resultado"] == "Complete")]
# print(P3)










