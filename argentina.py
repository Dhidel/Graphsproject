"""
Datos y Grafo de los pases de Argentina durante la fase de grupos del Qatar 2022
"""

import pandas as pd

import networkx as nx

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









# P2 = lf[(lf["fase"] == "Group Stage") & (lf["oponente"]== "Poland") & (lf["resultado"] == "Complete")]
# print(P2)

# P3 = lf[(lf["fase"] == "Group Stage") & (lf["oponente"]== "Mexico") & (lf["resultado"] == "Complete")]
# print(P3)










