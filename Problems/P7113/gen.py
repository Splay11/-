# -*- coding: utf-8 -*-
"""P7113 造数：首尾删除的最小总代价。"""
from __future__ import annotations

import importlib.util
from collections import deque
from pathlib import Path
from random import Random

ROOT = Path(__file__).resolve().parent
DATA = ROOT / "data"
RNG = Random(7113)


def load_std():
    spec = importlib.util.spec_from_file_location("p7113_std", ROOT / "std.py")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod.min_cost


min_cost = load_std()


def greedy_min(a):
    """每次取两端较小值（相等时取左）。常见错误贪心。"""
    q = deque(a)
    cost = 0
    while q:
        length = len(q)
        if q[0] <= q[-1]:
            cost += length * q.popleft()
        else:
            cost += length * q.pop()
    return cost


def always_left(a):
    q = deque(a)
    cost = 0
    while q:
        length = len(q)
        cost += length * q.popleft()
    return cost


def write_case(idx, a):
    n = len(a)
    assert 1 <= n <= 1000
    assert all(1 <= x <= 10**9 for x in a)
    text_in = str(n) + "\n" + " ".join(str(x) for x in a)
    (DATA / f"{idx}.in").write_bytes(text_in.encode("utf-8"))
    ans = min_cost(a)
    with open(DATA / f"{idx}.out", "w", encoding="utf-8", newline="\n") as f:
        f.write(str(ans) + "\n")
    return ans


def rand_arr(n, lo, hi):
    return [RNG.randint(lo, hi) for _ in range(n)]


def main():
    DATA.mkdir(parents=True, exist_ok=True)
    cases = []

    # 1. 样例
    cases.append([2, 2, 1, 2])
    # 2. 基础：n=1
    cases.append([5])
    # 3. 边界：n=2，值域两端
    cases.append([1, 10**9])
    # 4. 边界：全部相同
    cases.append([7] * 8)
    # 5. 构造：严格递增（总是从左删更优，卡“总从右删”）；n 仍小，普通递归可过
    cases.append(list(range(1, 13)))
    # 6. 随机小数据
    cases.append(rand_arr(12, 1, 100))
    # 7. hack：两端不等时“每次取较小端”仍非最优
    cases.append([3, 4, 1, 4])
    # 8~10. 卡无记忆化递归（指数级），记忆化 O(n^2) 仍能过
    cases.append(rand_arr(80, 1, 10**9))
    cases.append(rand_arr(400, 1, 10**9))
    unit = [3 * 10**8, 4 * 10**8, 10**8, 4 * 10**8]
    big = unit * 250
    assert len(big) == 1000
    cases.append(big)

    notes = [
        "样例 [2,2,1,2]，同时卡左端平局贪心（贪心 18，正解 17）",
        "最小规模 n=1",
        "n=2 且取到值域上下界，检查 64 位",
        "全部相等，任意删除顺序代价相同",
        "严格递增，卡“总是删右端”",
        "随机小数据，便于和暴力对拍",
        "hack [3,4,1,4]：较小端唯一，贪心仍错",
        "n=80，卡普通递归",
        "n=400，卡普通递归",
        "n=1000 重复放大版 [3,4,1,4]，卡贪心与普通递归",
    ]

    for i, a in enumerate(cases, 1):
        ans = write_case(i, a)
        g = greedy_min(a)
        L = always_left(a)
        print(f"case {i}: n={len(a)} ans={ans} greedy={g} left={L} note={notes[i - 1]}")

    # 自校验：用标程重算全部 .out
    for i in range(1, 11):
        raw = (DATA / f"{i}.in").read_text(encoding="utf-8")
        lines = raw.split("\n")
        n = int(lines[0])
        a = list(map(int, lines[1].split()))
        assert n == len(a)
        got = min_cost(a)
        expect = int((DATA / f"{i}.out").read_text(encoding="utf-8").strip())
        if got != expect:
            raise SystemExit(f"校验失败：{i}.out 期望 {expect} 实得 {got}")
        # .in 末尾不得有多余换行
        in_bytes = (DATA / f"{i}.in").read_bytes()
        if in_bytes.endswith(b"\n"):
            raise SystemExit(f"{i}.in 末尾有换行")
        out_bytes = (DATA / f"{i}.out").read_bytes()
        if not out_bytes.endswith(b"\n") or out_bytes.endswith(b"\n\n"):
            raise SystemExit(f"{i}.out 换行不符合约定")

    # 确认 hack 组确实卡住贪心
    for idx in (1, 7, 10):
        raw = (DATA / f"{idx}.in").read_text(encoding="utf-8")
        a = list(map(int, raw.split("\n")[1].split()))
        if greedy_min(a) == min_cost(a):
            raise SystemExit(f"第 {idx} 组未能卡掉较小端贪心")

    print("gen ok")


if __name__ == "__main__":
    main()
