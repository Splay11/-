# -*- coding: utf-8 -*-
"""P7007 测试数据生成。约束对齐题面_改写.md：k<=1000, n<=1200, 1<=v_i<=250。"""

from __future__ import annotations

import random
from pathlib import Path

ROOT = Path(__file__).resolve().parent
DATA = ROOT / "data"
SEED = 700720260818
RNG = random.Random(SEED)

K_MAX = 1000
N_MIN, N_MAX = 2, 1200
V_MIN, V_MAX = 1, 250


def can_reduce(vals: list[int]) -> bool:
    lo = min(vals)
    hi = max(vals)
    seen = [False] * (hi - lo + 1)
    for x in vals:
        seen[x - lo] = True
    return all(seen)


def brute(vals: list[int]) -> bool:
    """指数搜索：操作只依赖多重集。n<=8。"""

    def rec(t: tuple[int, ...]) -> bool:
        if len(t) == 1:
            return True
        s = list(t)
        n = len(s)
        tried = set()
        for i in range(n):
            for j in range(i + 1, n):
                if abs(s[i] - s[j]) > 1:
                    continue
                drop = i if s[i] >= s[j] else j
                nxt = tuple(sorted(s[p] for p in range(n) if p != drop))
                if nxt in tried:
                    continue
                tried.add(nxt)
                if rec(nxt):
                    return True
        return False

    return rec(tuple(vals))


def fmt_in(cases: list[list[int]]) -> str:
    lines = [str(len(cases))]
    for vals in cases:
        lines.append(str(len(vals)))
        lines.append(" ".join(str(x) for x in vals))
    return "\n".join(lines)


def fmt_out(cases: list[list[int]]) -> str:
    answers = [("YES" if can_reduce(v) else "NO") for v in cases]
    return "\n".join(answers) + "\n"


def validate_case(vals: list[int]) -> None:
    assert N_MIN <= len(vals) <= N_MAX
    assert all(V_MIN <= x <= V_MAX for x in vals)


def write_pair(idx: int, cases: list[list[int]]) -> None:
    DATA.mkdir(parents=True, exist_ok=True)
    assert 1 <= len(cases) <= K_MAX
    for vals in cases:
        validate_case(vals)
        if idx <= 8 and len(vals) <= 8:
            a, b = can_reduce(vals), brute(vals)
            if a != b:
                raise RuntimeError(f"case {idx}: std={a} brute={b} vals={vals}")
    tin = fmt_in(cases)
    tout = fmt_out(cases)
    if tin.endswith("\n"):
        raise RuntimeError(f"{idx}.in 末尾有换行")
    if not tout.endswith("\n") or tout.endswith("\n\n"):
        raise RuntimeError(f"{idx}.out 换行不合法")
    (DATA / f"{idx}.in").write_bytes(tin.encode("utf-8"))
    (DATA / f"{idx}.out").write_bytes(tout.encode("utf-8"))


def yes_consecutive(n: int, lo: int | None = None, hi: int | None = None) -> list[int]:
    """填满 [lo,hi] 后用区间内随机值补到 n。"""
    if lo is None:
        span = RNG.randint(0, min(n - 1, V_MAX - V_MIN))
        lo = RNG.randint(V_MIN, V_MAX - span)
        hi = lo + span
    need = hi - lo + 1
    if n < need:
        n = need
    vals = list(range(lo, hi + 1))
    while len(vals) < n:
        vals.append(RNG.randint(lo, hi))
    RNG.shuffle(vals)
    return vals


def no_gap(n: int) -> list[int]:
    """在 [lo,hi] 中挖掉至少一个内部值。"""
    span = RNG.randint(2, min(12, V_MAX - V_MIN))
    lo = RNG.randint(V_MIN, V_MAX - span)
    hi = lo + span
    gap = RNG.randint(lo + 1, hi - 1)
    pool = [x for x in range(lo, hi + 1) if x != gap]
    vals = [lo, hi]
    while len(vals) < n:
        vals.append(RNG.choice(pool))
    RNG.shuffle(vals)
    return vals


def two_blocks(n: int) -> list[int]:
    """两段分离值域，卡「存在可操作对就判 YES」。"""
    a1, b1 = 1, RNG.randint(2, 6)
    a2, b2 = 20, RNG.randint(21, 28)
    left_n = n // 2
    right_n = n - left_n
    left = yes_consecutive(max(left_n, b1 - a1 + 1), a1, b1)[:left_n]
    right = yes_consecutive(max(right_n, b2 - a2 + 1), a2, b2)[:right_n]
    while len(left) < left_n:
        left.append(RNG.randint(a1, b1))
    while len(right) < right_n:
        right.append(RNG.randint(a2, b2))
    vals = left + right
    RNG.shuffle(vals)
    return vals


def shuffled_consecutive_not_adj(n: int = 3) -> list[int]:
    """下标不相邻才能配对，卡「只能操作相邻位置」。"""
    vals = list(range(1, n + 1))
    # 刻意做成「相邻下标差值 > 1」的排列，例如 3,1,2
    if n == 3:
        return [3, 1, 2]
    RNG.shuffle(vals)
    return vals


def rand_small(n: int) -> list[int]:
    vmax = RNG.choice([5, 10, 20, 50, 250])
    return [RNG.randint(V_MIN, vmax) for _ in range(n)]


def main() -> None:
    groups: list[list[list[int]]] = []

    # 1 改写题面示例 1
    groups.append([[2, 3, 4], [5, 7], [1, 2, 2, 3, 3, 4]])

    # 2 改写题面示例 2 + 基础最小路径
    groups.append(
        [
            [8, 8, 10, 9],
            [1, 1, 3],
            [1, 1],
            [1, 2],
            [1, 3],
            [7, 7, 7],
        ]
    )

    # 3 边界：n=2 / 全相同 / 值域两端
    groups.append(
        [
            [250, 250],
            [1, 250],
            [249, 250],
            [1, 1, 1, 1],
            [100, 101, 102, 103],
            [100, 102, 103],
        ]
    )

    # 4 边界：单点缺口、覆盖满值域、重复堆在一端
    groups.append(
        [
            yes_consecutive(12, 1, 5),
            [1, 2, 3, 5, 5, 5],
            [10] * 8,
            yes_consecutive(15, 240, 250),
            no_gap(10),
        ]
    )

    # 5 随机小数据（可对拍）
    groups.append([rand_small(RNG.randint(2, 8)) for _ in range(12)])

    # 6 hack：必须跨下标配对；乱序连续段
    groups.append(
        [
            [3, 1, 2],
            [4, 1, 3, 2],
            [5, 1, 4, 2, 3],
            [2, 4, 6, 3, 5, 1],
            [9, 7, 8],
            [4, 2, 4, 3, 2],
        ]
    )

    # 7 hack：max-min>1 仍 YES；存在一对可操作但整体 NO
    groups.append(
        [
            [1, 2, 3, 4, 5],
            [1, 2, 4],
            [1, 2, 2, 4, 4],
            [10, 11, 12, 13],
            [10, 11, 13, 14],
            [6, 8, 7, 9, 10],
        ]
    )

    # 8 构造：两段分离、中间缺口、全值域稀疏/稠密
    groups.append(
        [
            two_blocks(16),
            no_gap(20),
            yes_consecutive(20, 1, 20),
            [1, 3, 5, 7, 9],
            [2, 2, 4, 4, 6, 6],
            yes_consecutive(18, 100, 110),
        ]
    )

    # 9 大数据：接近 k 上限，中等 n，YES/NO 混合
    g9: list[list[int]] = []
    for i in range(K_MAX):
        n = RNG.randint(8, 40)
        if i % 3 == 0:
            g9.append(yes_consecutive(n))
        elif i % 3 == 1:
            g9.append(no_gap(n))
        else:
            g9.append(two_blocks(n))
    groups.append(g9)

    # 10 大数据：n 拉满，k 取满，压 I/O 与线性扫描
    g10: list[list[int]] = []
    for i in range(K_MAX):
        n = N_MAX
        if i % 4 == 0:
            g10.append(yes_consecutive(n, 1, 250))
        elif i % 4 == 1:
            g10.append(no_gap(n))
        elif i % 4 == 2:
            g10.append(two_blocks(n))
        else:
            g10.append([RNG.randint(1, 250) for _ in range(n)])
    groups.append(g10)

    assert len(groups) == 10
    for i, cases in enumerate(groups, 1):
        write_pair(i, cases)
        yes_cnt = sum(1 for v in cases if can_reduce(v))
        print(f"{i}.in k={len(cases)} yes={yes_cnt} no={len(cases) - yes_cnt}")


if __name__ == "__main__":
    main()
