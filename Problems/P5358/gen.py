# -*- coding: utf-8 -*-
import random
from pathlib import Path

from std import shortest

ROOT = Path(__file__).resolve().parent
DATA = ROOT / "data"
DATA.mkdir(exist_ok=True)
rng = random.Random(53581)


def format_in(h, w, a):
    lines = [f"{h} {w}"]
    for row in a:
        lines.append(" ".join(str(x) for x in row))
    return "\n".join(lines)


def format_out(ans):
    return str(ans) + "\n"


def dump(idx, h, w, a, note):
    ans = shortest(h, w, a)
    (DATA / f"{idx}.in").write_bytes(format_in(h, w, a).encode("utf-8"))
    (DATA / f"{idx}.out").write_bytes(format_out(ans).encode("utf-8"))
    print(f"case {idx}: {h}x{w} ans={ans} note={note}")


dump(1, 2, 3, [[0, 1, 0], [0, 0, 0]], "样例1")
dump(2, 2, 2, [[0, 1], [1, 0]], "样例2 四连通断开")
dump(3, 1, 1, [[0]], "样例3 单格")

dump(4, 2, 2, [[0, 0], [0, 0]], "全空，长度 3 不是 2")
dump(5, 3, 3, [[1, 0, 0], [0, 0, 0], [0, 0, 0]], "起点货架")
dump(6, 3, 3, [[0, 0, 0], [0, 0, 0], [0, 0, 1]], "终点货架")
dump(7, 3, 3, [[0, 1, 1], [1, 0, 1], [1, 1, 0]], "斜可通、四连通不通")

# 蛇形走廊
h8, w8 = 6, 7
a8 = [[1] * w8 for _ in range(h8)]
x, y = 0, 0
a8[0][0] = 0
for i in range(h8):
    if i % 2 == 0:
        for j in range(w8):
            a8[i][j] = 0
        if i + 1 < h8:
            a8[i + 1][w8 - 1] = 0
    else:
        for j in range(w8 - 1, -1, -1):
            a8[i][j] = 0
        if i + 1 < h8:
            a8[i + 1][0] = 0
a8[h8 - 1][w8 - 1] = 0
dump(8, h8, w8, a8, "蛇形，卡 DFS 非最短")

h9, w9 = 500, 500
a9 = [[0] * w9 for _ in range(h9)]
dump(9, h9, w9, a9, "500x500 全空")

h10, w10 = 500, 500
a10 = [[0] * w10 for _ in range(h10)]
for i in range(h10):
    for j in range(w10):
        if (i + j) % 7 == 3 and not (i == 0 and j == 0) and not (i == h10 - 1 and j == w10 - 1):
            if rng.random() < 0.55:
                a10[i][j] = 1
dump(10, h10, w10, a10, "500x500 随机墙")

for i in range(1, 11):
    raw = (DATA / f"{i}.in").read_text(encoding="utf-8")
    lines = raw.split("\n")
    h, w = map(int, lines[0].split())
    a = [list(map(int, lines[r + 1].split())) for r in range(h)]
    got = format_out(shortest(h, w, a))
    exp = (DATA / f"{i}.out").read_bytes().decode("utf-8")
    assert got == exp, i
    inn = (DATA / f"{i}.in").read_bytes()
    assert not inn.endswith(b"\n"), i
    out = (DATA / f"{i}.out").read_bytes()
    assert out.endswith(b"\n") and not out.endswith(b"\n\n"), i

print("gen ok")
