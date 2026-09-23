# -*- coding: utf-8 -*-
"""生成 P5219 的 data/*.in/*.out。

规则：
- .in 末尾无多余换行
- .out 末尾恰有一个换行
- 前 8 组小数据，后 2 组接近 n=4e3 上限
"""

from __future__ import annotations

import random
from pathlib import Path

SEED = 521920260807
RNG = random.Random(SEED)
ROOT = Path(__file__).resolve().parent
DATA = ROOT / "data"
Q_MAX = 20
N_MAX = 4000
V_MAX = 10**9


def min_merges(v: list[int]) -> int:
    suf = 10**18
    ans = 0
    for x in reversed(v):
        if x <= suf:
            suf = x
        else:
            ans += 1
            suf += x
    return ans


def solve_cases(cases: list[list[int]]) -> list[int]:
    return [min_merges(v) for v in cases]


def fmt_in(q: int, cases: list[list[int]]) -> str:
    parts = [str(q)]
    for v in cases:
        parts.append(str(len(v)))
        parts.append(" ".join(map(str, v)))
    return "\n".join(parts)


def fmt_out(answers: list[int]) -> str:
    return "\n".join(map(str, answers)) + "\n"


def build_cases() -> list[tuple[str, str, str]]:
    """返回 (说明, in_text, out_text)。"""
    items: list[tuple[str, str, str]] = []

    def add(desc: str, q: int, cases: list[list[int]]) -> None:
        assert len(cases) == q
        for v in cases:
            assert 1 <= len(v) <= N_MAX
            assert all(1 <= x <= V_MAX for x in v)
        ans = solve_cases(cases)
        items.append((desc, fmt_in(q, cases), fmt_out(ans)))

    # 1-2：题面样例
    add(
        "样例1：题面多记录样例",
        3,
        [[2, 1, 3], [1, 2, 3, 4], [5, 1, 6]],
    )
    add("样例2：单记录中间逆序", 1, [[3, 2, 1, 4, 5]])

    # 3：最小规模
    add("边界：n=1，答案为 0", 1, [[42]])

    # 4：已非降
    add("边界：已非降序列", 1, [[1, 3, 3, 7, 9]])

    # 5：严格递减
    add("构造：严格递减，需 n-1 次合并", 1, [[9, 8, 7, 6, 5, 4]])

    # 6：卡从左向右立刻合并的假贪心
    add("hack：左贪心会多合并，正解 2", 1, [[4, 2, 3, 1, 5]])

    # 7：多记录小随机
    small_cases = []
    for _ in range(5):
        n = RNG.randint(2, 30)
        small_cases.append([RNG.randint(1, 100) for _ in range(n)])
    add("随机：q=5，n<=30", 5, small_cases)

    # 8：q 拉满 + 中等 n，测多组读入
    med_cases = []
    for _ in range(Q_MAX):
        n = RNG.randint(50, 200)
        med_cases.append([RNG.randint(1, V_MAX) for _ in range(n)])
    add("构造：q=20，n 在 50~200", Q_MAX, med_cases)

    # 9：单组 n=4000 随机
    n9 = N_MAX
    v9 = [RNG.randint(1, V_MAX) for _ in range(n9)]
    v9[0] = V_MAX
    v9[-1] = 1
    add("大数据：n=4000 随机，极值在两端", 1, [v9])

    # 10：单组 n=4000，大值递减链 + 局部凸起，卡 int 溢出
    n10 = N_MAX
    v10 = [V_MAX - i for i in range(n10)]
    for j in range(0, n10, 137):
        v10[j] = V_MAX
    add("大数据：n=4000 近递减大值，多次合并易溢出", 1, [v10])

    assert len(items) == 10
    return items


def write_cases(items: list[tuple[str, str, str]]) -> None:
    DATA.mkdir(parents=True, exist_ok=True)
    lines = [
        "# P5219 测试数据说明",
        "",
        "算法核：从右向左贪心维护后缀代表值，逆序则合并。",
        "",
        "| 编号 | 类型 | 说明 | 卡掉的错误解 |",
        "|---:|---|---|---|",
    ]
    tags = [
        ("样例", "无"),
        ("样例", "无"),
        ("边界", "未处理 n=1"),
        ("边界", "已非降仍盲目合并"),
        ("构造", "递减链合并次数统计错误"),
        ("hack", "从左向右遇逆序立刻合并"),
        ("随机", "多组读入/实现细节错误"),
        ("构造", "q=20 多组边界"),
        ("压力", "n=4000 复杂度与 I/O"),
        ("压力", "大值多次合并 int 溢出"),
    ]
    for i, ((desc, tin, tout), (tag, hack)) in enumerate(zip(items, tags), 1):
        (DATA / f"{i}.in").write_bytes(tin.encode("utf-8"))
        (DATA / f"{i}.out").write_bytes(tout.encode("utf-8"))
        lines.append(f"| {i} | {tag} | {desc} | {hack} |")
    lines.append("")
    lines.append(f"随机种子：`{SEED}`。")
    lines.append("")
    (DATA / "README.md").write_bytes(("\n".join(lines) + "\n").encode("utf-8"))


def self_check(items: list[tuple[str, str, str]]) -> None:
    for i, (_desc, tin, tout) in enumerate(items, 1):
        lines = tin.split("\n")
        q = int(lines[0])
        idx = 1
        cases: list[list[int]] = []
        for _ in range(q):
            n = int(lines[idx])
            idx += 1
            v = list(map(int, lines[idx].split()))
            idx += 1
            assert len(v) == n
            cases.append(v)
        got = solve_cases(cases)
        expect = list(map(int, tout.strip().split("\n")))
        if got != expect:
            raise RuntimeError(f"case {i}: got {got}, expect {expect}")
        if tin.endswith("\n"):
            raise RuntimeError(f"case {i}: .in must not end with newline")
        if not tout.endswith("\n") or tout.endswith("\n\n"):
            raise RuntimeError(f"case {i}: .out must end with exactly one newline")


def main() -> None:
    items = build_cases()
    self_check(items)
    write_cases(items)
    for i in range(1, 11):
        tin = (DATA / f"{i}.in").read_bytes().decode("utf-8")
        tout = (DATA / f"{i}.out").read_bytes().decode("utf-8")
        lines = tin.split("\n")
        q = int(lines[0])
        idx = 1
        cases: list[list[int]] = []
        for _ in range(q):
            n = int(lines[idx])
            idx += 1
            v = list(map(int, lines[idx].split()))
            idx += 1
            cases.append(v)
        got = solve_cases(cases)
        expect = list(map(int, tout.strip().split("\n")))
        assert got == expect, (i, got, expect)
        assert not tin.endswith("\n"), i
        assert tout.endswith("\n") and not tout.endswith("\n\n"), i
    print("generated 10 cases OK")


if __name__ == "__main__":
    main()
