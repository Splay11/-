import bisect


class Fenwick:
    def __init__(self, n):
        # 树状数组维护区间最小值（二元组）
        self.n = n
        inf = (10**18, 0)
        self.a = [inf] * (n + 2)

    def upd(self, i, val):
        # 单点与 val 取更小
        while i <= self.n:
            if val < self.a[i]:
                self.a[i] = val
            i += i & -i

    def qry(self, i):
        # 前缀 1..i 的最小值
        r = (10**18, 0)
        while i:
            if self.a[i] < r:
                r = self.a[i]
            i -= i & -i
        return r


def min_ops(h):
    # 把数组分成尽量多段、段和单调不减；答案 = 长度 - 段数 = 合并次数
    m = len(h)
    pre = [0] * (m + 1)
    for i in range(m):
        pre[i + 1] = pre[i] + h[i]
    uniq = sorted(set(pre))
    fw = Fenwick(len(uniq) + 2)
    last = [0] * (m + 1)
    dp = [0] * (m + 1)
    # 空前缀：最后一段和为 0，尚未合并
    fw.upd(bisect.bisect_left(uniq, 0) + 1, (0, 0))
    for i in range(1, m + 1):
        # last[j] + pre[j] <= pre[i]  等价于  last[j] <= 第 j+1..i 段的和
        best = fw.qry(bisect.bisect_right(uniq, pre[i]))
        # best = (dp[j] - j, -pre[j])，使合并次数最小，并列时最后一段尽量短
        dp[i] = (i - 1) + best[0]
        pj = -best[1]
        last[i] = pre[i] - pj
        key = last[i] + pre[i]
        fw.upd(bisect.bisect_left(uniq, key) + 1, (dp[i] - i, -pre[i]))
    return dp[m]


def main():
    q = int(input().strip())
    for _ in range(q):
        m = int(input().strip())
        h = list(map(int, input().split()))
        print(min_ops(h))


if __name__ == "__main__":
    main()
