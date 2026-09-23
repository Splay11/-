# -*- coding: utf-8 -*-
import random
from pathlib import Path

from std import farthest_posts

ROOT = Path(__file__).resolve().parent
DATA = ROOT / "data"
DATA.mkdir(exist_ok=True)
rng = random.Random(5368)


def format_in(grid):
    h = len(grid)
    w = len(grid[0])
    return str(h) + " " + str(w) + "\n" + "\n".join(grid)


def format_out(ans):
    return "%d %d %d %d\n" % ans


def dump(idx, grid, note):
    ans = farthest_posts(grid)
    (DATA / f"{idx}.in").write_bytes(format_in(grid).encode("utf-8"))
    (DATA / f"{idx}.out").write_bytes(format_out(ans).encode("utf-8"))
    print(f"case {idx}: {len(grid)}x{len(grid[0])} ans={ans} note={note}")


def brute(grid):
    pts = []
    for i, row in enumerate(grid, 1):
        for j, ch in enumerate(row, 1):
            if ch == ".":
                pts.append((i, j))
    best = -1
    pair = None
    for a in range(len(pts)):
        for b in range(a + 1, len(pts)):
            d = abs(pts[a][0] - pts[b][0]) + abs(pts[a][1] - pts[b][1])
            if d > best:
                best = d
                pair = (pts[a], pts[b])
    return best, pair


def check_small(grid):
    r1, c1, r2, c2 = farthest_posts(grid)
    got = abs(r1 - r2) + abs(c1 - c2)
    best, _ = brute(grid)
    assert got == best, (grid, got, best, (r1, c1, r2, c2))
    assert grid[r1 - 1][c1 - 1] == "." and grid[r2 - 1][c2 - 1] == "."
    assert (r1, c1) != (r2, c2)


def rand_grid(h, w, p_dot):
    rows = []
    dots = 0
    for _ in range(h):
        cells = []
        for _ in range(w):
            if rng.random() < p_dot:
                cells.append(".")
                dots += 1
            else:
                cells.append("#")
        rows.append("".join(cells))
    if dots < 2:
        rows[0] = "." + ("#" * (w - 1) if w > 1 else "")
        if w == 1:
            rows[1] = "."
        else:
            rows[0] = ".." + ("#" * (w - 2) if w > 2 else "")
            if w == 2:
                rows[0] = ".."
    return rows


dump(1, [".#..", "#..#", "..#."], "样例1")
dump(2, [".#..#."], "样例2 单行")
dump(3, ["#...", "####", "####", "..##"], "样例3 只用 r+c 会错")
dump(4, [".", ".", "#", "."], "单列")
dump(5, ["..", ".."], "2x2 全过道")

g6 = ["#####", "#...#", "#.#.#", "#...#", "#####"]
check_small(g6)
dump(6, g6, "封闭一圈过道")

g7 = rand_grid(6, 8, 0.45)
check_small(g7)
dump(7, g7, "6x8 随机与暴力对拍")

g8 = rand_grid(12, 12, 0.3)
check_small(g8)
dump(8, g8, "12x12 偏少过道")

# 1 x 200000：两端过道，中间夹一个过道，卡只看相邻或只看左右中间点
w9 = 200000
row9 = ["#"] * w9
row9[0] = "."
row9[w9 // 3] = "."
row9[-1] = "."
dump(9, ["".join(row9)], "w=2e5 单行三过道")

# 400 x 500 = 200000：角落 (1,w) 与 (h,1) 最远，卡只取 r+c
h10, w10 = 400, 500
g10 = [["#"] * w10 for _ in range(h10)]
g10[0][w10 - 1] = "."
g10[h10 - 1][0] = "."
g10[0][0] = "."
g10[h10 - 1][w10 - 1] = "#"
dump(10, ["".join(r) for r in g10], "400x500 反对角最远")

print("ok")
