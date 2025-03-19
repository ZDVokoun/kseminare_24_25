n = 8

q = ["in" + str(i) for i in range(n)]

nq = []

nnq = []

i = 0

while len(q) > 1:
    for j in range(0,len(q), 2):
        nn = "d" + str(i)
        nnn = "e" + str(i)
        i += 1
        if j == len(q) - 1:
            nq.append(q[j])
            continue
        nq.append(nn)
        nnq.append(nnn)
        print(f"{nn}: {q[j]} 1 {q[j + 1]}")
        print(f"{nnn}: {q[j]} {q[j + 1]} 0")
    q = nq.copy()
    nq = []


q = nnq.copy()
nq = []
nnq=[]

i = 0

while len(q) > 1:
    for j in range(0,len(q), 2):
        nn = "f" + str(i)
        i += 1
        if j == len(q) - 1:
            nq.append(q[j])
            continue
        nq.append(nn)
        print(f"{nn}: {q[j]} 1 {q[j + 1]}")
    q = nq.copy()
    nq = []
