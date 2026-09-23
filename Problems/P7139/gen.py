# -*- coding: utf-8 -*-
"""P7139 造数：统计回文子串个数（按位置计数）。

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
RNG = random.Random(713920260914)

N_MAX = 1000


def naive(s):
    """区间 DP：dp[i][j] 表示 s[i..j] 是否回文。"""
    n = len(s)
    pal = [[False] * n for _ in range(n)]
    ans = 0
    for i in range(n - 1, -1, -1):
        for j in range(i, n):
            if s[i] == s[j] and (j - i < 2 or pal[i + 1][j - 1]):
                pal[i][j] = True
                ans += 1
    return ans


def write_case(idx, s):
    n = len(s)
    assert 1 <= n <= N_MAX
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

    rand8 = "".join(RNG.choice(string.ascii_lowercase) for _ in range(40))
    all_a = "a" * N_MAX
    alt = ("ab" * (N_MAX // 2 + 1))[:N_MAX]
    pal = "abcba" * (N_MAX // 5)
    pal = pal[:N_MAX]
    rnd_big = "".join(RNG.choice(string.ascii_lowercase) for _ in range(N_MAX))

    plan = [
        ("abc",
         "样例 1", "三个单字符，答案 $3$",
         "把 $abc$ 整串也算进去"),
        ("aaa",
         "样例 2", "按位置计 $6$ 个，不去重",
         "按内容去重只输出 $3$"),
        ("a",
         "单字符", "答案 $1$",
         "输出 $0$"),
        ("abba",
         "偶数回文 $abba$、$bb$", "单字符 $4$ 个加 $bb$、$abba$，共 $6$",
         "漏掉偶数中心"),
        ("aba",
         "奇数回文 $aba$", "单字符 $3$ 个加 $aba$，共 $4$",
         "漏掉跨中心的 $aba$"),
        ("abcba",
         "更长回文", "中心扩张与 DP 对拍",
         "只统计最长回文"),
        (rand8,
         "小随机 $n=40$", "扩张与区间 DP 对拍",
         "子序列也当成子串"),
        (all_a,
         "压满 $n=1000$，全是 $a$", r"全部子串都是回文，答案 $n(n+1)/2=500500$",
         "int 溢出或只数了 $n$ 个单字符"),
        (alt,
         "压满 $n=1000$，$ab$ 交替", "几乎只有单字符和极少偶数回文",
         "把 $aba$ 漏计或多重计"),
        (rnd_big,
         "压满 $n=1000$ 随机小写字母", "线性扩张",
         "$O(n^3)$ 暴力在本组可能勉强过，但扩张更稳"),
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

    assert answers[0] == 3
    assert answers[1] == 6
    assert answers[2] == 1
    assert answers[3] == 6
    assert answers[4] == 4
    assert answers[7] == N_MAX * (N_MAX + 1) // 2

    rows = []
    for i, (_, scale, goal, hack) in enumerate(plan, 1):
        rows.append(f"| {i} | {scale} | {goal} | {hack} |")

    readme = "\n".join([
        "# P7139 测试数据说明",
        "",
        "主造数脚本：题目根目录 `gen.py`。",
        "stdin：一行小写字符串 $s$。",
        "输出：回文子串个数（按出现位置计数）。",
        "",
        r"约束：$1\le |s|\le 1000$，$s$ 仅含小写英文字母。",
        "",
        "| 组别 | 规模/分布 | 目标 | 卡掉的错误解 |",
        "|---|---|---|---|",
        *rows,
        "",
        "`.in` 最后一行后无换行符；`.out` 末尾恰好一个换行符。",
        "",
        "生成后自校验：中心扩张必须等于区间 DP 的回文个数。",
        "",
    ])
    (DATA / "README.md").write_text(readme, encoding="utf-8")
    print("generated 10 cases")
    for i, ans in enumerate(answers, 1):
        print(i, "ans", ans)


if __name__ == "__main__":
    main()
