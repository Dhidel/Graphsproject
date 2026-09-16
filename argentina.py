"""
Datos y Grafo de los pases de Argentina durante la fase de grupos del Qatar 2022
"""

import pandas as pd

lec = pd.read_csv("pases_argentina.csv")

FG = lec[lec["fase"] == "Group Stage"]
# print (FG)

"""
Los datos que voy a utilizar son: match
"""



