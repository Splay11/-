# -*- coding: utf-8 -*-
"""P7135 造数：统计 grid2 中被 grid1 完全包含的岛屿个数。

stdin：第一行 m n；随后 m 行 grid1，再 m 行 grid2。
`.in` 最后一行后不留换行；`.out` 末尾恰好一个换行。
"""
from __future__ import annotations

import random
import sys
from collections import deque
from pathlib import Path

sys.dont_write_bytecode = True
sys.path.insert(0, str(Path(__file__).resolve().parent))
from std import solve  # noqa: E402

ROOT = Path(__file__).resolve().parent
DATA = ROOT / "data"
RNG = random.Random(713520260914)

MN_MAX = 500


def naive(grid1, grid2):
    m, n = len(grid2), len(grid2[0])
    g2 = [row[:] for row in grid2]
    dirs = ((1, 0), (-1, 0), (0, 1), (0, -1))
    ans = 0
    for si in range(m):
        for sj in range(n):
            if g2[si][sj] != 1:
                continue
            ok = True
            q = deque([(si, sj)])
            g2[si][sj] = 0
            while q:
                i, j = q.popleft()
                if grid1[i][j] == 0:
                    ok = False
                for di, dj in dirs:
                    ni, nj = i + di, j + dj
                    if 0 <= ni < m and 0 <= nj < n and g2[ni][nj] == 1:
                        g2[ni][nj] = 0
                        q.append((ni, nj))
            if ok:
                ans += 1
    return ans


def case_in_text(g1, g2):
    m, n = len(g1), len(g1[0])
    lines = [f"{m} {n}"]
    for row in g1:
        lines.append(" ".join(map(str, row)))
    for row in g2:
        lines.append(" ".join(map(str, row)))
    return "\n".join(lines)


def write_case(idx, g1, g2):
    m, n = len(g1), len(g1[0])
    assert 1 <= m <= MN_MAX and 1 <= n <= MN_MAX
    assert len(g2) == m and all(len(r) == n for r in g1) and all(len(r) == n for r in g2)
    assert all(v in (0, 1) for row in g1 for v in row)
    assert all(v in (0, 1) for row in g2 for v in row)
    (DATA / f"{idx}.in").write_bytes(case_in_text(g1, g2).encode("utf-8"))
    ans = solve(g1, g2)
    expect = naive(g1, g2)
    assert ans == expect, (idx, ans, expect)
    with open(DATA / f"{idx}.out", "w", encoding="utf-8", newline="\n") as f:
        f.write(str(ans) + "\n")
    return ans


def full(m, n, v):
    return [[v] * n for _ in range(m)]


def snake(m, n):
    """一条蛇形陆地，专门压递归。"""
    g = [[0] * n for _ in range(m)]
    for i in range(m):
        if i % 2 == 0:
            for j in range(n):
                g[i][j] = 1
        else:
            g[i][n - 1] = 1
    return g


def main():
    DATA.mkdir(parents=True, exist_ok=True)

    s1_g1 = [
        [1, 1, 1, 0, 0],
        [0, 1, 1, 1, 1],
        [0, 0, 0, 0, 0],
        [1, 0, 0, 0, 0],
        [1, 1, 0, 1, 1],
    ]
    s1_g2 = [
        [1, 1, 1, 0, 0],
        [0, 0, 1, 1, 1],
        [0, 1, 0, 0, 0],
        [1, 0, 1, 1, 0],
        [0, 1, 0, 1, 0],
    ]
    s2_g1 = [
        [1, 0, 1, 0, 1],
        [1, 1, 1, 1, 1],
        [0, 0, 0, 0, 0],
        [1, 1, 1, 1, 1],
        [1, 0, 1, 0, 1],
    ]
    s2_g2 = [
        [0, 0, 0, 0, 0],
        [1, 1, 1, 1, 1],
        [0, 1, 0, 1, 0],
        [0, 1, 0, 1, 0],
        [1, 0, 0, 0, 1],
    ]

    # 一座岛有一格在 grid1 是水 → 整座不算
    partial_g1 = [
        [1, 1, 0],
        [1, 0, 0],
        [0, 0, 0],
    ]
    partial_g2 = [
        [1, 1, 1],
        [0, 0, 0],
        [0, 0, 0],
    ]

    # grid1 全陆地，grid2 四个不相邻的 1
    dots_g1 = full(3, 3, 1)
    dots_g2 = [
        [1, 0, 1],
        [0, 0, 0],
        [1, 0, 1],
    ]

    rand8_g1 = [[RNG.randint(0, 1) for _ in range(8)] for _ in range(8)]
    rand8_g2 = [[RNG.randint(0, 1) for _ in range(8)] for _ in range(8)]

    big1 = full(MN_MAX, MN_MAX, 1)
    big_snake = snake(MN_MAX, MN_MAX)
    # grid1 也是全 1，蛇形岛整座被包含 → 1

    rand_big_g1 = [[1 if RNG.random() < 0.7 else 0 for _ in range(MN_MAX)] for _ in range(MN_MAX)]
    rand_big_g2 = [[1 if RNG.random() < 0.4 else 0 for _ in range(MN_MAX)] for _ in range(MN_MAX)]

    plan = [
        (s1_g1, s1_g2,
         "样例 1", "子岛屿个数为 $3$",
         "按陆地格子数统计，或漏掉其中一座"),
        (s2_g1, s2_g2,
         "样例 2", "子岛屿个数为 $2$",
         "把底部两个对角 $1$ 也算进去"),
        ([[1]], [[1]],
         "单格两张都是陆地", "答案 $1$",
         "空岛或漏统计"),
        ([[0]], [[1]],
         "单格 grid2 是陆地但 grid1 是水", "答案 $0$",
         "不看 grid1 直接输出 $1$"),
        (partial_g1, partial_g2,
         "一座岛只有部分被覆盖", "整座不算，答案 $0$",
         "按格点覆盖率计算，输出 $2$"),
        (full(4, 4, 0), full(4, 4, 0),
         "全是水", "答案 $0$",
         "输出 $1$ 把空图当一座岛"),
        (dots_g1, dots_g2,
         "四座互不相邻的单格岛，全部被包含", "答案 $4$",
         "用八连通把它们合成一座"),
        (rand8_g1, rand8_g2,
         "小随机 $8\\times 8$", "DFS 与 BFS 对拍",
         "染色串岛"),
        (big1, big_snake,
         "压满 $500\\times 500$，grid1 全陆地，grid2 蛇形一座岛",
         "答案 $1$",
         "递归 DFS 爆栈"),
        (rand_big_g1, rand_big_g2,
         "压满 $500\\times 500$ 随机 $0/1$",
         "线性扫岛",
         "I/O 超时；或只扫了 grid2 没对照 grid1"),
    ]
    assert len(plan) == 10

    answers = []
    for idx, (g1, g2, _, _, _) in enumerate(plan, 1):
        answers.append(write_case(idx, g1, g2))

    for i, (g1, g2, _, _, _) in enumerate(plan, 1):
        ib = (DATA / f"{i}.in").read_bytes()
        ob = (DATA / f"{i}.out").read_bytes()
        assert not ib.endswith(b"\n") and b"\r" not in ib, f"{i}.in"
        assert ob.endswith(b"\n") and not ob.endswith(b"\n\n") and b"\r" not in ob
        text = ib.decode("utf-8")
        lines = text.split("\n")
        hm, hn = map(int, lines[0].split())
        assert hm == len(g1) and hn == len(g1[0])
        pg1 = [list(map(int, lines[1 + r].split())) for r in range(hm)]
        pg2 = [list(map(int, lines[1 + hm + r].split())) for r in range(hm)]
        assert pg1 == g1 and pg2 == g2
        got = int(ob.decode("utf-8").strip())
        assert got == answers[i - 1] == naive(g1, g2)

    assert answers[0] == 3
    assert answers[1] == 2
    assert answers[2] == 1
    assert answers[3] == 0
    assert answers[4] == 0
    assert answers[5] == 0
    assert answers[6] == 4
    assert answers[8] == 1

    rows = []
    for i, (_, _, scale, goal, hack) in enumerate(plan, 1):
        rows.append(f"| {i} | {scale} | {goal} | {hack} |")

    readme = "\n".join([
        "# P7135 测试数据说明",
        "",
        "主造数脚本：题目根目录 `gen.py`。",
        "stdin：第一行 `m n`；随后 $m$ 行 $grid1$，再 $m$ 行 $grid2$。",
        "输出：$grid2$ 中子岛屿的个数。",
        "",
        r"约束：$1\le m,n\le 500$，矩阵元素为 $0$ 或 $1$。",
        "",
        "| 组别 | 规模/分布 | 目标 | 卡掉的错误解 |",
        "|---|---|---|---|",
        *rows,
        "",
        "`.in` 最后一行后无换行符；`.out` 末尾恰好一个换行符。",
        "",
        "生成后自校验：栈 DFS 必须等于队列 BFS 的子岛屿个数。",
        "",
    ])
    (DATA / "README.md").write_text(readme, encoding="utf-8")
    print("generated 10 cases")
    for i, ans in enumerate(answers, 1):
        print(i, "ans", ans)


if __name__ == "__main__":
    main()
