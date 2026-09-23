# -*- coding: utf-8 -*-
"""P7124 造数：最短连续子数组使和 >= target。

stdin：第一行 n target，第二行 n 个正整数。
输出：一个整数（没有则 0）。
`.in` 最后一行后不留换行；`.out` 末尾恰好一个换行。
"""
from __future__ import annotations

import random
import sys
from pathlib import Path

sys.dont_write_bytecode = True
sys.path.insert(0, str(Path(__file__).resolve().parent))
from std import min_subarray_len  # noqa: E402

ROOT = Path(__file__).resolve().parent
DATA = ROOT / "data"
RNG = random.Random(712420260914)

N_MAX = 10**5
A_HI = 10**4
T_HI = 10**9


def brute(nums, target):
    n = len(nums)
    ans = n + 1
    for i in range(n):
        s = 0
        for j in range(i, n):
            s += nums[j]
            if s >= target:
                if j - i + 1 < ans:
                    ans = j - i + 1
                break
    return 0 if ans == n + 1 else ans


def alt_prefix_bin(nums, target):
    """前缀和 + 二分右端点，另一条 O(n log n) 路径。"""
    n = len(nums)
    pre = [0] * (n + 1)
    for i, x in enumerate(nums):
        pre[i + 1] = pre[i] + x
    ans = n + 1
    for i in range(n):
        need = pre[i] + target
        lo, hi = i + 1, n
        pos = n + 1
        while lo <= hi:
            mid = (lo + hi) // 2
            if pre[mid] >= need:
                pos = mid
                hi = mid - 1
            else:
                lo = mid + 1
        if pos <= n and pos - i < ans:
            ans = pos - i
    return 0 if ans == n + 1 else ans


def case_in_text(n, target, nums):
    return f"{n} {target}\n" + " ".join(map(str, nums))


def write_case(idx, target, nums):
    n = len(nums)
    assert 1 <= n <= N_MAX
    assert 1 <= target <= T_HI
    assert all(1 <= x <= A_HI for x in nums)
    (DATA / f"{idx}.in").write_bytes(case_in_text(n, target, nums).encode("utf-8"))
    ans = min_subarray_len(nums, target)
    with open(DATA / f"{idx}.out", "w", encoding="utf-8", newline="\n") as f:
        f.write(f"{ans}\n")
    return ans


def main():
    DATA.mkdir(parents=True, exist_ok=True)

    rand8 = [RNG.randint(1, 20) for _ in range(12)]
    t8 = RNG.randint(10, 40)

    big9 = [1] * N_MAX
    big10 = [1] * 40000 + [10000] * 5 + [1] * 59995
    assert len(big10) == N_MAX

    plan = [
        (7, [2, 3, 1, 2, 4, 3],
         "样例 1，$n=6,target=7$", "最短是 $4,3$，答案 $2$",
         "找到第一段 $2,3,1,2$ 就停，误输出 $4$", True),
        (4, [1, 4, 4],
         "样例 2，单元素已经够", "答案 $1$",
         "忽略长度为 $1$ 的合法段", True),
        (11, [1, 1, 1, 1, 1, 1, 1, 1],
         "样例 3，整段和仍不够", "答案 $0$",
         "没有解时误输出 $n$ 或最短正长度", True),
        (1, [1],
         "最小规模，刚好等于 $target$", "答案 $1$",
         "单点相等却输出 $0$", True),
        (2, [1],
         "最小规模，单点不够", "答案 $0$",
         "没有解时输出 $1$", True),
        (15, [1, 2, 3, 4, 5],
         "必须取整段，$sum=15$", "答案 $5$",
         "漏掉右端或提前收缩导致无解", True),
        (10, [1, 1, 1, 1, 10, 1, 1],
         "hack：中间一个 $10$ 就够", "答案 $1$，不是前面一长串",
         "取到第一段和 $\\ge target$ 就不再缩短", True),
        (t8, rand8,
         "小随机，$n=12$，值较小", "暴力可对拍",
         "收缩条件写成 $>$ 而不是 $\\ge$", True),
        (50000, big9,
         "压满 $n=10^5$，全 $1$，$target=50000$",
         "答案必须是 $50000$",
         "$O(n^2)$ 会超时；错误二分会偏 $1$", False),
        (30000, big10,
         "压满 $n=10^5$，中间连续 $5$ 个 $10^4$",
         "答案必须是 $3$（三个 $10000$ 刚好 $30000$）",
         "只看前缀/后缀，或把整段 $10^5$ 当答案", False),
    ]
    assert len(plan) == 10

    answers = []
    for idx, (target, nums, _, _, _, _) in enumerate(plan, 1):
        answers.append(write_case(idx, target, nums))

    for i, (target, nums, _, _, _, do_brute) in enumerate(plan, 1):
        ib = (DATA / f"{i}.in").read_bytes()
        ob = (DATA / f"{i}.out").read_bytes()
        assert not ib.endswith(b"\n") and b"\r" not in ib, f"{i}.in 换行规则不符"
        assert ob.endswith(b"\n") and not ob.endswith(b"\n\n") and b"\r" not in ob
        assert ob.count(b"\n") == 1

        lines = ib.decode("utf-8").split("\n")
        hn, ht = map(int, lines[0].split())
        arr = list(map(int, lines[1].split()))
        assert hn == len(nums) == len(arr) and ht == target and arr == nums

        got = int(ob.decode("utf-8").strip())
        truth = min_subarray_len(nums, target)
        alt = alt_prefix_bin(nums, target)
        assert got == truth == alt == answers[i - 1], f"{i} 不一致 {got} {truth} {alt}"
        if do_brute:
            bf = brute(nums, target)
            assert bf == truth, f"{i} 暴力 {bf} != {truth}"

    assert answers[0] == 2
    assert answers[1] == 1
    assert answers[2] == 0
    assert answers[3] == 1
    assert answers[4] == 0
    assert answers[5] == 5
    assert answers[6] == 1
    assert answers[8] == 50000
    assert answers[9] == 3

    rows = []
    for i, (_, _, scale, goal, hack, _) in enumerate(plan, 1):
        rows.append(f"| {i} | {scale} | {goal} | {hack} |")

    readme = "\n".join([
        "# P7124 测试数据说明",
        "",
        "主造数脚本：题目根目录 `gen.py`。",
        "stdin：第一行 `n target`，第二行 $n$ 个正整数。",
        "输出：最短连续子数组长度；不存在则 $0$。",
        "",
        r"约束：$1 \le n \le 10^5$，$1 \le target \le 10^9$，$1 \le nums_i \le 10^4$。",
        "",
        "| 组别 | 规模/分布 | 目标 | 卡掉的错误解 |",
        "|---|---|---|---|",
        *rows,
        "",
        "`.in` 最后一行后无换行符；`.out` 末尾恰好一个换行符。",
        "",
        "生成后自校验：",
        "",
        "1. 滑动窗口与「前缀和 + 二分」答案一致；",
        "2. 第 $1\\sim 8$ 组再用 $O(n^2)$ 暴力交叉校验。",
        "",
    ])
    (DATA / "README.md").write_text(readme, encoding="utf-8")
    print("generated 10 cases")
    for i, ans in enumerate(answers, 1):
        print(i, "ans", ans)


if __name__ == "__main__":
    main()
