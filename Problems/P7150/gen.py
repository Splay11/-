# -*- coding: utf-8 -*-
"""P7150 造数：反复删除相邻相同字符。

stdin：一行小写字母。
输出：消除后的字符串（可能为空）。
`.in` 最后一行后不留换行；`.out` 末尾恰好一个换行。
"""
from __future__ import annotations

import random
import string
import sys
from pathlib import Path

sys.dont_write_bytecode = True
sys.path.insert(0, str(Path(__file__).resolve().parent))
from std import solve  # noqa: E402

ROOT = Path(__file__).resolve().parent
DATA = ROOT / "data"
RNG = random.Random(715020260915)

N_MAX = 10**5
LETTERS = string.ascii_lowercase


def naive(s):
    """下标当栈顶，与 list 栈对拍。"""
    buf = [" "] * len(s)
    top = 0
    for c in s:
        if top and buf[top - 1] == c:
            top -= 1
        else:
            buf[top] = c
            top += 1
    return "".join(buf[:top])


def write_case(idx, s):
    assert 1 <= len(s) <= N_MAX
    assert s.isalpha() and s.islower()
    ans = solve(s)
    expect = naive(s)
    assert ans == expect, (idx, ans[:40], expect[:40])
    (DATA / f"{idx}.in").write_bytes(s.encode("utf-8"))
    with open(DATA / f"{idx}.out", "w", encoding="utf-8", newline="\n") as f:
        f.write(ans + "\n")
    return ans


def rand_s(n, alph=None):
    alph = alph or LETTERS
    return "".join(RNG.choice(alph) for _ in range(n))


def main():
    DATA.mkdir(parents=True, exist_ok=True)

    p8 = rand_s(30, "abc")
    p9 = rand_s(N_MAX)
    # 大量成对可消，夹少量残留
    p10 = "aa" * (N_MAX // 2 - 1) + "b" + "aa"
    p10 = p10[:N_MAX]
    if len(p10) < N_MAX:
        p10 += "c" * (N_MAX - len(p10))

    plan = [
        ("abbaca",
         "样例 1，连锁删除", "$ca$",
         "只删一轮得到 $aaca$"),
        ("azxxzy",
         "样例 2", "$ay$",
         "删 $xx$ 后不再删 $zz$"),
        ("a",
         "单个字符", "$a$",
         "空串"),
        ("aa",
         "一对相同", "删空，输出空行",
         "输出 $aa$"),
        ("aaa",
         "奇数个相同", "只剩 $a$，不能整段删光",
         "输出空串"),
        ("abc",
         "互不相同", "原串",
         "误删"),
        ("abba",
         "从内向外消成空", "空串",
         "只消 $bb$ 得到 $aa$ 就停"),
        (p8,
         "小随机 $a$–$c$", "栈与下标栈对拍",
         "只看相邻不连锁"),
        (p9,
         "压满 $10^5$ 随机小写", "线性栈",
         "每次 $erase$ 中间字符 $O(n^2)$ TLE"),
        (p10,
         "压满 $10^5$，大量成对 $aa$", "反复弹栈",
         "奇数段处理错误"),
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
        assert got == answers[i - 1] == naive(s)

    assert answers[0] == "ca"
    assert answers[1] == "ay"
    assert answers[2] == "a"
    assert answers[3] == ""
    assert answers[4] == "a"
    assert answers[5] == "abc"
    assert answers[6] == ""
    assert len(plan[8][0]) == N_MAX and len(plan[9][0]) == N_MAX

    rows = []
    for i, (_, scale, goal, hack) in enumerate(plan, 1):
        rows.append(f"| {i} | {scale} | {goal} | {hack} |")

    readme = "\n".join([
        "# P7150 测试数据说明",
        "",
        "主造数脚本：题目根目录 `gen.py`。",
        "stdin：一行小写字符串 $s$。",
        "输出：反复删除相邻相同字符后的结果，可能为空。",
        "",
        r"约束：$1\le |s|\le 10^5$，仅小写字母。",
        "",
        "| 组别 | 规模/分布 | 目标 | 卡掉的错误解 |",
        "|---|---|---|---|",
        *rows,
        "",
        "`.in` 最后一行后无换行符；`.out` 末尾恰好一个换行符。",
        "",
        "生成后自校验：list 栈必须等于下标栈。",
        "",
    ])
    (DATA / "README.md").write_text(readme, encoding="utf-8")
    print("generated 10 cases")
    for i, ans in enumerate(answers, 1):
        print(i, repr(ans[:20]), "len_in", len(plan[i - 1][0]), "len_out", len(ans))


if __name__ == "__main__":
    main()
