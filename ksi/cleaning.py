from typing import Set


class Value:
    def __init__(self, value: str):
        self._value = value
        self._is_disposed = False
    
    def free(self) -> None:
        assert not self._is_disposed
        self._is_disposed = True
        
    def get_value(self) -> str:
        assert not self._is_disposed
        return self._value

class ValueFactory:
    def __init__(self):
        self._values = []

    def make_value(self, value: str) -> Value:
        self._values.append(Value(value))
        return self._values[-1]

# from value_lib import ValueFactory, Value


class Vertex:
    def __init__(self, value: Value):
        self.value = value
        self.successors = []
        self.v_ref = 0
        self.it_ref = 0
        self.freed = False
    def inc_v_ref(self):
        """Increments the number of vertex references"""
        self.v_ref += 1
    def inc_it_ref(self):
        """Increments the number of iterator or country references"""
        self.it_ref += 1
    def dec_v_ref(self):
        """Decrements the number of vertex references"""
        self.v_ref -= 1
    def dec_it_ref(self):
        """Decrements the number of iterator or country references"""
        self.it_ref -= 1
    def no_ref(self):
        return self.v_ref + self.it_ref == 0
    def has_it_ref(self):
        return self.it_ref > 0
    def clear(self):
        if self.no_ref() and not self.freed:
            self.value.free()
            self.freed = True
            for u in self.successors:
                u.dec_v_ref()
                u.clear()

class Iterator:
    def __init__(self, path) -> None:
        self.lst = path
        self.i = -1
    def __iter__(self):
        return self
    def __next__(self):
        if self.i >= 0:
            self.lst[self.i].dec_it_ref()
            self.lst[self.i].clear()
        self.i += 1
        if self.i == len(self.lst):
            raise StopIteration
        return self.lst[self.i].value

class Country:
    def __init__(self, value_factory: ValueFactory):
        self.__value_factory = value_factory
        self.penguins = set()
        self.vertices = set()

    def add_penguin(self, name: str) -> None:
        penguin = Vertex(self.__value_factory.make_value(name))
        penguin.inc_it_ref()
        self.vertices.add(penguin)
        self.penguins.add(penguin)

    def add_nonpenguin(self, parent: str, value: str) -> None:
        searched: Set[Vertex] = set()
        for penguin in self.penguins:
            if self.__add_nonpenguin_aux(penguin, parent, value, searched):
                break

    def __add_nonpenguin_aux(self, current: Vertex, parent: str, new: str, 
                             searched: Set[Vertex]) -> bool:
        if current in searched:
            return False
        searched.add(current)
        if current.value.get_value() == parent:
            v = Vertex(self.__value_factory.make_value(new))
            v.inc_v_ref()
            current.successors.append(v)
            self.vertices.add(v)
            return True
        for vertex in current.successors:
            if self.__add_nonpenguin_aux(vertex, parent, new, searched):
                return True
        return False

    def add_edge(self, first: Vertex, second: Vertex) -> None:
        first.successors.append(second)
        second.inc_v_ref()

    def kill(self, name: str) -> None:
        for penguin in self.penguins:
            if penguin.value.get_value() == name:
                self.penguins.remove(penguin)
                penguin.dec_it_ref()
                penguin.clear()
                break

    def __has_aux(self, v: Vertex, dest: str):
        if v.value.get_value() == dest:
            v.inc_it_ref()
            return [v]
        for u in v.successors:
            child_path = self.__has_aux(u, dest)
            if len(child_path) > 0:
                v.inc_it_ref()
                return [v] + child_path
        return []

    def has(self, name: str, dest: str) -> Iterator:
        for penguin in self.penguins:
            if penguin.value.get_value() == name:
                return Iterator(self.__has_aux(penguin, dest))
        raise ValueError
        
    def __collect_aux(self, v: Vertex, visited: Set[Vertex]):
        visited.add(v)
        for u in v.successors:
            if u not in visited:
                self.__collect_aux(u, visited)


    def collect(self) -> None:
        to_visit = [v for v in self.vertices if not v.freed and v.has_it_ref()]
        visited = set()
        for v in to_visit:
            self.__collect_aux(v, visited)
        to_free = self.vertices.difference(visited)
        for v in to_free:
            if not v.freed:
                v.value.free()
        self.vertices = visited
    

# Základné testy
vf = ValueFactory()
c = Country(vf)
c.add_penguin("NieKarlik")
c.add_nonpenguin("NieKarlik", "pocitac")
c.add_penguin("ByvalyKral")
c.add_nonpenguin("ByvalyKral", "sen ovladnut svet")
c.add_nonpenguin("sen ovladnut svet", "vsetky tucniacice")

assert len(vf._values) == 5
assert all([not x._is_disposed for x in vf._values])

c.kill("ByvalyKral")
assert not vf._values[0]._is_disposed
assert not vf._values[1]._is_disposed
assert vf._values[2]._is_disposed
assert vf._values[3]._is_disposed
assert vf._values[4]._is_disposed

c.add_penguin("ByvalyKral")
c.add_nonpenguin("ByvalyKral", "sen ovladnut svet")
c.add_nonpenguin("sen ovladnut svet", "vsetky tucniacice")

for val in c.has("ByvalyKral", "vsetky tucniacice"):
    if val.get_value() == "sen ovladnut svet":
        c.kill("ByvalyKral")
        assert vf._values[5]._is_disposed
        assert not vf._values[6]._is_disposed
        assert not vf._values[7]._is_disposed

assert vf._values[6]._is_disposed
assert vf._values[7]._is_disposed

c.add_nonpenguin("pocitac", "suciastky")
# trochu hack, lebo sa mnozina neda indexovat
c.add_edge(next(iter(c.penguins)).successors[0].successors[0], 
           next(iter(c.penguins)).successors[0])
c.kill("NieKarlik")

assert vf._values[0]._is_disposed
assert not vf._values[1]._is_disposed
assert not vf._values[8]._is_disposed

c.collect()

assert vf._values[1]._is_disposed
assert vf._values[8]._is_disposed


