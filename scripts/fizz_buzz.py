#  Copyright (c) 2025.  Departamento de Ingenieria de Sistemas y Computacion


def fizzbuzz(n):
    """
    Función que imprime los números del 1 al n, pero por cada múltiplo de 3 imprime "Fizz",
    por cada múltiplo de 5 imprime "Buzz" y por cada múltiplo de 15 imprime "FizzBuzz".
    """

    for i in range(1, n + 1):
        if i % 15 == 0:
            print("FizzBuzz")
        elif i % 3 == 0:
            print("Fizz")
        elif i % 5 == 0:
            print("Buzz")
        else:
            print(i)


def main():
    fizzbuzz(150)


if __name__ == "__main__":
    main()
