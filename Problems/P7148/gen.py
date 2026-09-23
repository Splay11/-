# -*- coding: utf-8 -*-
"""P7148 造数：带星号的有效括号字符串。

stdin：一行由 ( ) * 组成的字符串。
输出：true 或 false。
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
RNG = random.Random(714820260915)

N_MAX = 100
CHARS = "()*"


def naive(s):
    """按位置和当前余额记忆化搜索，与贪心区间对拍。"""
    n = len(s)
    memo = {}

    def dfs(i, bal):
        if bal < 0:
            return False
        if i == n:
            return bal == 0
        key = (i, bal)
        if key in memo:
            return memo[key]
        c = s[i]
        if c == "(":
            ok = dfs(i + 1, bal + 1)
        elif c == ")":
            ok = dfs(i + 1, bal - 1)
        else:
            ok = (
                dfs(i + 1, bal + 1)
                or dfs(i + 1, bal - 1)
                or dfs(i + 1, bal)
            )
        memo[key] = ok
        return ok

    return dfs(0, 0)


def write_case(idx, s):
    assert 1 <= len(s) <= N_MAX
    for ch in s:
        assert ch in CHARS
    ans = solve(s)
    expect = naive(s)
    assert ans == expect, (idx, ans, expect, s)
    (DATA / f"{idx}.in").write_bytes(s.encode("utf-8"))
    with open(DATA / f"{idx}.out", "w", encoding="utf-8", newline="\n") as f:
        f.write(("true" if ans else "false") + "\n")
    return ans


def rand_s(n):
    return "".join(RNG.choice(CHARS) for _ in range(n))


def balanced_with_stars(n):
    """先造合法括号串，再随机把部分括号改成星号。"""
    if n == 1:
        return "*"
    half = n // 2
    body = []
    bal = 0
    for _ in range(half):
        if bal == 0 or (bal < half and RNG.random() < 0.55):
            body.append("(")
            bal += 1
        else:
            body.append(")")
            bal -= 1
    body.extend(")" * bal)
    s = "".join(body)
    if len(s) < n:
        s += "*" * (n - len(s))
    s = s[:n]
    lst = list(s)
    for i, ch in enumerate(lst):
        if ch in "()" and RNG.random() < 0.3:
            lst[i] = "*"
    return "".join(lst)


def main():
    DATA.mkdir(parents=True, exist_ok=True)

    p8 = rand_s(20)
    p9 = "*" * N_MAX
    p10 = balanced_with_stars(N_MAX)

    plan = [
        ("()",
         "样例 1，无星号合法", "$true$",
         "空串判错"),
        ("(*)",
         "样例 2，星号当空", "$true$",
         "星号必须当括号而判假"),
        ("(*))",
         "样例 3，星号当左括号", "$true$",
         "星号只当空得到 $())$ 判假"),
        (")(",
         "右括号在前", "$false$",
         "只数左右括号个数相等就判真"),
        ("(((",
         "左括号配不平", "$false$",
         "没有检查扫完后 $lo=0$"),
        ("***",
         "全是星号", "$true$（全当空）",
         "把星号必须配成括号"),
        ("*(",
         "星号在左括号前也配不平", "$false$",
         "把 $*$ 当右括号得到 $)($ 仍假，却有人判真"),
        (p8,
         "长度 $20$ 随机", "贪心区间与记忆化搜索对拍",
         "区间没把 $lo$ 夹回 $0$"),
        (p9,
         "压满 $100$ 个星号", "$true$",
         "递归按 $3^{100}$ 枚举 TLE"),
        (p10,
         "压满 $100$，合法括号再随机改星号", "上限规模仍 $O(n)$",
         "DP 状态漏记余额上界"),
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
        word = "true" if answers[i - 1] else "false"
        assert got == word
        assert naive(s) == answers[i - 1]

    assert answers[0] is True
    assert answers[1] is True
    assert answers[2] is True
    assert answers[3] is False
    assert answers[4] is False
    assert answers[5] is True
    assert answers[6] is False
    assert answers[8] is True
    assert len(plan[8][0]) == N_MAX and len(plan[9][0]) == N_MAX

    rows = []
    for i, (_, scale, goal, hack) in enumerate(plan, 1):
        rows.append(f"| {i} | {scale} | {goal} | {hack} |")

    readme = "\n".join([
        "# P7148 测试数据说明",
        "",
        "主造数脚本：题目根目录 `gen.py`。",
        "stdin：一行由 $($、$)$、$*$ 组成的字符串。",
        "输出：$true$ 或 $false$。",
        "",
        r"约束：$1\le |s|\le 100$。",
        "",
        "| 组别 | 规模/分布 | 目标 | 卡掉的错误解 |",
        "|---|---|---|---|",
        *rows,
        "",
        "`.in` 最后一行后无换行符；`.out` 末尾恰好一个换行符。",
        "",
        "生成后自校验：贪心区间必须等于记忆化搜索。",
        "",
    ])
    (DATA / "README.md").write_text(readme, encoding="utf-8")
    print("generated 10 cases")
    for i, ans in enumerate(answers, 1):
        print(i, "true" if ans else "false", "len", len(plan[i - 1][0]))


if __name__ == "__main__":
    main()
