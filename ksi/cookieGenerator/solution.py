#!/usr/bin/python3

from typing import Generator, List, Any
from types import GeneratorType


def fibonacci_generator() -> Generator[int, None, None]:
    # F_0 = 0, F_1 = 1, takže Fibonacciho posloupnost začíná od nuly,
    # ale testy chtěli, abych začal od jedničky
    yield 1
    fst, scnd = 0, 1
    while True:
        fst, scnd = scnd, fst + scnd
        yield scnd


def generator_connector(
    generators_list: List[Generator[Any, None, None]]
) -> Generator[Any, None, None]:
    for gen in generators_list:
        if not isinstance(gen, GeneratorType):
            continue
        for i in gen:
            yield i


def password_generator(length: int) -> Generator[str, None, None]:
    used = set()
    for i in range(10):
        nw = str(i) * length
        used.add(nw)
        yield nw
    increasing = "0123456789"
    for i in range(11 - length):
        nw = increasing[i: i + length]
        used.add(nw)
        yield nw
    decreasing = "9876543210"
    for i in range(11 - length):
        nw = decreasing[i: i + length]
        used.add(nw)
        yield nw
    for i in range(10**length):
        nw = str(i).zfill(length)
        if nw not in used:
            yield nw


def generator_of_generators() -> Generator[Generator[int, None, None], None, None]:
    mul = 1
    while True:

        def gen(mul) -> Generator[int, None, None]:
            i = 1
            while True:
                yield i * mul
                i += 1

        yield gen(mul)
        mul += 1


def primes_generator() -> Generator[int, None, None]:
    yield 2
    yield 3
    num = {9: [3]}
    p = 3
    while True:
        p += 2
        if p in num:
            lst = num.pop(p)
            for divisor in lst:
                if p + 2 * divisor not in num:
                    num[p + 2 * divisor] = []
                num[p + 2 * divisor].append(divisor)
        else:
            yield p
            num[p * p] = [p]
