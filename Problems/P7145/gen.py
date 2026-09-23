# -*- coding: utf-8 -*-
"""P7145 造数：删除重复字母得到字典序最小子序列。

stdin：一行小写字母 s。
输出：每个字母至多一次、保持相对顺序、字典序最小。
`.in` 最后一行后不留换行；`.out` 末尾恰好一个换行。
"""
from __future__ import annotations

import random
import string
import sys
from collections import Counter
from pathlib import Path

sys.dont_write_bytecode = True
sys.path.insert(0, str(Path(__file__).resolve().parent))
from std import solve  # noqa: E402

ROOT = Path(__file__).resolve().parent
DATA = ROOT / "data"
RNG = random.Random(714520260915)

N_MAX = 10**4
LETTERS = string.ascii_lowercase


def naive(s):
    """用剩余次数做单调栈，与「最后出现下标」版对拍。"""
    cnt = Counter(s)
    stack = []
    used = set()
    for c in s:
        cnt[c] -= 1
        if c in used:
            continue
        while stack and stack[-1] > c and cnt[stack[-1]] > 0:
            used.remove(stack.pop())
        stack.append(c)
        used.add(c)
    return "".join(stack)


def first_occ(s):
    """假解：每个字母只留第一次。"""
    seen = set()
    out = []
    for c in s:
        if c not in seen:
            seen.add(c)
            out.append(c)
    return "".join(out)


def last_occ(s):
    """假解：按最后一次出现的下标从左到右拼。"""
    last = {c: i for i, c in enumerate(s)}
    items = sorted(last.items(), key=lambda kv: kv[1])
    return "".join(c for c, _ in items)


def write_case(idx, s):
    assert 1 <= len(s) <= N_MAX
    assert s.isalpha() and s.islower()
    (DATA / f"{idx}.in").write_bytes(s.encode("utf-8"))
    ans = solve(s)
    expect = naive(s)
    assert ans == expect, (idx, ans, expect)
    assert len(ans) == len(set(s))
    assert len(set(ans)) == len(ans)
    with open(DATA / f"{idx}.out", "w", encoding="utf-8", newline="\n") as f:
        f.write(ans + "\n")
    return ans


def rand_s(n, alphabet=None):
    alph = alphabet or LETTERS
    return "".join(RNG.choice(alph) for _ in range(n))


def main():
    DATA.mkdir(parents=True, exist_ok=True)

    p8 = rand_s(40, "abcdef")
    p9 = rand_s(N_MAX)
    # 从 z 到 a 再穿插重复，迫使多次弹栈
    p10 = "".join(ch * RNG.randint(2, 8) for ch in reversed(LETTERS))
    p10 = (p10 + "a" * 10)[:N_MAX]
    if len(p10) < N_MAX:
        p10 += rand_s(N_MAX - len(p10))

    plan = [
        ("bcabc",
         "样例 1", "$abc$，不能只留第一次",
         "第一次出现得到 $bca$"),
        ("cbacdcbc",
         "样例 2", "$acdb$",
         "按最后出现下标得到 $adbc$"),
        ("a",
         "单个字母", "$a$",
         "空串"),
        ("ba",
         "不能重排", "$ba$ 而不是 $ab$",
         "排序去重得到 $ab$"),
        ("aaaa",
         "全部相同", "$a$",
         "输出 $aaaa$"),
        ("abc",
         "已经无重复且递增", "原串",
         "误删字母"),
        ("cba",
         "递减且各一次", "必须原样 $cba$",
         "弹栈把 $c$、$b$ 丢掉后无法再选"),
        (p8,
         "小随机，字母集 $a$–$f$", "两种单调栈对拍",
         "漏掉某字母"),
        (p9,
         "压满 $10^4$，全字母表随机", "线性栈",
         "$O(n^2)$ 枚举子序列"),
        (p10,
         "压满，高字母在前、重复多次", "反复弹栈仍能还原",
         "弹完不再入栈导致缺字母"),
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

    assert answers[0] == "abc"
    assert answers[1] == "acdb"
    assert answers[2] == "a"
    assert answers[3] == "ba"
    assert answers[4] == "a"
    assert answers[5] == "abc"
    assert answers[6] == "cba"
    assert first_occ("bcabc") == "bca" and answers[0] != "bca"
    assert last_occ("cbacdcbc") == "adbc" and answers[1] != "adbc"
    assert len(plan[8][0]) == N_MAX and len(plan[9][0]) == N_MAX

    rows = []
    for i, (_, scale, goal, hack) in enumerate(plan, 1):
        rows.append(f"| {i} | {scale} | {goal} | {hack} |")

    readme = "\n".join([
        "# P7145 测试数据说明",
        "",
        "主造数脚本：题目根目录 `gen.py`。",
        "stdin：一行小写字符串 $s$。",
        "输出：去重后字典序最小的子序列（每个原串出现过的字母恰好一次）。",
        "",
        r"约束：$1\le |s|\le 10^4$，仅小写字母。",
        "",
        "| 组别 | 规模/分布 | 目标 | 卡掉的错误解 |",
        "|---|---|---|---|",
        *rows,
        "",
        "`.in` 最后一行后无换行符；`.out` 末尾恰好一个换行符。",
        "",
        "生成后自校验：最后出现下标版必须等于剩余次数版单调栈。",
        "",
    ])
    (DATA / "README.md").write_text(readme, encoding="utf-8")
    print("generated 10 cases")
    for i, ans in enumerate(answers, 1):
        print(i, ans, "len_in", len(plan[i - 1][0]))


if __name__ == "__main__":
    main()
