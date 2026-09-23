# -*- coding: utf-8 -*-
"""生成 P5255 data/*.in/*.out。.in 无行末多余换行；.out 恰一换行。"""

from __future__ import annotations

import random
from pathlib import Path

ROOT = Path(__file__).resolve().parent
DATA = ROOT / "data"
N_MAX = 200000
SEED = 525520260816
RNG = random.Random(SEED)


def can_queue(u: str, v: str) -> bool:
    return u == v


def can_stack(u: str, v: str) -> bool:
    st: list[str] = []
    i = 0
    n = len(u)
    for c in v:
        while i < n and (not st or st[-1] != c):
            st.append(u[i])
            i += 1
        if not st or st[-1] != c:
            return False
        st.pop()
    return True


def solve(u: str, v: str) -> str:
    q = can_queue(u, v)
    s = can_stack(u, v)
    if q and s:
        return "both"
    if q:
        return "queue"
    if s:
        return "stack"
    return "neither"


def rand_letters(n: int) -> str:
    return "".join(RNG.choice("abcde") for _ in range(n))


def stack_pair_from(u: str) -> str:
    """由入站串随机交错压弹，生成栈可实现的出站串。"""
    n = len(u)
    st: list[str] = []
    v: list[str] = []
    i = 0
    while i < n or st:
        can_push = i < n
        can_pop = bool(st)
        if can_push and can_pop:
            if RNG.random() < 0.5:
                st.append(u[i])
                i += 1
            else:
                v.append(st.pop())
        elif can_push:
            st.append(u[i])
            i += 1
        else:
            v.append(st.pop())
    return "".join(v)


def fmt_in(u: str, v: str) -> str:
    return f"{u}\n{v}"


def write_pair(idx: int, u: str, v: str) -> str:
    DATA.mkdir(parents=True, exist_ok=True)
    assert len(u) == len(v)
    assert 1 <= len(u) <= N_MAX
    ans = solve(u, v)
    tin = fmt_in(u, v)
    tout = f"{ans}\n"
    if tin.endswith("\n"):
        raise RuntimeError(f"case {idx}: .in ends with newline")
    if not tout.endswith("\n") or tout.endswith("\n\n"):
        raise RuntimeError(f"case {idx}: bad .out newline")
    if solve(u, v) != ans:
        raise RuntimeError(f"case {idx}: self-check failed")
    (DATA / f"{idx}.in").write_bytes(tin.encode("utf-8"))
    (DATA / f"{idx}.out").write_bytes(tout.encode("utf-8"))
    return ans


def main() -> None:
    cases: list[tuple[str, str]] = []

    # 1-4 改写样例
    cases.append(("go", "go"))
    cases.append(("cat", "tac"))
    cases.append(("cat", "cta"))
    cases.append(("cat", "tca"))

    # 5 边界 n=1
    cases.append(("a", "a"))

    # 6 hack：U=V 但较长，卡输出 queue
    cases.append(("xyzxyz", "xyzxyz"))

    # 7 hack：重复字符的栈交错
    cases.append(("aab", "aba"))

    # 8 随机小数据：须通过贪心栈模拟，且 U!=V
    u8 = rand_letters(40)
    v8 = u8
    for _ in range(80):
        cand = stack_pair_from(u8)
        if cand != u8 and can_stack(u8, cand):
            v8 = cand
            break
    if v8 == u8:
        v8 = u8[::-1]
        if v8 == u8:
            u8, v8 = "abcd", "acdb"
    cases.append((u8, v8))

    # 9 压力：满长且 U=V → both
    u9 = rand_letters(N_MAX)
    cases.append((u9, u9))

    # 10 压力：满长 neither（前缀相同 + cab 模式）
    n10 = N_MAX
    prefix = "a" * (n10 - 3)
    u10 = prefix + "bcd"
    v10 = prefix + "dbc"
    cases.append((u10, v10))

    assert len(cases) == 10
    for i, (u, v) in enumerate(cases, 1):
        ans = write_pair(i, u, v)
        print(f"{i}.in n={len(u)} ans={ans}")


if __name__ == "__main__":
    main()
