"""Menu principal del proyecto.

Ejecutar:  python main.py   (funciona desde cualquier carpeta)

Tambien se puede usar directamente desde Python, por ejemplo:
    from graphs import analizar_partido
    analizar_partido("Argentina", "Arabia Saudita", origen="Papu Gómez",
                     destino="Acuña", destino_markov="Otamendi")
"""

from comparacion import imprimir_comparacion
from graphs import (DESTINO_POR_DEFECTO, analizar_partido, crear_grafo,
                    partidos_disponibles)
from nombres import nombre_corto, rival_es


def elegir(titulo, opciones, permitir_vacio=False):
    """Muestra opciones numeradas y repite hasta recibir una respuesta valida."""
    print(f"\n{titulo}")
    for i, opcion in enumerate(opciones, start=1):
        print(f"  {i}. {opcion}")
    while True:
        texto = input("Opcion" + (" (Enter = por defecto)" if permitir_vacio else "")
                      + ": ").strip()
        if texto == "" and permitir_vacio:
            return None
        if texto.isdigit() and 1 <= int(texto) <= len(opciones):
            return int(texto) - 1
        print(f"  Entrada no valida. Escriba un numero del 1 al {len(opciones)}.")


def pedir_umbral():
    while True:
        texto = input("\nMostrar conexiones con al menos cuantos pases? "
                      "(Enter = 5, 1 = grafo completo): ").strip()
        if texto == "":
            return 5
        if texto.isdigit() and int(texto) >= 1:
            return int(texto)
        print("  Entrada no valida. Escriba un numero entero mayor o igual a 1.")


def menu_partido():
    selecciones = ["Argentina", "Brasil"]
    seleccion = selecciones[elegir("Seleccion:", selecciones)]

    rivales = partidos_disponibles(seleccion)
    rival = rivales[elegir("Partido:", [rival_es(r) for r in rivales])]

    grafo, _ = crear_grafo(seleccion, rival)
    jugadores = list(grafo.nodes())
    nombres = [nombre_corto(j) for j in jugadores]

    i = elegir("Jugador de ORIGEN para la ruta mas corta:", nombres, True)
    j = elegir("Jugador DESTINO para la ruta mas corta:", nombres, True)
    print(f"\nDestino del modelo de Markov absorbente "
          f"(por defecto: {nombre_corto(DESTINO_POR_DEFECTO[seleccion])}).")
    k = elegir("Jugador destino de Markov:", nombres, True)
    umbral = pedir_umbral()
    mostrar = input("\nAbrir las graficas en pantalla? (s/n): ").strip().lower() == "s"

    analizar_partido(
        seleccion, rival,
        origen=None if i is None else jugadores[i],
        destino=None if j is None else jugadores[j],
        destino_markov=None if k is None else jugadores[k],
        umbral=umbral, mostrar=mostrar,
    )


def main():
    opciones = [
        "Analizar un partido",
        "Comparar los 12 partidos (Argentina vs Brasil)",
        "Salir",
    ]
    while True:
        opcion = elegir("=== ANALISIS DE PASES - QATAR 2022 ===", opciones)
        if opcion == 0:
            menu_partido()
        elif opcion == 1:
            mostrar = input("Abrir las graficas en pantalla? (s/n): ").strip().lower() == "s"
            imprimir_comparacion(mostrar=mostrar)
        else:
            print("Hasta luego.")
            break


if __name__ == "__main__":
    try:
        main()
    except (KeyboardInterrupt, EOFError):
        print("\nPrograma terminado.")
