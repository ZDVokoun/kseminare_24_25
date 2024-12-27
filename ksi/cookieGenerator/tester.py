#!/usr/bin/python3

from solution import primes_generator, generator_of_generators, password_generator, fibonacci_generator, generator_connector
from itertools import islice
from typing import List, Any, Callable

# -------------------- TEST FUNCTIONS --------------------------

# expected result: [1, 1, 2, 3, 5, 8, 13, 21, 34, 55]
def test_fibonacci_generator() -> List[int]:
    generator = fibonacci_generator()
    return list(islice(generator, 10))

# expected result: [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 5, 7, 9]
def test_generator_connector() -> List[int]:
    g1 = (x for x in range(5))
    g2 = (x for x in range(5,10))
    g3 = (x for x in range(5,10, 2))
    generator = generator_connector([g1, g2, g3, ""])
    return [x for x in generator]

# expected result: 761
def test_pwd_generator() -> int:
    generator = password_generator(3)
    target_pwd = "753"
    i = 1
    for pwd in generator:
        if pwd == target_pwd:
            return i
        i += 1
    raise Exception("Password not found")

# expected result: [[1, 2, 3, 4], [2, 4], [3, 6, 9, 12, 15, 18]]
def test_generator_of_generators() -> List[List[int]]:
    generator = generator_of_generators()
    g1 = next(generator)
    g2 = next(generator)
    g3 = next(generator)
    return [list(islice(g1, 4)), list(islice(g2, 2)), list(islice(g3, 6))]

# expected result: [2, 3, 5, 7, 11, 13]
def test_primes_generator() -> List[int]:
    generator = primes_generator()
    return list(islice(generator, 6))


# ---------------  END OF TEST FUNCTIONS ------------------------


def array_equals(a: List[Any], b: List[Any], compare: Callable[[Any, Any], bool] = lambda x, y: x == y) -> bool:
    try:
        if len(a) != len(b):
            return False
        for i in range(len(a)):
            if not compare(a[i], b[i]):
                return False
        return True
    except:
        return False

def run_test(testFunction: Callable[[], Any], testResult: Callable[[Any], bool], testName: str):
    print("\n\n-------- TEST: " + testName + " --------\n")
    try:
        res = testFunction()
    except:
        print("\n\33[31mTEST FAILED WITH EXCEPTON\33[0m")
        return
    print("Result")
    print(res)
    if testResult(res):
        print("\n\33[32mTEST WAS SUCCESSFULL\33[0m")
    else:
        print("\n\33[31mTEST FAILED\33[0m")

def run_all_tests():
    run_test(test_fibonacci_generator, lambda x: array_equals(x, [1, 1, 2, 3, 5, 8, 13, 21, 34, 55]), "Fibonacci")
    run_test(test_generator_connector, lambda x: array_equals(x, [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 5, 7, 9]), "Connector")
    run_test(test_pwd_generator, lambda x: x == 761, "Passwords")
    run_test(test_generator_of_generators, lambda x: array_equals(x, [[1, 2, 3, 4], [2, 4], [3, 6, 9, 12, 15, 18]], lambda a, b: array_equals(a, b)), "Generator²")
    run_test(test_primes_generator, lambda x: array_equals(x, [2, 3, 5, 7, 11, 13]), "Prime numbers")

run_all_tests()
