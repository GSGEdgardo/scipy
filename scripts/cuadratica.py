#  Copyright (c) 2025.  Departamento de Ingenieria de Sistemas y Computacion
import math


def cuadratica(a: float, b: float, c: float):
    """
    Función que resuelve una ecuación cuadrática de la forma ax^2 + bx + c = 0
    """

    print(type(a))
    if a == 0:
        print("El coeficiente a no puede ser cero")
        return None, None

    discriminante = b**2 - 4 * a * c
    if discriminante < 0:
        print("La ecuación no tiene solución real")
        return None, None

    raiz = math.sqrt(discriminante)
    res1 = (-b + raiz) / (2 * a)
    res2 = (-b - raiz) / (2 * a)

    return res1, res2

def pedir_coeficientes(mensaje):
    """
    Función que pide al usuario los coeficientes de la ecuación cuadrática
    """
    while True:
        try:
            return float(input(mensaje))
        except ValueError:
            print("Por favor, ingrese un número válido.")

def main():

    a = pedir_coeficientes("Ingrese el coeficiente a: ")
    b = pedir_coeficientes("Ingrese el coeficiente b: ")
    c = pedir_coeficientes("Ingrese el coeficiente c: ")

    resultado1, resultado2 = cuadratica(a, b, c)

    if resultado1 is not None and resultado2 is not None:
        print(f"Las soluciones son: {resultado1} y {resultado2}")


if __name__ == "__main__":
    main()
