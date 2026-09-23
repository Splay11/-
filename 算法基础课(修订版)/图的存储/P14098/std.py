# 读取结点数
n = int(input())

# 读取图 A 的邻接矩阵并转换为邻接表
adj_a = {i: [] for i in range(n+1)}
for i in range(1, n + 1):
    row = list(map(int, input().split()))  # 一次读取一行矩阵数据
    for j in range(1, n + 1):
        if row[j - 1] == 1:  # 矩阵从 0 索引开始
            adj_a[i].append(j)

# 读取图 B 的邻接表
adj_b = [[] for _ in range(n + 1)]
for _ in range(n):
    data = list(map(int, input().split()))
    node = data[0]  # 第一个数是节点
    k = data[1]  # 第二个数是该节点的邻居数量
    neighbors = data[2:]  # 后续的 k 个数是邻居
    adj_b[node].extend(neighbors)

# 对每个节点的邻接表进行排序
for i in range(1, n + 1):
    adj_a[i].sort()
    adj_b[i].sort()

# 比较两张图的邻接表是否一致
same = True
for i in range(1, n + 1):
    if adj_a[i] != adj_b[i]:
        same = False
        break

print("YES" if same else "NO")
