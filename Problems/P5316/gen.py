# -*- coding: utf-8 -*-
"""P5316 造数：扫描线维护稀释上界 / 回灌下界。"""
import os
import random
import heapq
from collections import defaultdict

DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data")
os.makedirs(DIR, exist_ok=True)


class LazyHeap:
    def __init__(self, want_max):
        self.h = []
        self.cnt = defaultdict(int)
        self.want_max = want_max

    def add(self, x):
        if self.want_max:
            x = -x
        heapq.heappush(self.h, x)
        self.cnt[x] += 1

    def remove(self, x):
        if self.want_max:
            x = -x
        self.cnt[x] -= 1

    def top(self):
        while self.h and self.cnt[self.h[0]] == 0:
            heapq.heappop(self.h)
        if not self.h:
            return None
        x = self.h[0]
        if self.want_max:
            return -x
        return x


def solve(w, v, caps, floors):
    add_c = [[] for _ in range(w + 2)]
    del_c = [[] for _ in range(w + 2)]
    for L, R, c in caps:
        add_c[L].append(c)
        del_c[R + 1].append(c)
    add_d = [[] for _ in range(w + 2)]
    del_d = [[] for _ in range(w + 2)]
    for L, R, d in floors:
        add_d[L].append(d)
        del_d[R + 1].append(d)
    hc = LazyHeap(False)
    hd = LazyHeap(True)
    inf = 10 ** 18
    e = [0] * w
    for i in range(1, w + 1):
        for x in del_c[i]:
            hc.remove(x)
        for x in add_c[i]:
            hc.add(x)
        for x in del_d[i]:
            hd.remove(x)
        for x in add_d[i]:
            hd.add(x)
        hi = hc.top()
        if hi is None:
            hi = inf
        lo = hd.top()
        if lo is None:
            lo = 0
        val = v[i - 1]
        if val < lo:
            val = lo
        if val > hi:
            val = hi
        e[i - 1] = val
    return e


def write_file(idx, w, v, caps, floors):
    assert 1 <= w <= 200000
    assert 0 <= len(caps) <= 200000
    assert 0 <= len(floors) <= 200000
    assert len(v) == w
    for x in v:
        assert 0 <= x <= 10 ** 9
    for L, R, c in caps:
        assert 1 <= L <= R <= w
        assert 0 <= c <= 10 ** 9
    for L, R, d in floors:
        assert 1 <= L <= R <= w
        assert 0 <= d <= 10 ** 9
    lines = ["%d %d %d" % (w, len(caps), len(floors))]
    lines.append(" ".join(str(x) for x in v))
    for L, R, c in caps:
        lines.append("%d %d %d" % (L, R, c))
    for L, R, d in floors:
        lines.append("%d %d %d" % (L, R, d))
    e = solve(w, v, caps, floors)
    out = " ".join(str(z) for z in e)
    with open(os.path.join(DIR, "%d.in" % idx), "w", encoding="utf-8", newline="\n") as f:
        f.write("\n".join(lines))
    with open(os.path.join(DIR, "%d.out" % idx), "w", encoding="utf-8", newline="\n") as f:
        f.write(out + "\n")


def rnd_seg(rng, w, vmax):
    L = rng.randint(1, w)
    R = rng.randint(L, w)
    return (L, R, rng.randint(0, vmax))


def main():
    rng = random.Random(53161)

    write_file(1, 4, [2, 9, 1, 6], [(2, 4, 5)], [(1, 2, 4)])
    write_file(2, 3, [1, 0, 7], [], [])
    write_file(3, 3, [5, 5, 5], [(1, 3, 2)], [(1, 3, 8)])
    # 4 重叠稀释取最小上界
    write_file(4, 5, [9, 9, 9, 9, 9], [(1, 4, 7), (2, 5, 3)], [])
    # 5 重叠回灌取最大下界
    write_file(5, 5, [0, 0, 0, 0, 0], [], [(1, 3, 2), (2, 5, 6)])
    # 6 单点指令 + 重复上界
    write_file(6, 4, [1, 8, 3, 4], [(2, 2, 5), (2, 2, 5)], [(3, 4, 2)])
    # 7 全覆盖与空覆盖交错
    write_file(7, 6, [4, 0, 9, 1, 2, 8], [(1, 6, 10)], [(4, 4, 7)])
    # 8 随机中等
    w = 30
    caps = [rnd_seg(rng, w, 100) for _ in range(12)]
    floors = [rnd_seg(rng, w, 100) for _ in range(12)]
    write_file(8, w, [rng.randint(0, 100) for _ in range(w)], caps, floors)
    # 9 大数据
    w = 70000
    x = y = 65000
    caps = [rnd_seg(rng, w, 10 ** 9) for _ in range(x)]
    floors = [rnd_seg(rng, w, 10 ** 9) for _ in range(y)]
    write_file(9, w, [rng.randint(0, 10 ** 9) for _ in range(w)], caps, floors)
    # 10 最大规模
    w = 200000
    write_file(
        10,
        w,
        [rng.randint(0, 10 ** 9) for _ in range(w)],
        [(1, w, 10 ** 9)],
        [(1, w, 0)],
    )


if __name__ == "__main__":
    main()
