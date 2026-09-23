import sys

class DSU:
    # 简单并查集，路径压缩+按秩
    def __init__(self, n):
        self.p = list(range(n+1))
        self.r = [0]*(n+1)
    def find(self, x):
        if self.p[x] != x:
            self.p[x] = self.find(self.p[x])
        return self.p[x]
    def unite(self, a, b):
        a, b = self.find(a), self.find(b)
        if a == b: 
            return False
        if self.r[a] < self.r[b]:
            a, b = b, a
        self.p[b] = a
        if self.r[a] == self.r[b]:
            self.r[a] += 1
        return True

data = sys.stdin.read().strip().split()
it = iter(data)
try:
    T = int(next(it))
except StopIteration:
    sys.exit(0)

out_lines = []
for _ in range(T):
    n = int(next(it)); m = int(next(it))
    X = [int(next(it)) for _ in range(m)]
    Y = [int(next(it)) for _ in range(m)]

    # diff[i][j] = True 表示 i 与 j 判定为“不同”
    diff = [[False]*(n+1) for _ in range(n+1)]
    for x, y in zip(X, Y):
        diff[x][y] = diff[y][x] = True

    dsu = DSU(n)
    # 枚举未出现在 diff 中的对，认为“相同”，做合并
    for i in range(1, n+1):
        for j in range(i+1, n+1):
            if not diff[i][j]:
                dsu.unite(i, j)

    ok = True
    # 检查所有“不同”对的两端是否被合到同一集合
    for x, y in zip(X, Y):
        if dsu.find(x) == dsu.find(y):
            ok = False
            break

    out_lines.append("Yes" if ok else "No")

print("\n".join(out_lines))
