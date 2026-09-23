import sys

input = sys.stdin.readline

m, r = map(int, input().split())
z = list(input().strip())


class Fenwick:
    """树状数组：维护哪些位置是 0，便于找左右最近 0。"""

    def __init__(self, n):
        self.n = n
        self.bit = [0] * (n + 1)

    def add(self, i, v):
        while i <= self.n:
            self.bit[i] += v
            i += i & -i

    def sum(self, i):
        s = 0
        while i > 0:
            s += self.bit[i]
            i -= i & -i
        return s

    def find_kth(self, k):
        # 找第 k 个 1（1-based 秩）
        idx = 0
        bit = 1 << (self.n.bit_length())
        while bit:
            nxt = idx + bit
            if nxt <= self.n and self.bit[nxt] < k:
                k -= self.bit[nxt]
                idx = nxt
            bit >>= 1
        return idx + 1


# 哨兵位置 0 与 m+1 视为 0
fw = Fenwick(m + 2)
fw.add(1, 1)  # 位置 0 → 下标 1
fw.add(m + 2, 1)  # 位置 m+1 → 下标 m+2
for i, c in enumerate(z, 1):
    if c == "0":
        fw.add(i + 1, 1)

# 初始权值
w = 0
i = 0
while i < m:
    if z[i] == "0":
        i += 1
        continue
    j = i
    while j < m and z[j] == "1":
        j += 1
    L = j - i
    w += L * (L + 1) // 2
    i = j


def nearest_zeros(p):
    # p 为 1..m；树状数组下标 = 位置+1
    # 位置 p 对应下标 p+1
    pref = fw.sum(p + 1)  # 含位置 p 及左侧（含哨兵）的 0 个数
    if z[p - 1] == "0":
        # p 本身是 0，左右是第 pref-1 与 pref+1 个 0
        L = fw.find_kth(pref - 1) - 1
        R = fw.find_kth(pref + 1) - 1
    else:
        L = fw.find_kth(pref) - 1
        R = fw.find_kth(pref + 1) - 1
    return L, R


out = []
for _ in range(r):
    p = int(input())
    L, R = nearest_zeros(p)
    a = p - L - 1
    b = R - p - 1
    if z[p - 1] == "0":
        # 0→1：合并，权值增加
        w += (a + 1) * (b + 1)
        fw.add(p + 1, -1)
        z[p - 1] = "1"
    else:
        # 1→0：拆段，权值减少
        w -= (a + 1) * (b + 1)
        fw.add(p + 1, 1)
        z[p - 1] = "0"
    out.append(str(w))
sys.stdout.write("\n".join(out) + "\n")
