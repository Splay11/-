# -*- coding: utf-8 -*-
"""P7146 造数：带括号与一元减号的基本计算器。

stdin：一行表达式（可含空格）。
输出：整数值。
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
RNG = random.Random(714620260915)

N_MAX = 3 * 10**5
INT_MIN = -(2**31)
INT_MAX = 2**31 - 1


def naive(s):
    """递归下降：表达式 = 项 {(+|-) 项}，项 = 一元减 | 括号 | 数字。"""
    t = s.replace(" ", "")
    i = 0
    n = len(t)

    def peek():
        return t[i] if i < n else ""

    def expr():
        nonlocal i
        v = term()
        while peek() == "+" or peek() == "-":
            op = t[i]
            i += 1
            u = term()
            v = v + u if op == "+" else v - u
        return v

    def term():
        nonlocal i
        if peek() == "-":
            i += 1
            return -term()
        if peek() == "(":
            i += 1
            v = expr()
            assert peek() == ")"
            i += 1
            return v
        assert peek().isdigit()
        num = 0
        while peek().isdigit():
            num = num * 10 + ord(t[i]) - 48
            i += 1
        return num

    ans = expr()
    assert i == n
    return ans


def maybe_space():
    if RNG.random() < 0.35:
        return " " * RNG.randint(1, 2)
    return ""


def gen_atom(depth):
    # 原子只能是数字或括号，不以运算符开头，避免出现 1+-2 这种连续运算符
    if depth > 0 and RNG.random() < 0.35:
        inner = gen_expr(depth - 1)
        return "(" + maybe_space() + inner + maybe_space() + ")"
    return str(RNG.randint(0, 20))


def gen_expr(depth):
    first = gen_atom(depth)
    if RNG.random() < 0.2:
        # 一元减号只能出现在表达式开头或左括号之后
        first = "-" + first
    parts = [first]
    for _ in range(RNG.randint(0, 3)):
        op = RNG.choice("+-")
        parts.append(maybe_space() + op + maybe_space() + gen_atom(depth))
    return "".join(parts)


def long_plus_chain(n):
    # 1+1+... 压满长度，中间结果仍在 int32
    s = "1"
    while len(s) + 2 <= n:
        s += "+1"
    return s


def long_paren_sum(n):
    # (1)+(1)+... 或 (1-0)+...
    piece = "(1)"
    s = piece
    while len(s) + 1 + len(piece) <= n:
        s += "+" + piece
    return s


def write_case(idx, s):
    assert 1 <= len(s) <= N_MAX, len(s)
    for ch in s:
        assert ch.isdigit() or ch in "+-() "
    ans = solve(s)
    expect = naive(s)
    assert ans == expect, (idx, ans, expect, s[:80])
    assert INT_MIN <= ans <= INT_MAX
    (DATA / f"{idx}.in").write_bytes(s.encode("utf-8"))
    with open(DATA / f"{idx}.out", "w", encoding="utf-8", newline="\n") as f:
        f.write(str(ans) + "\n")
    return ans


def main():
    DATA.mkdir(parents=True, exist_ok=True)

    p8 = gen_expr(3)
    if len(p8) > 200:
        p8 = "(1+(2-3))+4"
    p9 = long_plus_chain(N_MAX)
    p10 = long_paren_sum(N_MAX)

    plan = [
        ("1 + 1",
         "样例 1，含空格", "$2$",
         "用 $cin$ 只读到 $1$"),
        (" 2-1 + 2 ",
         "样例 2，首尾空格", "$3$",
         "没有跳过空格把数字读坏"),
        ("(1+(4+5+2)-3)+(6+8)",
         "样例 3，多层括号", "$23$",
         "括号层符号没压栈"),
        ("-(2+3)",
         "一元减号作用在括号上", "$-5$",
         "算成 $-2+3=1$"),
        ("0",
         "单个 $0$", "$0$",
         "空结果"),
        ("10+20-3",
         "多位整数", "$27$",
         "数字只读一位得到 $1+2-3$"),
        ("1-(2-(3-4))",
         "嵌套减法", "$1-(2-(3-4))=-2$",
         "从左到右无括号得到错误值"),
        (p8,
         "小随机加减、括号、一元减与空格", "栈扫描与递归下降对拍",
         "把加号当一元正号"),
        (p9,
         "压满约 $3\\times 10^5$ 的 $1+1+\\cdots$", "线性扫，不能递归按加号深度",
         "递归求值爆栈或 TLE"),
        (p10,
         "压满约 $3\\times 10^5$ 的 $(1)+(1)+\\cdots$", "大量括号进出栈",
         "右括号没把内层乘回外层符号"),
    ]
    assert len(plan) == 10

    answers = []
    for idx, (s, _, _, _) in enumerate(plan, 1):
        answers.append(write_case(idx, s))

    for i, (s, _, _, _) in enumerate(plan, 1):
        ib = (DATA / f"{i}.in").read_bytes()
        ob = (DATA / f"{i}.out").read_bytes()
        assert not ib.endswith(b"\n") and b"\r" not in ib, f"{i}.in"
        assert ob.endswith(b"\n") and not ob.endswith(b"\n\n") and b"\r" not in ob
        assert ib.decode("utf-8") == s
        got = ob.decode("utf-8")[:-1]
        assert got == str(answers[i - 1]) == str(naive(s))

    assert answers[0] == 2
    assert answers[1] == 3
    assert answers[2] == 23
    assert answers[3] == -5
    assert answers[4] == 0
    assert answers[5] == 27
    assert answers[6] == -2
    assert len(plan[8][0]) <= N_MAX and len(plan[9][0]) <= N_MAX
    assert len(plan[8][0]) >= N_MAX - 5
    assert len(plan[9][0]) >= N_MAX - 10

    rows = []
    for i, (_, scale, goal, hack) in enumerate(plan, 1):
        rows.append(f"| {i} | {scale} | {goal} | {hack} |")

    readme = "\n".join([
        "# P7146 测试数据说明",
        "",
        "主造数脚本：题目根目录 `gen.py`。",
        "stdin：一行合法加减表达式，可含空格、括号、一元减号。",
        "输出：表达式的值（有符号 $32$ 位整数范围内）。",
        "",
        r"约束：$1\le |s|\le 3\times 10^5$。加号不能作一元运算符；没有两个连续运算符。",
        "",
        "| 组别 | 规模/分布 | 目标 | 卡掉的错误解 |",
        "|---|---|---|---|",
        *rows,
        "",
        "`.in` 最后一行后无换行符；`.out` 末尾恰好一个换行符。",
        "",
        "生成后自校验：栈扫描必须等于递归下降求值。",
        "",
    ])
    (DATA / "README.md").write_text(readme, encoding="utf-8")
    print("generated 10 cases")
    for i, ans in enumerate(answers, 1):
        print(i, ans, "len_in", len(plan[i - 1][0]))


if __name__ == "__main__":
    main()
