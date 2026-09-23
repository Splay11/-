# -*- coding: utf-8 -*-
"""P7125 造数：多数元素（出现次数 > floor(n/2)）。

stdin：第一行 n，第二行 n 个整数。
输出：多数元素。题目保证一定存在。
`.in` 最后一行后不留换行；`.out` 末尾恰好一个换行。
"""
from __future__ import annotations

import random
import sys
from collections import Counter
from pathlib import Path

sys.dont_write_bytecode = True
sys.path.insert(0, str(Path(__file__).resolve().parent))
from std import majority_element  # noqa: E402

ROOT = Path(__file__).resolve().parent
DATA = ROOT / "data"
RNG = random.Random(712520260914)

N_MAX = 5 * 10**4
V_LO, V_HI = -10**9, 10**9


def count_mode(nums):
    """哈希计数，返回出现次数最多的数及其次数。"""
    c = Counter(nums)
    x, k = c.most_common(1)[0]
    return x, k


def make_array(n, maj, others):
    k = n // 2 + 1
    assert k + len(others) == n
    assert all(x != maj for x in others)
    arr = [maj] * k + list(others)
    RNG.shuffle(arr)
    return arr


def case_in_text(nums):
    return f"{len(nums)}\n" + " ".join(map(str, nums))


def write_case(idx, nums):
    n = len(nums)
    assert 1 <= n <= N_MAX
    assert all(V_LO <= x <= V_HI for x in nums)
    x, k = count_mode(nums)
    assert k > n // 2, (idx, x, k, n)
    (DATA / f"{idx}.in").write_bytes(case_in_text(nums).encode("utf-8"))
    ans = majority_element(nums)
    with open(DATA / f"{idx}.out", "w", encoding="utf-8", newline="\n") as f:
        f.write(f"{ans}\n")
    return ans


def main():
    DATA.mkdir(parents=True, exist_ok=True)

    others8 = [RNG.randint(V_LO, V_HI) for _ in range(5)]
    maj8 = 42
    others8 = [x if x != maj8 else maj8 + 1 for x in others8]
    arr8 = make_array(11, maj8, others8)

    maj9 = 1
    n9 = N_MAX
    k9 = n9 // 2 + 1
    others9 = []
    for _ in range(n9 - k9):
        x = RNG.randint(2, 1000)
        others9.append(x)
    arr9 = [maj9] * k9 + others9
    RNG.shuffle(arr9)

    maj10 = -10**9
    n10 = N_MAX
    k10 = n10 // 2 + 1
    others10 = [10**9 if i % 2 == 0 else 0 for i in range(n10 - k10)]
    arr10 = [maj10] * k10 + others10
    RNG.shuffle(arr10)

    plan = [
        ([3, 2, 3],
         "样例 1，$n=3$", "答案 $3$，出现 $2$ 次",
         "输出第一个数 $3$ 碰巧对，不足以覆盖后面的组"),
        ([2, 2, 1, 1, 1, 2, 2],
         "样例 2，$n=7$", "答案 $2$，出现 $4$ 次",
         "误把出现 $3$ 次的 $1$ 当成多数"),
        ([9],
         "最小规模 $n=1$", "答案就是唯一那个数",
         "空数组/下标越界"),
        ([5, 5, 5, 5],
         "全部相同", "答案 $5$",
         "投票时票数加减写反"),
        ([-3, 8, -3, 4, -3],
         "多数元素是负数", "答案 $-3$",
         "只统计正数，或用无符号类型"),
        ([7, 1, 7, 2, 7],
         "刚好过半：$3>\\lfloor 5/2 \\rfloor$", "答案 $7$",
         "写成 $\\ge n/2$ 时本题仍对，但次数判断要严格大于"),
        ([0, 1, 0, 1, 0, 1, 1],
         "多数 $1$ 偏后，开头不是答案", "答案 $1$",
         "直接输出 $nums_0$"),
        (arr8,
         "小随机，$n=11$，多数为 $42$", "哈希计数可对拍",
         "投票候选人更新条件写错"),
        (arr9,
         "压满 $n=5\\times 10^4$，多数为 $1$，刚过半",
         "答案 $1$",
         "$O(n^2)$ 计数超时"),
        (arr10,
         "压满 $n=5\\times 10^4$，多数为 $-10^9$，其余为 $0$ 或 $10^9$",
         "答案 $-10^9$",
         "32 位不够存元素，或漏掉负数"),
    ]
    assert len(plan) == 10

    answers = []
    for idx, (nums, _, _, _) in enumerate(plan, 1):
        answers.append(write_case(idx, nums))

    for i, (nums, _, _, _) in enumerate(plan, 1):
        ib = (DATA / f"{i}.in").read_bytes()
        ob = (DATA / f"{i}.out").read_bytes()
        assert not ib.endswith(b"\n") and b"\r" not in ib, f"{i}.in 换行规则不符"
        assert ob.endswith(b"\n") and not ob.endswith(b"\n\n") and b"\r" not in ob
        assert ob.count(b"\n") == 1

        lines = ib.decode("utf-8").split("\n")
        n = int(lines[0])
        arr = list(map(int, lines[1].split()))
        assert n == len(nums) == len(arr) and arr == nums

        got = int(ob.decode("utf-8").strip())
        x, k = count_mode(nums)
        assert k > n // 2
        assert got == x == majority_element(nums) == answers[i - 1], (i, got, x)

    assert answers[0] == 3
    assert answers[1] == 2
    assert answers[2] == 9
    assert answers[3] == 5
    assert answers[4] == -3
    assert answers[5] == 7
    assert answers[6] == 1
    assert answers[7] == 42
    assert answers[8] == 1
    assert answers[9] == -10**9

    rows = []
    for i, (_, scale, goal, hack) in enumerate(plan, 1):
        rows.append(f"| {i} | {scale} | {goal} | {hack} |")

    readme = "\n".join([
        "# P7125 测试数据说明",
        "",
        "主造数脚本：题目根目录 `gen.py`。",
        "stdin：第一行 `n`，第二行 $n$ 个整数。",
        "输出：多数元素（出现次数 $> \\lfloor n/2 \\rfloor$）。输入保证存在。",
        "",
        r"约束：$1 \le n \le 5\times 10^4$，$-10^9 \le nums_i \le 10^9$。",
        "",
        "| 组别 | 规模/分布 | 目标 | 卡掉的错误解 |",
        "|---|---|---|---|",
        *rows,
        "",
        "`.in` 最后一行后无换行符；`.out` 末尾恰好一个换行符。",
        "",
        "生成后自校验：哈希计数得到的众数必须与 Boyer-Moore 结果一致，且次数严格大于 $\\lfloor n/2 \\rfloor$。",
        "",
    ])
    (DATA / "README.md").write_text(readme, encoding="utf-8")
    print("generated 10 cases")
    for i, ans in enumerate(answers, 1):
        print(i, "ans", ans)


if __name__ == "__main__":
    main()
