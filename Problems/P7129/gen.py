# -*- coding: utf-8 -*-
"""P7129 造数：单向链表倒数第 k 个节点的值。k 保证合法。

stdin：第一行 n k，第二行 n 个整数。
输出：一个整数。
题面未给 n、a_i 上界，本套按邻近链表题取 n<=1e4、a_i 在 [-1e9,1e9]。
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
RNG = random.Random(712920260914)

N_MAX = 10**4
V_LO, V_HI = -10**9, 10**9


def naive(vals, k):
    return vals[len(vals) - k]


def case_in_text(n, k, vals):
    return f"{n} {k}\n" + " ".join(map(str, vals))


def write_case(idx, k, vals):
    n = len(vals)
    assert 1 <= n <= N_MAX
    assert 1 <= k <= n
    assert all(V_LO <= v <= V_HI for v in vals)
    (DATA / f"{idx}.in").write_bytes(case_in_text(n, k, vals).encode("utf-8"))
    ans = solve(vals, k)
    expect = naive(vals, k)
    assert ans == expect, (idx, ans, expect)
    with open(DATA / f"{idx}.out", "w", encoding="utf-8", newline="\n") as f:
        f.write(f"{ans}\n")
    return ans


def main():
    DATA.mkdir(parents=True, exist_ok=True)

    rand8 = [RNG.randint(V_LO, V_HI) for _ in range(15)]
    k8 = RNG.randint(1, 15)
    big9 = list(range(N_MAX))
    big10 = [RNG.randint(V_LO, V_HI) for _ in range(N_MAX)]

    plan = [
        (2, [1, 2, 3, 4, 5],
         "样例 1，$n=5,k=2$", "倒数第 $2$ 个是 $4$",
         "输出正数第 $2$ 个 $2$，或下标从 $0$ 数错成 $3$"),
        (1, [1, 2, 3, 4, 5],
         "倒数第 $1$ 个即尾节点", "答案 $5$",
         "快指针多走一步走到空，空指针"),
        (5, [1, 2, 3, 4, 5],
         "倒数第 $n$ 个即头节点", "答案 $1$",
         "快指针先走 $n$ 步后已是空，慢指针没动却取了错节点"),
        (1, [9],
         "最小规模 $n=k=1$", "答案 $9$",
         "空链表/越界"),
        (2, [-3, 8, -1],
         "含负数，$k=2$", "倒数第 $2$ 个是 $8$",
         "只看绝对值"),
        (3, [10, 20, 30, 40],
         "$k=3$，落在中间", "答案 $20$",
         "快指针走 $k-1$ 步，答案偏成 $30$"),
        (4, [7, 7, 7, 7, 8],
         "有重复值", "倒数第 $4$ 个是 $7$（从头数第 $2$ 个 $7$）",
         "按值去重"),
        (k8, rand8,
         "小随机 $n=15$", "与下标 $n-k$ 对拍",
         "快慢不同步"),
        (1, big9,
         "压满 $n=10^4$，$k=1$ 取尾",
         "答案 $9999$",
         "整表存成数组后倒着数写错边界"),
        (N_MAX // 2, big10,
         "压满 $n=10^4$，$k=n/2$",
         "取中间偏后那个节点",
         "两遍扫描长度算错"),
    ]
    assert len(plan) == 10

    answers = []
    for idx, (k, vals, _, _, _) in enumerate(plan, 1):
        answers.append(write_case(idx, k, vals))

    for i, (k, vals, _, _, _) in enumerate(plan, 1):
        ib = (DATA / f"{i}.in").read_bytes()
        ob = (DATA / f"{i}.out").read_bytes()
        assert not ib.endswith(b"\n") and b"\r" not in ib, f"{i}.in"
        assert ob.endswith(b"\n") and not ob.endswith(b"\n\n") and b"\r" not in ob
        lines = ib.decode("utf-8").split("\n")
        hn, hk = map(int, lines[0].split())
        arr = list(map(int, lines[1].split()))
        assert hn == len(vals) == len(arr) and hk == k and arr == vals
        got = int(ob.decode("utf-8").strip())
        assert got == answers[i - 1] == naive(vals, k)

    assert answers[0] == 4
    assert answers[1] == 5
    assert answers[2] == 1
    assert answers[3] == 9
    assert answers[4] == 8
    assert answers[5] == 20
    assert answers[8] == 9999

    rows = []
    for i, (_, _, scale, goal, hack) in enumerate(plan, 1):
        rows.append(f"| {i} | {scale} | {goal} | {hack} |")

    readme = "\n".join([
        "# P7129 测试数据说明",
        "",
        "主造数脚本：题目根目录 `gen.py`。",
        "stdin：第一行 `n k`，第二行 $n$ 个整数。",
        "输出：倒数第 $k$ 个节点的值。保证 $1 \\le k \\le n$。",
        "",
        r"题面未写 $n$、$a_i$ 上界。本套取 $1 \le n \le 10^4$，$-10^9 \le a_i \le 10^9$（与邻近链表题一致）。",
        "",
        "| 组别 | 规模/分布 | 目标 | 卡掉的错误解 |",
        "|---|---|---|---|",
        *rows,
        "",
        "`.in` 最后一行后无换行符；`.out` 末尾恰好一个换行符。",
        "",
        "生成后自校验：双指针结果必须等于 $vals[n-k]$。",
        "",
    ])
    (DATA / "README.md").write_text(readme, encoding="utf-8")
    print("generated 10 cases")
    for i, ans in enumerate(answers, 1):
        print(i, "ans", ans)


if __name__ == "__main__":
    main()
