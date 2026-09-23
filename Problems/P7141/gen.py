# -*- coding: utf-8 -*-
"""P7141 造数：两个相同字符之间最长子串长度（不含两端）。

stdin：一行小写字符串 s。
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
RNG = random.Random(714120260915)

N_MAX = 300


def naive(s):
    ans = -1
    n = len(s)
    for i in range(n):
        for j in range(i + 1, n):
            if s[i] == s[j]:
                ans = max(ans, j - i - 1)
    return ans


def write_case(idx, s):
    assert 1 <= len(s) <= N_MAX
    assert s.isalpha() and s.islower()
    (DATA / f"{idx}.in").write_bytes(s.encode("utf-8"))
    ans = solve(s)
    expect = naive(s)
    assert ans == expect, (idx, ans, expect)
    with open(DATA / f"{idx}.out", "w", encoding="utf-8", newline="\n") as f:
        f.write(str(ans) + "\n")
    return ans


def main():
    DATA.mkdir(parents=True, exist_ok=True)

    uniq26 = string.ascii_lowercase
    all_a = "a" * 8
    rnd = "".join(RNG.choice(string.ascii_lowercase) for _ in range(40))
    big_span = "a" + "b" * (N_MAX - 2) + "a"
    big_rnd = "".join(RNG.choice(string.ascii_lowercase) for _ in range(N_MAX))

    plan = [
        ("aa",
         "样例 1", "相邻相同，中间长度 $0$",
         "当成不存在，输出 $-1$"),
        ("abca",
         "样例 2", "首尾 $a$，中间 $bc$，答案 $2$",
         "算成 $j-i=3$"),
        ("cbzxy",
         "样例 3，全部只出现一次", "输出 $-1$",
         "输出 $0$"),
        ("cabbac",
         "样例 4", "首尾 $c$ 中间 $abba$，答案 $4$",
         "只看了相邻的 $bb$ 输出 $0$"),
        ("z",
         "单字符", "输出 $-1$",
         "输出 $0$"),
        (uniq26,
         "26 个字母各一次", "输出 $-1$",
         "把整串长度当答案"),
        (all_a,
         "连续 8 个 $a$", "最左到最右中间 $6$",
         "只统计相邻对得到 $0$"),
        (rnd,
         "小随机 $n=40$", "哈希表与二重循环对拍",
         "漏掉某字母的最右出现"),
        (big_span,
         "压满 $n=300$，首尾相同", "答案 $298$",
         "$j-i$ 得到 $299$"),
        (big_rnd,
         "压满 $n=300$ 随机小写字母", "线性扫一遍即可",
         "枚举所有下标对写错公式"),
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
        got = int(ob.decode("utf-8").strip())
        assert got == answers[i - 1] == naive(s)

    assert answers[0] == 0
    assert answers[1] == 2
    assert answers[2] == -1
    assert answers[3] == 4
    assert answers[4] == -1
    assert answers[5] == -1
    assert answers[6] == 6
    assert answers[8] == N_MAX - 2

    rows = []
    for i, (_, scale, goal, hack) in enumerate(plan, 1):
        rows.append(f"| {i} | {scale} | {goal} | {hack} |")

    readme = "\n".join([
        "# P7141 测试数据说明",
        "",
        "主造数脚本：题目根目录 `gen.py`。",
        "stdin：一行小写字符串 $s$。",
        "输出：两个相同字符之间最长子串长度（不含两端）；无重复字符则为 $-1$。",
        "",
        r"约束：$1\le |s|\le 300$，$s$ 仅含小写英文字母。",
        "",
        "| 组别 | 规模/分布 | 目标 | 卡掉的错误解 |",
        "|---|---|---|---|",
        *rows,
        "",
        "`.in` 最后一行后无换行符；`.out` 末尾恰好一个换行符。",
        "",
        "生成后自校验：首末出现下标法必须等于枚举所有相等下标对。",
        "",
    ])
    (DATA / "README.md").write_text(readme, encoding="utf-8")
    print("generated 10 cases")
    for i, ans in enumerate(answers, 1):
        print(i, "ans", ans)


if __name__ == "__main__":
    main()
