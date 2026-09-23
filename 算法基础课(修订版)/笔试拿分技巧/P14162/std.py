import heapq

# 输入 n 和 k
n, k = map(int, input().split())

# 存储每个博览会的起始和结束时间
a = [list(map(int, input().split())) for _ in range(n)]
# 按照开始时间排序
a.sort(key=lambda x: x[0])

start = 0  # 当前时间
q = []  # 小根堆，存储结束时间
idx = 0  # 当前处理的博览会索引
ans = 0  # 参加的博览会数量

while idx < n or q:
    # 移除已结束的博览会
    while q and q[0] < start:
        heapq.heappop(q)

    # 将当前可以参加的博览会加入堆
    while idx < n and a[idx][0] <= start:
        heapq.heappush(q, a[idx][1])
        idx += 1

    # 如果没有可参加的博览会，更新开始时间
    if not q:
        if idx == n:
            break
        start = max(start, a[idx][0])
    while idx < n and a[idx][0] <= start:
        heapq.heappush(q, a[idx][1])
        idx += 1
        
    # 每次从堆中取出最多 k 个结束时间最早的博览会
    for _ in range(k):
        if q:
            ans += 1
            heapq.heappop(q)

    start += 1  # 增加当前时间

print(ans)  # 输出参加的博览会数量
