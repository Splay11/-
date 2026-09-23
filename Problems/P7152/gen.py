# -*- coding: utf-8 -*-
"""P7152 造数：第 k 大元素（含重复排名）。

stdin：第一行 n k，第二行 n 个整数。
输出：第 k 大。
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
RNG = random.Random(715220260915)

N_MAX = 10**5
V_MIN, V_MAX = -10**4, 10**4


def naive(nums, k):
    """全排序后取第 k 大，与计数对拍。"""
    return sorted(nums, reverse=True)[k - 1]


def unique_kth(nums, k):
    """假解：去重后再取第 k 大。"""
    return sorted(set(nums), reverse=True)[k - 1]


def write_case(idx, nums, k):
    n = len(nums)
    assert 1 <= k <= n <= N_MAX
    for x in nums:
        assert V_MIN <= x <= V_MAX
    ans = solve(nums, k)
    expect = naive(nums, k)
    assert ans == expect, (idx, ans, expect)
    inp = f"{n} {k}\n" + " ".join(str(x) for x in nums)
    (DATA / f"{idx}.in").write_bytes(inp.encode("utf-8"))
    with open(DATA / f"{idx}.out", "w", encoding="utf-8", newline="\n") as f:
        f.write(str(ans) + "\n")
    return ans


def main():
    DATA.mkdir(parents=True, exist_ok=True)

    p8 = [RNG.randint(V_MIN, V_MAX) for _ in range(30)]
    k8 = RNG.randint(1, 30)
    p9 = [RNG.randint(V_MIN, V_MAX) for _ in range(N_MAX)]
    k9 = RNG.randint(1, N_MAX)
    p10 = [RNG.choice([-10000, -1, 0, 1, 10000, 5, 5, 6]) for _ in range(N_MAX)]
    k10 = 4

    plan = [
        ([3, 2, 1, 5, 6, 4], 2,
         "样例 1", "第 $2$ 大是 $5$",
         "当成第 $2$ 小得到 $2$"),
        ([3, 2, 3, 1, 2, 4, 5, 5, 6], 4,
         "样例 2，重复值占名次", "$6,5,5,4$ 所以是 $4$",
         "去重后第 $4$ 大得到 $3$"),
        ([7], 1,
         "只有一个数", "$7$",
         "下标越界"),
        ([1, 2, 3], 1,
         "第 $1$ 大即最大值", "$3$",
         "取成最小值"),
        ([1, 2, 3], 3,
         "第 $n$ 大即最小值", "$1$",
         "取成最大值"),
        ([-5, -1, -5, 0], 2,
         "含负数", "排序 $0,-1,-5,-5$，第 $2$ 大是 $-1$",
         "绝对值比较得到 $-5$"),
        ([9, 9, 9, 9], 3,
         "全部相同", "$9$",
         "去重后没有第 $3$ 个"),
        (p8, k8,
         "小随机", "计数与全排序对拍",
         "k 从 $0$ 开始取错一位"),
        (p9, k9,
         "压满 $n=10^5$ 随机值域", "$O(n+|V|)$ 计数",
         "$O(n^2)$ 选择排序 TLE"),
        (p10, k10,
         "压满，大量重复与极值", "重复值分别占名次",
         "去重后再取第 $k$ 大"),
    ]
    assert len(plan) == 10

    answers = []
    metas = []
    for idx, (nums, k, _, _, _) in enumerate(plan, 1):
        metas.append((nums, k))
        answers.append(write_case(idx, nums, k))

    for i, (nums, k) in enumerate(metas, 1):
        ib = (DATA / f"{i}.in").read_bytes()
        ob = (DATA / f"{i}.out").read_bytes()
        assert not ib.endswith(b"\n") and b"\r" not in ib, f"{i}.in"
        assert ob.endswith(b"\n") and not ob.endswith(b"\n\n") and b"\r" not in ob
        expect_in = f"{len(nums)} {k}\n" + " ".join(str(x) for x in nums)
        assert ib.decode("utf-8") == expect_in
        got = ob.decode("utf-8")[:-1]
        assert got == str(answers[i - 1]) == str(naive(nums, k))

    assert answers[0] == 5
    assert answers[1] == 4
    assert answers[2] == 7
    assert answers[3] == 3
    assert answers[4] == 1
    assert answers[5] == -1
    assert answers[6] == 9
    u2 = unique_kth(metas[1][0], 4)
    assert u2 != answers[1]
    assert len(metas[8][0]) == N_MAX and len(metas[9][0]) == N_MAX

    rows = []
    for i, (_, _, scale, goal, hack) in enumerate(plan, 1):
        rows.append(f"| {i} | {scale} | {goal} | {hack} |")

    readme = "\n".join([
        "# P7152 测试数据说明",
        "",
        "主造数脚本：题目根目录 `gen.py`。",
        "stdin：第一行 $n$ $k$，第二行 $n$ 个整数。",
        "输出：第 $k$ 大（重复值分别占名次）。",
        "",
        r"约束：$1\le k\le n\le 10^5$，$-10^4\le nums_i\le 10^4$。",
        "",
        "| 组别 | 规模/分布 | 目标 | 卡掉的错误解 |",
        "|---|---|---|---|",
        *rows,
        "",
        "`.in` 最后一行后无换行符；`.out` 末尾恰好一个换行符。",
        "",
        "生成后自校验：计数排序必须等于从大到小全排序后的第 $k$ 项。",
        "",
    ])
    (DATA / "README.md").write_text(readme, encoding="utf-8")
    print("generated 10 cases")
    for i, ans in enumerate(answers, 1):
        print(i, ans, "n", len(metas[i - 1][0]), "k", metas[i - 1][1])


if __name__ == "__main__":
    main()
