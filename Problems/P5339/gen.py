# -*- coding: utf-8 -*-
"""P5339 造数：统计无法通到边界的村庄个数。"""
from __future__ import annotations

import importlib.util
from pathlib import Path
from random import Random

ROOT = Path(__file__).resolve().parent
DATA = ROOT / "data"
RNG = Random(5339)


def load_std():
    spec = importlib.util.spec_from_file_location("p5339_std", ROOT / "std.py")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod.count_closed


count_closed = load_std()


def wrong_eight(grid):
    """错误：斜对角也算连通。"""
    h = len(grid)
    w = len(grid[0])
    vis = [[False] * w for _ in range(h)]
    q = []

    def add(i, j):
        if 0 <= i < h and 0 <= j < w and grid[i][j] == "V" and not vis[i][j]:
            vis[i][j] = True
            q.append((i, j))

    for j in range(w):
        add(0, j)
        add(h - 1, j)
    for i in range(h):
        add(i, 0)
        add(i, w - 1)
    dirs = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]
    while q:
        i, j = q.pop()
        for di, dj in dirs:
            add(i + di, j + dj)
    ans = 0
    for i in range(h):
        for j in range(w):
            if grid[i][j] == "V" and not vis[i][j]:
                ans += 1
    return ans


def write_case(idx, grid):
    h = len(grid)
    w = len(grid[0])
    assert 1 <= h <= 200 and 1 <= w <= 200
    for row in grid:
        assert len(row) == w
        assert all(ch in "WV" for ch in row)
    ans = count_closed(grid)
    lines = [f"{h} {w}"] + list(grid)
    text_in = "\n".join(lines)
    (DATA / f"{idx}.in").write_bytes(text_in.encode("utf-8"))
    with open(DATA / f"{idx}.out", "w", encoding="utf-8", newline="\n") as f:
        f.write(str(ans) + "\n")
    return ans


def rand_grid(h, w, p_v=0.35):
    g = []
    for _ in range(h):
        row = "".join("V" if RNG.random() < p_v else "W" for _ in range(w))
        g.append(row)
    return g


def main():
    DATA.mkdir(parents=True, exist_ok=True)
    cases = []

    cases.append(["WW", "WW"])
    cases.append(["WWWWW", "WVVVW", "WWWWW"])
    cases.append(["WWWWW", "WVWWW", "WVWVW", "WWVVW", "WWWWW"])
    cases.append(["V"])
    cases.append(["VVV", "VVV", "VVV"])
    # 对角线连通：四连通应封闭，八连通会误判为自由
    cases.append(["VWWWW", "WVWWW", "WWVWW", "WWWVW", "WWWWW"])
    cases.append(["WWW", "WVW", "WWW"])
    cases.append(rand_grid(12, 15, 0.4))
    cases.append(rand_grid(50, 50, 0.3))
    # 边界全是城墙，内部全是村庄
    h, w = 200, 200
    big = ["W" * w]
    for _ in range(h - 2):
        big.append("W" + "V" * (w - 2) + "W")
    big.append("W" * w)
    cases.append(big)

    notes = [
        "样例1 全是城墙",
        "样例2 中间三个封闭村庄",
        "样例3 五个内部村庄",
        "1x1 的 V 在边界上，不改建",
        "整图都是 V，都能通边界",
        "对角线串起来，卡八连通",
        "单格被围",
        "小随机",
        "50x50 随机",
        "200x200 内部全封闭",
    ]

    for i, grid in enumerate(cases, 1):
        ans = write_case(i, grid)
        e8 = wrong_eight(grid)
        print(f"case {i}: {len(grid)}x{len(grid[0])} ans={ans} eight={e8} note={notes[i - 1]}")

    for i in range(1, 11):
        raw = (DATA / f"{i}.in").read_text(encoding="utf-8")
        lines = raw.split("\n")
        h, w = map(int, lines[0].split())
        grid = lines[1 : h + 1]
        got = count_closed(grid)
        expect = int((DATA / f"{i}.out").read_text(encoding="utf-8").strip())
        if got != expect:
            raise SystemExit(f"校验失败：{i}.out 期望 {expect} 实得 {got}")
        in_bytes = (DATA / f"{i}.in").read_bytes()
        if in_bytes.endswith(b"\n"):
            raise SystemExit(f"{i}.in 末尾有换行")
        out_bytes = (DATA / f"{i}.out").read_bytes()
        if not out_bytes.endswith(b"\n") or out_bytes.endswith(b"\n\n"):
            raise SystemExit(f"{i}.out 换行不符合约定")

    g = cases[5]
    if wrong_eight(g) == count_closed(g):
        raise SystemExit("第 6 组未能卡掉八连通")
    if count_closed(["V"]) != 0:
        raise SystemExit("1x1 V 应变为 0")
    if count_closed(cases[9]) != 198 * 198:
        raise SystemExit("第 10 组内部封闭计数错误")

    print("gen ok")


if __name__ == "__main__":
    main()
