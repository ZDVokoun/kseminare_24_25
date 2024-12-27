from math import ceil
from types import FunctionType
from typing import Callable, Union
from collections import Counter
from inspect import signature

Bowl = list[str]
Action = (
    Callable[[Bowl], Bowl]
    | Callable[[Bowl, Bowl], Bowl]
    | Callable[[Bowl, Bowl, Bowl], Bowl]
)


def add(bowl_a: Bowl, bowl_b: Bowl) -> Bowl:
    return bowl_a + bowl_b


def mix(bowl_a: Bowl, bowl_b: Bowl) -> Bowl:
    return [j for i in zip(bowl_a, bowl_b) for j in i] + (
        bowl_a[len(bowl_b):]
        if len(bowl_a) > len(bowl_b)
        else bowl_b[len(bowl_a):]
    )


def cut(bowl_a: Bowl) -> Bowl:
    return [
        ing[i * 2: i * 2 + 2]
        for ing in bowl_a
        for i in range(ceil(len(ing) / 2))
    ]


def bake(bowl_a: Bowl, bowl_b: Bowl, bowl_c: Bowl) -> Bowl:
    max_len = max(len(bowl_b), len(bowl_c))
    mul_factor = ceil(max_len / len(bowl_a))
    return add((bowl_a * mul_factor)[:max_len], add(bowl_b, bowl_c))


def boil(bowl_a: Bowl) -> Bowl:
    return [f"\u00b0{ingredience}\u00b0" for ingredience in bowl_a]


def remove(bowl_a: Bowl, bowl_b: Bowl) -> Bowl:
    cnt = Counter(bowl_a)
    res = []
    for ing in bowl_b:
        if cnt[ing] > 0:
            cnt[ing] -= 1
        else:
            res.append(ing)
    return res


def compress(bowl_a: Bowl, bowl_b: Bowl) -> Bowl:
    to_be_inserted = "".join(bowl_b)
    i = 0
    res = []
    for ing in bowl_a:
        new_ing = ""
        for ch in ing:
            new_ing += ch + to_be_inserted[i]
            i += 1
            i %= len(to_be_inserted)
        res.append(new_ing)
    return res


def sieve(bowl_a: Bowl, bowl_b: Bowl) -> Bowl:
    res = []
    min_len = min(len(bowl_a), len(bowl_b))
    for i in range(min_len):
        if len(bowl_a[i]) == len(bowl_b[i]):
            res.append(bowl_a[i])
            res.append(bowl_b[i])
        elif len(bowl_a[i]) > len(bowl_b[i]):
            res.append(bowl_b[i])
        else:
            res.append(bowl_a[i])
    rest = (
        bowl_a[min_len:] if len(bowl_a) > len(bowl_b) else bowl_b[min_len:]
    )
    return res + rest


def cook(recipe: list[Union[Bowl, Action]]) -> Bowl:
    stack: list[Bowl] = []
    for item in reversed(recipe):
        if isinstance(item, FunctionType):
            params = len(signature(item).parameters)
            args = []
            for _ in range(params):
                if len(stack) == 0:
                    return []
                top = stack.pop()
                if isinstance(top, FunctionType):
                    return []
                args.append(top)
            stack.append(item(*args))
        else:
            stack.append(item)
    if len(stack) > 1:
        return []
    return stack[0]
