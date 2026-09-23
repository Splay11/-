import sys

# 并查集
class DSU:
    def __init__(self, n):
        self.p = list(range(n))
        self.r = [0]*n
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
T = int(next(it))
out_lines = []
for _ in range(T):
    n = int(next(it)); m = int(next(it))  # m 不直接使用
    a = [int(next(it)) for _ in range(n)]
    b = [int(next(it)) for _ in range(n)]

    # 坐标压缩
    vals = sorted(set(a + b))
    idx = {v:i for i, v in enumerate(vals)}
    K = len(vals)

    dsu = DSU(K)
    for i in range(n):
        u = idx[a[i]]
        v = idx[b[i]]
        dsu.unite(u, v)

    C = sum(1 for i in range(K) if dsu.find(i) == i)
    out_lines.append(str(K - C))

sys.stdout.write("\n".join(out_lines))
