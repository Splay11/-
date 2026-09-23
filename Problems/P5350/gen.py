# -*- coding: utf-8 -*-
"""P5350 造数：双机器人同步网格 DP。"""
from __future__ import annotations

import importlib.util
from pathlib import Path
from random import Random

ROOT = Path(__file__).resolve().parent
DATA = ROOT / "data"
RNG = Random(5350)
NEG = -10**18


def load_std():
    spec = importlib.util.spec_from_file_location("p5350_std", ROOT / "std.py")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod.max_value


max_value = load_std()


def brute(h, w, grid):
    a_paths = []
    b_paths = []

    def dfs_a(r, c, path):
        if r == h - 1 and c == w - 1:
            a_paths.append(list(path))
            return
        if r + 1 < h:
            path.append((r + 1, c))
            dfs_a(r + 1, c, path)
            path.pop()
        if c + 1 < w:
            path.append((r, c + 1))
            dfs_a(r, c + 1, path)
            path.pop()

    def dfs_b(r, c, path):
        if r == h - 1 and c == 0:
            b_paths.append(list(path))
            return
        if r + 1 < h:
            path.append((r + 1, c))
            dfs_b(r + 1, c, path)
            path.pop()
        if c - 1 >= 0:
            path.append((r, c - 1))
            dfs_b(r, c - 1, path)
            path.pop()

    dfs_a(0, 0, [(0, 0)])
    dfs_b(0, w - 1, [(0, w - 1)])
    best = NEG
    for A in a_paths:
        for B in b_paths:
            ok = True
            s = 0
            for t in range(len(A)):
                if A[t] == B[t]:
                    ok = False
                    break
                s += grid[A[t][0]][A[t][1]] + grid[B[t][0]][B[t][1]]
            if ok and s > best:
                best = s
    return best


def write_case(idx, h, w, v):
    assert 3 <= h <= 100 and 3 <= w <= 100
    assert len(v) == h and all(len(row) == w for row in v)
    ans = max_value(h, w, v)
    lines = [f"{h} {w}"] + [" ".join(str(x) for x in row) for row in v]
    (DATA / f"{idx}.in").write_bytes("\n".join(lines).encode("utf-8"))
    with open(DATA / f"{idx}.out", "w", encoding="utf-8", newline="\n") as f:
        f.write(str(ans) + "\n")
    return ans


def main():
    DATA.mkdir(parents=True, exist_ok=True)
    cases = []
    cases.append((3, 3, [[2, 1, 4], [3, 0, 5], [6, 7, 8]]))
    cases.append((3, 4, [[1, 0, 0, 2], [3, 4, 5, 6], [7, 8, 9, 1]]))
    cases.append((4, 4, [[1, 2, 3, 4], [5, 0, 9, 1], [2, 8, 0, 3], [4, 5, 6, 7]]))
    cases.append((3, 3, [[0, 0, 0], [0, 0, 0], [0, 0, 0]]))
    cases.append((3, 5, [[1] * 5, [1] * 5, [1] * 5]))
    # 中间高价值，卡同时撞车
    cases.append((4, 5, [[1, 1, 1, 1, 1], [1, 1, 1, 1, 1], [1, 1, 50, 1, 1], [1, 1, 0, 1, 1]]))
    cases.append((3, 3, [[9, 1, 2], [3, 8, 4], [5, 6, 7]]))
    cases.append((5, 5, [[RNG.randint(0, 20) for _ in range(5)] for _ in range(5)]))
    cases.append((100, 100, [[1] * 100 for _ in range(100)]))
    cases.append((100, 100, [[RNG.randint(0, 100000) for _ in range(100)] for _ in range(100)]))

    notes = [
        "样例1",
        "样例2",
        "样例3",
        "全 0",
        "全 1 奇数宽",
        "中间高峰卡对撞",
        "3x3 另一组",
        "5x5 随机对拍",
        "100x100 全 1",
        "100x100 随机满值域",
    ]
    for i, (h, w, v) in enumerate(cases, 1):
        ans = write_case(i, h, w, v)
        print(f"case {i}: {h}x{w} ans={ans} note={notes[i - 1]}")

    for i, (h, w, v) in enumerate(cases[:8], 1):
        b = brute(h, w, v)
        g = max_value(h, w, v)
        if b != g:
            raise SystemExit(f"与暴力不符 case {i} brute={b} dp={g}")

    for i in range(1, 11):
        raw = (DATA / f"{i}.in").read_bytes()
        if raw.endswith(b"\n"):
            raise SystemExit(f"{i}.in 末尾有换行")
        out = (DATA / f"{i}.out").read_bytes()
        if not out.endswith(b"\n") or out.endswith(b"\n\n"):
            raise SystemExit(f"{i}.out 换行不符合约定")
    print("gen ok")


if __name__ == "__main__":
    main()
