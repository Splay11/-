# -*- coding: utf-8 -*-
"""P7164 造数：能否分成每组恰好 k 个相同元素。输出小写 true/false。"""
from __future__ import annotations

import random
import sys
from pathlib import Path

sys.dont_write_bytecode = True
sys.path.insert(0, str(Path(__file__).resolve().parent))
from std import solve  # noqa: E402

ROOT = Path(__file__).resolve().parent
DATA = ROOT / "data"
RNG = random.Random(716420260915)
N_MAX = 10**5
V_MIN, V_MAX = -(10**9), 10**9


def brute(nums, k):
    from collections import Counter
    return all(v % k == 0 for v in Counter(nums).values())


def only_n_mod(nums, k):
    return len(nums) % k == 0


def write_case(idx, nums, k):
    n = len(nums)
    assert 1 <= k <= n <= N_MAX
    for x in nums:
        assert V_MIN <= x <= V_MAX
    ans = solve(nums, k)
    assert ans == brute(nums, k)
    text = "true" if ans else "false"
    inp = f"{n} {k}\n" + " ".join(str(x) for x in nums)
    (DATA / f"{idx}.in").write_bytes(inp.encode("utf-8"))
    with open(DATA / f"{idx}.out", "w", encoding="utf-8", newline="\n") as f:
        f.write(text + "\n")
    return text


def main():
    DATA.mkdir(parents=True, exist_ok=True)
    # n % k == 0 但有一个数次数不能整除
    hack = [1, 1, 1, 2]
    ok_big = [i % 50 for i in range(N_MAX)]  # 每个 0..49 各 2000 次，k=8
    bad_big = [1] * (N_MAX - 1) + [2]

    plan = [
        ([1, 1, 2, 2, 3, 3, 4, 4], 2, "样例 1", "true", "输出 false"),
        ([1, 1, 1, 2, 2, 3, 3], 2, "样例 2，$1$ 出现 3 次", "false", "只看 n%k"),
        ([5, 5, 5, 2, 2, 2, 5, 5, 5, 7, 7, 7], 3, "样例 3", "true", "5 出现 6 次没拆两组"),
        ([9], 1, "n=k=1", "true", "输出 false"),
        ([1, 2, 3], 1, "k=1 恒成立", "true", "要求值相同"),
        (hack, 2, "n 能被 k 整除但 1 出现 3 次", "false", "只判断 n%k==0"),
        ([7, 7, 7, 7], 4, "k=n 且全相同", "true", "k=n 时输出 false"),
        ([7, 7, 8, 8], 4, "k=n 但有两种值", "false", "只看长度"),
        (ok_big, 8, "压满 n=10^5，每值 2000 次，$k=8$", "true", "O(n^2) TLE"),
        (bad_big, 2, "压满几乎全是 1，多一个 2", "false", "忽略落单的 2"),
    ]
    assert only_n_mod(hack, 2) and not brute(hack, 2)

    answers, metas = [], []
    for i, (nums, k, _, _, _) in enumerate(plan, 1):
        metas.append((nums, k))
        answers.append(write_case(i, nums, k))
    assert answers[0] == "true" and answers[1] == "false" and answers[2] == "true"
    assert answers[5] == "false" and answers[8] == "true" and answers[9] == "false"

    for i, (nums, k) in enumerate(metas, 1):
        ib = (DATA / f"{i}.in").read_bytes()
        ob = (DATA / f"{i}.out").read_bytes()
        assert not ib.endswith(b"\n") and b"\r" not in ib
        assert ob.endswith(b"\n") and not ob.endswith(b"\n\n")
        assert ib.decode("utf-8") == f"{len(nums)} {k}\n" + " ".join(str(x) for x in nums)

    rows = [f"| {i} | {p[2]} | {p[3]} | {p[4]} |" for i, p in enumerate(plan, 1)]
    (DATA / "README.md").write_text(
        "\n".join([
            "# P7164 测试数据说明",
            "",
            "主造数脚本：题目根目录 `gen.py`。输出小写 true/false。",
            r"约束：$1\le k\le n\le 10^5$，$-10^9\le nums_i\le 10^9$。",
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
        print(i, a, "n", len(metas[i - 1][0]), "k", metas[i - 1][1])


if __name__ == "__main__":
    main()
