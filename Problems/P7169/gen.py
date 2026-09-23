# -*- coding: utf-8 -*-
"""P7169 造数：小于 n 的质数个数。"""
from __future__ import annotations

import sys
from pathlib import Path

sys.dont_write_bytecode = True
sys.path.insert(0, str(Path(__file__).resolve().parent))
from std import solve  # noqa: E402

ROOT = Path(__file__).resolve().parent
DATA = ROOT / "data"
N_MAX = 5 * 10**6


def naive(n):
    """小 n 试除对拍。"""
    if n <= 2:
        return 0
    ans = 0
    for x in range(2, n):
        ok = True
        d = 2
        while d * d <= x:
            if x % d == 0:
                ok = False
                break
            d += 1
        if ok:
            ans += 1
    return ans


def write_case(idx, n):
    assert 0 <= n <= N_MAX
    ans = solve(n)
    if n <= 5000:
        assert ans == naive(n)
    (DATA / f"{idx}.in").write_bytes(str(n).encode("utf-8"))
    with open(DATA / f"{idx}.out", "w", encoding="utf-8", newline="\n") as f:
        f.write(str(ans) + "\n")
    return ans


def main():
    DATA.mkdir(parents=True, exist_ok=True)
    plan = [
        (10, "样例 1，2 3 5 7", "4", "把 1 算进去"),
        (0, "样例 2", "0", "输出负数"),
        (1, "样例 3", "0", "把 1 当质数"),
        (2, "没有小于 2 的质数", "0", "输出 1"),
        (3, "只有 2", "1", "把 3 也算上"),
        (4, "2 和 3", "2", "统计 <=n"),
        (100, "中等", "25", "试除后面 TLE"),
        (997, "质数本身，答案不含它", "筛法", "统计成 pi(n) 而不是 pi(n-1) 附近"),
        (N_MAX, "压满 n=5e6", "埃氏筛", "O(n sqrt n) TLE"),
        (N_MAX - 1, "压满附近", "筛法", "数组开成 n+1 把 n 算进去"),
    ]
    answers, ns = [], []
    for i, (n, _, _, _) in enumerate(plan, 1):
        ns.append(n)
        answers.append(write_case(i, n))
    assert answers[0] == 4 and answers[1] == 0 and answers[2] == 0
    assert answers[3] == 0 and answers[4] == 1 and answers[5] == 2
    assert answers[6] == 25

    for i, n in enumerate(ns, 1):
        ib = (DATA / f"{i}.in").read_bytes()
        ob = (DATA / f"{i}.out").read_bytes()
        assert not ib.endswith(b"\n") and b"\r" not in ib
        assert ob.endswith(b"\n") and not ob.endswith(b"\n\n")
        assert ib.decode("utf-8") == str(n)

    rows = [f"| {i} | {p[1]} | {p[2]} | {p[3]} |" for i, p in enumerate(plan, 1)]
    (DATA / "README.md").write_text(
        "\n".join([
            "# P7169 测试数据说明",
            "",
            r"主造数脚本：题目根目录 `gen.py`。约束 $0\le n\le 5\times 10^6$，统计严格小于 $n$ 的质数。",
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
        print(i, a, "n", ns[i - 1])


if __name__ == "__main__":
    main()
