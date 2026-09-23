# -*- coding: utf-8 -*-
"""生成 P5216 的 data/*.in/*.out。

规则：
- .in 末尾无多余换行
- .out 末尾恰有一个换行
- 前 8 组小数据，后 2 组接近 n=1e5、m=1e18 上限
"""

from __future__ import annotations

import random
from pathlib import Path

SEED = 521620260806
RNG = random.Random(SEED)
ROOT = Path(__file__).resolve().parent
DATA = ROOT / "data"
N_MAX = 100_000
M_MAX = 10**18


def solve_one(m: int) -> int:
    return (m // 2) ^ ((m + 1) // 2)


def solve(ms: list[int]) -> list[int]:
    return [solve_one(m) for m in ms]


def fmt_in(ms: list[int]) -> str:
    lines = [str(len(ms))] + [str(m) for m in ms]
    return "\n".join(lines)


def fmt_out(ans: list[int]) -> str:
    return "\n".join(map(str, ans)) + "\n"


def build_cases() -> list[tuple[str, str, str]]:
    """返回 (说明, in_text, out_text)。"""
    cases: list[tuple[str, str, str]] = []

    def add(desc: str, ms: list[int]) -> None:
        assert 1 <= len(ms) <= N_MAX
        assert all(1 <= m <= M_MAX for m in ms)
        ans = solve(ms)
        cases.append((desc, fmt_in(ms), fmt_out(ans)))

    # 1-2：题面样例
    add("样例1：偶数得0、奇数均分", [4, 5, 11])
    add("样例2：偶数与全1二进制", [2, 7])

    # 3：最小额度
    add("边界：m=1", [1])

    # 4：连续小值，覆盖奇偶
    add("基础：1..16 全覆盖", list(range(1, 17)))

    # 5：2^k 与 2^k-1（假解易混）
    add(
        "构造：2^k 与梅森数",
        [8, 15, 16, 31, 32, 63, 64],
    )

    # 6：hack「答案=最低位」假解（m=11 最低位1，正解3）
    add(
        "hack：答案≠m&-m",
        [11, 19, 23, 27, 35, 39, 43, 47],
    )

    # 7：hack「奇数恒为1」假解
    add(
        "hack：奇数答案可>1",
        [7, 11, 13, 15, 21, 25, 29, 31],
    )

    # 8：小随机混合
    ms8 = [RNG.randint(1, 10**6) for _ in range(40)]
    ms8[0] = 1
    ms8[1] = 10**6
    ms8[2] = (1 << 20) - 1
    ms8[3] = 1 << 20
    add("随机小数据：n=40", ms8)

    # 9：大数据 n=1e5，m 中等偏大
    n9 = N_MAX
    ms9 = [RNG.randint(1, 10**12) for _ in range(n9)]
    ms9[0] = 1
    ms9[1] = (1 << 40) - 1
    ms9[2] = 1 << 40
    ms9[3] = 10**12
    add("大数据：n=1e5，m<=1e12", ms9)

    # 10：大数据拉满 m=1e18，并混入全1/2^k
    n10 = N_MAX
    ms10 = [RNG.randint(1, M_MAX) for _ in range(n10)]
    ms10[0] = M_MAX
    ms10[1] = M_MAX - 1
    ms10[2] = (1 << 59) - 1  # 2^59-1 < 1e18
    ms10[3] = 1 << 59
    ms10[4] = (1 << 50) - 1
    ms10[5] = 1
    add("大数据：n=1e5，m 接近 1e18", ms10)

    assert len(cases) == 10
    return cases


def write_cases(cases: list[tuple[str, str, str]]) -> None:
    DATA.mkdir(parents=True, exist_ok=True)
    readme_lines = [
        "# P5216 测试数据说明",
        "",
        "| 编号 | 说明 |",
        "|---:|---|",
    ]
    for i, (desc, in_text, out_text) in enumerate(cases, 1):
        in_path = DATA / f"{i}.in"
        out_path = DATA / f"{i}.out"
        in_path.write_bytes(in_text.encode("utf-8"))
        out_path.write_bytes(out_text.encode("utf-8"))
        readme_lines.append(f"| {i} | {desc} |")
    (DATA / "README.md").write_bytes(("\n".join(readme_lines) + "\n").encode("utf-8"))


def self_check(cases: list[tuple[str, str, str]]) -> None:
    for i, (desc, in_text, out_text) in enumerate(cases, 1):
        lines = in_text.split("\n")
        n = int(lines[0])
        ms = [int(x) for x in lines[1:]]
        assert len(ms) == n, f"case {i}: n mismatch"
        got = fmt_out(solve(ms))
        if got != out_text:
            raise SystemExit(f"自检失败：第 {i} 组（{desc}）\n期望:\n{out_text!r}\n得到:\n{got!r}")
        # .in 末尾无换行；.out 末尾恰一个换行
        assert not in_text.endswith("\n"), f"case {i}: .in 不应以换行结尾"
        assert out_text.endswith("\n") and not out_text.endswith("\n\n"), f"case {i}: .out 换行规则"


def main() -> None:
    cases = build_cases()
    write_cases(cases)
    self_check(cases)
    print(f"已生成 {len(cases)} 组数据到 {DATA}")


if __name__ == "__main__":
    main()
