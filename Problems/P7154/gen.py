# -*- coding: utf-8 -*-
"""P7154 造数：网格最小路径和（只能向右或向下）。

stdin：第一行 m n，接着 m 行每行 n 个非负整数。
输出：最小路径和。
`.in` 最后一行后不留换行；`.out` 末尾恰好一个换行。
"""
from __future__ import annotations

import random
import sys
from pathlib import Path

sys.dont_write_bytecode = True
sys.path.insert(0, str(Path(__file__).resolve().parent))
from std import solve  # noqa: E402

ROOT = Path(__file__).resolve().parent
DATA = ROOT / "data"
RNG = random.Random(715420260915)

MN_MAX = 200
V_MAX = 200


def naive(grid):
    """一维滚动 DP，与二维 DP 对拍。"""
    m = len(grid)
    n = len(grid[0])
    dp = grid[0][:]
    for j in range(1, n):
        dp[j] += dp[j - 1]
    for i in range(1, m):
        dp[0] += grid[i][0]
        for j in range(1, n):
            dp[j] = grid[i][j] + min(dp[j], dp[j - 1])
    return dp[n - 1]


def greedy(grid):
    """假解：每步走当前更小的邻居。"""
    m = len(grid)
    n = len(grid[0])
    i = j = 0
    s = grid[0][0]
    while i < m - 1 or j < n - 1:
        if i == m - 1:
            j += 1
        elif j == n - 1:
            i += 1
        elif grid[i + 1][j] < grid[i][j + 1]:
            i += 1
        else:
            j += 1
        s += grid[i][j]
    return s


def write_case(idx, grid):
    m = len(grid)
    n = len(grid[0])
    assert 1 <= m <= MN_MAX and 1 <= n <= MN_MAX
    for row in grid:
        assert len(row) == n
        for x in row:
            assert 0 <= x <= V_MAX
    ans = solve([row[:] for row in grid])
    expect = naive(grid)
    assert ans == expect, (idx, ans, expect)
    lines = [f"{m} {n}"]
    for row in grid:
        lines.append(" ".join(str(x) for x in row))
    inp = "\n".join(lines)
    (DATA / f"{idx}.in").write_bytes(inp.encode("utf-8"))
    with open(DATA / f"{idx}.out", "w", encoding="utf-8", newline="\n") as f:
        f.write(str(ans) + "\n")
    return ans


def rand_grid(m, n):
    return [[RNG.randint(0, V_MAX) for _ in range(n)] for _ in range(m)]


def main():
    DATA.mkdir(parents=True, exist_ok=True)

    g_hack = [[1, 4, 1], [1, 9, 1], [6, 2, 1]]
    p8 = rand_grid(5, 6)
    p9 = rand_grid(MN_MAX, MN_MAX)
    p10 = rand_grid(MN_MAX, 1)

    plan = [
        ([[1, 3, 1], [1, 5, 1], [4, 2, 1]],
         "样例 1", "$7$",
         "贪心先向下得到 $9$"),
        ([[1, 2, 3], [4, 5, 6]],
         "样例 2", "$12$",
         "漏加终点"),
        ([[5]],
         "单格", "$5$",
         "当成 $0$"),
        ([[1, 2, 3]],
         "只有一行，只能向右", "$6$",
         "尝试向下越界"),
        ([[1], [2], [3]],
         "只有一列，只能向下", "$6$",
         "尝试向右越界"),
        (g_hack,
         "贪心陷阱：局部更小的向下走廊更差", "最优沿上方再下去得到 $8$",
         "每步取局部最小得到 $11$"),
        ([[0, 0], [0, 0]],
         "全 $0$", "$0$",
         "输出路径长度而不是和"),
        (p8,
         "小随机 $5\\times 6$", "二维 DP 与滚动数组对拍",
         "只更新一行忘记列"),
        (p9,
         "压满 $200\\times 200$", "$O(mn)$ DP",
         "搜索全部路径 TLE"),
        (p10,
         "压满 $200\\times 1$ 的细长网格", "退化成前缀和",
         "下标把列当成行"),
    ]
    assert len(plan) == 10

    answers = []
    grids = []
    for idx, (grid, _, _, _) in enumerate(plan, 1):
        grids.append(grid)
        answers.append(write_case(idx, grid))

    for i, grid in enumerate(grids, 1):
        ib = (DATA / f"{i}.in").read_bytes()
        ob = (DATA / f"{i}.out").read_bytes()
        assert not ib.endswith(b"\n") and b"\r" not in ib, f"{i}.in"
        assert ob.endswith(b"\n") and not ob.endswith(b"\n\n") and b"\r" not in ob
        m, n = len(grid), len(grid[0])
        lines = [f"{m} {n}"] + [" ".join(str(x) for x in row) for row in grid]
        assert ib.decode("utf-8") == "\n".join(lines)
        got = ob.decode("utf-8")[:-1]
        assert got == str(answers[i - 1]) == str(naive(grid))

    assert answers[0] == 7
    assert answers[1] == 12
    assert answers[2] == 5
    assert answers[3] == 6
    assert answers[4] == 6
    assert answers[5] == 8
    assert greedy(g_hack) == 11
    assert answers[6] == 0
    assert len(grids[8]) == MN_MAX and len(grids[8][0]) == MN_MAX
    assert len(grids[9]) == MN_MAX and len(grids[9][0]) == 1

    rows = []
    for i, (_, scale, goal, hack) in enumerate(plan, 1):
        rows.append(f"| {i} | {scale} | {goal} | {hack} |")

    readme = "\n".join([
        "# P7154 测试数据说明",
        "",
        "主造数脚本：题目根目录 `gen.py`。",
        "stdin：第一行 $m$ $n$，接着 $m$ 行每行 $n$ 个非负整数。",
        "输出：从左上到右下（只能向右或向下）的最小路径和。",
        "",
        r"约束：$1\le m,n\le 200$，$0\le grid_{i,j}\le 200$。",
        "",
        "| 组别 | 规模/分布 | 目标 | 卡掉的错误解 |",
        "|---|---|---|---|",
        *rows,
        "",
        "`.in` 最后一行后无换行符；`.out` 末尾恰好一个换行符。",
        "",
        "生成后自校验：二维 DP 必须等于滚动一维 DP。",
        "",
    ])
    (DATA / "README.md").write_text(readme, encoding="utf-8")
    print("generated 10 cases")
    for i, ans in enumerate(answers, 1):
        print(i, ans, "m", len(grids[i - 1]), "n", len(grids[i - 1][0]))


if __name__ == "__main__":
    main()
