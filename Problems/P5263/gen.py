# -*- coding: utf-8 -*-
"""P5263 测试数据生成。"""

from __future__ import annotations

import random
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))
from std import min_bottleneck

DATA = ROOT / "data"
SEED = 526320260819
RNG = random.Random(SEED)

N_MAX = 128
M_MAX = 128
V_MAX = 1000


def solve_dp(layers, m):
    n = len(layers)
    pref = [0]
    for x in layers:
        pref.append(pref[-1] + x)

    def seg(l, r):
        return pref[r + 1] - pref[l]

    INF = 10 ** 18
    dp = [[INF] * (m + 1) for _ in range(n)]
    for i in range(n):
        dp[i][1] = seg(0, i)
    for j in range(2, m + 1):
        for i in range(j - 1, n):
            best = INF
            for p in range(j - 2, i):
                best = min(best, max(dp[p][j - 1], seg(p + 1, i)))
            dp[i][j] = best
    return dp[n - 1][m]


def brute(layers, m):
    n = len(layers)
    INF = 10 ** 18

    def go(pos, segs_left, cur_max):
        if segs_left == 1:
            return max(cur_max, sum(layers[pos:]))
        best = INF
        s = 0
        for i in range(pos, n - segs_left + 1):
            s += layers[i]
            best = min(best, go(i + 1, segs_left - 1, max(cur_max, s)))
        return best

    return go(0, m, 0)


def fmt_in(layers, m):
    return f"{len(layers)}\n{' '.join(map(str, layers))}\n{m}"


def fmt_out(ans):
    return f"{ans}\n"


def validate(layers, m):
    n = len(layers)
    assert 1 <= n <= N_MAX
    assert 1 <= m <= n
    assert all(1 <= x <= V_MAX for x in layers)


def write_pair(idx, layers, m):
    DATA.mkdir(parents=True, exist_ok=True)
    validate(layers, m)
    ans = min_bottleneck(layers, m)
    if len(layers) <= 16:
        b = brute(layers, m)
        d = solve_dp(layers, m)
        if ans != b or ans != d:
            raise RuntimeError(f"{idx}: std={ans} brute={b} dp={d}")
    tin = fmt_in(layers, m)
    tout = fmt_out(ans)
    if tin.endswith("\n"):
        raise RuntimeError(f"{idx}.in trailing newline")
    if not tout.endswith("\n") or tout.endswith("\n\n"):
        raise RuntimeError(f"{idx}.out bad newline")
    (DATA / f"{idx}.in").write_bytes(tin.encode("utf-8"))
    (DATA / f"{idx}.out").write_bytes(tout.encode("utf-8"))
    return ans


def rand_case(n, m):
    layers = [RNG.randint(1, V_MAX) for _ in range(n)]
    return layers, m


def main():
    cases = []
    cases.append(([3, 1, 4, 1, 5], 2))
    cases.append(([10, 20, 30, 40], 2))
    cases.append(([5], 1))
    cases.append(([1000, 1, 1, 1], 2))
    cases.append(([1, 1, 1, 1, 1, 1, 1, 1], 4))
    cases.append(rand_case(12, 3))
    cases.append(([500, 500, 500, 500], 2))
    cases.append(([7, 3, 9, 2, 8, 4, 6], 3))
    cases.append(rand_case(N_MAX, 64))
    cases.append(( [RNG.randint(1, V_MAX) for _ in range(N_MAX)], N_MAX ))

    assert len(cases) == 10
    for i, item in enumerate(cases, 1):
        layers, m = item
        ans = write_pair(i, layers, m)
        print(f"{i}.in n={len(layers)} m={m} ans={ans}")


if __name__ == "__main__":
    main()
