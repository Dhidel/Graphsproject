# Nombres cortos y reconocibles para las graficas y las matrices.
# Los CSV traen el nombre completo (ej. "Lionel Andrés Messi Cuccittini");
# usar solo el ultimo apellido producia etiquetas confusas ("Cuccittini")
# o repetidas (cuatro jugadores de Brasil aparecian como "Silva").

NOMBRES_CORTOS = {
    # Argentina
    "Alejandro Darío Gómez": "Papu Gómez",
    "Alexis Mac Allister": "Mac Allister",
    "Cristian Gabriel Romero": "Cuti Romero",
    "Damián Emiliano Martínez": "Dibu Martínez",
    "Enzo Fernandez": "Enzo Fernández",
    "Exequiel Alejandro Palacios": "Palacios",
    "Germán Alejandro Pezzella": "Pezzella",
    "Gonzalo Ariel Montiel": "Montiel",
    "Guido Rodríguez": "Guido Rodríguez",
    "Juan Marcos Foyth": "Foyth",
    "Julián Álvarez": "Julián Álvarez",
    "Lautaro Javier Martínez": "Lautaro Martínez",
    "Leandro Daniel Paredes": "Paredes",
    "Lionel Andrés Messi Cuccittini": "Messi",
    "Lisandro Martínez": "Lisandro Martínez",
    "Marcos Javier Acuña": "Acuña",
    "Nahuel Molina Lucero": "Molina",
    "Nicolás Alejandro Tagliafico": "Tagliafico",
    "Nicolás Hernán Otamendi": "Otamendi",
    "Paulo Bruno Exequiel Dybala": "Dybala",
    "Rodrigo Javier De Paul": "De Paul",
    "Thiago Ezequiel Almada": "Almada",
    "Ángel Fabián Di María Hernández": "Di María",
    "Ángel Martín Correa": "Ángel Correa",
    # Brasil
    "Alex Nicolao Telles": "Alex Telles",
    "Alex Sandro Lobo Silva": "Alex Sandro",
    "Alisson Ramsés Becker": "Alisson",
    "Antony Matheus dos Santos": "Antony",
    "Bruno Guimarães Rodriguez Moura": "Bruno Guimarães",
    "Carlos Henrique Casimiro": "Casemiro",
    "Daniel Alves da Silva": "Dani Alves",
    "Danilo Luiz da Silva": "Danilo",
    "Ederson Santana de Moraes": "Ederson",
    "Frederico Rodrigues Santos": "Fred",
    "Fábio Henrique Tavares": "Fabinho",
    "Gabriel Fernando de Jesus": "Gabriel Jesus",
    "Gabriel Teodoro Martinelli Silva": "Martinelli",
    "Gleison Bremer Silva Nascimento": "Bremer",
    "Lucas Tolentino Coelho de Lima": "Paquetá",
    "Marcos Aoás Corrêa": "Marquinhos",
    "Neymar da Silva Santos Junior": "Neymar",
    "Pedro Guilherme Abreu dos Santos": "Pedro",
    "Raphael Dias Belloli": "Raphinha",
    "Richarlison de Andrade": "Richarlison",
    "Rodrygo Silva de Goes": "Rodrygo",
    "Thiago Emiliano da Silva": "Thiago Silva",
    "Vinícius José Paixão de Oliveira Júnior": "Vinícius Jr.",
    "Weverton Pereira da Silva": "Weverton",
    "Éder Gabriel Militão": "Militão",
    "Éverton Augusto de Barros Ribeiro": "Everton Ribeiro",
}

# Nombres de los rivales en español (el CSV los tiene en inglés)
RIVALES_ES = {
    "Saudi Arabia": "Arabia Saudita",
    "Mexico": "México",
    "Poland": "Polonia",
    "Australia": "Australia",
    "Netherlands": "Países Bajos",
    "Croatia": "Croacia",
    "France": "Francia",
    "Serbia": "Serbia",
    "Switzerland": "Suiza",
    "Cameroon": "Camerún",
    "South Korea": "Corea del Sur",
}

FASES_ES = {
    "Group Stage": "Fase de grupos",
    "Round of 16": "Octavos de final",
    "Quarter-finals": "Cuartos de final",
    "Semi-finals": "Semifinal",
    "Final": "Final",
}


def nombre_corto(nombre_completo):
    # Si un jugador no esta en el diccionario se usa su nombre completo
    return NOMBRES_CORTOS.get(nombre_completo, nombre_completo)


def rival_es(rival):
    return RIVALES_ES.get(rival, rival)
