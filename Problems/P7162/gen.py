# -*- coding: utf-8 -*-
"""P7162 造数：互不相同、不含 0 的相反数对个数。"""
from __future__ import annotations

import random
import sys
from pathlib import Path

sys.dont_write_bytecode = True
sys.path.insert(0, str(Path(__file__).resolve().parent))
from std import solve  # noqa: E402

ROOT = Path(__file__).resolve().parent
DATA = ROOT / "data"
RNG = random.Random(716220260915)
N_MAX = 10**5
V_MAX = 10**9


def brute(nums):
    s = set(nums)
    return sum(1 for x in nums if x > 0 and -x in s)


def double_count(nums):
    s = set(nums)
    return sum(1 for x in nums if -x in s)


def write_case(idx, nums):
    n = len(nums)
    assert 1 <= n <= N_MAX
    assert len(set(nums)) == n
    for x in nums:
        assert x != 0 and -V_MAX <= x <= V_MAX
    ans = solve(nums)
    assert ans == brute(nums)
    inp = f"{n}\n" + " ".join(str(x) for x in nums)
    (DATA / f"{idx}.in").write_bytes(inp.encode("utf-8"))
    with open(DATA / f"{idx}.out", "w", encoding="utf-8", newline="\n") as f:
        f.write(str(ans) + "\n")
    return ans


def main():
    DATA.mkdir(parents=True, exist_ok=True)
    pos = list(range(1, N_MAX // 2 + 1))
    pairs_big = pos + [-x for x in pos]
    RNG.shuffle(pairs_big)
    all_pos = list(range(1, N_MAX + 1))

    plan = [
        ([1, -2, 3, -1, 2], "样例 1，两对", "2", "数两次得到 4"),
        ([1, 2, 3, 4, 5, 6], "样例 2，没有相反数", "0", "输出 n"),
        ([-5, 3, 8, 5, -3, 10, -8], "样例 3，三对", "3", "漏掉负数一侧"),
        ([9], "n=1", "0", "输出 1"),
        ([V_MAX, -V_MAX], "值域两端成对", "1", "int 取负溢出"),
        ([-7, 4, 7], "一对夹一个无关正数", "1", "把 4 也算进去"),
        ([1, -1, 2, -2, 3], "两对加一个落单", "2", "双计数得到 4"),
        ([RNG.choice([-1, 1]) * (i + 1) for i in range(40)], "中等互异随机符号", "对拍", "排序去重后丢符号"),
        (all_pos, "压满全是正数", "0", "O(n^2) TLE"),
        (pairs_big, "压满 5e4 对相反数", "50000", "双计数得到 100000"),
    ]
    assert double_count([1, -1, 2, -2, 3]) == 4

    answers, metas = [], []
    for i, (nums, _, _, _) in enumerate(plan, 1):
        metas.append(nums)
        answers.append(write_case(i, nums))
    assert answers[0] == 2 and answers[1] == 0 and answers[2] == 3
    assert answers[4] == 1 and answers[8] == 0 and answers[9] == 50000

    for i, nums in enumerate(metas, 1):
        ib = (DATA / f"{i}.in").read_bytes()
        ob = (DATA / f"{i}.out").read_bytes()
        assert not ib.endswith(b"\n") and b"\r" not in ib
        assert ob.endswith(b"\n") and not ob.endswith(b"\n\n")
        assert ib.decode("utf-8") == f"{len(nums)}\n" + " ".join(str(x) for x in nums)

    rows = [f"| {i} | {p[1]} | {p[2]} | {p[3]} |" for i, p in enumerate(plan, 1)]
    (DATA / "README.md").write_text(
        "\n".join([
            "# P7162 测试数据说明",
            "",
            "主造数脚本：题目根目录 `gen.py`。元素互异且不含 $0$。",
            r"约束：$1\le n\le 10^5$，$-10^9\le nums_i\le 10^9$，$nums_i\\ne 0$。",
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
