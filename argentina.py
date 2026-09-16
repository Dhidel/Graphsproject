"""
Datos y Grafo de los pases de Argentina durante la fase de grupos del Qatar 2022
"""

import pandas as pd
lec = pd.read_csv("pases_argentina.csv")

# - 3.1 FILTROS

columnas = ["match_id", "fase", "oponente", "minuto", "jugador_nombre", "receptor_nombre", "resultado", "longitud_pase"]
lf= pd.read_csv("pases_argentina.csv", usecols= columnas)
fg = lf[lf["fase"] == "Group Stage"]
# print(lf)












# # - Partidos

# P1 = lec[lec["match_id"] == 3857300]
# # print(P1)

# P2 = lec[lec["match_id"] == 3857289]
# # print(P2)

# P3 = lec[lec["match_id"] == 3857264]
# print(P3)








