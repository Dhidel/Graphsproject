import pandas as pd 
import networkx as nx 
import matplotlib.pyplot as plt

#3.1 limpieza de datos
df = pd.read_csv("pases_brasil.csv")

df_grupos = df [df["fase"] == "Group Stage"]

#print (df_grupos ["oponente"].unique()) #Oponentes en la fase de grupos

df_grupos.to_csv("Pases_brasil_grupos.csv", index = False ) #Datos limpios guardados


#3.2 Construcción del grafo - Brasil vs. Serbia 

serbia = df_grupos [df_grupos["oponente"] == "Serbia"] #extraemos de la columna oponente a Serbia 
#print (serbia["oponente"].unique())


#Solo pases completos 
serbia_completos = serbia [
    serbia["resultado"] == "Complete"
]

#print(serbia_completos["resultado"].unique())

grafo_serbia = nx.DiGraph() #Creamos grafo dirigido y lo guardamos

for indice, fila in serbia_completos.iterrows(): #cada fila contiene toda la información de un pase 

    #Guardamos quién hizo el pase y quién lo recibió
    emisor = fila["jugador_nombre"] 
    receptor = fila ["receptor_nombre"]

    #Pregunta si ya existe una flecha desde emisor hasta receptor
    if grafo_serbia.has_edge(emisor, receptor): 
        grafo_serbia[emisor][receptor]["weight"] += 1 #Si es que existe, significa que hubo un pase entre ellos
                                                      #Entonces aumentamos el peso de la conexión en 1

    else:                                             
        grafo_serbia.add_edge(emisor, receptor, weight=1) #si no existe, significa que es el primer pase entre ellos
                                                          #Creamos la conexión y empezamos su peso en 1
    #print(emisor, "→", receptor)

#for emisor, receptor, datos in grafo_serbia.edges(data=True): 
                               #Brinda todas las conexiones que existen en el grafo y también los datos en ella
    #print(emisor, "→", receptor, "| Peso:", datos["weight"])

peso_minimo = 4 #Peso mínimo para mostrar una conexión

#Lista donde guardamos las conexiones que cumplan con el peso
aristas_relevantes = []

#Recorremos todas las conexiones del grafo
for emisor, receptor, datos in grafo_serbia.edges(data=True): 

    if datos ["weight"] >= peso_minimo: #Revisamios si el peso de la conexión es mayor o igual al mínimo

        aristas_relevantes.append((emisor, receptor)) #Si cumple guardamos la conexión

#Creamos un nuevo grafo que contiene solo las conexiones relevantes 
grafo_serbia_filtrado = grafo_serbia.edge_subgraph(aristas_relevantes).copy()

pos = nx.spring_layout(grafo_serbia_filtrado, seed=42, k=1.5) #Calculamos la posicion de cada jugador en el dibujo, osea que pos guarda las posiciones
         #Spring layout, hace que networkX acomoda a los jugadores intentando que el grafo quede distribuido y las conexiones se puedan ver.
                                              #Seed hace que el dibujo no cambue de posición cada vez que se ejecuta el programa
                                              #K (espacio entre nodos)

plt.figure(figsize=(12,9)) #Creamos el espacio donde se dibujará el grafo

# 12 = ancho, 9 = alto (TAMAÑO DE LA HOJA)

nx.draw_networkx_nodes( #dibuja los nodos de mi grafo
    grafo_serbia_filtrado, #el grado que dibujará, usando el filtro de 3 pases
    pos, #Cada jugador en las coordenadas calculadas 
    node_size=1300,#controla el tamaño de los círculos
    node_color="#882E8B" #define el color de los nodos 
)

#Creamos nombres más cortos para que el grafo sea fácil de leer
nombre_cortos = {
    jugador: jugador.split()[0]
    for jugador in grafo_serbia_filtrado.nodes()
}


#Mostramos el nombre de cada jugador sobre su nodo
nx.draw_networkx_labels(
    grafo_serbia_filtrado, #Queremos los nombres de los jugadores en el grafo filtrado
    pos, #para que NetworkX sepa donde está cada jugador para colocar el nombre
    labels=nombre_cortos,
    font_size=8 #Tamaño de la letra
)

#Dibuja las conexiones entre jugadores
nx.draw_networkx_edges( 
    grafo_serbia_filtrado, 
    pos, #coordenadas de los jugadores
    arrows=True, #Indice que si queremos flechas, ya que es dirigido
    arrowstyle="-|>", #define la forma de la punta de la flecha
    arrowsize=30, #Define el tamaño de la punta
    width=1, #Todas las conexiones serán del mismo grosor
    connectionstyle="arc3,rad=0.20", #Hace que las flechas tengan una pequeña curva 
    edge_color="gray" #flechas grises 
)

#Obtenemos el peso de cada conexión
pesos = nx.get_edge_attributes(grafo_serbia_filtrado, "weight") #Se guarda en pesos todas las conexiones de mi grafo

#Escribe una etiqueta sobre cada conexión
nx.draw_networkx_edge_labels(
    grafo_serbia_filtrado, 
    pos, 
    edge_labels=pesos, #la etiqueta que queremos mostrar es el peso
    font_size=8, 
    label_pos=0.5 #Indicaen qué parte de la conexión colocamos el número 
)

#Título de la gráfica 
plt.title("Brasil vs Serbia - Pases completos")

#Quítamos los ejes porque no son necesarios en un grado
plt.axis("off")

#Ajustamos el conetenido para que aproveche bien el espacio 
plt.tight_layout()

plt.savefig("Brasil_vs_Serbia.png", dpi=300, bbox_inches= "tight")
#Mostramos la gráfica 



#3.3 Construcción del grafo - Brasil vs. Suiza

suiza = df_grupos[df_grupos["oponente"] == "Switzerland"] #Extraemos de la columna oponente a Suiza

#Solo pases completos
suiza_completos = suiza[
    suiza["resultado"] == "Complete"
]

grafo_suiza = nx.DiGraph() #Creamos grafo dirigido y lo guardamos

for indice, fila in suiza_completos.iterrows(): #Cada fila contiene toda la información de un pase

    #Guardamos quién hizo el pase y quién lo recibió
    emisor = fila["jugador_nombre"]
    receptor = fila["receptor_nombre"]

    #Pregunta si ya existe una flecha desde emisor hasta receptor
    if grafo_suiza.has_edge(emisor, receptor):
        grafo_suiza[emisor][receptor]["weight"] += 1 #Si existe, significa que ya hubo un pase entre ellos
                                                     #Entonces aumentamos el peso de la conexión en 1

    else:
        grafo_suiza.add_edge(emisor, receptor, weight=1) #Si no existe, significa que es el primer pase entre ellos
                                                        #Creamos la conexión y empezamos su peso en 1


peso_minimo = 4 #Peso mínimo para mostrar una conexión

#Lista donde guardamos las conexiones que cumplan con el peso
aristas_relevantes_suiza = []

#Recorremos todas las conexiones del grafo
for emisor, receptor, datos in grafo_suiza.edges(data=True):

    #Revisamos si el peso de la conexión es mayor o igual al mínimo
    if datos["weight"] >= peso_minimo:

        #Si cumple, guardamos la conexión
        aristas_relevantes_suiza.append((emisor, receptor))


#Creamos un nuevo grafo que contiene solo las conexiones relevantes
grafo_suiza_filtrado = grafo_suiza.edge_subgraph(aristas_relevantes_suiza).copy()


#Calculamos la posición de cada jugador en el dibujo
pos_suiza = nx.spring_layout(grafo_suiza_filtrado, seed=42, k=1.5)
#Spring layout hace que NetworkX acomode a los jugadores intentando que el grafo quede distribuido
#Seed hace que el dibujo no cambie de posición cada vez que se ejecuta el programa
#K controla el espacio entre nodos


plt.figure(figsize=(12,9)) #Creamos el espacio donde se dibujará el grafo

#12 = ancho, 9 = alto (TAMAÑO DE LA HOJA)


#Dibujamos los nodos de nuestro grafo
nx.draw_networkx_nodes(
    grafo_suiza_filtrado, #El grafo que dibujará usando el filtro de peso
    pos_suiza, #Cada jugador en las coordenadas calculadas
    node_size=1300, #Controla el tamaño de los círculos
    node_color="#882E8B" #Define el color de los nodos
)


#Creamos nombres más cortos para que el grafo sea fácil de leer
nombres_cortos_suiza = {
    jugador: jugador.split()[0]
    for jugador in grafo_suiza_filtrado.nodes()
}


#Mostramos el nombre de cada jugador sobre su nodo
nx.draw_networkx_labels(
    grafo_suiza_filtrado, #Queremos los nombres de los jugadores en el grafo filtrado
    pos_suiza, #Para que NetworkX sepa dónde está cada jugador
    labels=nombres_cortos_suiza,
    font_size=8 #Tamaño de la letra
)


#Dibujamos las conexiones entre jugadores
nx.draw_networkx_edges(
    grafo_suiza_filtrado,
    pos_suiza, #Coordenadas de los jugadores
    arrows=True, #Indicamos que queremos flechas porque el grafo es dirigido
    arrowstyle="-|>", #Define la forma de la punta de la flecha
    arrowsize=30, #Define el tamaño de la punta
    width=1, #Todas las conexiones tendrán el mismo grosor
    connectionstyle="arc3,rad=0.20", #Hace que las flechas tengan una pequeña curva
    edge_color="gray" #Flechas grises
)


#Obtenemos el peso de cada conexión
pesos_suiza = nx.get_edge_attributes(grafo_suiza_filtrado, "weight")


#Escribimos el peso sobre cada conexión
nx.draw_networkx_edge_labels(
    grafo_suiza_filtrado,
    pos_suiza,
    edge_labels=pesos_suiza, #La etiqueta que queremos mostrar es el peso
    font_size=8,
    label_pos=0.5 #Indica en qué parte de la conexión colocamos el número
)


#Título de la gráfica
plt.title("Brasil vs Suiza - Pases completos")

#Quitamos los ejes porque no son necesarios en un grafo
plt.axis("off")

#Ajustamos el contenido para que aproveche bien el espacio
plt.tight_layout()

#Guardamos el grafo como imagen
plt.savefig("Brasil_vs_Suiza.png", dpi=300, bbox_inches="tight")




#3.4 Construcción del grafo - Brasil y Camerún

camerun = df_grupos[df_grupos["oponente"] == "Cameroon"] #Extraemos de la columna oponente a Camerún

#Solo pases completos
camerun_completos = camerun[
    camerun["resultado"] == "Complete"
]

grafo_camerun = nx.DiGraph() #Creamos grafo dirigido y lo guardamos

for indice, fila in camerun_completos.iterrows(): #Cada fila contiene toda la información de un pase

    #Guardamos quién hizo el pase y quién lo recibió
    emisor = fila["jugador_nombre"]
    receptor = fila["receptor_nombre"]

    #Pregunta si ya existe una flecha desde emisor hasta receptor
    if grafo_camerun.has_edge(emisor, receptor):
        grafo_camerun[emisor][receptor]["weight"] += 1 #Si existe, significa que ya hubo un pase entre ellos
                                                       #Entonces aumentamos el peso de la conexión en 1

    else:
        grafo_camerun.add_edge(emisor, receptor, weight=1) #Si no existe, significa que es el primer pase entre ellos
                                                          #Creamos la conexión y empezamos su peso en 1


peso_minimo = 4 #Peso mínimo para mostrar una conexión

#Lista donde guardamos las conexiones que cumplan con el peso
aristas_relevantes_camerun = []

#Recorremos todas las conexiones del grafo
for emisor, receptor, datos in grafo_camerun.edges(data=True):

    #Revisamos si el peso de la conexión es mayor o igual al mínimo
    if datos["weight"] >= peso_minimo:

        #Si cumple, guardamos la conexión
        aristas_relevantes_camerun.append((emisor, receptor))


#Creamos un nuevo grafo que contiene solo las conexiones relevantes
grafo_camerun_filtrado = grafo_camerun.edge_subgraph(aristas_relevantes_camerun).copy()


#Calculamos la posición de cada jugador en el dibujo
pos_camerun = nx.spring_layout(grafo_camerun_filtrado, seed=42, k=1.5)
#Spring layout hace que NetworkX acomode a los jugadores intentando que el grafo quede distribuido
#Seed hace que el dibujo no cambie de posición cada vez que se ejecuta el programa
#K controla el espacio entre nodos


plt.figure(figsize=(12,9)) #Creamos el espacio donde se dibujará el grafo

#12 = ancho, 9 = alto (TAMAÑO DE LA HOJA)


#Dibujamos los nodos de nuestro grafo
nx.draw_networkx_nodes(
    grafo_camerun_filtrado, #El grafo que dibujará usando el filtro de peso
    pos_camerun, #Cada jugador en las coordenadas calculadas
    node_size=1300, #Controla el tamaño de los círculos
    node_color="#882E8B" #Define el color de los nodos
)


#Creamos nombres más cortos para que el grafo sea fácil de leer
nombres_cortos_camerun = {
    jugador: jugador.split()[0]
    for jugador in grafo_camerun_filtrado.nodes()
}


#Mostramos el nombre de cada jugador sobre su nodo
nx.draw_networkx_labels(
    grafo_camerun_filtrado, #Queremos los nombres de los jugadores en el grafo filtrado
    pos_camerun, #Para que NetworkX sepa dónde está cada jugador
    labels=nombres_cortos_camerun,
    font_size=8 #Tamaño de la letra
)


#Dibujamos las conexiones entre jugadores
nx.draw_networkx_edges(
    grafo_camerun_filtrado,
    pos_camerun, #Coordenadas de los jugadores
    arrows=True, #Indicamos que queremos flechas porque el grafo es dirigido
    arrowstyle="-|>", #Define la forma de la punta de la flecha
    arrowsize=30, #Define el tamaño de la punta
    width=1, #Todas las conexiones tendrán el mismo grosor
    connectionstyle="arc3,rad=0.20", #Hace que las flechas tengan una pequeña curva
    edge_color="gray" #Flechas grises
)


#Obtenemos el peso de cada conexión
pesos_camerun = nx.get_edge_attributes(grafo_camerun_filtrado, "weight")


#Escribimos el peso sobre cada conexión
nx.draw_networkx_edge_labels(
    grafo_camerun_filtrado,
    pos_camerun,
    edge_labels=pesos_camerun, #La etiqueta que queremos mostrar es el peso
    font_size=8,
    label_pos=0.5 #Indica en qué parte de la conexión colocamos el número
)


#Título de la gráfica
plt.title("Brasil vs Camerún - Pases completos")

#Quitamos los ejes porque no son necesarios en un grafo
plt.axis("off")

#Ajustamos el contenido para que aproveche bien el espacio
plt.tight_layout()

#Guardamos el grafo como imagen
plt.savefig("Brasil_vs_Camerun.png", dpi=300, bbox_inches="tight")

#Mostramos las tres gráficas
plt.show()