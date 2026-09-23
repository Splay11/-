import sys

input = sys.stdin.readline


class SegmentTree:
    __slots__ = ("n", "mx", "lazy")

    def __init__(self, arr):
        self.n = len(arr) - 1
        size = self.n * 4
        self.mx = arr[:] + [0] * (size - len(arr))
        self.lazy = [0] * size
        self._build(1, 1, self.n, arr)

    def _build(self, node, l, r, arr):
        if l == r:
            self.mx[node] = arr[l]
            return
        mid = (l + r) >> 1
        self._build(node << 1, l, mid, arr)
        self._build((node << 1) | 1, mid + 1, r, arr)
        self.mx[node] = max(self.mx[node << 1], self.mx[(node << 1) | 1])

    def _push(self, node):
        tag = self.lazy[node]
        if tag:
            for ch in (node << 1, (node << 1) | 1):
                self.mx[ch] += tag
                self.lazy[ch] += tag
            self.lazy[node] = 0

    def range_add(self, node, l, r, ql, qr, val):
        if ql <= l and r <= qr:
            self.mx[node] += val
            self.lazy[node] += val
            return
        self._push(node)
        mid = (l + r) >> 1
        if ql <= mid:
            self.range_add(node << 1, l, mid, ql, qr, val)
        if qr > mid:
            self.range_add((node << 1) | 1, mid + 1, r, ql, qr, val)
        self.mx[node] = max(self.mx[node << 1], self.mx[(node << 1) | 1])

    def query_max(self):
        return self.mx[1]


def solve_case(n, h, sigma, tau):
    seq = [0] * (n + 1)
    pos_sigma = [0] * (n + 1)
    for i in range(1, n + 1):
        seq[i] = h[sigma[i]]
        pos_sigma[sigma[i]] = i

    pre = [0] * (n + 1)
    for i in range(1, n + 1):
        pre[i] = pre[i - 1] + seq[i]

    seg = SegmentTree(pre)
    ans = max(0, seg.query_max())

    for i in range(1, n + 1):
        idx = tau[i]
        p = pos_sigma[idx]
        v = h[idx]
        seg.range_add(1, 1, n, p, n, -v)
        cur = seg.query_max()
        if cur > ans:
            ans = cur

    return ans


def main():
    t = int(input())
    out = []
    for _ in range(t):
        n = int(input())
        h = [0] + list(map(int, input().split()))
        sigma = [0] + list(map(int, input().split()))
        tau = [0] + list(map(int, input().split()))
        out.append(str(solve_case(n, h, sigma, tau)))
    sys.stdout.write("\n".join(out))


if __name__ == "__main__":
    main()
