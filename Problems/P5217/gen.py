# -*- coding: utf-8 -*-
"""生成 P5217 data/*.in/*.out。.in 无行末多余换行；.out 恰一换行。"""

from __future__ import annotations

import math
import random
from pathlib import Path

SEED = 521720260806
RNG = random.Random(SEED)
ROOT = Path(__file__).resolve().parent
DATA = ROOT / "data"
MOD = 10**9 + 7
N_MAX = 200_000


def cycle_period(chars: list[str]) -> int:
    m = len(chars)
    for d in range(1, m + 1):
        if m % d != 0:
            continue
        if all(chars[i] == chars[i % d] for i in range(m)):
            return d
    return m


def solve(n: int, u: str, p0: list[int]) -> int:
    vis = [False] * n
    ans = 1
    for i in range(n):
        if vis[i]:
            continue
        cycle = []
        x = i
        while not vis[x]:
            vis[x] = True
            cycle.append(u[x])
            x = p0[x]
        per = cycle_period(cycle)
        ans = ans // math.gcd(ans, per) * per
    return ans % MOD


def fmt_in(n: int, u: str, p1: list[int]) -> str:
    return f"{n}\n{u}\n" + " ".join(map(str, p1))


def fmt_out(ans: int) -> str:
    return f"{ans}\n"


def perm_from_cycles(n: int, cycles: list[list[int]]) -> list[int]:
    """cycles 为 0-based 环列表，返回 0-based 置换。"""
    p = list(range(n))
    used = set()
    for cyc in cycles:
        for x in cyc:
            assert x not in used
            used.add(x)
        for i, x in enumerate(cyc):
            p[x] = cyc[(i + 1) % len(cyc)]
    for i in range(n):
        if i not in used:
            p[i] = i
    return p


def random_perm(n: int) -> list[int]:
    p = list(range(n))
    RNG.shuffle(p)
    return p


def build_cases() -> list[tuple[str, str, str]]:
    cases: list[tuple[str, str, str]] = []

    def add(desc: str, u: str, p0: list[int]) -> None:
        n = len(u)
        assert n == len(p0)
        assert sorted(p0) == list(range(n))
        assert all("a" <= c <= "z" for c in u)
        ans = solve(n, u, p0)
        p1 = [x + 1 for x in p0]
        cases.append((desc, fmt_in(n, u, p1), fmt_out(ans)))

    # 1-3 样例
    add("样例1：二元交换", "xy", [1, 0])
    add("样例2：环上全相同，周期 1", "zzz", [1, 2, 0])
    add("样例3：单环、字符近乎互异", "hello", [1, 2, 3, 4, 0])

    # 4 最小
    add("边界：n=1", "a", [0])

    # 5 恒等置换
    add("构造：恒等置换，答案 1", "abcde", [0, 1, 2, 3, 4])

    # 6 hack：环长与字符串周期不同（重复块）
    # 环 (0..5)，串 abcabc，周期 3 而非 6
    add(
        "hack：环长 6 但串周期 3（卡只取环长）",
        "abcabc",
        [1, 2, 3, 4, 5, 0],
    )

    # 7 多环 LCM
    # 环长 4 串 abcd 周期4；环长 6 串 aaaaaa 周期1；环长 3 串 xyz 周期3 → lcm=12
    u7 = ["?"] * 13
    # cycles: [0,1,2,3]=abcd, [4,5,6,7,8,9]=aaaaaa, [10,11,12]=xyz
    for i, ch in enumerate("abcd"):
        u7[i] = ch
    for i in range(4, 10):
        u7[i] = "a"
    for i, ch in enumerate("xyz"):
        u7[10 + i] = ch
    p7 = perm_from_cycles(
        13,
        [
            [0, 1, 2, 3],
            [4, 5, 6, 7, 8, 9],
            [10, 11, 12],
        ],
    )
    add("构造：多环 LCM", "".join(u7), p7)

    # 8 小随机
    n8 = 40
    u8 = "".join(RNG.choice("abcde") for _ in range(n8))
    add("随机小数据 n=40", u8, random_perm(n8))

    # 9 大数据：单大环 + 有真周期，卡复杂度与只取 n
    n9 = N_MAX
    block = "abcde"
    # 构造长度 n9 且周期为 len(block) 的串（n9 % 5 == 0）
    assert n9 % len(block) == 0
    u9 = (block * (n9 // len(block)))
    p9 = [(i + 1) % n9 for i in range(n9)]
    add("大数据：单环 n=2e5，串周期 5", u9, p9)

    # 10 大数据：许多小环，LCM 很大需取模；含全同环
    n10 = N_MAX
    # 用质数环长堆积 LCM
    primes = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47]
    cycles = []
    cur = 0
    u_chars = ["a"] * n10
    for pr in primes:
        cyc = list(range(cur, cur + pr))
        # 互异字符使周期=环长
        for j, idx in enumerate(cyc):
            u_chars[idx] = chr(ord("a") + (j % 26))
        # 若环长>26 可能周期变小，对质数环长>26 用互异不够；
        # 对 >26 的质数，强制周期=pr：用位置相关且保证最小周期为 pr
        # 简单做法：前 pr 个用不同模式 —— 对质数，只要不是全同，周期必为 pr（因周期|pr）
        # 若 pr>26，字母会重复，但仍可能周期为1仅当全同；质数只有1和自身，非全同则周期=pr
        cycles.append(cyc)
        cur += pr
    # 剩余做成全 a 的若干环与单点，周期1
    while cur < n10:
        # 尽量切成长度 1
        cycles.append([cur])
        cur += 1
    p10 = perm_from_cycles(n10, cycles)
    add("大数据：多质数环 LCM 取模 + 剩余单点", "".join(u_chars), p10)

    assert len(cases) == 10
    return cases


def write_cases(cases: list[tuple[str, str, str]]) -> None:
    DATA.mkdir(parents=True, exist_ok=True)
    tags = [
        ("样例", "无"),
        ("样例", "无"),
        ("样例", "无"),
        ("边界", "未处理 n=1"),
        ("构造", "恒等时输出 0"),
        ("hack", "直接对环长取 LCM"),
        ("构造", "多环不会求 LCM"),
        ("随机", "实现错误"),
        ("压力", "O(n^2)；只输出 n"),
        ("压力", "LCM 溢出未取模"),
    ]
    lines = [
        "# P5217 测试数据说明",
        "",
        "算法核：置换拆环 → 各环字符串最小旋转周期 → 全体 LCM，再模 $10^9+7$。",
        "",
        "| 编号 | 类型 | 说明 | 卡掉的错误解 |",
        "|---:|---|---|---|",
    ]
    for i, ((desc, tin, tout), (tag, hack)) in enumerate(zip(cases, tags), 1):
        (DATA / f"{i}.in").write_text(tin, encoding="utf-8")
        (DATA / f"{i}.out").write_text(tout, encoding="utf-8")
        lines.append(f"| {i} | {tag} | {desc} | {hack} |")
    lines.append("")
    lines.append(f"随机种子：`{SEED}`。")
    lines.append("")
    (DATA / "README.md").write_text("\n".join(lines) + "\n", encoding="utf-8")


def self_check(cases: list[tuple[str, str, str]]) -> None:
    for i, (_d, tin, tout) in enumerate(cases, 1):
        lines = tin.split("\n")
        n = int(lines[0])
        u = lines[1]
        p1 = list(map(int, lines[2].split()))
        p0 = [x - 1 for x in p1]
        got = solve(n, u, p0)
        expect = int(tout.strip())
        if got != expect:
            raise RuntimeError(f"case {i}: {got} != {expect}")
        if tin.endswith("\n"):
            raise RuntimeError(f"case {i}: .in ends with newline")
        if not tout.endswith("\n") or tout.endswith("\n\n"):
            raise RuntimeError(f"case {i}: bad .out newline")


def main() -> None:
    cases = build_cases()
    self_check(cases)
    write_cases(cases)
    print("generated 10 cases OK")
    for i in range(1, 11):
        print(i, (DATA / f"{i}.out").read_text(encoding="utf-8").strip())


if __name__ == "__main__":
    main()
