# -*- coding: utf-8 -*-
"""P7137 造数：切至少 k 段等长绳子，求最大整数长度。

stdin：第一行 n k；第二行 n 个正整数 a_i。
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
RNG = random.Random(713720260914)

N_MAX = 10**5
A_MAX = 10**9
K_MAX = 10**9


def naive(a, k):
    """换一种二分写法对拍：上整取 mid，用 lo<hi。"""
    lo = 1
    hi = max(a)
    while lo < hi:
        mid = (lo + hi + 1) // 2
        got = 0
        ok = False
        for x in a:
            got += x // mid
            if got >= k:
                ok = True
                break
        if ok:
            lo = mid
        else:
            hi = mid - 1
    return lo


def case_in_text(k, a):
    n = len(a)
    return f"{n} {k}\n" + " ".join(map(str, a))


def write_case(idx, k, a):
    n = len(a)
    assert 1 <= n <= N_MAX
    assert 1 <= k <= K_MAX
    assert all(1 <= x <= A_MAX for x in a)
    assert sum(a) >= k
    (DATA / f"{idx}.in").write_bytes(case_in_text(k, a).encode("utf-8"))
    ans = solve(a, k)
    expect = naive(a, k)
    assert ans == expect, (idx, ans, expect)
    with open(DATA / f"{idx}.out", "w", encoding="utf-8", newline="\n") as f:
        f.write(str(ans) + "\n")
    return ans


def main():
    DATA.mkdir(parents=True, exist_ok=True)

    sample1 = [8, 7, 9, 10]
    sample2 = [10, 15, 20]
    rand8 = [RNG.randint(1, 200) for _ in range(12)]
    k8 = RNG.randint(1, sum(rand8))

    big9 = [A_MAX] * N_MAX
    k9 = 10**9

    big10 = [RNG.randint(1, A_MAX) for _ in range(N_MAX)]
    # k 取总和的一个比例，保证合法且不是 1 或 max
    s10 = sum(big10)
    k10 = min(K_MAX, max(1, s10 // 1000))

    plan = [
        (10, sample1,
         "样例 1（原题误写成 $k=11$ 已改正）", "最大长度 $3$",
         "按 $k=11$ 会得到 $2$；或长度 $4$ 只切出 $7$ 段仍输出 $4$"),
        (5, sample2,
         "样例 2", "最大长度 $7$",
         "长度 $8$ 只切出 $4$ 段仍输出 $8$"),
        (100, [100],
         "一根绳子切成 $100$ 段", "答案 $1$",
         "输出 $100$"),
        (1, [100],
         "只要求 $1$ 段", "答案就是整根 $100$",
         "输出 $1$"),
        (sum(sample1), sample1,
         "$k$ 等于长度总和", "只能切长度 $1$",
         "输出 $0$ 或平均数"),
        (6, [5, 5, 5],
         "三根等长，要 $6$ 段", "$5//2=2$，三根共 $6$ 段，答案 $2$",
         "平均一下输出 $2.5$ 取整成 $3$"),
        (11, sample1,
         "原错误样例：$k=11$", "长度 $3$ 只够 $10$ 段，答案应为 $2$",
         "照着错样例输出 $3$"),
        (k8, rand8,
         "小随机 $n=12$", "两种二分对拍",
         "浮点除法四舍五入"),
        (k9, big9,
         "压满 $n=10^5$，$a_i=10^9$，$k=10^9$", "答案 $10^5$",
         "int 累加溢出；或 $L$ 用 double"),
        (k10, big10,
         "压满 $n=10^5$ 随机长度", "线性检查 + 二分长度",
         "每轮 $O(n)$ 写成 $O(n^2)$ 会 TLE"),
    ]
    assert len(plan) == 10

    answers = []
    for idx, (k, a, _, _, _) in enumerate(plan, 1):
        answers.append(write_case(idx, k, a))

    for i, (k, a, _, _, _) in enumerate(plan, 1):
        ib = (DATA / f"{i}.in").read_bytes()
        ob = (DATA / f"{i}.out").read_bytes()
        assert not ib.endswith(b"\n") and b"\r" not in ib, f"{i}.in"
        assert ob.endswith(b"\n") and not ob.endswith(b"\n\n") and b"\r" not in ob
        text = ib.decode("utf-8")
        lines = text.split("\n")
        hn, hk = map(int, lines[0].split())
        arr = list(map(int, lines[1].split()))
        assert hn == len(a) == len(arr) and hk == k and arr == a
        got = int(ob.decode("utf-8").strip())
        assert got == answers[i - 1] == naive(a, k)

    assert answers[0] == 3
    assert answers[1] == 7
    assert answers[2] == 1
    assert answers[3] == 100
    assert answers[4] == 1
    assert answers[5] == 2
    assert answers[6] == 2
    assert answers[8] == 10**5

    rows = []
    for i, (_, _, scale, goal, hack) in enumerate(plan, 1):
        rows.append(f"| {i} | {scale} | {goal} | {hack} |")

    readme = "\n".join([
        "# P7137 测试数据说明",
        "",
        "主造数脚本：题目根目录 `gen.py`。",
        "stdin：第一行 `n k`；第二行 $n$ 个正整数 $a_i$。",
        "输出：能切出至少 $k$ 段时，每段的最大整数长度。",
        "",
        r"约束：$1\le n\le 10^5$，$1\le k\le 10^9$，$1\le a_i\le 10^9$，$\sum a_i\ge k$。",
        "",
        "| 组别 | 规模/分布 | 目标 | 卡掉的错误解 |",
        "|---|---|---|---|",
        *rows,
        "",
        "`.in` 最后一行后无换行符；`.out` 末尾恰好一个换行符。",
        "",
        "生成后自校验：闭区间二分必须等于另一种上整二分。",
        "",
        "题面样例 1 原文 $k=11$ 与输出 $3$ 矛盾，已改为 $k=10$；第 $7$ 组保留 $k=11$ 的正确结果 $2$。",
        "",
    ])
    (DATA / "README.md").write_text(readme, encoding="utf-8")
    print("generated 10 cases")
    for i, ans in enumerate(answers, 1):
        print(i, "ans", ans)


if __name__ == "__main__":
    main()
