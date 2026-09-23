q = int(input())
for _ in range(q):
    m = int(input())
    h = list(map(int, input().split()))
    L = [0] * m
    R = [0] * m
    mx = -1
    pos = -1
    for i in range(m):
        L[i] = pos
        if h[i] > mx:
            mx = h[i]
            pos = i
        elif h[i] == mx:
            pos = i
    mx = -1
    pos = -1
    for i in range(m - 1, -1, -1):
        R[i] = pos
        if h[i] > mx:
            mx = h[i]
            pos = i
        elif h[i] == mx:
            pos = i
    ans = 0
    for p in range(1, m - 1):
        if p - L[p] == R[p] - p:
            ans += 1
    print(ans)
