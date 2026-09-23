q = int(input())
for _ in range(q):
    m = int(input())
    h = list(map(int, input().split()))  # 温感读数序列
    L = [0] * m
    R = [0] * m
    mx, pos = -1, -1
    # 左扫：L[p] = 左侧最大值中距 p 最近（最右）的下标
    for i in range(m):
        L[i] = pos
        if h[i] > mx:
            mx, pos = h[i], i
        elif h[i] == mx:
            pos = i
    mx, pos = -1, -1
    # 右扫：R[p] = 右侧最大值中距 p 最近（最左）的下标
    for i in range(m - 1, -1, -1):
        R[i] = pos
        if h[i] > mx:
            mx, pos = h[i], i
        elif h[i] == mx:
            pos = i
    ans = 0
    for p in range(1, m - 1):
        if p - L[p] == R[p] - p:  # 等距峰点
            ans += 1
    print(ans)
