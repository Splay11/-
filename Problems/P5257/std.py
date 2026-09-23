from bisect import bisect_left

n, m = map(int, input().split())
U = [0] * m
V = [0] * m
W = [0] * m
inc = [[] for _ in range(n + 1)]
for i in range(m):
    u, v, w = map(int, input().split())
    U[i] = u
    V[i] = v
    W[i] = w
    inc[v].append(w)

comp = [None] * (n + 1)
base = [0] * (n + 1)
sz = [0] * (n + 1)
total = 0
for i in range(1, n + 1):
    a = inc[i]
    if not a:
        continue
    a.sort()
    k = 1
    for j in range(1, len(a)):
        if a[j] != a[k - 1]:
            a[k] = a[j]
            k += 1
    del a[k:]
    comp[i] = a
    sz[i] = k
    base[i] = total
    total += k

bit = [0] * (total + 1)
ans = 0
for i in range(m):
    u = U[i]
    v = V[i]
    w = W[i]
    best = 1
    cu = comp[u]
    if cu is not None:
        k = bisect_left(cu, w)
        if k:
            r = 0
            t = k
            b = base[u]
            while t > 0:
                val = bit[b + t]
                if val > r:
                    r = val
                t -= t & -t
            best = 1 + r
    if best > ans:
        ans = best
    pos = bisect_left(comp[v], w) + 1
    b = base[v]
    s = sz[v]
    while pos <= s:
        idx = b + pos
        if best > bit[idx]:
            bit[idx] = best
        pos += pos & -pos
print(ans)
