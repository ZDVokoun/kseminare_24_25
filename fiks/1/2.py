if __name__ == "__main__":
    t = int(input())
    global n, k, a, p, res
    res = [0]
    for _ in range(t):
        [n, k] = [int(i) for i in input().split()]
        a = [int(i) for i in input().split()]
        p = [int(i) - 1 for i in input().split()]
        res[0] = 0

        graph = [None] * n
        root = -1

        for i, v in enumerate(p):
            if v < 0:
                root = i
                continue
            if graph[v] is None:
                graph[v] = []
            graph[v].append(i)

        lst = []

        def DFS2(v):
            comp = a[v]
            if graph[v] is not None:
                for u in graph[v]:
                    comp = max(DFS2(u) + 1,comp)
            res[0] += comp - a[v]
            a[v] = comp
            return comp


        def DFS1(v):
            from_leaf = 0
            if graph[v] is not None:
                for u in graph[v]:
                    from_leaf = max(DFS1(u) + 1, from_leaf)
            lst.append((a[v] - from_leaf, -from_leaf))
            return from_leaf

        DFS2(root)
        if res[0] > k:
            print("ajajaj")
            continue
        DFS1(root)
        lst.sort()
        last = lst[0][0]
        max_depth = lst[0][1]
        best = -1
        for i, (x, d) in enumerate(lst):
            if last != x:
                if k - res[0] >= i * (x - last):
                    res[0] += i * (x - last)
                    last = x
                else:
                    best = last - max_depth + (k - res[0]) // i
                    break
            max_depth = max(max_depth, d)

        if best == -1:
            best = last - max_depth + (k - res[0]) // n
        print(best)

