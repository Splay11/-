class Fenwick:
    def __init__(self, n):
        # 下标对应工位编号 1..n，存已经插入的工位个数
        self.n = n
        self.c = [0] * (n + 1)

    def add(self, i, v):
        # 在工位 i 上加上 v
        while i <= self.n:
            self.c[i] += v
            i += i & -i

    def pre(self, i):
        # 编号 1..i 上已插入的工位数
        s = 0
        while i > 0:
            s += self.c[i]
            i -= i & -i
        return s

    def rng(self, left, right):
        # 统计上游窗口 [left, right]
        if left > right:
            return 0
        return self.pre(right) - self.pre(left - 1)


def solve(n, d, k, w, qs):
    # 工位按重量从小到大，询问按阈值从小到大，离线插入
    stations = []
    for i in range(1, n + 1):
        stations.append((w[i], i))
    stations.sort()
    queries = []
    for qid in range(len(qs)):
        x = qs[qid]
        left = x - d
        if left < 1:
            left = 1
        right = x - 1
        # 阈值是 w_x - K，重量不超过它的才算偏低
        thresh = w[x] - k
        queries.append((thresh, left, right, qid))
    queries.sort()
    bit = Fenwick(n)
    ans = [0] * len(qs)
    p = 0
    for t in range(len(queries)):
        thresh, left, right, qid = queries[t]
        while p < n and stations[p][0] <= thresh:
            bit.add(stations[p][1], 1)
            p += 1
        ans[qid] = bit.rng(left, right)
    return ans


def main():
    parts = list(map(int, input().split()))
    n, m, d, k = parts[0], parts[1], parts[2], parts[3]
    w = [0] + list(map(int, input().split()))
    qs = []
    for _ in range(m):
        qs.append(int(input().strip()))
    out = solve(n, d, k, w[: n + 1], qs)
    for x in out:
        print(x)


if __name__ == "__main__":
    main()
