# -*- coding: utf-8 -*-
"""生成 P5256 data/*.in/*.out。.in 无行末多余换行；.out 恰一换行。"""

from __future__ import annotations

import random
from bisect import bisect_right
from pathlib import Path

ROOT = Path(__file__).resolve().parent
DATA = ROOT / "data"
N_MAX = 250000
T_MAX = 10**9
V_MAX = 10**9
SEED = 525620260816
RNG = random.Random(SEED)


def solve(jobs: list[tuple[int, int, int]]) -> int:
    jobs = sorted(jobs, key=lambda x: x[1])
    n = len(jobs)
    ends = [e for _s, e, _v in jobs]
    dp = [0] * (n + 1)
    for i in range(1, n + 1):
        s, _e, v = jobs[i - 1]
        k = bisect_right(ends, s, hi=i - 1)
        take = dp[k] + v
        skip = dp[i - 1]
        dp[i] = take if take > skip else skip
    return dp[n]


def brute(jobs: list[tuple[int, int, int]]) -> int:
    n = len(jobs)
    best = 0
    for mask in range(1 << n):
        sel = [jobs[i] for i in range(n) if mask >> i & 1]
        sel.sort()
        ok = True
        tot = 0
        last = -1
        for s, e, v in sel:
            if s < last:
                ok = False
                break
            last = e
            tot += v
        if ok and tot > best:
            best = tot
    return best


def fmt_in(jobs: list[tuple[int, int, int]]) -> str:
    lines = [str(len(jobs))]
    lines.extend(f"{s} {e} {v}" for s, e, v in jobs)
    return "\n".join(lines)


def write_pair(idx: int, jobs: list[tuple[int, int, int]]) -> int:
    DATA.mkdir(parents=True, exist_ok=True)
    n = len(jobs)
    assert 1 <= n <= N_MAX
    for s, e, v in jobs:
        assert 0 <= s < e <= T_MAX and 1 <= v <= V_MAX
    ans = solve(jobs)
    if n <= 18:
        b = brute(jobs)
        if b != ans:
            raise RuntimeError(f"case {idx}: brute {b} != {ans}")
    tin = fmt_in(jobs)
    tout = f"{ans}\n"
    if tin.endswith("\n"):
        raise RuntimeError(f"case {idx}: .in ends with newline")
    if not tout.endswith("\n") or tout.endswith("\n\n"):
        raise RuntimeError(f"case {idx}: bad .out newline")
    (DATA / f"{idx}.in").write_bytes(tin.encode("utf-8"))
    (DATA / f"{idx}.out").write_bytes(tout.encode("utf-8"))
    return ans


def rand_jobs(n: int, tspan: int, vmax: int) -> list[tuple[int, int, int]]:
    jobs = []
    for _ in range(n):
        s = RNG.randint(0, tspan - 1)
        e = RNG.randint(s + 1, tspan)
        v = RNG.randint(1, vmax)
        jobs.append((s, e, v))
    return jobs


def main() -> None:
    cases: list[list[tuple[int, int, int]]] = []

    # 1-2 改写样例
    cases.append([(0, 2, 10), (2, 4, 20), (1, 3, 100)])
    cases.append([(5, 9, 8), (0, 4, 3), (4, 5, 1), (8, 10, 2)])

    # 3 原样例：卡把相接当冲突
    cases.append([(1, 3, 50), (2, 5, 40), (4, 6, 70), (6, 7, 30), (7, 9, 60)])

    # 4 边界 n=1
    cases.append([(0, 1, 1)])

    # 5 全部重叠，选最大收益
    cases.append([(0, 10, 5), (1, 9, 8), (2, 8, 100), (3, 7, 9)])

    # 6 相接链
    cases.append([(0, 1, 5), (1, 2, 5), (2, 3, 5)])

    # 7 长区间收益大，短区间相接收益更大
    cases.append([(0, 10, 100), (0, 3, 40), (3, 6, 40), (6, 10, 40)])

    # 8 随机小数据
    cases.append(rand_jobs(16, 40, 100))

    # 9 压力：满长相接，收益 1e9，测 64 位
    n9 = N_MAX
    cases.append([(i, i + 1, V_MAX) for i in range(n9)])

    # 10 压力：随机
    cases.append(rand_jobs(N_MAX, T_MAX, V_MAX))

    assert len(cases) == 10
    for i, jobs in enumerate(cases, 1):
        ans = write_pair(i, jobs)
        print(f"{i}.in n={len(jobs)} ans={ans}")


if __name__ == "__main__":
    main()
