import math
import sys


def merge(a, b):
    mx_a, wd_a, sv_a = a
    mx_b, wd_b, sv_b = b
    mx = mx_a if mx_a >= mx_b else mx_b
    ea = math.exp(mx_a - mx)
    eb = math.exp(mx_b - mx)
    return mx, wd_a * ea + wd_b * eb, sv_a * ea + sv_b * eb


class SegTree:
    __slots__ = ("n", "size", "tree")

    def __init__(self, blocks):
        self.n = len(blocks)
        self.size = 1
        while self.size < self.n:
            self.size <<= 1
        self.tree = [(0.0, 0.0, 0.0)] * (2 * self.size)
        off = self.size
        for i, st in enumerate(blocks):
            self.tree[off + i] = st
        for i in range(self.size - 1, 0, -1):
            self.tree[i] = merge(self.tree[i * 2], self.tree[i * 2 + 1])

    def update(self, pos, val):
        i = self.size + pos
        self.tree[i] = val
        i //= 2
        tree = self.tree
        while i:
            tree[i] = merge(tree[i * 2], tree[i * 2 + 1])
            i //= 2

    def query(self, l, r):
        l += self.size
        r += self.size
        left = right = None
        tree = self.tree
        while l <= r:
            if l & 1:
                left = tree[l] if left is None else merge(left, tree[l])
                l += 1
            if not (r & 1):
                right = tree[r] if right is None else merge(tree[r], right)
                r -= 1
            l //= 2
            r //= 2
        if left is None:
            return right
        if right is None:
            return left
        return merge(left, right)


def main():
    data = sys.stdin.buffer.read().split()
    it = iter(data)
    B = int(next(it))
    Q = int(next(it))
    blocks = []
    for _ in range(B):
        blocks.append((float(next(it)), float(next(it)), float(next(it))))
    seg = SegTree(blocks)
    out = []
    append = out.append
    for _ in range(Q):
        op = next(it).decode()
        if op == "1":
            i = int(next(it)) - 1
            st = float(next(it)), float(next(it)), float(next(it))
            seg.update(i, st)
        else:
            l = int(next(it)) - 1
            r = int(next(it)) - 1
            mx, wd, sv = seg.query(l, r)
            append(f"{sv / wd:.6f}")
    sys.stdout.write("\n".join(out))


if __name__ == "__main__":
    main()
