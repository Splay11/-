# -*- coding: utf-8 -*-
"""P7175 造数：添加括号的所有运算结果（保留重复，排序）。"""
from __future__ import annotations

import random
import sys
from pathlib import Path

sys.dont_write_bytecode = True
sys.path.insert(0, str(Path(__file__).resolve().parent))
from std import parse, solve  # noqa: E402

ROOT = Path(__file__).resolve().parent
DATA = ROOT / "data"
RNG = random.Random(717520260915)
INT_MIN = -(2**31)
INT_MAX = 2**31 - 1


def expr_len(nums, ops):
    s = str(nums[0])
    for i, op in enumerate(ops):
        s += op + str(nums[i + 1])
    return len(s)


def to_expr(nums, ops):
    s = str(nums[0])
    for i, op in enumerate(ops):
        s += op + str(nums[i + 1])
    return s


def valid_expr(expression):
    assert 1 <= len(expression) <= 20
    assert all(ch.isdigit() or ch in "+-*" for ch in expression)
    nums, ops = parse(expression)
    assert len(nums) == len(ops) + 1
    for x in nums:
        assert 0 <= x <= 99
    vals = solve(expression)
    for v in vals:
        assert INT_MIN <= v <= INT_MAX
    return vals


def write_case(idx, expression, note, hack):
    vals = valid_expr(expression)
    (DATA / f"{idx}.in").write_bytes(expression.encode("utf-8"))
    with open(DATA / f"{idx}.out", "w", encoding="utf-8", newline="\n") as f:
        f.write(str(len(vals)) + "\n")
        f.write(" ".join(str(x) for x in vals) + "\n")
    return note, hack, len(expression), len(vals)


def rand_num(two_digit_ok=True):
    if two_digit_ok and RNG.random() < 0.45:
        return RNG.randint(10, 99)
    return RNG.randint(0, 9)


def try_random(n_nums, ops_pool, two_digit_ok=True, max_try=2000):
    for _ in range(max_try):
        nums = [rand_num(two_digit_ok) for _ in range(n_nums)]
        ops = [RNG.choice(ops_pool) for _ in range(n_nums - 1)]
        expr = to_expr(nums, ops)
        if len(expr) > 20:
            continue
        try:
            valid_expr(expr)
            return expr
        except AssertionError:
            continue
    raise RuntimeError("failed to generate valid expression")


def main():
    DATA.mkdir(parents=True, exist_ok=True)
    plan = [
        ("2-1-1", "样例 1 两种结合", "只算左结合得到 0"),
        ("2*3-4*5", "样例 2 含重复 -10", "结果去重少一个 -10"),
        ("0", "单个 0", "空表达式或漏掉无运算符"),
        ("99", "单个两位数", "把 99 拆成 9 和 9"),
        ("10-1-1", "两位数减两次", "按字符拆成 1,0,1,1"),
        ("8*0-1+2", "乘 0 再加减", "按四则优先级只出一个答案"),
        ("1+2+3+4+5", "全加号卡特兰", "漏掉某一种划分"),
        (try_random(5, "+-*", True), "五数随机混合", "忘记排序"),
        ("1+1+1+1+1+1+1+1+1+1", "长度 19 全加号", "方案数不是卡特兰数"),
        ("12*13-14+15+16-7+8-9", "长度 20 两位数混合", "乘法结合或两位数拆开"),
    ]

    rows = []
    for i, (expr, note, hack) in enumerate(plan, 1):
        note, hack, n, k = write_case(i, expr, note, hack)
        rows.append(f"| {i} | {note}（|s|={n}, k={k}） | 全部加括号结果 | {hack} |")

    for i in range(1, 11):
        ib = (DATA / f"{i}.in").read_bytes()
        ob = (DATA / f"{i}.out").read_bytes()
        assert not ib.endswith(b"\n") and b"\r" not in ib
        assert ob.endswith(b"\n") and not ob.endswith(b"\n\n")
        assert b"\r" not in ob

    s1 = (DATA / "1.out").read_text(encoding="utf-8")
    assert s1 == "2\n0 2\n"
    s2 = (DATA / "2.out").read_text(encoding="utf-8")
    assert s2 == "5\n-34 -14 -10 -10 10\n"

    (DATA / "README.md").write_text(
        "\n".join(
            [
                "# P7175 测试数据说明",
                "",
                r"主造数脚本：题目根目录 `gen.py`。所有加括号结果都保留（含重复），再从小到大输出。",
                r"约束：$1\le |expression|\le 20$，数字 $0..99$，结果在 $32$ 位有符号整数内。",
                "",
                "| 组别 | 规模/分布 | 目标 | 卡掉的错误解 |",
                "|---|---|---|---|",
                *rows,
                "",
                "`.in` 最后一行后无换行符；`.out` 末尾恰好一个换行符。",
                "",
            ]
        ),
        encoding="utf-8",
    )
    print("generated 10 cases")
    for i, (expr, _, _) in enumerate(plan, 1):
        print(i, expr, "len", len(expr))


if __name__ == "__main__":
    main()
