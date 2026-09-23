# -*- coding: utf-8 -*-
"""P7153 造数：数字串解码方法数。

stdin：一行数字串。
输出：方案数，无法解码为 0。
`.in` 最后一行后不留换行；`.out` 末尾恰好一个换行。
答案保证在有符号 32 位整数范围内。
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
RNG = random.Random(715320260915)

N_MAX = 100
INT_MAX = 2**31 - 1


def naive(s):
    """记忆化搜索，与线性 DP 对拍。"""
    n = len(s)
    memo = [-1] * (n + 1)

    def dfs(i):
        if i == n:
            return 1
        if memo[i] != -1:
            return memo[i]
        if s[i] == "0":
            memo[i] = 0
            return 0
        ans = dfs(i + 1)
        if i + 1 < n:
            x = (ord(s[i]) - 48) * 10 + (ord(s[i + 1]) - 48)
            if 10 <= x <= 26:
                ans += dfs(i + 2)
        memo[i] = ans
        return ans

    return dfs(0)


def write_case(idx, s):
    assert 1 <= len(s) <= N_MAX
    assert s.isdigit()
    ans = solve(s)
    expect = naive(s)
    assert ans == expect, (idx, ans, expect, s)
    assert 0 <= ans <= INT_MAX
    (DATA / f"{idx}.in").write_bytes(s.encode("utf-8"))
    with open(DATA / f"{idx}.out", "w", encoding="utf-8", newline="\n") as f:
        f.write(str(ans) + "\n")
    return ans


def rand_digit_s(n):
    # 少用 0，避免方案数直接变 0；又不能全是 1/2 以免 Fibonacci 爆 int
    chars = []
    for i in range(n):
        r = RNG.random()
        if r < 0.08:
            chars.append("0")
        elif r < 0.35:
            chars.append(RNG.choice("12"))
        else:
            chars.append(RNG.choice("3456789"))
    return "".join(chars)


def main():
    DATA.mkdir(parents=True, exist_ok=True)

    p8 = rand_digit_s(20)
    # 压满 100：方案数为 1，避免 Fibonacci 超出 32 位
    p9 = "3" * N_MAX
    # 44 个 1 再接 10，再接 9，方案数 = F(45) 仍在 int 内
    p10 = "1" * 44 + "0" + "9" * 55
    assert len(p10) == N_MAX

    plan = [
        ("12",
         "样例 1", "$2$ 种：$AB$ 或 $L$",
         "漏掉两位编码"),
        ("226",
         "样例 2", "$3$ 种",
         "把 $26$ 漏掉或把 $27$ 当成合法两位"),
        ("06",
         "样例 3，前导零", "$0$",
         "把 $06$ 当成 $6$"),
        ("0",
         "单个 $0$", "$0$",
         "当成 $A$ 得到 $1$"),
        ("10",
         "$10$ 只能两位", "$1$",
         "拆成 $1,0$ 得到 $0$ 或再加一种"),
        ("27",
         "$27$ 不能当两位", "只能 $2,7$，共 $1$ 种",
         "当成 $B$ 和某非法字母仍加一"),
        ("101",
         "中间的 $0$ 必须跟前面组成 $10$", "$1$ 种：$10,1$",
         "拆成 $1,01$ 或 $10,1$ 和 $1,0,1$"),
        (p8,
         "长度 $20$ 随机数字", "DP 与记忆化搜索对拍",
         "不处理前导零"),
        (p9,
         "压满 $100$ 个 $3$", "每位只能单独译，方案数 $1$",
         "当成斐波那契得到巨大数"),
        (p10,
         "压满 $100$，含 $10$ 与一长串 $1$", "方案数仍在 $32$ 位整数内",
         "递归无记忆化 TLE"),
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
    assert answers[2] == 0
    assert answers[3] == 0
    assert answers[4] == 1
    assert answers[5] == 1
    assert answers[6] == 1
    assert answers[8] == 1
    assert len(plan[8][0]) == N_MAX and len(plan[9][0]) == N_MAX

    rows = []
    for i, (_, scale, goal, hack) in enumerate(plan, 1):
        rows.append(f"| {i} | {scale} | {goal} | {hack} |")

    readme = "\n".join([
        "# P7153 测试数据说明",
        "",
        "主造数脚本：题目根目录 `gen.py`。",
        "stdin：一行数字字符串 $s$。",
        "输出：解码方案数；不能完整解码则为 $0$。",
        "",
        r"约束：$1\le |s|\le 100$，答案在有符号 $32$ 位整数范围内。",
        "",
        "| 组别 | 规模/分布 | 目标 | 卡掉的错误解 |",
        "|---|---|---|---|",
        *rows,
        "",
        "`.in` 最后一行后无换行符；`.out` 末尾恰好一个换行符。",
        "",
        "生成后自校验：线性 DP 必须等于记忆化搜索，且答案 $\\le 2^{31}-1$。",
        "",
    ])
    (DATA / "README.md").write_text(readme, encoding="utf-8")
    print("generated 10 cases")
    for i, ans in enumerate(answers, 1):
        print(i, ans, "len", len(plan[i - 1][0]))


if __name__ == "__main__":
    main()
