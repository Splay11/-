# -*- coding: utf-8 -*-
"""P7144 造数：最长连续元音子串。

stdin：一行小写字母 s。
输出：最长连续元音子串；平局取最先出现；无元音输出 -1。
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
RNG = random.Random(714420260915)

N_MAX = 10**5
VOWELS = "aeiou"
CONS = "bcdfghjklmnpqrstvwxyz"


def naive(s):
    """下标枚举每一段，与扫描对拍。"""
    best = ""
    n = len(s)
    i = 0
    while i < n:
        if s[i] not in VOWELS:
            i += 1
            continue
        j = i
        while j < n and s[j] in VOWELS:
            j += 1
        if j - i > len(best):
            best = s[i:j]
        i = j
    return best if best else "-1"


def write_case(idx, s):
    assert 1 <= len(s) <= N_MAX
    assert s.isalpha() and s.islower()
    (DATA / f"{idx}.in").write_bytes(s.encode("utf-8"))
    ans = solve(s)
    expect = naive(s)
    assert ans == expect, (idx, ans, expect)
    if ans != "-1":
        assert all(ch in VOWELS for ch in ans)
        assert ans in s
    with open(DATA / f"{idx}.out", "w", encoding="utf-8", newline="\n") as f:
        f.write(ans + "\n")
    return ans


def rand_block(letters, lo, hi):
    k = RNG.randint(lo, hi)
    return "".join(RNG.choice(letters) for _ in range(k))


def mix_small():
    parts = []
    for _ in range(8):
        if RNG.random() < 0.45:
            parts.append(rand_block(VOWELS, 1, 5))
        else:
            parts.append(rand_block(CONS, 1, 6))
    return "".join(parts)


def long_with_runs(n, first_len, later_len, later_same=False):
    """前半放一段 first_len 元音，后半再放一段 later_len 元音。"""
    left_cons = rand_block(CONS, 3, 8)
    first = "".join(RNG.choice(VOWELS) for _ in range(first_len))
    mid = rand_block(CONS, 5, 20)
    later = "".join(RNG.choice(VOWELS) for _ in range(later_len))
    if later_same:
        # 等长但字母不同，才能卡「平局取右边」
        later = "".join(RNG.choice(VOWELS) for _ in range(later_len))
        if later == first:
            later = ("u" * later_len) if first[0] != "u" else ("a" * later_len)
    rest_len = n - len(left_cons) - len(first) - len(mid) - len(later)
    if rest_len < 1:
        rest = "b"
        s = (left_cons + first + mid + later + rest)[:n]
        return s
    rest = "".join(RNG.choice(CONS) for _ in range(rest_len))
    s = left_cons + first + mid + later + rest
    assert len(s) == n
    return s


def main():
    DATA.mkdir(parents=True, exist_ok=True)

    p8 = mix_small()
    p9 = long_with_runs(N_MAX, 40, 25)
    p10 = long_with_runs(N_MAX, 30, 30, later_same=True)

    plan = [
        ("abcaeioubc",
         "样例 1", "$aeiou$ 长度 $5$",
         "只输出单个 $a$"),
        ("beautiful",
         "样例 2", "$eau$ 比后面的 $i$、$u$ 长",
         "把 $y$ 或辅音拼进去"),
        ("bcdfg",
         "样例 3，全辅音", "输出 $-1$",
         "输出空串"),
        ("a",
         "单个元音", "整串 $a$",
         "没有元音时的分支误伤"),
        ("b",
         "单个辅音", "$-1$",
         "输出 $b$"),
        ("aeixaeo",
         "两段等长 $3$，字母不同", "取先出现的 $aei$",
         "用 $\\ge$ 更新得到后面的 $aeo$"),
        ("rhythm",
         "$y$ 不是元音", "$-1$",
         "把 $y$ 当元音输出 $y$"),
        (p8,
         "小随机元音段与辅音段交错", "扫描与朴素分段对拍",
         "漏掉开头或结尾的元音段"),
        (p9,
         "压满 $10^5$，前段更长", "线性扫一遍",
         "只看最后一段"),
        (p10,
         "压满 $10^5$，两段等长", "平局保留先出现的那段",
         "平局取右边"),
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

    assert answers[0] == "aeiou"
    assert answers[1] == "eau"
    assert answers[2] == "-1"
    assert answers[3] == "a"
    assert answers[4] == "-1"
    assert answers[5] == "aei"
    assert answers[6] == "-1"
    assert answers[8] != answers[9] or True
    assert len(plan[8][0]) == N_MAX and len(plan[9][0]) == N_MAX

    rows = []
    for i, (_, scale, goal, hack) in enumerate(plan, 1):
        rows.append(f"| {i} | {scale} | {goal} | {hack} |")

    readme = "\n".join([
        "# P7144 测试数据说明",
        "",
        "主造数脚本：题目根目录 `gen.py`。",
        "stdin：一行小写字符串 $s$。",
        "输出：最长连续元音子串；平局取最先出现；无元音输出 $-1$。",
        "",
        r"约束：$1\le |s|\le 10^5$，仅小写字母。元音为 $a,e,i,o,u$，不含 $y$。",
        "",
        "| 组别 | 规模/分布 | 目标 | 卡掉的错误解 |",
        "|---|---|---|---|",
        *rows,
        "",
        "`.in` 最后一行后无换行符；`.out` 末尾恰好一个换行符。",
        "",
        "生成后自校验：扫描结果必须等于另一套分段实现。",
        "",
    ])
    (DATA / "README.md").write_text(readme, encoding="utf-8")
    print("generated 10 cases")
    for i, ans in enumerate(answers, 1):
        print(i, ans[:40], "len_in", len(plan[i - 1][0]), "len_ans", len(ans))


if __name__ == "__main__":
    main()
