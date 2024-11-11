from typing import List

def lower_bound(arr, target):
    lo = 0
    hi = len(arr) - 1
    res = len(arr)
    
    while lo <= hi:
        mid = lo + (hi - lo) // 2
        
        if arr[mid] >= target:
            res = mid
            hi = mid - 1
            
        else:
            lo = mid + 1
            
    return res

class Line:
    def __init__(self, a=0, b=float('inf'), i=-1):
        self.a = a
        self.b = b
        self.i = i
    
    def get(self, x):
        return self.a * x + self.b


class SegmentTree:
    def __init__(self, n, values: List[int]):
        self.tree = [Line() for _ in range(4 * n)]
        self.values = values
        self.n = n
        self.counter = 0

    def _insert(self, idx, tl, tr, line):
        if self.tree[idx].get(self.values[tl]) > line.get(self.values[tl]):
            self.tree[idx], line = line, self.tree[idx]
        if self.tree[idx].get(self.values[tr]) < line.get(self.values[tr]):
            return
        if tl == tr:
            return
        mid = (tl + tr) // 2
        if self.tree[idx].get(self.values[mid]) < line.get(self.values[mid]):
            self._insert(2 * idx + 1, mid + 1, tr, line)
        else:
            self.tree[idx], line = line, self.tree[idx]
            self._insert(2 * idx, tl, mid, line)

    def insert(self, l, r, line):
        self._insert_in_range(1, 0, self.n - 1, l, r, line)
        self.counter += 1
    
    def _insert_in_range(self, idx, tl, tr, l, r, line):
        if tr < l or r < tl or tl > tr or l > r:
            return
        if tl >= l and tr <= r:
            self._insert(idx, tl, tr, line)
            return
        mid = (tl + tr) // 2
        self._insert_in_range(2 * idx, tl, mid, l, r, line)
        self._insert_in_range(2 * idx + 1, mid + 1, tr, l, r, line)
    
    def query(self, idx, tl, tr, x):
        if tl == tr:
            return self.tree[idx].get(self.values[x]), self.tree[idx]
        mid = (tl + tr) // 2
        res = self.tree[idx].get(self.values[x])
        ids = self.tree[idx]
        if x <= mid:
            fn = self.query(2 * idx, tl, mid, x)
            if res > fn[0]:
                res = fn[0]
                ids = fn[1]
        else:
            fn = self.query(2 * idx + 1, mid + 1, tr, x)
            if res > fn[0]:
                res = fn[0]
                ids = fn[1]
        return res, ids

    def query_point(self, x):
        return self.query(1, 0, self.n - 1, x)

# Returns only one penguin per query
def solve_faster(
    positions: List[int], velocities: List[int], queries: List[int]
) -> List[List[int]]:
    srt_queries = list(sorted(queries))
    tree = SegmentTree(len(queries), srt_queries)
    
    for i in range(len(positions)):
        pos = lower_bound(srt_queries,positions[i])
        if pos != 0:
            segment = Line(-1/velocities[i], positions[i] / velocities[i], i)
            tree.insert(0, pos - 1, segment)
        if pos != 6:
            segment = Line(1/velocities[i], - positions[i] / velocities[i], i)
            tree.insert(pos, len(queries) - 1, segment)
    res = []
    for q in queries:
        pos = lower_bound(srt_queries,q)
        res.append([tree.query_point(pos)[1].i])
    return res

def solve_bruteforce(
    positions: List[int], velocities: List[int], queries: List[int]
) -> List[List[int]]:
    mn: List[float] = [float('inf')] * len(queries)
    res: List[List[int]] = []
    for i in range(len(queries)):
        res.append([])
    for i, q in enumerate(queries):
        for j, p in enumerate(positions):
            if mn[i] > abs(p - q) / velocities[j]:
                res[i] = []
                res[i].append(j)
                mn[i] = abs(p - q) / velocities[j]
            elif mn[i] == abs(p - q) / velocities[j]:
                res[i].append(j)
    return res

def solve(
    positions: List[int], velocities: List[int], queries: List[int]
) -> List[List[int]]:
    if len(positions) < 700 and len(velocities) < 700:
        return solve_bruteforce(positions, velocities, queries)
    return solve_faster(positions, velocities, queries)
