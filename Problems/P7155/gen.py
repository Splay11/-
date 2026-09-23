# -*- coding: utf-8 -*-
"""P7155 造数：组合总和 IV（可重复、顺序不同算不同）。

stdin：第一行 n target，第二行 n 个互不相同正整数。
输出：有序方案数。
`.in` 最后一行后不留换行；`.out` 末尾恰好一个换行。
答案保证在有符号 32 位整数范围内。
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
RNG = random.Random(715520260915)

N_MAX = 200
V_MAX = 1000
T_MAX = 1000
INT_MAX = 2**31 - 1


def naive(nums, target):
    """记忆化搜索：当前剩余量每次选一个数，与 DP 对拍。"""
    memo = {}

    def dfs(rest):
        if rest == 0:
            return 1
        if rest in memo:
            return memo[rest]
        s = 0
        for x in nums:
            if rest >= x:
                s += dfs(rest - x)
        memo[rest] = s
        return s

    return dfs(target)


def combo(nums, target):
    """假解：组合背包，顺序不同只计一次。"""
    dp = [0] * (target + 1)
    dp[0] = 1
    for x in nums:
        for t in range(x, target + 1):
            dp[t] += dp[t - x]
    return dp[target]


def write_case(idx, nums, target):
    n = len(nums)
    assert 1 <= n <= N_MAX
    assert 1 <= target <= T_MAX
    assert len(set(nums)) == n
    for x in nums:
        assert 1 <= x <= V_MAX
    ans = solve(nums, target)
    expect = naive(nums, target)
    assert ans == expect, (idx, ans, expect)
    assert 0 <= ans <= INT_MAX
    inp = f"{n} {target}\n" + " ".join(str(x) for x in nums)
    (DATA / f"{idx}.in").write_bytes(inp.encode("utf-8"))
    with open(DATA / f"{idx}.out", "w", encoding="utf-8", newline="\n") as f:
        f.write(str(ans) + "\n")
    return ans


def unique_from(lo, hi, n):
    pool = list(range(lo, hi + 1))
    RNG.shuffle(pool)
    return pool[:n]


def main():
    DATA.mkdir(parents=True, exist_ok=True)

    p8 = unique_from(2, 20, 8)
    t8 = 12
    # 大数为主，避免含 1 时方案数爆 int
    p9 = unique_from(400, 1000, N_MAX)
    p10 = unique_from(250, 1000, N_MAX)

    plan = [
        ([1, 2, 3], 4,
         "样例 1，顺序不同要分开计", "$7$",
         "组合背包得到 $4$"),
        ([9], 3,
         "样例 2，凑不出", "$0$",
         "输出 $1$"),
        ([4], 4,
         "单个数正好等于目标", "$1$",
         "输出 $0$"),
        ([2], 4,
         "重复使用同一个数", "$2+2$ 只有一种顺序，答案 $1$",
         "当成不能重复得到 $0$"),
        ([1, 2], 3,
         "$1+1+1$、$1+2$、$2+1$", "$3$",
         "漏掉 $2,1$"),
        ([3, 4], 7,
         "两个不同数的两种顺序", "$3+4$ 与 $4+3$，答案 $2$",
         "只计一种"),
        ([5, 7], 3,
         "所有数都比目标大", "$0$",
         "输出负数"),
        (p8, t8,
         "小随机、不含 $1$", "DP 与记忆化搜索对拍",
         "0-1 背包每个数只用一次"),
        (p9, T_MAX,
         "压满 $n=200$，数值 $\\ge 400$，$target=1000$", "至多选两个数",
         "含 $1$ 时斐波那契式爆 int"),
        (p10, T_MAX,
         "压满 $n=200$，数值 $\\ge 250$，$target=1000$", "$O(n\\cdot target)$",
         "指数枚举排列 TLE"),
    ]
    assert len(plan) == 10

    answers = []
    metas = []
    for idx, (nums, target, _, _, _) in enumerate(plan, 1):
        metas.append((nums, target))
        answers.append(write_case(idx, nums, target))

    for i, (nums, target) in enumerate(metas, 1):
        ib = (DATA / f"{i}.in").read_bytes()
        ob = (DATA / f"{i}.out").read_bytes()
        assert not ib.endswith(b"\n") and b"\r" not in ib, f"{i}.in"
        assert ob.endswith(b"\n") and not ob.endswith(b"\n\n") and b"\r" not in ob
        expect_in = f"{len(nums)} {target}\n" + " ".join(str(x) for x in nums)
        assert ib.decode("utf-8") == expect_in
        got = ob.decode("utf-8")[:-1]
        assert got == str(answers[i - 1])

    assert answers[0] == 7
    assert answers[1] == 0
    assert answers[2] == 1
    assert answers[3] == 1
    assert answers[4] == 3
    assert answers[5] == 2
    assert answers[6] == 0
    assert combo([1, 2, 3], 4) == 4
    assert len(metas[8][0]) == N_MAX and len(metas[9][0]) == N_MAX

    rows = []
    for i, (_, _, scale, goal, hack) in enumerate(plan, 1):
        rows.append(f"| {i} | {scale} | {goal} | {hack} |")

    readme = "\n".join([
        "# P7155 测试数据说明",
        "",
        "主造数脚本：题目根目录 `gen.py`。",
        "stdin：第一行 $n$ $target$，第二行 $n$ 个互不相同的正整数。",
        "输出：有序方案数（可重复使用；顺序不同算不同）。",
        "",
        r"约束：$1\le n\le 200$，$1\le nums_i,target\le 1000$，答案在 $32$ 位有符号整数内。",
        "",
        "| 组别 | 规模/分布 | 目标 | 卡掉的错误解 |",
        "|---|---|---|---|",
        *rows,
        "",
        "`.in` 最后一行后无换行符；`.out` 末尾恰好一个换行符。",
        "",
        "生成后自校验：完全背包 DP 必须等于记忆化搜索，且答案 $\\le 2^{31}-1$。",
        "",
    ])
    (DATA / "README.md").write_text(readme, encoding="utf-8")
    print("generated 10 cases")
    for i, ans in enumerate(answers, 1):
        print(i, ans, "n", len(metas[i - 1][0]), "t", metas[i - 1][1])


if __name__ == "__main__":
    main()
