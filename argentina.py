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


# NETWORKX Y DATOS

P1 = lf[(lf["fase"] == "Group Stage") & (lf["oponente"]== "Saudi Arabia") & (lf["resultado"] == "Complete")]

c_pases = ( P1.groupby(["jugador_nombre", "receptor_nombre"])
                .size()
                .reset_index(name = "peso"))

pt = c_pases["peso"].sum()

G1 = nx.from_pandas_edgelist( c_pases, source= "jugador_nombre", target="receptor_nombre", edge_attr="peso", create_using=nx.DiGraph())

plt.figure(figsize=(20, 20), facecolor="#36b63e")

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
    G1, pos, node_size=2000, node_color="#7FCDE7", edgecolors="#FAF9F9"
)
nx.draw_networkx_labels(
    G1, pos, font_size=8, font_family="sans-serif", font_weight="bold"
)
nx.draw_networkx_edges(
    G1, pos, arrows=True, arrowstyle="-|>",  arrowsize=10,  edge_color="#232222",  connectionstyle="arc3,rad=0.1",  node_size=2000
    )

etiquetas_pesos = nx.get_edge_attributes(G1, "peso")

nx.draw_networkx_edge_labels(
    G1, pos, edge_labels=etiquetas_pesos, font_size=7, font_color="black", connectionstyle="arc3,rad=0.1",
)

plt.title(f"Argentina vs Arabia Saudita - Pases completados totales: {pt}", fontsize=14, color = "white")
plt.axis("off")
plt.tight_layout()
plt.savefig("grafica_arabia_saudita.png")
plt.show()


P2 = lf[(lf["fase"] == "Group Stage") & (lf["oponente"]== "Mexico") & (lf["resultado"] == "Complete")]


c_pases_2 = ( P2.groupby(["jugador_nombre", "receptor_nombre"])
                .size()
                .reset_index(name = "peso"))

pt_2 = c_pases_2["peso"].sum()

G2 = nx.from_pandas_edgelist( c_pases_2, source= "jugador_nombre", target="receptor_nombre", edge_attr="peso", create_using=nx.DiGraph())

plt.figure(figsize=(20, 20), facecolor="#36b63e")

pos_2 = {
    "Damián Emiliano Martínez": (10, 50),
    "Gonzalo Ariel Montiel": (30, 15),
    "Nicolás Hernán Otamendi": (25, 38),
    "Lisandro Martínez": (25, 62),
    "Marcos Javier Acuña": (30, 85),
    "Rodrigo Javier De Paul": (50, 25),
    "Guido Rodríguez": (45, 50),
    "Alexis Mac Allister": (50, 75),
    "Lionel Andrés Messi Cuccittini": (75, 20),
    "Lautaro Javier Martínez": (80, 50),
    "Ángel Fabián Di María Hernández": (75, 80),
    "Enzo Fernandez": (115, 85),
    "Julián Álvarez": (115, 70),
    "Nahuel Molina Lucero": (115, 55),
    "Exequiel Alejandro Palacios": (115, 40),
    "Cristian Gabriel Romero": (115, 25),
}

nx.draw_networkx_nodes(
    G2, pos_2, node_size=2000, node_color="#7FCDE7", edgecolors="#035F14"
)
nx.draw_networkx_labels(
    G2, pos_2, font_size=8, font_family="sans-serif", font_weight="bold"
)
nx.draw_networkx_edges(
    G2, pos_2, arrows=True, arrowstyle="-|>",  arrowsize=10,  edge_color="#232222",  connectionstyle="arc3,rad=0.1",  node_size=2000
    )

etiquetas_pesos_2 = nx.get_edge_attributes(G2, "peso")

nx.draw_networkx_edge_labels(
    G2, pos_2, edge_labels=etiquetas_pesos_2, font_size=7, font_color="black", connectionstyle="arc3,rad=0.1",
)

plt.title(f"Argentina vs Mexico - Pases completados totales: {pt_2}", fontsize=14, color = "white")
plt.axis("off")
plt.tight_layout()
plt.savefig("grafica_mexico.png")
plt.show()



P3 = lf[(lf["fase"] == "Group Stage") & (lf["oponente"]== "Poland") & (lf["resultado"] == "Complete")]

c_pases_3 = ( P3.groupby(["jugador_nombre", "receptor_nombre"])
                .size()
                .reset_index(name = "peso"))

pt_3 = c_pases_3["peso"].sum()

G3 = nx.from_pandas_edgelist( c_pases_3, source= "jugador_nombre", target="receptor_nombre", edge_attr="peso", create_using=nx.DiGraph())

plt.figure(figsize=(20, 20), facecolor="#36b63e")

pos_3= {
    "Damián Emiliano Martínez": (10, 50),
    "Nahuel Molina Lucero": (30, 15),
    "Cristian Gabriel Romero": (25, 38),
    "Nicolás Hernán Otamendi": (25, 62),
    "Marcos Javier Acuña": (30, 85),
    "Rodrigo Javier De Paul": (50, 25),
    "Enzo Fernandez": (45, 50),
    "Alexis Mac Allister": (50, 75),
    "Lionel Andrés Messi Cuccittini": (75, 20),
    "Julián Álvarez": (80, 50),
    "Ángel Fabián Di María Hernández": (75, 80),
    "Leandro Daniel Paredes": (115, 85),
    "Nicolás Alejandro Tagliafico": (115, 70),
    "Germán Alejandro Pezzella": (115, 55),
    "Lautaro Javier Martínez": (115, 40),
    "Thiago Ezequiel Almada": (115, 25),
}

nx.draw_networkx_nodes(
    G3, pos_3, node_size=2000, node_color="#7FCDE7", edgecolors="#ED0E0E"
)
nx.draw_networkx_labels(
    G3, pos_3, font_size=8, font_family="sans-serif", font_weight="bold"
)
nx.draw_networkx_edges(
    G3, pos_3, arrows=True, arrowstyle="-|>",  arrowsize=10,  edge_color="#232222",  connectionstyle="arc3,rad=0.1",  node_size=2000
    )

etiquetas_pesos_3 = nx.get_edge_attributes(G3, "peso")

nx.draw_networkx_edge_labels(
    G3, pos_3, edge_labels=etiquetas_pesos_3, font_size=7, font_color="black", connectionstyle="arc3,rad=0.1",
)

plt.title(f"Argentina vs Polonia - Pases completados totales: {pt_3}", fontsize=14, color = "white")
plt.axis("off")
plt.tight_layout()
plt.savefig("grafica_polonia.png")
plt.show()









