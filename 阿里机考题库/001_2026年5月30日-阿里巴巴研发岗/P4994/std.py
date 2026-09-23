q = int(input())
for _ in range(q):
    h, w = map(int, input().split())
    G = []
    rs = [0] * h  # 行和
    cs = [0] * w  # 列和
    for i in range(h):
        row = list(map(int, input().split()))
        G.append(row)
        for j in range(w):
            rs[i] += row[j]
            cs[j] += row[j]
    ans = max(rs + cs)  # 同一条线摘两次 = 只取一次
    if h >= 2:
        a = b = -(10**30)
        for v in rs:
            if v >= a: b, a = a, v
            elif v > b: b = v
        ans = max(ans, a + b)  # 两行
    if w >= 2:
        a = b = -(10**30)
        for v in cs:
            if v >= a: b, a = a, v
            elif v > b: b = v
        ans = max(ans, a + b)  # 两列
    for i in range(h):
        for j in range(w):
            # 一行一列：扣掉交点重复
            ans = max(ans, rs[i] + cs[j] - G[i][j])
    print(ans)
