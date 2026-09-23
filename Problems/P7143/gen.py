# -*- coding: utf-8 -*-
"""P7143 造数：英文句子单词平均长度。

stdin：一行由字母和空格组成的句子。
输出：平均长度，固定两位小数。
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
RNG = random.Random(714320260915)

N_MAX = 10**4
LETTERS = string.ascii_letters


def naive(s):
    """手写扫描，与 split 对拍。"""
    total = 0
    cnt = 0
    i = 0
    n = len(s)
    while i < n:
        while i < n and s[i] == " ":
            i += 1
        if i >= n:
            break
        j = i
        while j < n and s[j] != " ":
            j += 1
        total += j - i
        cnt += 1
        i = j
    return "{:.2f}".format(total / cnt)


def write_case(idx, s):
    assert 1 <= len(s) <= N_MAX
    assert any(ch.isalpha() for ch in s)
    for ch in s:
        assert ch.isalpha() or ch == " "
    (DATA / f"{idx}.in").write_bytes(s.encode("utf-8"))
    ans = solve(s)
    expect = naive(s)
    assert ans == expect, (idx, ans, expect, s[:80])
    assert len(ans) >= 4 and ans[-3] == "."
    with open(DATA / f"{idx}.out", "w", encoding="utf-8", newline="\n") as f:
        f.write(ans + "\n")
    return ans


def rand_word(lo=1, hi=8):
    k = RNG.randint(lo, hi)
    return "".join(RNG.choice(LETTERS) for _ in range(k))


def join_words(words, multi_space=False, lead=False, trail=False):
    parts = []
    for i, w in enumerate(words):
        if i:
            parts.append(" " * (RNG.randint(2, 4) if multi_space else 1))
        parts.append(w)
    s = "".join(parts)
    if lead:
        s = " " * RNG.randint(1, 3) + s
    if trail:
        s = s + " " * RNG.randint(1, 3)
    if len(s) > N_MAX:
        s = s[:N_MAX]
        # 截断后仍要至少有一个字母
        if not any(ch.isalpha() for ch in s):
            s = "A"
    return s


def long_many_words():
    words = []
    s = ""
    while True:
        w = rand_word(1, 6)
        extra = (" " * RNG.randint(1, 3) + w) if s else w
        if len(s) + len(extra) > N_MAX:
            break
        s += extra
        words.append(w)
    if not s:
        s = "A"
    return s


def long_few_words():
    # 少数很长的单词，压满长度
    left = N_MAX
    words = []
    while left > 1:
        k = min(left, RNG.randint(200, 800))
        if left - k == 1:
            k = left
        words.append("".join(RNG.choice(LETTERS) for _ in range(k)))
        left -= k
        if left <= 0:
            break
        if left == 1:
            words[-1] += RNG.choice(LETTERS)
            break
        # 一个空格
        left -= 1
    return " ".join(words)[:N_MAX]


def main():
    DATA.mkdir(parents=True, exist_ok=True)

    p8 = join_words([rand_word() for _ in range(12)], multi_space=True, lead=True, trail=True)
    p9 = long_many_words()
    p10 = long_few_words()

    plan = [
        ("I love coding",
         "样例 1，$11/3$", "$3.67$，不能先四舍五入成整数",
         "输出 $4.00$ 或 $3$"),
        ("this is a test",
         "样例 2，$11/4$", "$2.75$",
         "整数除法得到 $2$"),
        ("A",
         "单个字母单词", "$1.00$，必须两位小数",
         "输出 $1$ 或 $1.0$"),
        ("Hello",
         "单个长单词", "$5.00$",
         "漏掉末尾单词"),
        ("a    bb   ccc",
         "多个连续空格", "$(1+2+3)/3=2.00$",
         "把空串当成单词得到更小平均值"),
        ("  leading trailing  ",
         "首尾空格", "只有两个单词 $leading$、$trailing$",
         "把首尾空格切成空单词"),
        ("a b c d e f g h i j k",
         "大量单字母", "平均值 $1.00$",
         "按字符总数含空格去除"),
        (p8,
         "小随机、多空格、大小写混合", "扫描与 $split$ 对拍",
         "只读第一个单词"),
        (p9,
         "压满约 $10^4$，很多短单词", "线性扫一遍",
         "$O(n^2)$ 反复拼接"),
        (p10,
         "压满约 $10^4$，少数长单词", "长度累加不能用 $int$ 溢出（本题不会，但格式仍要两位小数）",
         "只统计单词个数忘记累加长度"),
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

    assert answers[0] == "3.67"
    assert answers[1] == "2.75"
    assert answers[2] == "1.00"
    assert answers[3] == "5.00"
    assert answers[4] == "2.00"

    rows = []
    for i, (_, scale, goal, hack) in enumerate(plan, 1):
        rows.append(f"| {i} | {scale} | {goal} | {hack} |")

    readme = "\n".join([
        "# P7143 测试数据说明",
        "",
        "主造数脚本：题目根目录 `gen.py`。",
        "stdin：一行英文句子（字母与空格）。",
        "输出：单词平均长度，固定两位小数。",
        "",
        r"约束：$1\le |s|\le 10^4$，至少 $1$ 个单词。",
        "",
        "题面原稿样例 $1$ 误写输出 $4.00$，已按 $(1+4+6)/3=3.67$ 纠正。",
        "",
        "| 组别 | 规模/分布 | 目标 | 卡掉的错误解 |",
        "|---|---|---|---|",
        *rows,
        "",
        "`.in` 最后一行后无换行符；`.out` 末尾恰好一个换行符。",
        "",
        "生成后自校验：手写扫描必须等于 $split$ 后求平均。",
        "",
    ])
    (DATA / "README.md").write_text(readme, encoding="utf-8")
    print("generated 10 cases")
    for i, ans in enumerate(answers, 1):
        print(i, ans, "len_in", len(plan[i - 1][0]))


if __name__ == "__main__":
    main()
