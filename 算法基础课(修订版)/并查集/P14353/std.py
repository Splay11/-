# 初始化
def init(n):
    return [i for i in range(n+1)]

# 查找（路径压缩）
def find(parent, x):
    if parent[x] != x:
        parent[x] = find(parent, parent[x])
    return parent[x]

# 合并
def union(parent, x, y):
    x_root = find(parent, x)
    y_root = find(parent, y)
    if x_root != y_root:
        parent[x_root] = y_root

# 主函数
n, m = map(int, input().split())
parent = init(n)

for _ in range(m):
    z, x, y = map(int, input().split())
    if z == 1:
        union(parent, x, y)
    else:
        print("Y" if find(parent, x) == find(parent, y) else "N")
