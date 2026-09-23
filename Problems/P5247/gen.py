# -*- coding: utf-8 -*-
"""生成 P5247 的 data/*.in/*.out。

规则：
- .in 末尾无多余换行
- .out 末尾恰有一个换行
- 前 8 组小数据，后 2 组接近 q=80、n=30 上限
"""

from __future__ import annotations

import bisect
import random
from itertools import combinations
from pathlib import Path

SEED = 524720260815
RNG = random.Random(SEED)
ROOT = Path(__file__).resolve().parent
DATA = ROOT / "data"
Q_MAX = 80
N_MAX = 30
V_MAX = 10**9


def enum_sums(arr):
    n = len(arr)
    by_cnt = [[] for _ in range(n + 1)]
    for mask in range(1 << n):
        s = 0
        c = 0
        for i in range(n):
            if mask >> i & 1:
                s += arr[i]
                c += 1
        by_cnt[c].append(s)
    for c in range(n + 1):
        by_cnt[c].sort()
    return by_cnt


def min_diff(vals):
    n = len(vals)
    half = n // 2
    tot = sum(vals)
    sl = enum_sums(vals[:half])
    sr = enum_sums(vals[half:])
    best = tot
    for k in range(half + 1):
        A = sl[k]
        B = sr[half - k]
        if not A or not B:
            continue
        for x in A:
            t = tot // 2 - x
            i = bisect.bisect_left(B, t)
            for j in (i - 1, i, i + 1):
                if 0 <= j < len(B):
                    s = x + B[j]
                    d = abs(tot - 2 * s)
                    if d < best:
                        best = d
    return best


def brute(vals):
    n = len(vals)
    m = n // 2
    tot = sum(vals)
    best = tot
    for comb in combinations(range(n), m):
        s = sum(vals[i] for i in comb)
        best = min(best, abs(tot - 2 * s))
    return best


def validate(queries):
    assert 1 <= len(queries) <= Q_MAX
    for n, arr in queries:
        assert n == len(arr)
        assert 2 <= n <= N_MAX and n % 2 == 0
        assert all(1 <= x <= V_MAX for x in arr)


def fmt_in(queries):
    lines = [str(len(queries))]
    for n, arr in queries:
        lines.append(str(n))
        lines.append(" ".join(map(str, arr)))
    return "\n".join(lines)


def fmt_out(ans):
    return "\n".join(map(str, ans)) + "\n"


def solve_queries(queries):
    return [min_diff(arr) for _, arr in queries]


def rand_arr(n, lo=1, hi=20):
    return [RNG.randint(lo, hi) for _ in range(n)]


def build_cases():
    cases = []

    def add(desc, queries):
        validate(queries)
        ans = solve_queries(queries)
        for n, arr in queries:
            if n <= 16:
                assert min_diff(arr) == brute(arr)
        cases.append((desc, fmt_in(queries), fmt_out(ans)))

    add(
        "样例1：n=2 与可均分的 n=4",
        [(2, [4, 9]), (4, [3, 5, 6, 8])],
    )
    add(
        "样例2：交替贪心非最优；n=6 差为 1",
        [(4, [1, 2, 3, 6]), (6, [1, 2, 3, 4, 5, 6])],
    )
    add("边界：n=2 最小规模", [(2, [1, 1]), (2, [1, V_MAX])])
    add(
        "边界：全相等，差必为 0",
        [(4, [7, 7, 7, 7]), (8, [3] * 8)],
    )
    add(
        "hack：排序交替放入两班（1 2 3 6 会得到 4）",
        [(4, [1, 2, 3, 6]), (4, [1, 5, 6, 8])],
    )
    add(
        "hack：忽略「每班恰好 n/2 个」（1 1 1 3 无基数约束可得 0）",
        [(4, [1, 1, 1, 3]), (6, [1, 1, 1, 1, 1, 9])],
    )
    add(
        "构造：含 1e9 极值，检查大整数求和",
        [(4, [1, 1, V_MAX, V_MAX]), (6, [V_MAX, 1, 1, 1, 1, 1])],
    )
    qs8 = []
    for n in (2, 4, 6, 8, 10, 12):
        qs8.append((n, rand_arr(n, 1, 50)))
    qs8.append((4, [10, 1, 10, 1]))
    add("随机小数据：若干偶数 n<=12", qs8)

    a9 = rand_arr(N_MAX, 1, 10**6)
    a9[0] = 1
    a9[1] = 10**6
    a9[-1] = V_MAX
    add("大数据：q=1，n=30", [(N_MAX, a9)])

    qs10 = []
    for i in range(Q_MAX):
        if i < 10:
            qs10.append((2, [RNG.randint(1, V_MAX), RNG.randint(1, V_MAX)]))
        elif i < 20:
            qs10.append((N_MAX, [1] * N_MAX))
        else:
            qs10.append((N_MAX, rand_arr(N_MAX, 1, 10**5)))
    qs10[0] = (N_MAX, list(range(1, N_MAX + 1)))
    qs10[1] = (N_MAX, [V_MAX] * N_MAX)
    add("大数据：q=80，混入 n=30 与 1e9", qs10)

    assert len(cases) == 10
    return cases


def write_cases(cases):
    DATA.mkdir(parents=True, exist_ok=True)
    readme_lines = [
        "# P5247 测试数据说明",
        "",
        "多询问：第一行 $q$，每个询问两行（$n$ 与 $n$ 个收益）。",
        "约束：$1\\le q\\le 80$，$2\\le n\\le 30$ 且 $n$ 为偶数，$1\\le v_i\\le 10^9$。",
        "",
        "| 编号 | 类型 | 说明 | 针对的错误解 |",
        "|---:|---|---|---|",
    ]
    tags = [
        "样例",
        "样例",
        "边界",
        "边界",
        "hack",
        "hack",
        "构造",
        "随机",
        "压力",
        "压力",
    ]
    hacks = [
        "—",
        "—",
        "n=2 / 极值差",
        "全相等仍输出非 0",
        "排序交替贪心",
        "无基数约束的划分",
        "int 溢出 / 大值求和",
        "随机噪声",
        "n=30 折半枚举",
        "q=80 满询问",
    ]
    for i, ((desc, in_text, out_text), tag, hack) in enumerate(
        zip(cases, tags, hacks), 1
    ):
        (DATA / f"{i}.in").write_bytes(in_text.encode("utf-8"))
        (DATA / f"{i}.out").write_bytes(out_text.encode("utf-8"))
        readme_lines.append(f"| {i} | {tag} | {desc} | {hack} |")
    (DATA / "README.md").write_bytes(("\n".join(readme_lines) + "\n").encode("utf-8"))


def self_check(cases):
    for i, (desc, in_text, out_text) in enumerate(cases, 1):
        assert not in_text.endswith("\n"), f"case {i}: .in 不应以换行结尾"
        assert out_text.endswith("\n") and not out_text.endswith("\n\n"), (
            f"case {i}: .out 换行规则"
        )
        lines = in_text.split("\n")
        q = int(lines[0])
        queries = []
        p = 1
        for _ in range(q):
            n = int(lines[p])
            arr = list(map(int, lines[p + 1].split()))
            queries.append((n, arr))
            p += 2
        got = fmt_out(solve_queries(queries))
        if got != out_text:
            raise SystemExit(f"自检失败：第 {i} 组（{desc}）")


def main():
    cases = build_cases()
    write_cases(cases)
    self_check(cases)
    print(f"已生成 {len(cases)} 组数据到 {DATA}")


if __name__ == "__main__":
    main()
