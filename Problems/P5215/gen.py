# -*- coding: utf-8 -*-
"""生成 P5215 的 data/*.in/*.out。

规则：
- .in 末尾无多余换行
- .out 末尾恰有一个换行
- 前 8 组小数据，后 2 组接近 n=3e5 上限
"""

from __future__ import annotations

import random
from pathlib import Path

SEED = 521520260806
RNG = random.Random(SEED)
ROOT = Path(__file__).resolve().parent
DATA = ROOT / "data"
N_MAX = 300_000
V_MAX = 10**9


def solve(n: int, v: list[int]) -> int:
    return (max(v) - min(v)) * n


def fmt_in(n: int, v: list[int]) -> str:
    return f"{n}\n" + " ".join(map(str, v))


def fmt_out(ans: int) -> str:
    return f"{ans}\n"


def build_cases() -> list[tuple[str, str, str]]:
    """返回 (说明, in_text, out_text)。"""
    cases: list[tuple[str, str, str]] = []

    def add(desc: str, v: list[int]) -> None:
        n = len(v)
        assert 1 <= n <= N_MAX
        assert all(1 <= x <= V_MAX for x in v)
        ans = solve(n, v)
        cases.append((desc, fmt_in(n, v), fmt_out(ans)))

    # 1-2：题面样例
    add("样例1：整段最优展示公式", [2, 5, 1])
    add("样例2：整段最优，切开更差", [1, 5, 2, 4])

    # 3：最小规模
    add("边界：n=1，答案为 0", [7])

    # 4：全相等
    add("边界：全部相等，极差为 0", [3, 3, 3, 3, 3])

    # 5：严格递增（假解易用相邻差分代替极差）
    add("构造：严格递增", [1, 2, 3, 4, 5, 6, 7, 8])

    # 6：尖峰在中间——切开尖峰的假贪心会变差
    add("hack：中间尖峰，切开劣于整段", [1, 1, 100, 1, 1])

    # 7：极值在两端 + 中间噪声
    add(
        "构造：最小最大分居两端",
        [1, 50, 20, 80, 30, 60, 40, 100],
    )

    # 8：小随机，含重复值
    v8 = [RNG.randint(1, 1000) for _ in range(50)]
    v8[0] = 1
    v8[-1] = 1000
    add("随机小数据：n=50", v8)

    # 9：大数据，卡 int 溢出：极差约 1e9，n=3e5
    n9 = N_MAX
    v9 = [RNG.randint(2, V_MAX - 1) for _ in range(n9)]
    v9[0] = 1
    v9[n9 // 2] = V_MAX
    add("大数据：n=3e5，极差拉满，卡 32 位溢出", v9)

    # 10：大数据单调下降 + 局部扰动，卡漏乘 n / 只看端点
    n10 = N_MAX
    v10 = [V_MAX - (i % 100000) for i in range(n10)]
    v10[12345] = 1
    v10[234567] = V_MAX
    add("大数据：n=3e5，极值不在端点", v10)

    assert len(cases) == 10
    return cases


def write_cases(cases: list[tuple[str, str, str]]) -> None:
    DATA.mkdir(parents=True, exist_ok=True)
    lines = [
        "# P5215 测试数据说明",
        "",
        "算法核：答案恒为 $(\\max v - \\min v)\\times n$。",
        "",
        "| 编号 | 类型 | 说明 | 卡掉的错误解 |",
        "|---:|---|---|---|",
    ]
    tags = [
        ("样例", "无"),
        ("样例", "无"),
        ("边界", "未处理 n=1"),
        ("边界", "未处理全相等"),
        ("构造", "用相邻差分之和代替极差×长度"),
        ("hack", "切开尖峰的错误贪心/局部最优"),
        ("构造", "只看端点当 max/min"),
        ("随机", "基础实现错误"),
        ("压力", "int 溢出；复杂度不足"),
        ("压力", "只看端点；漏乘 n"),
    ]
    for i, ((desc, tin, tout), (tag, hack)) in enumerate(zip(cases, tags), 1):
        (DATA / f"{i}.in").write_text(tin, encoding="utf-8")
        (DATA / f"{i}.out").write_text(tout, encoding="utf-8")
        lines.append(f"| {i} | {tag} | {desc} | {hack} |")
    lines.append("")
    lines.append(f"随机种子：`{SEED}`。")
    lines.append("")
    (DATA / "README.md").write_text("\n".join(lines) + "\n", encoding="utf-8")


def self_check(cases: list[tuple[str, str, str]]) -> None:
    for i, (_desc, tin, tout) in enumerate(cases, 1):
        lines = tin.split("\n")
        n = int(lines[0])
        v = list(map(int, lines[1].split()))
        assert len(v) == n
        got = solve(n, v)
        expect = int(tout.strip())
        if got != expect:
            raise RuntimeError(f"case {i}: got {got}, expect {expect}")
        if tin.endswith("\n\n") or (tin.endswith("\n") and tin.count("\n") > 1 and tin[-1] == "\n" and not tin.endswith(" \n")):
            # .in 允许中间换行，但文件末尾不得有多余空行；最后一行后不要换行
            pass
        if tin.endswith("\n"):
            raise RuntimeError(f"case {i}: .in must not end with newline")
        if not tout.endswith("\n") or tout.endswith("\n\n"):
            raise RuntimeError(f"case {i}: .out must end with exactly one newline")


def main() -> None:
    cases = build_cases()
    self_check(cases)
    write_cases(cases)
    # 再读盘校验
    for i in range(1, 11):
        tin = (DATA / f"{i}.in").read_text(encoding="utf-8")
        tout = (DATA / f"{i}.out").read_text(encoding="utf-8")
        lines = tin.split("\n")
        n = int(lines[0])
        v = list(map(int, lines[1].split()))
        got = solve(n, v)
        expect = int(tout.strip())
        assert got == expect, (i, got, expect)
        assert not tin.endswith("\n"), i
        assert tout.endswith("\n") and not tout.endswith("\n\n"), i
    print("generated 10 cases OK")


if __name__ == "__main__":
    main()
