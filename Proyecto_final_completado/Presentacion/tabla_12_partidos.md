# Tabla comparativa de los 12 partidos

Generada por `generar_presentacion.py` a partir de los CSV.

## Estructura del grafo

| Selección | Rival | Fase | Jugadores | Pases completados | Pases intentados | Precisión de pase (%) | Conexiones | Densidad | Grado medio entrada | Grado medio salida | Pases por jugador | Concentración top-5 (%) |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| Argentina | Arabia Saudita | Fase de grupos | 15 | 542 | 646 | 83.9 | 124 | 0.59 | 8.27 | 8.27 | 36.1 | 14.0 |
| Argentina | México | Fase de grupos | 16 | 476 | 567 | 84.0 | 125 | 0.52 | 7.81 | 7.81 | 29.8 | 16.8 |
| Argentina | Polonia | Fase de grupos | 16 | 826 | 909 | 90.9 | 154 | 0.64 | 9.62 | 9.62 | 51.6 | 14.2 |
| Argentina | Australia | Octavos de final | 16 | 646 | 728 | 88.7 | 133 | 0.55 | 8.31 | 8.31 | 40.4 | 15.0 |
| Argentina | Países Bajos | Cuartos de final | 17 | 531 | 640 | 83.0 | 147 | 0.54 | 8.65 | 8.65 | 31.2 | 12.8 |
| Argentina | Croacia | Semifinal | 16 | 358 | 432 | 82.9 | 121 | 0.5 | 7.56 | 7.56 | 22.4 | 13.4 |
| Argentina | Francia | Final | 17 | 560 | 693 | 80.8 | 129 | 0.47 | 7.59 | 7.59 | 32.9 | 13.6 |
| Brasil | Serbia | Fase de grupos | 16 | 539 | 618 | 87.2 | 125 | 0.52 | 7.81 | 7.81 | 33.7 | 17.3 |
| Brasil | Suiza | Fase de grupos | 16 | 507 | 597 | 84.9 | 135 | 0.56 | 8.44 | 8.44 | 31.7 | 21.1 |
| Brasil | Camerún | Fase de grupos | 16 | 512 | 593 | 86.3 | 138 | 0.57 | 8.62 | 8.62 | 32.0 | 18.9 |
| Brasil | Corea del Sur | Octavos de final | 16 | 566 | 641 | 88.3 | 129 | 0.54 | 8.06 | 8.06 | 35.4 | 18.2 |
| Brasil | Croacia | Cuartos de final | 16 | 652 | 747 | 87.3 | 129 | 0.54 | 8.06 | 8.06 | 40.8 | 18.1 |

## Jugadores

| Selección | Rival | Más pases realizados | Más pases recibidos | Conexión más frecuente | Jugadores destacados |
|---|---|---|---|---|---|
| Argentina | Arabia Saudita | Otamendi (84) | Otamendi (80) | Otamendi → Cuti Romero (18) | Otamendi, De Paul, Cuti Romero |
| Argentina | México | Otamendi (76) | Otamendi (68) | Otamendi → Montiel (18) | Otamendi, De Paul, Guido Rodríguez |
| Argentina | Polonia | De Paul (142) | De Paul (138) | Molina → De Paul (27) | De Paul, Otamendi, Enzo Fernández |
| Argentina | Australia | Enzo Fernández (94) | Enzo Fernández (86) | Otamendi → Acuña (21) | Enzo Fernández, Otamendi, De Paul |
| Argentina | Países Bajos | Otamendi (80) | Enzo Fernández (66) | Otamendi → Cuti Romero (19) | Otamendi, Enzo Fernández, De Paul |
| Argentina | Croacia | Enzo Fernández (41) | Enzo Fernández (44) | Otamendi → Enzo Fernández (11) | Enzo Fernández, Messi, Mac Allister |
| Argentina | Francia | Enzo Fernández (79) | Enzo Fernández (84) | Otamendi → Cuti Romero (18) | Enzo Fernández, Otamendi, De Paul |
| Brasil | Serbia | Alex Sandro (83) | Alex Sandro (69) | Alex Sandro → Thiago Silva (19) | Alex Sandro, Danilo, Thiago Silva |
| Brasil | Suiza | Marquinhos (92) | Marquinhos (81) | Thiago Silva → Marquinhos (31) | Marquinhos, Thiago Silva, Alex Sandro |
| Brasil | Camerún | Dani Alves (71) | Militão (64) | Bremer → Militão (27) | Militão, Dani Alves, Bremer |
| Brasil | Corea del Sur | Thiago Silva (82) | Thiago Silva (77) | Thiago Silva → Danilo (28) | Thiago Silva, Danilo, Marquinhos |
| Brasil | Croacia | Marquinhos (93) | Marquinhos (88) | Marquinhos → Danilo (27) | Marquinhos, Danilo, Thiago Silva |

## Markov absorbente (destino fijo por selección)

| Selección | Rival | Destino Markov | Otros absorbentes | t medio |
|---|---|---|---|---|
| Argentina | Arabia Saudita | Otamendi | Julián Álvarez | 5.81 |
| Argentina | México | Otamendi | — | 6.75 |
| Argentina | Polonia | Otamendi | — | 9.41 |
| Argentina | Australia | Otamendi | — | 8.61 |
| Argentina | Países Bajos | Otamendi | — | 8.12 |
| Argentina | Croacia | Otamendi | — | 12.44 |
| Argentina | Francia | Otamendi | — | 9.5 |
| Brasil | Serbia | Marquinhos | — | 12.93 |
| Brasil | Suiza | Marquinhos | — | 6.29 |
| Brasil | Camerún | Marquinhos | — | 18.1 |
| Brasil | Corea del Sur | Marquinhos | — | 10.63 |
| Brasil | Croacia | Marquinhos | — | 8.22 |

## Argentina vs Brasil (promedio por partido)

|  | Partidos (n) | Jugadores (promedio) | Jugadores (desv.) | Pases completados (promedio) | Pases completados (desv.) | Precisión de pase (%) (promedio) | Precisión de pase (%) (desv.) | Conexiones (promedio) | Conexiones (desv.) | Densidad (promedio) | Densidad (desv.) | Grado medio (promedio) | Grado medio (desv.) | Pases por jugador (promedio) | Pases por jugador (desv.) | Concentración top-5 (%) (promedio) | Concentración top-5 (%) (desv.) |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| **Argentina** | 7.0 | 16.14 | 0.69 | 562.71 | 145.56 | 84.89 | 3.57 | 133.29 | 12.53 | 0.55 | 0.06 | 8.26 | 0.72 | 34.91 | 9.22 | 14.26 | 1.32 |
| **Brasil** | 5.0 | 16.0 | 0.0 | 555.2 | 59.03 | 86.8 | 1.28 | 131.2 | 5.22 | 0.55 | 0.02 | 8.2 | 0.33 | 34.72 | 3.71 | 18.72 | 1.45 |
