def gcd(a, b):
    a = abs(a)
    b = abs(b)
    if a < b:
        a, b = b, a
    while (b != 0):
        a %= b;
        a,b=b,a
    return a;

def solve():
    v = int(input())
    for _ in range(v):
        i = input()
        i = i.split(" ")
        a = tuple([int(x) for x in i[0].split("/")])
        if a[1] < 0:
            a = (-a[0], -a[1])
        b = tuple([int(x) for x in i[2].split("/")])
        if b[1] < 0:
            b = (-b[0], -b[1])
        aa = a[0] * b[1] // gcd(a[1],b[1])
        bb = b[0] * a[1] // gcd(a[1],b[1])
        if i[1] == "+":
            res = (aa + bb, a[1]*b[1]//gcd(a[1],b[1]))
        else:
            res = (aa - bb, a[1]*b[1]//gcd(a[1],b[1]))
        ress = (res[0]//gcd(res[0],res[1]),res[1]//gcd(res[0],res[1]))
        if ress[1] == 1:
            print(ress[0])
        else:
            print(f"{ress[0]}/{ress[1]}")


if __name__ == "__main__":
    solve()
