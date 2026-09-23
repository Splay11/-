q = int(input())
for _ in range(q):
    h, w = map(int, input().split())
    G = []
    rs = [0] * h
    cs = [0] * w
    for i in range(h):
        row = list(map(int, input().split()))
        G.append(row)
        for j in range(w):
            rs[i] += row[j]
            cs[j] += row[j]
    ans = max(rs + cs)
    if h >= 2:
        a = b = -(10**30)
        for v in rs:
            if v >= a:
                b = a
                a = v
            elif v > b:
                b = v
        ans = max(ans, a + b)
    if w >= 2:
        a = b = -(10**30)
        for v in cs:
            if v >= a:
                b = a
                a = v
            elif v > b:
                b = v
        ans = max(ans, a + b)
    for i in range(h):
        for j in range(w):
            ans = max(ans, rs[i] + cs[j] - G[i][j])
    print(ans)
