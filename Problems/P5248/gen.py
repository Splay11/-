# -*- coding: utf-8 -*-
"""生成 P5248 的 data/*.in/*.out。

规则：
- .in 末尾无多余换行
- .out 末尾恰有一个换行
- 前 8 组小数据，后 2 组接近 q=1e5、n=1e9 上限
"""

from __future__ import annotations

import math
import random
from pathlib import Path

SEED = 524820260815
RNG = random.Random(SEED)
ROOT = Path(__file__).resolve().parent
DATA = ROOT / "data"
Q_MAX = 100000
N_MAX = 10**9
ODDS = [3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41]


def impossible(n: int) -> bool:
    return n <= 9 or n == 11 or n == 13 or n == 17


def solve(n: int):
    if impossible(n):
        return None
    if n % 2 == 0:
        if n % 6 != 2:
            return (2, 3, n - 5)
        return (3, 4, n - 7)
    for i, a in enumerate(ODDS):
        for b in ODDS[i:]:
            if math.gcd(a, b) != 1:
                continue
            c = n - a - b
            if c >= 2 and math.gcd(a, c) == 1 and math.gcd(b, c) == 1:
                return (a, b, c)
    raise RuntimeError(f"no construction for {n}")


def valid_triple(n, t) -> bool:
    if t is None:
        return impossible(n)
    x, y, z = t
    return (
        x >= 2
        and y >= 2
        and z >= 2
        and x + y + z == n
        and math.gcd(x, y) == 1
        and math.gcd(x, z) == 1
        and math.gcd(y, z) == 1
    )


def fmt_in(ns: list[int]) -> str:
    lines = [str(len(ns))] + [str(x) for x in ns]
    return "\n".join(lines)


def fmt_out(ns: list[int]) -> str:
    rows = []
    for n in ns:
        t = solve(n)
        if t is None:
            rows.append("-1")
        else:
            rows.append(f"{t[0]} {t[1]} {t[2]}")
    return "\n".join(rows) + "\n"


def add(cases, desc, ns):
    assert 1 <= len(ns) <= Q_MAX
    assert all(1 <= x <= N_MAX for x in ns)
    for n in ns:
        t = solve(n)
        assert valid_triple(n, t), (n, t)
    cases.append((desc, fmt_in(ns), fmt_out(ns)))


def build_cases():
    cases = []
    add(cases, "样例1：无解与两种偶数构造", [1, 10, 17, 14])
    add(cases, "样例2：奇数构造与偶数 2,3,n-5", [15, 23, 24])
    add(cases, "边界：全部无解 n", [1, 2, 3, 4, 5, 6, 7, 8, 9, 11, 13, 17])
    add(cases, "基础：n=10 起连续一段", list(range(10, 41)))
    add(
        cases,
        "hack：2 2 n-4 不互质；漏掉 11/13/17",
        [10, 11, 12, 13, 14, 16, 17, 18],
    )
    add(
        cases,
        "hack：只处理偶数；n mod 6=2 时 2 3 n-5 与 3 不互质",
        [14, 20, 26, 32, 15, 19, 21, 103],
    )
    add(
        cases,
        "构造：1e9 附近奇偶与模 6",
        [N_MAX, N_MAX - 1, N_MAX - 2, N_MAX - 3, 10**9 - 17, 999999998],
    )
    ns8 = [RNG.randint(1, 200) for _ in range(40)]
    ns8[0] = 17
    ns8[1] = 1
    ns8[2] = 103
    add(cases, "随机小数据：n<=200，q=40", ns8)

    ns9 = [RNG.randint(1, N_MAX) for _ in range(Q_MAX)]
    ns9[0] = 1
    ns9[1] = 17
    ns9[2] = N_MAX
    ns9[3] = 14
    ns9[4] = 103
    add(cases, "大数据：q=1e5，n 均匀到 1e9", ns9)

    ns10 = []
    for i in range(Q_MAX):
        if i % 7 == 0:
            ns10.append(17 if i % 2 == 0 else 13)
        elif i % 7 == 1:
            ns10.append(N_MAX)
        elif i % 7 == 2:
            ns10.append(14)
        else:
            ns10.append(RNG.randint(10, N_MAX))
    add(cases, "大数据：q=1e5，混入无解与 1e9", ns10)

    assert len(cases) == 10
    return cases


def write_cases(cases):
    DATA.mkdir(parents=True, exist_ok=True)
    readme_lines = [
        "# P5248 测试数据说明",
        "",
        "多询问：第一行 $q$，随后 $q$ 行每个 $n$。",
        "约束：$1\\le q\\le 100000$，$1\\le n\\le 10^9$。",
        "",
        "| 编号 | 类型 | 说明 | 针对的错误解 |",
        "|---:|---|---|---|",
    ]
    tags = [
        "样例",
        "样例",
        "边界",
        "基础",
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
        "漏无解集合",
        "小范围构造错误",
        "输出 2 2 n-4；漏 11/13/17",
        "只做偶数；n≡2 (mod 6) 仍用 2,3,n-5",
        "大整数 / 边界模 6",
        "随机",
        "q=1e5 读入与构造",
        "q=1e5 无解与上限混洗",
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
        ns = [int(x) for x in lines[1:]]
        assert len(ns) == q
        got = fmt_out(ns)
        if got != out_text:
            raise SystemExit(f"自检失败：第 {i} 组（{desc}）")


def main():
    cases = build_cases()
    write_cases(cases)
    self_check(cases)
    print(f"已生成 {len(cases)} 组数据到 {DATA}")


if __name__ == "__main__":
    main()
