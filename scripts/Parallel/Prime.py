#  Copyright (c) 2025.  Departamento de Ingenieria de Sistemas y Computacion
import logging
import math

from tqdm import tqdm
from typeguard import typechecked
from threading import Thread, Lock
from benchmark import benchmark
from logger import configure_logging

primes = 0
lock = Lock()

@typechecked
def is_prime(n: int) -> bool:
    """
    Check if a number is prime
    """
    if n <= 1:
        return False
    if n == 2:
        return True
    if n % 2 == 0:
        return False
    for i in range(3, int(math.sqrt(n)) + 1, 2):
        if n % i == 0:
            return False

    return True

@typechecked
def search_primes(start: int, end: int):
    global primes
    local_primes = 0
    for i in range(start, end):
        if is_prime(i):
            local_primes += 1
    with lock:
        primes += local_primes

def threads():
    global primes
    primes = 0
    hilos = []

    hilo = Thread(target=search_primes, args=[1, 500000])
    hilos.append(hilo)
    hilo.start()

    hilo = Thread(target=search_primes, args=[500001, 1000000])
    hilos.append(hilo)
    hilo.start()

    for h in hilos:
        h.join()
    return primes


def mono():
    local_primes = 0
    for i in range(1, 1000000):
        if is_prime(i):
            local_primes += 1

    return local_primes

def main():
    configure_logging(log_level=logging.DEBUG)
    log = logging.getLogger(__name__)
    log.debug("Starting ..")

    with benchmark(log=log):
        log.debug(f"Primes in mono: {mono()}")

    with benchmark(log=log):
        log.debug(f"Primes in threads: {threads()}")

    log.debug("Done ...")
    pass

if __name__ == "__main__":
    main()