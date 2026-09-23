# -*- coding: utf-8 -*-
"""P7160 造数：是否存在重复元素。输出小写 true/false。"""
from __future__ import annotations

import random
import sys
from pathlib import Path

sys.dont_write_bytecode = True
sys.path.insert(0, str(Path(__file__).resolve().parent))
from std import solve  # noqa: E402

ROOT = Path(__file__).resolve().parent
DATA = ROOT / "data"
RNG = random.Random(716020260915)
N_MAX = 10**5
V_MIN, V_MAX = -(10**9), 10**9


def brute(nums):
    return len(nums) != len(set(nums))


def adj_only(nums):
    return any(nums[i] == nums[i + 1] for i in range(len(nums) - 1))


def write_case(idx, nums):
    n = len(nums)
    assert 1 <= n <= N_MAX
    for x in nums:
        assert V_MIN <= x <= V_MAX
    ans = solve(nums)
    if n <= 5000:
        assert ans == brute(nums)
    text = "true" if ans else "false"
    inp = f"{n}\n" + " ".join(str(x) for x in nums)
    (DATA / f"{idx}.in").write_bytes(inp.encode("utf-8"))
    with open(DATA / f"{idx}.out", "w", encoding="utf-8", newline="\n") as f:
        f.write(text + "\n")
    return text


def main():
    DATA.mkdir(parents=True, exist_ok=True)
    unique_big = list(range(1, N_MAX + 1))
    dup_big = list(range(N_MAX - 1)) + [0]

    plan = [
        ([1, 2, 3, 1], "样例 1，末尾重复", "true", "只看相邻得到 false"),
        ([1, 2, 3, 4], "样例 2，全不同", "false", "输出 true"),
        ([1, 1, 1, 3, 3, 4, 3, 2, 4, 2], "样例 3，多处重复", "true", "去重后比长度"),
        ([7], "n=1", "false", "输出 true"),
        ([-1, -1], "负数重复", "true", "没处理负数"),
        ([V_MIN, V_MAX], "值域两端且不同", "false", "溢出当相同"),
        ([3, 1, 2, 3], "重复不在相邻位置", "true", "只比较相邻"),
        ([RNG.randint(-50, 50) for _ in range(80)], "中等随机", "与集合对拍", "O(n^2) 后面 TLE"),
        (unique_big, "压满 n=10^5 全不同", "false", "O(n^2) TLE"),
        (dup_big, "压满 n=10^5 最后两数相同", "true", "只查前半段"),
    ]
    assert adj_only([3, 1, 2, 3]) is False

    answers, metas = [], []
    for i, (nums, _, _, _) in enumerate(plan, 1):
        metas.append(nums)
        answers.append(write_case(i, nums))
    assert answers[0] == "true" and answers[1] == "false" and answers[2] == "true"
    assert answers[3] == "false" and answers[8] == "false" and answers[9] == "true"

    for i, nums in enumerate(metas, 1):
        ib = (DATA / f"{i}.in").read_bytes()
        ob = (DATA / f"{i}.out").read_bytes()
        assert not ib.endswith(b"\n") and b"\r" not in ib
        assert ob.endswith(b"\n") and not ob.endswith(b"\n\n")
        assert ib.decode("utf-8") == f"{len(nums)}\n" + " ".join(str(x) for x in nums)
        assert ob.decode("utf-8")[:-1] == answers[i - 1]

    rows = [f"| {i} | {p[1]} | {p[2]} | {p[3]} |" for i, p in enumerate(plan, 1)]
    (DATA / "README.md").write_text(
        "\n".join([
            "# P7160 测试数据说明",
            "",
            "主造数脚本：题目根目录 `gen.py`。输出小写 true/false。",
            r"约束：$1\le n\le 10^5$，$-10^9\le nums_i\le 10^9$。",
            "",
            "| 组别 | 规模/分布 | 目标 | 卡掉的错误解 |",
            "|---|---|---|---|",
            *rows,
            "",
            "`.in` 最后一行后无换行符；`.out` 末尾恰好一个换行符。",
            "",
        ]),
        encoding="utf-8",
    )
    print("generated 10 cases")
    for i, a in enumerate(answers, 1):
        print(i, a, "n", len(metas[i - 1]))


if __name__ == "__main__":
    main()
