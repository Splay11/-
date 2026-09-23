# -*- coding: utf-8 -*-
"""P7159 造数：总和 >= target 的最短连续子数组长度。"""
from __future__ import annotations

import random
import sys
from pathlib import Path

sys.dont_write_bytecode = True
sys.path.insert(0, str(Path(__file__).resolve().parent))
from std import solve  # noqa: E402

ROOT = Path(__file__).resolve().parent
DATA = ROOT / "data"
RNG = random.Random(715920260915)

N_MAX = 10**5
V_MAX = 10**4
T_MAX = 10**9


def brute(nums, target):
    """O(n^2) 枚举所有子数组。"""
    n = len(nums)
    ans = n + 1
    for i in range(n):
        s = 0
        for j in range(i, n):
            s += nums[j]
            if s >= target:
                ans = min(ans, j - i + 1)
                break
    return 0 if ans == n + 1 else ans


def strict_greater(nums, target):
    """假解：用 > 而不是 >=。"""
    n = len(nums)
    left = 0
    s = 0
    ans = n + 1
    for right in range(n):
        s += nums[right]
        while s > target:
            ans = min(ans, right - left + 1)
            s -= nums[left]
            left += 1
    return 0 if ans == n + 1 else ans


def write_case(idx, nums, target):
    n = len(nums)
    assert 1 <= n <= N_MAX
    assert 1 <= target <= T_MAX
    for x in nums:
        assert 1 <= x <= V_MAX
    ans = solve(nums, target)
    if n <= 400:
        assert brute(nums, target) == ans
    inp = f"{n} {target}\n" + " ".join(str(x) for x in nums)
    (DATA / f"{idx}.in").write_bytes(inp.encode("utf-8"))
    with open(DATA / f"{idx}.out", "w", encoding="utf-8", newline="\n") as f:
        f.write(str(ans) + "\n")
    return ans


def main():
    DATA.mkdir(parents=True, exist_ok=True)

    small = [RNG.randint(1, 20) for _ in range(50)]
    t8 = sum(small) // 3 + 1
    no_sol = [1] * N_MAX
    # 末尾放一个刚好等于 target 的数，前面都是 1，卡最短为 1
    has_one = [1] * N_MAX
    has_one[-1] = V_MAX
    t10 = V_MAX

    plan = [
        ([2, 3, 1, 2, 4, 3], 7,
         "样例 1，最短是 $4+3$", "$2$",
         "输出更长的 $2+3+1+2$"),
        ([1, 4, 4], 4,
         "样例 2，单元素达标", "$1$",
         "用 $>$ 判断会漏掉等于 $target$"),
        ([1, 1, 1, 1, 1, 1, 1, 1], 11,
         "样例 3，总和不够", "$0$",
         "输出 $8$ 或 $n$"),
        ([9], 9,
         "$n=1$ 且恰好达标", "$1$",
         "输出 $0$"),
        ([3], 10,
         "$n=1$ 且不够", "$0$",
         "输出 $1$"),
        ([1, 1, 1, 100], 100,
         "后面一个数单独达标", "$1$",
         "不收缩窗口输出 $4$"),
        ([5, 1, 1, 1, 2], 5,
         "第一个数就达标", "$1$",
         "求最长合法段"),
        (small, t8,
         "中等随机 $n=50$", "与 $O(n^2)$ 枚举对拍",
         "枚举全部子数组在后面 TLE"),
        (no_sol, T_MAX,
         "压满 $n=10^5$，总和 $10^5$ 远小于 $target$", "$0$",
         "没判断整段不够仍输出正数"),
        (has_one, t10,
         "压满 $n=10^5$，最后一张 $10^4$ 单独达标", "$1$",
         "$O(n^2)$ TLE；不收缩窗口输出 $n$"),
    ]
    assert len(plan) == 10
    assert strict_greater([1, 4, 4], 4) != 1

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
        expect = f"{len(nums)} {target}\n" + " ".join(str(x) for x in nums)
        assert ib.decode("utf-8") == expect
        assert ob.decode("utf-8")[:-1] == str(answers[i - 1])

    assert answers[0] == 2
    assert answers[1] == 1
    assert answers[2] == 0
    assert answers[3] == 1
    assert answers[4] == 0
    assert answers[5] == 1
    assert answers[6] == 1
    assert answers[8] == 0
    assert answers[9] == 1
    assert len(metas[8][0]) == N_MAX and len(metas[9][0]) == N_MAX

    rows = []
    for i, (_, _, scale, goal, hack) in enumerate(plan, 1):
        rows.append(f"| {i} | {scale} | {goal} | {hack} |")
    readme = "\n".join([
        "# P7159 测试数据说明",
        "",
        "主造数脚本：题目根目录 `gen.py`。",
        "stdin：第一行 $n$ $target$，第二行 $n$ 个正整数。",
        "输出：总和 $\\ge target$ 的最短连续子数组长度，不存在则 $0$。",
        "",
        r"约束：$1\le n\le 10^5$，$1\le nums_i\le 10^4$，$1\le target\le 10^9$。",
        "",
        "| 组别 | 规模/分布 | 目标 | 卡掉的错误解 |",
        "|---|---|---|---|",
        *rows,
        "",
        "`.in` 最后一行后无换行符；`.out` 末尾恰好一个换行符。",
        "",
        "生成后自校验：$n\\le 400$ 时滑动窗口必须等于枚举所有子数组。",
        "",
    ])
    (DATA / "README.md").write_text(readme, encoding="utf-8")
    print("generated 10 cases")
    for i, ans in enumerate(answers, 1):
        print(i, ans, "n", len(metas[i - 1][0]), "t", metas[i - 1][1])


if __name__ == "__main__":
    main()
