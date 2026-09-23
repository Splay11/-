# -*- coding: utf-8 -*-
"""P5259 测试数据。约束对齐题面_改写.md。"""

from __future__ import annotations

import math
import random
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))
from std import MOD, solve

DATA = ROOT / "data"
SEED = 525920260818
RNG = random.Random(SEED)

K_MAX = 120
X_MAX = 100000
R_MAX = 10**18


def brute(x, y, left, right):
    s = 0
    for i in range(left, right + 1):
        s += math.gcd(x + i, y + i)
    return s % MOD


def fmt_in(qs):
    lines = [str(len(qs))]
    for x, y, s, t in qs:
        lines.append(f"{x} {y} {s} {t}")
    return "\n".join(lines)


def fmt_out(qs):
    return "".join(str(solve(x, y, s, t)) + "\n" for x, y, s, t in qs)


def validate(qs):
    assert 1 <= len(qs) <= K_MAX
    for x, y, s, t in qs:
        assert 1 <= x <= X_MAX and 1 <= y <= X_MAX
        assert 0 <= s <= t <= R_MAX


def write_pair(idx, qs):
    DATA.mkdir(parents=True, exist_ok=True)
    validate(qs)
    for x, y, s, t in qs:
        if t - s <= 2000:
            a, b = solve(x, y, s, t), brute(x, y, s, t)
            if a != b:
                raise RuntimeError(f"{idx}: {x,y,s,t} std={a} brute={b}")
    tin = fmt_in(qs)
    tout = fmt_out(qs)
    if tin.endswith("\n"):
        raise RuntimeError(f"{idx}.in 末尾有换行")
    if not tout.endswith("\n") or tout.endswith("\n\n"):
        raise RuntimeError(f"{idx}.out 换行不合法")
    (DATA / f"{idx}.in").write_bytes(tin.encode("utf-8"))
    (DATA / f"{idx}.out").write_bytes(tout.encode("utf-8"))


def rand_q(small=True):
    x = RNG.randint(1, 200 if small else X_MAX)
    y = RNG.randint(1, 200 if small else X_MAX)
    if small:
        s = RNG.randint(0, 50)
        t = RNG.randint(s, s + 80)
    else:
        s = RNG.randint(0, 10**12)
        span = RNG.choice([0, 1, 10**6, 10**12, R_MAX - s])
        t = min(R_MAX, s + span)
    return (x, y, s, t)


def main():
    groups = []

    # 1 改写样例 1
    groups.append([(8, 14, 0, 2), (5, 5, 1, 3), (3, 9, 0, 4)])
    # 2 改写样例 2
    groups.append([(2, 10, 0, 0), (7, 11, 2, 5)])
    # 3 原样例（隐藏）+ 边界 l=r
    groups.append([(10, 12, 0, 3), (4, 9, 1, 3), (1, 7, 1, 3), (6, 20, 5, 8), (9, 1, 7, 7)])
    # 4 D=0 等差
    groups.append([(1, 1, 0, 0), (100000, 100000, 0, 10), (7, 7, 3, 9), (12345, 12345, 0, 100)])
    # 5 边界：s=0、单点、x>y
    groups.append([(1, 2, 0, 0), (100000, 1, 0, 5), (2, 1, 0, 8), (99999, 100000, 0, 20)])
    # 6 随机小，可对拍
    groups.append([rand_q(True) for _ in range(20)])
    # 7 hack：把区间当成 s..t 而不是 (x+s)..(x+t)；以及漏 D=0
    groups.append(
        [
            (50, 80, 0, 30),
            (50, 50, 0, 30),
            (1, 60, 10, 40),
            (90, 10, 0, 25),
        ]
    )
    # 8 约数多的 D + 中等区间
    groups.append(
        [
            (1, 55440, 0, 5000),
            (100, 100 + 83160, 0, 2000) if 100 + 83160 <= X_MAX else (1, 83160, 0, 2000),
            (2, 75600, 100, 3000),
            (3, 92400, 0, 1000),
        ]
    )

    # 9 接近 k 上限，混合大 r
    g9 = []
    for i in range(K_MAX):
        if i % 5 == 0:
            x = RNG.randint(1, X_MAX)
            g9.append((x, x, RNG.randint(0, 10), R_MAX))
        elif i % 5 == 1:
            g9.append((RNG.randint(1, X_MAX), RNG.randint(1, X_MAX), 0, R_MAX))
        else:
            g9.append(rand_q(False))
    groups.append(g9)

    # 10 极限：满 k、满 a/b、r=1e18
    g10 = []
    hc = [55440, 72072, 75600, 83160, 92400, 50400, 27720, 25200]
    for i in range(K_MAX):
        if i < len(hc):
            d = hc[i]
            x = 1
            y = min(X_MAX, 1 + d)
            g10.append((x, y, 0, R_MAX))
        elif i % 3 == 0:
            x = X_MAX
            g10.append((x, x, 0, R_MAX))
        else:
            g10.append((RNG.randint(1, X_MAX), RNG.randint(1, X_MAX), 0, R_MAX))
    groups.append(g10)

    assert len(groups) == 10
    for i, qs in enumerate(groups, 1):
        write_pair(i, qs)
        print(f"{i}.in k={len(qs)}")


if __name__ == "__main__":
    main()
