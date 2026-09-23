# -*- coding: utf-8 -*-
"""P7122 造数：最大子矩阵（ACM 模式，stdin：N M，然后 N 行每行 M 个数）。

输出四个整数 r1 c1 r2 c2（最优子矩阵的左上角与右下角），并列时输出任意一个即可。
写文件规则：`.in` 最后一行后不留换行；`.out` 末尾恰好一个换行。

题面只给了 N,M 的范围（<=200），没有给元素取值范围，因此元素取 [-1000, 1000]：
此时总和上界为 200*200*1000 = 4*10^7，仍在 32 位内，但标程统一用 64 位更稳妥。
"""
from __future__ import annotations

import random
import sys
from pathlib import Path

sys.dont_write_bytecode = True

ROOT = Path(__file__).resolve().parent
DATA = ROOT / "data"
RNG = random.Random(712220260914)

N_MAX = 200
V_LO, V_HI = -1000, 1000


def max_submatrix(matrix):
    """基准解：枚举行区间 + 一维 Kadane，返回 (r1, c1, r2, c2)。"""
    n, m = len(matrix), len(matrix[0])
    best = None
    res = (0, 0, 0, 0)
    for r1 in range(n):
        col = [0] * m
        for r2 in range(r1, n):
            row = matrix[r2]
            for j in range(m):
                col[j] += row[j]
            cur = 0
            c_start = 0
            for j in range(m):
                if cur <= 0:
                    cur = col[j]
                    c_start = j
                else:
                    cur += col[j]
                if best is None or cur > best:
                    best = cur
                    res = (r1, c_start, r2, j)
    return res


def rect_sum(matrix, r1, c1, r2, c2):
    return sum(matrix[i][j] for i in range(r1, r2 + 1) for j in range(c1, c2 + 1))


def brute_max_sum(matrix):
    """独立暴力：二维前缀和 + 枚举所有矩形，返回真实最大总和。"""
    n, m = len(matrix), len(matrix[0])
    pre = [[0] * (m + 1) for _ in range(n + 1)]
    for i in range(n):
        for j in range(m):
            pre[i + 1][j + 1] = pre[i][j + 1] + pre[i + 1][j] - pre[i][j] + matrix[i][j]
    best = None
    for r1 in range(n):
        for r2 in range(r1, n):
            for c1 in range(m):
                for c2 in range(c1, m):
                    s = pre[r2 + 1][c2 + 1] - pre[r1][c2 + 1] - pre[r2 + 1][c1] + pre[r1][c1]
                    if best is None or s > best:
                        best = s
    return best


def alt_max_sum(matrix):
    """第二条独立路径：列前缀和取列和 + 另一种 Kadane 写法 cur = max(x, cur+x)。"""
    n, m = len(matrix), len(matrix[0])
    colpre = [[0] * m for _ in range(n + 1)]
    for i in range(n):
        for j in range(m):
            colpre[i + 1][j] = colpre[i][j] + matrix[i][j]
    best = None
    for r1 in range(n):
        for r2 in range(r1, n):
            cur = None
            for j in range(m):
                x = colpre[r2 + 1][j] - colpre[r1][j]
                cur = x if cur is None else max(x, cur + x)
                if best is None or cur > best:
                    best = cur
    return best


def case_in_text(matrix):
    return f"{len(matrix)} {len(matrix[0])}\n" + "\n".join(
        " ".join(str(x) for x in row) for row in matrix
    )


def write_case(idx, matrix):
    n, m = len(matrix), len(matrix[0])
    assert 1 <= n <= N_MAX and 1 <= m <= N_MAX, (idx, n, m)
    assert all(V_LO <= x <= V_HI for row in matrix for x in row), idx
    # .in：最后一行数据后不留换行符
    (DATA / f"{idx}.in").write_bytes(case_in_text(matrix).encode("utf-8"))
    r1, c1, r2, c2 = max_submatrix(matrix)
    # .out：末尾恰好一个换行符
    with open(DATA / f"{idx}.out", "w", encoding="utf-8", newline="\n") as f:
        f.write(f"{r1} {c1} {r2} {c2}\n")


def main():
    DATA.mkdir(parents=True, exist_ok=True)

    neg5 = [[-5] * 7 for _ in range(7)]
    for i in range(2, 5):
        for j in range(2, 5):
            neg5[i][j] = 3

    # (matrix, 规模/分布, 目标, 卡掉的错误解, 是否做暴力对拍)
    plan = [
        ([[-1, 0], [0, -1]], "样例，$2\\times2$",
         "最优总和为 $0$，输出某个总和为 $0$ 的单格子", "把空子矩阵（总和 $0$）当成答案，给不出坐标", True),
        ([[5]], "最小规模 $1\\times1$，元素为正",
         "输出 $0\\ 0\\ 0\\ 0$", "行/列下标从 $1$ 开始编号", True),
        ([[-7]], "最小规模 $1\\times1$，元素为负",
         "输出 $0\\ 0\\ 0\\ 0$（子矩阵必须非空）",
         "允许空子矩阵的 Kadane 会返回总和 $0$，从而输出非法坐标", True),
        ([[-2, 1, -3, 4, -1, 2, 1, -5, 4]], "单行 $1\\times9$",
         "最大子段 $4,-1,2,1$，总和 $6$", "一维情况下的边界处理错误", True),
        ([[-2], [1], [-3], [4], [-1], [2], [1], [-5], [4]], "单列 $9\\times1$",
         "最大子段总和 $6$（第 $3\\sim6$ 行）", "只处理了行方向，列方向退化错误", True),
        ([[-1, -2, -3], [-4, -5, -6], [-7, -8, -9]], "全负数 $3\\times3$",
         "最大的是 $-1$，位于 $(0,0)$", "认为答案一定非负", True),
        ([[0] * 4 for _ in range(3)], "全 $0$，$3\\times4$",
         "任何单个格子总和都是 $0$，输出合法坐标即可",
         "把「总和为 $0$」误判成「没有合法子矩阵」", True),
        ([[RNG.randint(1, 1000) for _ in range(6)] for _ in range(5)], "全正数 $5\\times6$",
         "最优就是整个矩阵，必须输出 $0\\ 0\\ 4\\ 5$",
         "只取部分行列导致总和偏小", True),
        (neg5, "hack 组：$7\\times7$，四周全 $-5$，中间 $3\\times3$ 为 $3$",
         "最优是中间那块 $3\\times3$，总和 $27$",
         "只考虑整行/整列/整个矩阵的错解会算出更小的总和", True),
        ([[RNG.randint(V_LO, V_HI) for _ in range(N_MAX)] for _ in range(N_MAX)],
         "压满 $200\\times200$，元素 $[-1000,1000]$",
         "压测 $O(N^2M)$ 与读入", "$O(N^2M^2)$ 全枚举会超时", False),
    ]
    assert len(plan) == 10

    for idx, (matrix, _, _, _, _) in enumerate(plan, 1):
        write_case(idx, matrix)

    # ---- 生成后自校验 ----
    for i, (matrix, _, _, _, do_brute) in enumerate(plan, 1):
        ib = (DATA / f"{i}.in").read_bytes()
        ob = (DATA / f"{i}.out").read_bytes()
        assert not ib.endswith(b"\n") and b"\r" not in ib, f"{i}.in 换行规则不符"
        assert ob.endswith(b"\n") and not ob.endswith(b"\n\n") and b"\r" not in ob, f"{i}.out 换行规则不符"
        assert ob.count(b"\n") == 1, f"{i}.out 应只有一行"

        n, m = len(matrix), len(matrix[0])
        lines = ib.decode("utf-8").split("\n")
        hn, hm = map(int, lines[0].split())
        assert (hn, hm) == (n, m), f"{i}.in 首行的 N M 与矩阵不符"
        for k in range(n):
            assert len(lines[1 + k].split()) == m, f"{i}.in 第 {k} 行元素个数不符"

        # 坐标合法性
        r1, c1, r2, c2 = map(int, ob.decode("utf-8").split())
        assert 0 <= r1 <= r2 < n and 0 <= c1 <= c2 < m, f"{i} 坐标越界或顺序颠倒"
        assert ob.decode("utf-8").strip() == f"{r1} {c1} {r2} {c2}", f"{i}.out 格式不符"

        # 关键：输出坐标对应的总和必须等于真实最大总和
        got = rect_sum(matrix, r1, c1, r2, c2)
        truth = alt_max_sum(matrix)
        assert got == truth, f"{i} 输出坐标的总和 {got} != 真实最大 {truth}"
        if do_brute:
            bf = brute_max_sum(matrix)
            assert bf == truth, f"{i} 暴力 {bf} != 另一路径 {truth}"

    # 关键期望值锁定
    assert max_submatrix([[-1, 0], [0, -1]]) == (0, 1, 0, 1) or \
        rect_sum([[-1, 0], [0, -1]], *max_submatrix([[-1, 0], [0, -1]])) == 0
    assert rect_sum([[-2, 1, -3, 4, -1, 2, 1, -5, 4]],
                    *max_submatrix([[-2, 1, -3, 4, -1, 2, 1, -5, 4]])) == 6
    assert max_submatrix(neg5) == (2, 2, 4, 4)
    allpos = plan[7][0]
    assert max_submatrix(allpos) == (0, 0, 4, 5)
    assert rect_sum(plan[8][0], *max_submatrix(plan[8][0])) == 27
    assert rect_sum(plan[5][0], *max_submatrix(plan[5][0])) == -1

    readme = [
        "# P7122 测试数据说明",
        "",
        "主造数脚本：题目根目录 `gen.py`。",
        "stdin：第一行 `N M`，接下来 `N` 行每行 `M` 个整数。",
        "输出：四个整数 `r1 c1 r2 c2`（最优子矩阵的左上角与右下角，并列时任取一个）。",
        "",
        "元素取值范围说明：题面只约束 $1 \\le N, M \\le 200$，未给元素范围，",
        "本套数据取 $[-1000, 1000]$。此时总和上界为 $200 \\times 200 \\times 1000 = 4 \\times 10^7$，",
        "仍在 $32$ 位内，但标程统一用 $64$ 位保存总和更稳妥。",
        "",
        "| 组别 | 规模/分布 | 目标 | 卡掉的错误解 |",
        "|---|---|---|---|",
    ]
    for i, (_, scale, goal, hack, _) in enumerate(plan, 1):
        readme.append(f"| {i} | {scale} | {goal} | {hack} |")
    readme += [
        "",
        "`.in` 最后一行后无换行符；`.out` 末尾恰好一个换行符。",
        "",
        "生成后自校验（因题面允许并列，比对的是**总和**而不是坐标）：",
        "",
        "1. 输出的四个坐标必须满足 `0 <= r1 <= r2 < N`、`0 <= c1 <= c2 < M`；",
        "2. 用二维前缀和算出「输出坐标对应子矩阵的真实总和」，它必须等于真实最大总和；",
        "3. 第 1~9 组额外用 `brute_max_sum`（二维前缀和枚举全部矩形，$O(N^2M^2)$）独立求出真实最大总和做交叉校验；",
        "4. 第 10 组规模为 $200 \\times 200$，改用另一条独立实现路径 `alt_max_sum`",
        "   （列前缀和取列和 + 另一种 Kadane 写法 `cur = max(x, cur+x)`）校验总和。",
        "",
    ]
    (DATA / "README.md").write_text("\n".join(readme), encoding="utf-8")

    print("P7122 data ok:", [max_submatrix(c[0]) for c in plan])


if __name__ == "__main__":
    main()
