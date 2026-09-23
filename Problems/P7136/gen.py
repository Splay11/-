# -*- coding: utf-8 -*-
"""P7136 造数：升序数组二分查找。

stdin：第一行 n target；第二行 n 个严格升序互异整数。
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
RNG = random.Random(713620260914)

N_MAX = 10000
V_LO, V_HI = -9999, 9999


def naive(nums, target):
    for i, x in enumerate(nums):
        if x == target:
            return i
        if x > target:
            return -1
    return -1


def case_in_text(target, nums):
    n = len(nums)
    return f"{n} {target}\n" + " ".join(map(str, nums))


def write_case(idx, target, nums):
    n = len(nums)
    assert 1 <= n <= N_MAX
    assert all(V_LO <= x <= V_HI for x in nums)
    assert nums == sorted(nums)
    assert len(set(nums)) == n
    (DATA / f"{idx}.in").write_bytes(case_in_text(target, nums).encode("utf-8"))
    ans = solve(nums, target)
    expect = naive(nums, target)
    assert ans == expect, (idx, ans, expect)
    with open(DATA / f"{idx}.out", "w", encoding="utf-8", newline="\n") as f:
        f.write(str(ans) + "\n")
    return ans


def main():
    DATA.mkdir(parents=True, exist_ok=True)

    sample = [-1, 0, 3, 5, 9, 12]
    big = list(range(V_LO, V_LO + N_MAX))
    assert len(big) == N_MAX
    assert 0 in big
    big_hit = big[N_MAX // 2]
    # 数组是 -9999..0，1 不在其中
    big_miss = 1

    rand_vals = sorted(RNG.sample(range(V_LO, V_HI + 1), 30))
    rand_hit = rand_vals[11]
    hole = None
    for x in range(rand_vals[0], rand_vals[-1]):
        if x not in set(rand_vals):
            hole = x
            break

    plan = [
        (9, sample,
         "样例 1", "找到 $9$，下标 $4$",
         "返回值而不是下标"),
        (2, sample,
         "样例 2，目标不在数组中", "输出 $-1$",
         "返回插入位置 $2$"),
        (7, [7],
         "单元素且命中", "下标 $0$",
         "区间写成开区间漏掉唯一元素"),
        (0, [7],
         "单元素且未命中", "输出 $-1$",
         "仍输出 $0$"),
        (-1, sample,
         "命中左端点", "下标 $0$",
         "mid 取上整漏掉左边界"),
        (12, sample,
         "命中右端点", "下标 $5$",
         "right=mid 死循环或漏掉右端"),
        (-2, sample,
         "比最小值还小", "输出 $-1$",
         "返回 $0$"),
        (13, sample,
         "比最大值还大", "输出 $-1$",
         "返回 $n$ 或 $n-1$"),
        (big_hit, big,
         "压满 $n=10000$，命中中点附近", "返回对应下标",
         "下标算错差一"),
        (big_miss, big,
         "压满 $n=10000$，目标 $1$ 不在 $-9999\\cdots 0$ 中", "输出 $-1$",
         "在空洞处返回错误插入下标"),
    ]
    assert len(plan) == 10
    _ = (rand_hit, hole)

    answers = []
    for idx, (target, nums, _, _, _) in enumerate(plan, 1):
        answers.append(write_case(idx, target, nums))

    for i, (target, nums, _, _, _) in enumerate(plan, 1):
        ib = (DATA / f"{i}.in").read_bytes()
        ob = (DATA / f"{i}.out").read_bytes()
        assert not ib.endswith(b"\n") and b"\r" not in ib, f"{i}.in"
        assert ob.endswith(b"\n") and not ob.endswith(b"\n\n") and b"\r" not in ob
        text = ib.decode("utf-8")
        lines = text.split("\n")
        hn, ht = map(int, lines[0].split())
        arr = list(map(int, lines[1].split()))
        assert hn == len(nums) == len(arr) and ht == target and arr == nums
        got = int(ob.decode("utf-8").strip())
        assert got == answers[i - 1] == naive(nums, target)

    assert answers[0] == 4
    assert answers[1] == -1
    assert answers[2] == 0
    assert answers[3] == -1
    assert answers[4] == 0
    assert answers[5] == 5
    assert answers[6] == -1
    assert answers[7] == -1
    assert answers[8] == N_MAX // 2
    assert answers[9] == -1

    rows = []
    for i, (_, _, scale, goal, hack) in enumerate(plan, 1):
        rows.append(f"| {i} | {scale} | {goal} | {hack} |")

    readme = "\n".join([
        "# P7136 测试数据说明",
        "",
        "主造数脚本：题目根目录 `gen.py`。",
        "stdin：第一行 `n target`；第二行 $n$ 个严格升序互异整数。",
        "输出：目标下标，不存在则为 $-1$。",
        "",
        r"约束：$1\le n\le 10000$，$-9999\le nums_i\le 9999$，严格升序且互异。",
        "",
        "| 组别 | 规模/分布 | 目标 | 卡掉的错误解 |",
        "|---|---|---|---|",
        *rows,
        "",
        "`.in` 最后一行后无换行符；`.out` 末尾恰好一个换行符。",
        "",
        "生成后自校验：二分结果必须等于从左到右线性扫描的下标。",
        "",
        "说明：$n$ 上限较小，线性扫描也能过最大数据；本组仍覆盖命中/未命中与两端边界。",
        "",
    ])
    (DATA / "README.md").write_text(readme, encoding="utf-8")
    print("generated 10 cases")
    for i, ans in enumerate(answers, 1):
        print(i, "ans", ans)


if __name__ == "__main__":
    main()
