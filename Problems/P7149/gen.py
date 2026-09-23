# -*- coding: utf-8 -*-
"""P7149 造数：嵌套 k[encoded] 字符串解码。

stdin：一行编码串。
输出：解码后的字符串。
`.in` 最后一行后不留换行；`.out` 末尾恰好一个换行。
"""
from __future__ import annotations

import sys
from pathlib import Path

sys.dont_write_bytecode = True
sys.path.insert(0, str(Path(__file__).resolve().parent))
from std import solve  # noqa: E402

ROOT = Path(__file__).resolve().parent
DATA = ROOT / "data"

S_MAX = 30
OUT_MAX = 10**5
K_MAX = 300


def naive(s):
    """递归下降按括号匹配解码，与栈实现对拍。"""
    i = 0
    n = len(s)

    def parse():
        nonlocal i
        parts = []
        while i < n and s[i] != "]":
            if s[i].isdigit():
                k = 0
                while i < n and s[i].isdigit():
                    k = k * 10 + ord(s[i]) - 48
                    i += 1
                assert s[i] == "["
                i += 1
                inner = parse()
                assert s[i] == "]"
                i += 1
                parts.append(inner * k)
            else:
                assert s[i].isalpha() and s[i].islower()
                parts.append(s[i])
                i += 1
        return "".join(parts)

    ans = parse()
    assert i == n
    return ans


def write_case(idx, s):
    assert 1 <= len(s) <= S_MAX
    ans = solve(s)
    expect = naive(s)
    assert ans == expect, (idx, ans[:40], expect[:40])
    assert 1 <= len(ans) <= OUT_MAX
    (DATA / f"{idx}.in").write_bytes(s.encode("utf-8"))
    with open(DATA / f"{idx}.out", "w", encoding="utf-8", newline="\n") as f:
        f.write(ans + "\n")
    return ans


def main():
    DATA.mkdir(parents=True, exist_ok=True)

    # 解码长度分别约 9e4 与 1e5，编码长度仍 <= 30
    p9 = "300[300[a]]"
    p10 = "10[10[10[100[a]]]]"

    plan = [
        ("3[a]2[bc]",
         "样例 1，两段并列", "$aaabcbc$",
         "只解码第一段"),
        ("3[a2[c]]",
         "样例 2，嵌套", "$accaccacc$",
         "不处理内层 $2[c]$"),
        ("2[abc]3[cd]ef",
         "样例 3，括号后再拼字母", "$abcabccdcdcdef$",
         "丢掉末尾 $ef$"),
        ("abc3[cd]xyz",
         "样例 4，括号前后都有字母", "$abccdcdcdxyz$",
         "丢掉前缀 $abc$"),
        ("a",
         "没有括号", "原串 $a$",
         "空串"),
        ("10[ab]",
         "两位数 $k$", "$ab$ 重复 $10$ 次",
         "把 $10$ 当成重复 $1$ 次再拼字符 $0$"),
        ("1[z]",
         "$k=1$", "$z$",
         "漏掉一层"),
        ("2[a3[b]c]",
         "内层夹在字母中间", "$abbbcabbbc$",
         "内层重复后没有拼回 $a$、$c$"),
        (p9,
         "压满解码长度约 $9\\times 10^4$", "$a$ 重复 $90000$ 次",
         "字符串反复平方拼接 TLE / MLE"),
        (p10,
         "压满解码长度 $10^5$", "$a$ 重复 $100000$ 次",
         "没有按层重复而是只重复最内层一次"),
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

    assert answers[0] == "aaabcbc"
    assert answers[1] == "accaccacc"
    assert answers[2] == "abcabccdcdcdef"
    assert answers[3] == "abccdcdcdxyz"
    assert answers[4] == "a"
    assert answers[5] == "ab" * 10
    assert answers[6] == "z"
    assert answers[7] == "abbbcabbbc"
    assert answers[8] == "a" * 90000
    assert answers[9] == "a" * 100000
    assert len(plan[8][0]) <= S_MAX and len(plan[9][0]) <= S_MAX

    rows = []
    for i, (_, scale, goal, hack) in enumerate(plan, 1):
        rows.append(f"| {i} | {scale} | {goal} | {hack} |")

    readme = "\n".join([
        "# P7149 测试数据说明",
        "",
        "主造数脚本：题目根目录 `gen.py`。",
        "stdin：一行编码字符串 $s$。",
        "输出：完全解码后的字符串。",
        "",
        r"约束：$1\le |s|\le 30$，$k\in[1,300]$，解码后长度 $\le 10^5$。",
        "",
        "| 组别 | 规模/分布 | 目标 | 卡掉的错误解 |",
        "|---|---|---|---|",
        *rows,
        "",
        "`.in` 最后一行后无换行符；`.out` 末尾恰好一个换行符。",
        "",
        "生成后自校验：栈解码必须等于递归下降。",
        "",
    ])
    (DATA / "README.md").write_text(readme, encoding="utf-8")
    print("generated 10 cases")
    for i, ans in enumerate(answers, 1):
        print(i, ans[:20], "len_in", len(plan[i - 1][0]), "len_out", len(ans))


if __name__ == "__main__":
    main()
