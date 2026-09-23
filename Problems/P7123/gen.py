# -*- coding: utf-8 -*-
"""P7123 造数：最长公共子数组（ACM：第一行 n m，第二行 nums1，第三行 nums2）。

输出一个整数：最长公共连续段的长度。
写文件规则：`.in` 最后一行后不留换行；`.out` 末尾恰好一个换行。
"""
from __future__ import annotations

import random
import sys
from pathlib import Path

sys.dont_write_bytecode = True
sys.path.insert(0, str(Path(__file__).resolve().parent))
from std import longest_common_subarray  # noqa: E402

ROOT = Path(__file__).resolve().parent
DATA = ROOT / "data"
RNG = random.Random(712320260914)

N_MAX = 1000
V_LO, V_HI = 0, 100


def brute(a, b):
    """独立暴力：枚举所有起点，向右匹配，O(n m L)。"""
    n, m = len(a), len(b)
    ans = 0
    for i in range(n):
        for j in range(m):
            k = 0
            while i + k < n and j + k < m and a[i + k] == b[j + k]:
                k += 1
            if k > ans:
                ans = k
    return ans


def alt_dp(a, b):
    """另一条 DP：滚动一维，从后往前填，避免覆盖依赖。"""
    n, m = len(a), len(b)
    prev = [0] * (m + 1)
    ans = 0
    for i in range(1, n + 1):
        cur = [0] * (m + 1)
        for j in range(1, m + 1):
            if a[i - 1] == b[j - 1]:
                cur[j] = prev[j - 1] + 1
                if cur[j] > ans:
                    ans = cur[j]
        prev = cur
    return ans


def lcs_subseq(a, b):
    """错误解：当成最长公共子序列。"""
    n, m = len(a), len(b)
    dp = [[0] * (m + 1) for _ in range(n + 1)]
    for i in range(1, n + 1):
        for j in range(1, m + 1):
            if a[i - 1] == b[j - 1]:
                dp[i][j] = dp[i - 1][j - 1] + 1
            else:
                dp[i][j] = max(dp[i - 1][j], dp[i][j - 1])
    return dp[n][m]


def case_in_text(a, b):
    return f"{len(a)} {len(b)}\n" + " ".join(map(str, a)) + "\n" + " ".join(map(str, b))


def write_case(idx, a, b):
    n, m = len(a), len(b)
    assert 1 <= n <= N_MAX and 1 <= m <= N_MAX, (idx, n, m)
    assert all(V_LO <= x <= V_HI for x in a + b), idx
    (DATA / f"{idx}.in").write_bytes(case_in_text(a, b).encode("utf-8"))
    ans = longest_common_subarray(a, b)
    with open(DATA / f"{idx}.out", "w", encoding="utf-8", newline="\n") as f:
        f.write(f"{ans}\n")
    return ans


def main():
    DATA.mkdir(parents=True, exist_ok=True)

    rand8_a = [RNG.randint(V_LO, V_HI) for _ in range(15)]
    rand8_b = [RNG.randint(V_LO, V_HI) for _ in range(12)]
    rand10_a = [RNG.randint(V_LO, V_HI) for _ in range(N_MAX)]
    rand10_b = [RNG.randint(V_LO, V_HI) for _ in range(N_MAX)]

    constructed9_a = [0] * N_MAX
    constructed9_b = [1] * 250 + [0] * 500 + [1] * 250
    assert len(constructed9_b) == N_MAX

    # (a, b, 规模/分布, 目标, 卡掉的错误解, 是否暴力对拍)
    plan = [
        ([1, 2, 3, 2, 1], [3, 2, 1, 4, 7],
         "样例 1，$n=m=5$", "公共段 $3,2,1$，答案 $3$",
         "把子数组理解成子序列以外的别的东西", True),
        ([0, 0, 0, 0, 0], [0, 0, 0, 0, 0],
         "样例 2，两数组完全相同", "答案等于数组长度 $5$",
         "漏掉整段相等、答案偏小", True),
        ([1], [2],
         "最小规模 $1\\times1$，元素不同", "答案 $0$",
         "没有公共元素时误输出 $1$ 或数组长度", True),
        ([7], [7],
         "最小规模 $1\\times1$，元素相同", "答案 $1$",
         "单点相等却输出 $0$", True),
        ([1, 2, 3], [4, 5, 6],
         "完全没有公共元素", "答案 $0$",
         "用 $\\min(n,m)$ 当答案", True),
        ([1, 2, 3, 4], [1, 3, 2, 4],
         "hack：子序列更长、子数组很短", "公共子数组最长为 $1$，子序列却是 $3$",
         "按 LCS 子序列做会输出 $3$", True),
        ([9, 8, 1, 2, 3], [0, 1, 2, 3],
         "公共后缀，$n\\ne m$", "公共段 $1,2,3$，答案 $3$",
         "只处理等长数组、或只看前缀", True),
        (rand8_a, rand8_b,
         "小随机，$15\\times12$，值域 $[0,100]$", "暴力可对拍",
         "转移写反、忘记取全局最大值", True),
        (constructed9_a, constructed9_b,
         "压满 $1000\\times1000$，一边全 $0$，另一边中间连续 $500$ 个 $0$",
         "答案必须是 $500$",
         "只比较整段或只取两端公共前缀/后缀", False),
        (rand10_a, rand10_b,
         "压满 $1000\\times1000$ 随机，值域 $[0,100]$",
         "压测 $O(nm)$ 与读入",
         "$O(n^2m)$ 枚举起点再匹配会超时", False),
    ]
    assert len(plan) == 10

    answers = []
    for idx, (a, b, _, _, _, _) in enumerate(plan, 1):
        answers.append(write_case(idx, a, b))

    for i, (a, b, _, _, _, do_brute) in enumerate(plan, 1):
        ib = (DATA / f"{i}.in").read_bytes()
        ob = (DATA / f"{i}.out").read_bytes()
        assert not ib.endswith(b"\n") and b"\r" not in ib, f"{i}.in 换行规则不符"
        assert ob.endswith(b"\n") and not ob.endswith(b"\n\n") and b"\r" not in ob, f"{i}.out 换行规则不符"
        assert ob.count(b"\n") == 1, f"{i}.out 应只有一行"

        lines = ib.decode("utf-8").split("\n")
        hn, hm = map(int, lines[0].split())
        aa = list(map(int, lines[1].split()))
        bb = list(map(int, lines[2].split()))
        assert (hn, hm) == (len(a), len(b)) == (len(aa), len(bb))
        assert aa == a and bb == b

        got = int(ob.decode("utf-8").strip())
        truth = longest_common_subarray(a, b)
        alt = alt_dp(a, b)
        assert got == truth == alt == answers[i - 1], f"{i} DP 不一致 {got} {truth} {alt}"
        if do_brute:
            bf = brute(a, b)
            assert bf == truth, f"{i} 暴力 {bf} != DP {truth}"

        # 再算一遍，防止写出后被改
        rec = longest_common_subarray(aa, bb)
        if rec != got:
            raise SystemExit(f"自校验失败：{i}")

    assert answers[0] == 3
    assert answers[1] == 5
    assert answers[2] == 0
    assert answers[3] == 1
    assert answers[4] == 0
    assert answers[5] == 1
    assert lcs_subseq(plan[5][0], plan[5][1]) == 3
    assert answers[6] == 3
    assert answers[8] == 500

    rows = []
    for i, (_, _, scale, goal, hack, _) in enumerate(plan, 1):
        rows.append(f"| {i} | {scale} | {goal} | {hack} |")

    readme = "\n".join([
        "# P7123 测试数据说明",
        "",
        "主造数脚本：题目根目录 `gen.py`。",
        "stdin：第一行 `n m`，第二行 $n$ 个整数（$nums1$），第三行 $m$ 个整数（$nums2$）。",
        "输出：一个整数，最长公共子数组长度。",
        "",
        r"约束：$1 \le n,m \le 1000$，$0 \le nums1_i,nums2_i \le 100$。",
        "",
        "| 组别 | 规模/分布 | 目标 | 卡掉的错误解 |",
        "|---|---|---|---|",
        *rows,
        "",
        "`.in` 最后一行后无换行符；`.out` 末尾恰好一个换行符。",
        "",
        "生成后自校验：",
        "",
        "1. 标程 DP 与滚动数组 DP 答案一致；",
        "2. 第 $1\\sim 8$ 组再用 $O(nmL)$ 暴力匹配交叉校验；",
        "3. 第 $6$ 组确认 LCS 子序列答案为 $3$，而正确子数组答案为 $1$。",
        "",
    ])
    (DATA / "README.md").write_text(readme, encoding="utf-8")
    print("generated 10 cases")
    for i, ans in enumerate(answers, 1):
        print(i, "ans", ans)


if __name__ == "__main__":
    main()
