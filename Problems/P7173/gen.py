# -*- coding: utf-8 -*-
"""P7173 造数：两个只出现一次的数。标程按从小到大输出；OJ 用 checker。"""
from __future__ import annotations

import random
import sys
from pathlib import Path

sys.dont_write_bytecode = True
sys.path.insert(0, str(Path(__file__).resolve().parent))
from std import solve  # noqa: E402

ROOT = Path(__file__).resolve().parent
DATA = ROOT / "data"
RNG = random.Random(717320260915)
N_MAX = 3 * 10**4
INT_MIN = -(2**31)
INT_MAX = 2**31 - 1


def brute(nums):
    cnt = {}
    for x in nums:
        cnt[x] = cnt.get(x, 0) + 1
    hits = [x for x, c in cnt.items() if c == 1]
    assert len(hits) == 2
    hits.sort()
    return hits[0], hits[1]


def write_case(idx, nums):
    n = len(nums)
    assert 2 <= n <= N_MAX and n % 2 == 0
    for x in nums:
        assert INT_MIN <= x <= INT_MAX
    a, b = solve(list(nums))
    ba, bb = brute(nums)
    assert {a, b} == {ba, bb}
    if a > b:
        a, b = b, a
    inp = f"{n}\n" + " ".join(str(x) for x in nums)
    (DATA / f"{idx}.in").write_bytes(inp.encode("utf-8"))
    with open(DATA / f"{idx}.out", "w", encoding="utf-8", newline="\n") as f:
        f.write(f"{a} {b}\n")
    return a, b


def make_arr(pairs, two):
    arr = []
    for x in pairs:
        arr.extend([x, x])
    arr.extend(two)
    RNG.shuffle(arr)
    return arr


def main():
    DATA.mkdir(parents=True, exist_ok=True)
    mid = list(range(1, N_MAX // 2 - 1))
    big = make_arr(mid, [N_MAX, -N_MAX])
    assert len(big) <= N_MAX
    # 补到接近上限
    while len(big) + 2 <= N_MAX:
        x = RNG.randint(-10000, 10000)
        if x in (N_MAX, -N_MAX) or big.count(x) > 0:
            continue
        big.extend([x, x])
    # 含 INT_MIN
        extra = make_arr(list(range(100)), [INT_MIN, 1000])

    plan = [
        ([1, 2, 1, 3, 2, 5], "样例 1", "3 5", "输出 1 2"),
        ([-1, 0], "样例 2 两个落单", "-1 0", "漏负数"),
        ([0, 1], "样例 3", "0 1", "顺序必须 1 0 才会和样例展示不同，SPJ 都收"),
        ([4, 4, 9, -3], "一对加两个落单", "-3 9", "哈希表以外空间"),
        ([INT_MIN, INT_MAX], "下界和上界", "INT_MIN INT_MAX", "异或最低位取错"),
        (make_arr([0], [1, 2]), "0 出现两次", "1 2", "把 0 当落单"),
        (extra, "含 INT_MIN 的中等数组", "1000 和 INT_MIN", "符号位分组出错"),
        (make_arr(list(range(20, 40)), [5, 8]), "多对重复", "5 8", "只异或一次拆不开"),
        (big, "压满约 3e4", "O(n) 位运算", "排序后数次数 TLE/空间"),
        (make_arr(list(range(1, N_MAX // 2)), [-5, N_MAX]), "压满偶数长度", "O(1) 额外空间", "哈希表"),
    ]

    answers, metas = [], []
    for i, (nums, _, _, _) in enumerate(plan, 1):
        metas.append(nums)
        answers.append(write_case(i, nums))
    assert answers[0] == (3, 5)
    assert answers[1] == (-1, 0)
    assert answers[2] == (0, 1)

    for i, nums in enumerate(metas, 1):
        ib = (DATA / f"{i}.in").read_bytes()
        ob = (DATA / f"{i}.out").read_bytes()
        assert not ib.endswith(b"\n") and b"\r" not in ib
        assert ob.endswith(b"\n") and not ob.endswith(b"\n\n")
        assert ib.decode("utf-8") == f"{len(nums)}\n" + " ".join(str(x) for x in nums)

    assert (DATA / "checker.cc").is_file()
    assert (DATA / "config.yaml").is_file()

    rows = [f"| {i} | {p[1]} | {p[2]} | {p[3]} |" for i, p in enumerate(plan, 1)]
    (DATA / "README.md").write_text(
        "\n".join([
            "# P7173 测试数据说明",
            "",
            "主造数脚本：题目根目录 `gen.py`。两个答案顺序任意，评测用 `checker.cc`。",
            r"约束：$2\le n\le 3\times 10^4$，恰好两个数出现一次，其余出现两次。",
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
