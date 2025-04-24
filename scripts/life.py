#  Copyright (c) 2025.  Departamento de Ingenieria de Sistemas y Computacion

"""
Implementacion del Juego de la vida de Conway

Este modulo implementa el juego de la vida basado en un automata celular ideado
por Don John Conway en 1970.

En cada celda se puede encontrar una celula que podría estar viva o muerta
dependiendo de los vecinos que tienen.

"""


def contar_vecinos(estado, fila, columna):

    contador_vecinos = 0

    for f in range(fila - 1, fila + 2):
        for c in range(columna - 1, columna + 2):
            if f == fila and c == columna:
                continue
            if f < 0 or f >= len(estado):
                continue
            if c < 0 or c >= len(estado[0]):
                continue
            if estado[f][c] == 1:
                contador_vecinos += 1
    return contador_vecinos


def imprimir_estado(estado):
    for fila in estado:
        #print("".join(str(cell) for cell in fila))
        print(''.join('࿕' if celula == 1 else '.' for celula in fila))


def crear_nuevo_estado(estado):
    n_filas = len(estado)
    n_columnas = len(estado[0])

    nuevo_estado = []

    for f in range(n_filas):
        # construyo una nueva fila
        nueva_fila = []
        for c in range(n_columnas):
            # agrego el valor segun la fila y la columna a la matriz
            nueva_fila.append(0)
        nuevo_estado.append(nueva_fila)
    return nuevo_estado

def expandir(estado):
    """
    Funcion que agrega una fila y una columna al inicio y al final de una matriz
    """
    n_filas = len(estado)
    n_columnas = len(estado[0])

    nuevo_estado = []

    for f in range(n_filas + 2):
        # construyo una nueva fila
        nueva_fila = []
        for c in range(n_columnas + 2):
            # agrego el valor segun la fila y la columna a la matriz
            nueva_fila.append(0)
        nuevo_estado.append(nueva_fila)

    for f in range(n_filas):
        for c in range(n_columnas):
            nuevo_estado[f+1][c+1] = estado[f][c]

    return nuevo_estado


def evolucionar(estado):
    estado = expandir(estado)
    nuevo_estado = crear_nuevo_estado(estado)

    for f in range(len(estado)):
        for c in range(len(estado[0])):
            n_vecinos = contar_vecinos(estado, f, c)

            if estado[f][c] == 1:
                if n_vecinos < 2 or n_vecinos > 3:
                    nuevo_estado[f][c] = 0
                else:
                    nuevo_estado[f][c] = 1
            else:
                if n_vecinos == 3:
                    nuevo_estado[f][c] = 1
                else:
                    nuevo_estado[f][c] = 0

    return nuevo_estado


def contar_poblacion(estado):
    celulas = 0
    for fila in estado:
        for columna in fila:
            # Si en cada una de las celdas es un 1, lo cuento y si es un cero no
            if columna == 1:
                celulas += 1
    return celulas


def main():
    # Matriz que contiene el estado inicial del juego de la vida
    estado = [
        [1, 1, 0],
        [0, 1, 1],
        [0, 1, 0],
    ]

    print(f"Estado inicial con poblacion de: {contar_poblacion(estado)}")
    imprimir_estado(estado)

    for i in range(10):
        estado = evolucionar(estado)
        print(f"Generacion {i+1} con poblacion de: {contar_poblacion(estado)}")
        imprimir_estado(estado)


if __name__ == "__main__":
    main()
