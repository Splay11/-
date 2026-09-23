MOD = 998244353


def encode(x):
    # 三进制去掉前导零后，先倒序再把 0 与 2 互换，得到 (值, 位数)
    if x == 0:
        return 2, 1
    val = 0
    ln = 0
    while x > 0:
        d = x % 3
        x //= 3
        val = val * 3 + (2 - d)
        ln += 1
    return val % MOD, ln


class SegTree:
    def __init__(self, a):
        n = len(a)
        N = 1
        while N < n:
            N *= 2
        self.N = N
        self.val = [0] * (2 * N)
        self.ln = [0] * (2 * N)
        mx = 20 * n + 5
        self.pow3 = [1] * mx
        for i in range(1, mx):
            self.pow3[i] = self.pow3[i - 1] * 3 % MOD
        for i, x in enumerate(a):
            self.val[N + i], self.ln[N + i] = encode(x)
        # 自底向上合并：右儿子（下标更大）放在高位
        for p in range(N - 1, 0, -1):
            ll = self.ln[p * 2]
            self.ln[p] = ll + self.ln[p * 2 + 1]
            self.val[p] = (self.val[p * 2 + 1] * self.pow3[ll] + self.val[p * 2]) % MOD

    def pull(self, p):
        ll = self.ln[p * 2]
        self.ln[p] = ll + self.ln[p * 2 + 1]
        self.val[p] = (self.val[p * 2 + 1] * self.pow3[ll] + self.val[p * 2]) % MOD

    def update(self, idx, x):
        p = self.N + idx
        self.val[p], self.ln[p] = encode(x)
        p //= 2
        while p:
            self.pull(p)
            p //= 2

    def query(self, ql, qr):
        # 覆盖 [ql,qr] 的节点从左到右收集，再倒序拼成从右到左
        l = ql + self.N
        r = qr + self.N
        left = []
        right = []
        while l <= r:
            if l & 1:
                left.append(l)
                l += 1
            if r & 1 == 0:
                right.append(r)
                r -= 1
            l //= 2
            r //= 2
        nodes = left + right[::-1]
        ans = 0
        for p in reversed(nodes):
            ans = (ans * self.pow3[self.ln[p]] + self.val[p]) % MOD
        return ans


def main():
    m, q = map(int, input().split())
    a = list(map(int, input().split()))
    st = SegTree(a)
    out = []
    for _ in range(q):
        parts = input().split()
        if parts[0] == "1":
            l = int(parts[1]) - 1
            r = int(parts[2]) - 1
            out.append(str(st.query(l, r)))
        else:
            idx = int(parts[1]) - 1
            x = int(parts[2])
            st.update(idx, x)
    print("\n".join(out))


if __name__ == "__main__":
    main()
