#!/usr/bin/python3

from Pinguin import Gender, Pingu
from sys import setrecursionlimit
from typing import List, Set


TARGET_PENGUIN = "Karlík Veliký"


def DFS(king: Pingu, visited: Set[str], stop: List[bool]) -> None:
    if stop[0]:
        return
    if king.getName() == TARGET_PENGUIN:
        stop[0] = True
        return
    res = [
        (-p.getAge(), p)
        for p in king.getChildren()
        if p.getName() not in visited and p.getGender() == Gender.MALE
    ]
    res.sort()
    king.kill()
    for _, p in res:
        visited.add(p.getName())
        DFS(p, visited, stop)


def killPenguins(king: Pingu) -> None:
    # raději vyšší než aby to kvůli tomu spadlo
    setrecursionlimit(1000000000)
    visited: Set[str] = set()
    stop = [False]
    DFS(king, visited, stop)
