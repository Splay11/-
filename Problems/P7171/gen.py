# -*- coding: utf-8 -*-
"""P7171 造数：1..n 的最小公倍数，n<=40。"""
from __future__ import annotations

import math
import sys
from pathlib import Path

sys.dont_write_bytecode = True
sys.path.insert(0, str(Path(__file__).resolve().parent))
from std import solve  # noqa: E402

ROOT = Path(__file__).resolve().parent
DATA = ROOT / "data"


def brute(n):
    ans = 1
    for i in range(1, n + 1):
        ans = ans // math.gcd(ans, i) * i
    return ans


def write_case(idx, n):
    assert 1 <= n <= 40
    ans = solve(n)
    assert ans == brute(n)
    assert -(2**63) <= ans < 2**63
    (DATA / f"{idx}.in").write_bytes(str(n).encode("utf-8"))
    with open(DATA / f"{idx}.out", "w", encoding="utf-8", newline="\n") as f:
        f.write(str(ans) + "\n")
    return ans


def main():
    DATA.mkdir(parents=True, exist_ok=True)
    plan = [
        (5, "样例 1", "60", "输出 120 阶乘"),
        (10, "样例 2", "2520", "漏掉 8=2^3"),
        (1, "样例 3", "1", "输出 0"),
        (2, "1 和 2", "2", "输出 1"),
        (7, "质数 n", "420", "没用最高次幂"),
        (15, "含 8、9、7、5、11、13", "360360", "int 溢出"),
        (20, "中等", "232792560", "连乘阶乘"),
        (30, "较大", "lcm", "32 位溢出"),
        (39, "接近上限", "64 位 lcm", "漏 37"),
        (40, "压满 n=40", "5342931457063200", "用 int 存答案"),
    ]
    answers, ns = [], []
    for i, (n, _, _, _) in enumerate(plan, 1):
        ns.append(n)
        answers.append(write_case(i, n))
    assert answers[0] == 60 and answers[1] == 2520 and answers[2] == 1
    assert answers[9] == 5342931457063200

    for i, n in enumerate(ns, 1):
        ib = (DATA / f"{i}.in").read_bytes()
        ob = (DATA / f"{i}.out").read_bytes()
        assert not ib.endswith(b"\n") and b"\r" not in ib
        assert ob.endswith(b"\n") and not ob.endswith(b"\n\n")
        assert ib.decode("utf-8") == str(n)

    rows = [f"| {i} | {p[1]} | {p[2]} | {p[3]} |" for i, p in enumerate(plan, 1)]
    (DATA / "README.md").write_text(
        "\n".join([
            "# P7171 测试数据说明",
            "",
            r"主造数脚本：题目根目录 `gen.py`。约束 $1\le n\le 40$，答案在 64 位有符号整数内。",
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
