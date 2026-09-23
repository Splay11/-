from collections import deque

q = int(input())
for _ in range(q):
    m = int(input())
    g = [0] + list(map(int, input().split()))  # g[i] 为站点 i 的传送目标
    INF = 10**18
    dis = [INF] * (m + 1)
    dis[1] = 0
    dq = deque([1])
    while dq:
        x = dq.popleft()
        y = g[x]
        if dis[y] > dis[x]:  # 花费 0 的传送
            dis[y] = dis[x]
            dq.appendleft(y)
        if x < m and dis[x + 1] > dis[x] + 1:  # 花费 1 的右移
            dis[x + 1] = dis[x] + 1
            dq.append(x + 1)
    print(dis[m])
