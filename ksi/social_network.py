from abc import ABC, abstractmethod
from collections import deque
from typing import Optional, Tuple, Set, List

class Animal(ABC):
    def __init__(self, name, n) -> None:
        self.__name = name
        min_id, max_id = self._get_id_range()
        if max_id == -1:
            if not (min_id <= n):
                raise ValueError(f"Entered ID is outside the range > {min_id}")
        else:
            if not (min_id <= n <= max_id):
                raise ValueError(f"Entered ID is outside the range {min_id} - {max_id}")
        self.__id = n
    
    @abstractmethod
    def _get_id_range(self) -> Tuple[int, int]:
        return (0,0)

    @abstractmethod
    def can_connect_with(self, other: 'Animal') -> bool:
        pass

    def __str__(self) -> str:
        return f"Ahoj, já jsem {self.__name}!"
    
    def get_name(self) -> str:
        return self.__name

    def get_id(self) -> int:
        return self.__id

    def __eq__(self, other: 'object') -> bool:
        if not isinstance(other, Animal):
            return self is other
        return self.__id == other.__id

    def __ne__(self, other: 'object') -> bool:
        if not isinstance(other, Animal):
            return self is not other
        return self.__id == other.__id

    def __lt__(self, other: 'Animal') -> bool:
        return self.__id < other.__id

    def __le__(self, other: 'Animal') -> bool:
        return self.__id <= other.__id

    def __gt__(self, other: 'Animal') -> bool:
        return self.__id > other.__id

    def __ge__(self, other: 'Animal') -> bool:
        return self.__id >= other.__id

class Student(Animal):
    def can_connect_with(self, other: 'Animal') -> bool:
        return not isinstance(other, Host)
    def _get_id_range(self) -> Tuple[int,int]:
        return (100000, 700000)

class AkademickyPracovnik(Animal):
    def can_connect_with(self, other: 'Animal') -> bool:
        return True
    def _get_id_range(self) -> Tuple[int,int]:
        return (700001, 999999)

class Host(Animal):
    def can_connect_with(self, other: 'Animal') -> bool:
        return not isinstance(other, Student)
    def _get_id_range(self) -> Tuple[int,int]:
        return (1000000, -1)

class University:
    def __init__(self):
        # Jelikož třídy jsou obecně mutable, nemůžu je používat jako
        # klíč v dictionary, proto místo nich používám tuple s jménem
        # a ID tučňáka, který bude jednoznačně tučňáka na univerzitě
        # identifikovat
        self._edges: dict[Tuple[str, int], set[Tuple[str, int]]] = {}
        self._users: dict[Tuple[str, int], Animal] = {}

    def AddUser(self, user: Animal) -> None:
        name_id = (user.get_name(), user.get_id())
        if name_id in self._users:
            raise ValueError(f"User {user.get_name()} with ID {user.get_id()} already exists")
        self._edges[name_id] = set()
        self._users[name_id] = user

    def _get_user(self, user: Animal) -> Tuple[str,int]:
        """
        Provádí kontrolu, zda je uživatel v databázi, 
        pak vrátí jeho jméno a ID.
        """
        name_id = (user.get_name(), user.get_id())
        if name_id not in self._users:
            raise ValueError(f"User {name_id[0]} with ID {name_id[1]} is not in the database")
        if self._users[name_id] is not user:
            raise ValueError(f"The object of user {name_id[0]} with ID {name_id[1]} does not match the object in the database")
        return name_id
    def Connect(self, user_1: Animal, user_2 : Animal) -> None:
        name_id_1 = self._get_user(user_1)
        name_id_2 = self._get_user(user_2)

        if not user_1.can_connect_with(user_2):
            raise ValueError("The given users cannot be friends")

        self._edges[name_id_1].add(name_id_2)
        self._edges[name_id_2].add(name_id_1)
    def Disconnect(self, user_1:Animal, user_2:Animal) -> None:
        name_id_1 = self._get_user(user_1)
        name_id_2 = self._get_user(user_2)

        self._edges[name_id_1].remove(name_id_2)
        self._edges[name_id_2].remove(name_id_1)
    def _set_to_users(self, users: Set[Tuple[str,int]]) -> List[Animal]:
        return [self._users[user] for user in users]
    def GetFriends(self, user: Animal):
        name_id = self._get_user(user)
        return self._set_to_users(self._edges[name_id])
    def CommonFriends(self, users: List[Animal]) -> List[Animal]:
        common_friends = set(self._users.keys())
        for user in users:
            name_id = self._get_user(user)
            common_friends = common_friends.intersection(self._edges[name_id])
        return self._set_to_users(common_friends)
    def _bfs(self, start: Tuple[str, int],end : Optional[Tuple[str,int]] = None) -> int:
        q = deque()
        q.append((start, -1))
        visited = {user: False for user in self._users.keys()}
        visited[start] = True
        res = -1
        while len(q) > 0:
            cur, dist = q.popleft()
            if end is None:
                res = max(res, dist)
            elif cur == end:
                res = dist
                break
            for neigh in self._edges[cur]:
                if not visited[neigh]:
                    visited[neigh] = True
                    q.append((neigh, dist + 1))
        if end is None and not all(visited.values()):
            res = -1
        return res
    def FindConnection(self, user_1: Animal, user_2: Animal) -> int:
        name_id_1 = self._get_user(user_1)
        name_id_2 = self._get_user(user_2)

        if name_id_1 == name_id_2:
            return 0
        return self._bfs(name_id_1, name_id_2)
    def CheckHypothesis(self) -> int:
        """
        Tento algoritmus spustí z každého vrcholu BFS, čímž najde nejdelší 
        vzdálenost z každého vrcholu. Pokud není graf sociální sítě jedna 
        komponenta, provede se jen první volání BFS, jinak se provede celkem 
        V volání BFS, tedy časová složitost je O(V (V + E)) = O(V E + V^2).
        """
        res = 0
        for user in self._users.keys():
            mx_dist = self._bfs(user)
            if mx_dist == -1:
                return -1
            res = max(res, mx_dist)
        return res
