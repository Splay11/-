# -*- coding: utf-8 -*-
"""P7115 造数：区间博弈。"""
from __future__ import annotations

import importlib.util
from collections import deque
from pathlib import Path
from random import Random

ROOT = Path(__file__).resolve().parent
DATA = ROOT / "data"
RNG = Random(7115)


def load_std():
    spec = importlib.util.spec_from_file_location("p7115_std", ROOT / "std.py")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod.first_score


first_score = load_std()


def greedy_max_end(a):
    """双方都每次取两端较大值（先手视角得分）。"""
    q = deque(a)
    first = 0
    turn = 0
    while q:
        if q[0] >= q[-1]:
            x = q.popleft()
        else:
            x = q.pop()
        if turn == 0:
            first += x
        turn ^= 1
    return first


def always_left(a):
    q = deque(a)
    first = 0
    turn = 0
    while q:
        x = q.popleft()
        if turn == 0:
            first += x
        turn ^= 1
    return first


def brute(a):
    """双方最优的先手得分，用于小数据核对 DP。"""
    n = len(a)

    def dfs(l, r, is_first, f, s):
        if l > r:
            return f
        take_l = dfs(l + 1, r, not is_first, f + a[l] if is_first else f, s if is_first else s + a[l])
        take_r = dfs(l, r - 1, not is_first, f + a[r] if is_first else f, s if is_first else s + a[r])
        if is_first:
            return take_l if take_l > take_r else take_r
        return take_l if take_l < take_r else take_r

    return dfs(0, n - 1, True, 0, 0)


def write_case(idx, a):
    n = len(a)
    assert 1 <= n <= 200
    assert all(1 <= x <= 10**9 for x in a)
    text_in = str(n) + "\n" + " ".join(str(x) for x in a)
    (DATA / f"{idx}.in").write_bytes(text_in.encode("utf-8"))
    ans = first_score(a)
    with open(DATA / f"{idx}.out", "w", encoding="utf-8", newline="\n") as f:
        f.write(str(ans) + "\n")
    return ans


def rand_arr(n, lo, hi):
    return [RNG.randint(lo, hi) for _ in range(n)]


def main():
    DATA.mkdir(parents=True, exist_ok=True)
    cases = []

    # 1. 样例：卡「每次取较大端」
    cases.append([3, 9, 1, 2])
    # 2. 样例：n=1
    cases.append([5])
    # 3. 边界 n=2
    cases.append([1, 10**9])
    # 4. 全部相同
    cases.append([4] * 7)
    # 5. 右端明显更大，卡总从左取
    cases.append([1, 2, 3, 100])
    # 6. 随机小数据，可与暴力对拍；n 仍小，无记忆化递归也能过
    cases.append(rand_arr(12, 1, 30))
    # 7. hack：两端较大值唯一，贪心仍非最优
    cases.append([4, 9, 1, 2])
    # 8~10. 卡无记忆化递归（指数级），记忆化 O(n^2) 状态仍能过
    cases.append(rand_arr(80, 1, 10**9))
    cases.append(rand_arr(150, 1, 10**9))
    unit = [3, 9, 1, 2]
    big = unit * 50
    assert len(big) == 200
    cases.append(big)

    notes = [
        "样例 [3,9,1,2]，卡较大端贪心",
        "n=1",
        "n=2 值域边界，检查 64 位",
        "全部相等",
        "右端大数，卡总从左取",
        "随机小数据，与暴力对拍",
        "hack [4,9,1,2]：较大端唯一仍非最优",
        "n=80，卡普通递归",
        "n=150，卡普通递归",
        "n=200 重复 [3,9,1,2]，卡贪心与普通递归",
    ]

    for i, a in enumerate(cases, 1):
        ans = write_case(i, a)
        g = greedy_max_end(a)
        L = always_left(a)
        extra = ""
        if len(a) <= 12:
            b = brute(a)
            if b != ans:
                raise SystemExit(f"DP 与暴力不一致：第 {i} 组 {ans} vs {b}")
            extra = f" brute={b}"
        print(f"case {i}: n={len(a)} ans={ans} greedy={g} left={L}{extra} note={notes[i - 1]}")

    for i in range(1, 11):
        raw = (DATA / f"{i}.in").read_text(encoding="utf-8")
        lines = raw.split("\n")
        n = int(lines[0])
        a = list(map(int, lines[1].split()))
        assert n == len(a)
        got = first_score(a)
        expect = int((DATA / f"{i}.out").read_text(encoding="utf-8").strip())
        if got != expect:
            raise SystemExit(f"校验失败：{i}.out")
        if (DATA / f"{i}.in").read_bytes().endswith(b"\n"):
            raise SystemExit(f"{i}.in 末尾有换行")
        out_bytes = (DATA / f"{i}.out").read_bytes()
        if not out_bytes.endswith(b"\n") or out_bytes.endswith(b"\n\n"):
            raise SystemExit(f"{i}.out 换行不符合约定")

    for idx in (1, 7, 10):
        raw = (DATA / f"{idx}.in").read_text(encoding="utf-8")
        a = list(map(int, raw.split("\n")[1].split()))
        if greedy_max_end(a) == first_score(a):
            raise SystemExit(f"第 {idx} 组未能卡掉较大端贪心")

    print("gen ok")


if __name__ == "__main__":
    main()
