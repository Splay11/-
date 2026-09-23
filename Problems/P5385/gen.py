# -*- coding: utf-8 -*-
import random
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from std import best_score

ROOT = Path(__file__).resolve().parent
DATA = ROOT / "data"
DATA.mkdir(exist_ok=True)
rng = random.Random(5385)


def format_in(cases):
    lines = [str(len(cases))]
    for g in cases:
        m = len(g)
        lines.append(str(m))
        for row in g:
            lines.append(" ".join(str(x) for x in row))
    return "\n".join(lines)


def format_out(cases):
    return "".join(str(best_score(g)) + "\n" for g in cases)


def dump(idx, cases, note):
    (DATA / f"{idx}.in").write_bytes(format_in(cases).encode("utf-8"))
    (DATA / f"{idx}.out").write_bytes(format_out(cases).encode("utf-8"))
    anss = [best_score(g) for g in cases]
    print(f"case {idx}: q={len(cases)} ans={anss} note={note}")


def all_val(m, v):
    return [[v] * m for _ in range(m)]


def identity_win(m):
    g = [[-1] * m for _ in range(m)]
    for i in range(m):
        g[i][i] = 1
    return g


def cycle_rps(m):
    # 循环克制：i 胜 i 与 i+1
    g = [[-1] * m for _ in range(m)]
    for i in range(m):
        g[i][i] = 1
        g[i][(i + 1) % m] = 1
    return g


def upper_win(m):
    g = [[-1] * m for _ in range(m)]
    for i in range(m):
        for j in range(i, m):
            g[i][j] = 1
    return g


def random_pm(m, rnd, p=0.5):
    g = []
    for _ in range(m):
        g.append([1 if rnd.random() < p else -1 for _ in range(m)])
    return g


# 1-3 改写样例
dump(1, [[[-1]], [[1, -1], [1, 1]]], "样例1")
dump(2, [[[1, 1, -1], [1, -1, -1], [-1, -1, 1]]], "样例2 完美匹配")
dump(3, [[[1, 1, -1], [-1, -1, -1], [1, -1, -1]]], "样例3 匹配 2")

dump(
    4,
    [
        [[1]],
        all_val(2, 1),
        all_val(2, -1),
        identity_win(3),
    ],
    "单艇胜、全胜、全负、对角胜",
)
dump(
    5,
    [
        cycle_rps(3),
        upper_win(4),
        [[1, -1], [-1, -1]],
        [[-1, 1], [-1, 1]],
    ],
    "循环克制 / 上三角 / 原题同类结构换数",
)
dump(
    6,
    [
        [[1, -1, -1], [1, -1, -1], [1, -1, -1]],
        [[-1, -1, 1], [-1, 1, -1], [1, -1, -1]],
        all_val(5, 1),
        all_val(5, -1),
    ],
    "hack：一列全胜；置换；输出匹配数而不乘 2",
)
dump(7, [cycle_rps(k) for k in range(1, 8)], "短循环，卡贪心排序")
dump(8, [random_pm(rng.randint(1, 12), rng, rng.uniform(0.2, 0.8)) for _ in range(8)], "随机小矩阵")

# 9-10 大数据 q=10 m=100
big9 = [
    all_val(100, 1),
    all_val(100, -1),
    identity_win(100),
    cycle_rps(100),
    upper_win(100),
]
big9 += [random_pm(100, rng, p) for p in (0.1, 0.3, 0.5, 0.7, 0.9)]
dump(9, big9, "m=100 构造+随机")

big10 = [random_pm(100, rng, rng.uniform(0.05, 0.95)) for _ in range(9)]
big10.append(identity_win(100))
dump(10, big10, "m=100 混合压测")

ok = True
for i in range(1, 11):
    raw = (DATA / f"{i}.in").read_bytes().decode("utf-8")
    parts = raw.split("\n")
    q = int(parts[0])
    p = 1
    cases = []
    for _ in range(q):
        m = int(parts[p])
        p += 1
        g = []
        for _r in range(m):
            g.append(list(map(int, parts[p].split())))
            p += 1
        cases.append(g)
    if format_out(cases) != (DATA / f"{i}.out").read_text(encoding="utf-8"):
        print("MISMATCH", i)
        ok = False
if not ok:
    raise SystemExit(1)
print("ok")
